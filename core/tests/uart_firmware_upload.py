#!/usr/bin/env python3
# Usage: python3 uart_firmware_upload.py <COM#> ../build/firmware/firmware.bin

import serial
import struct
import time
import argparse
import logging
from typing import BinaryIO

# Configure logging
logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Message types from messages.proto
MSG_FIRMWARE_ERASE = 6
MSG_FIRMWARE_UPLOAD = 7
MSG_SUCCESS = 2
MSG_FIRMWARE_REQUEST = 8

# Map message types to human-readable names for logging
MSG_TYPES = {
    MSG_FIRMWARE_ERASE: "FIRMWARE_ERASE",
    MSG_FIRMWARE_UPLOAD: "FIRMWARE_UPLOAD",
    MSG_SUCCESS: "SUCCESS",
    MSG_FIRMWARE_REQUEST: "FIRMWARE_REQUEST"
}

# Increased delay between packets to allow more processing time
PACKET_DELAY = 0.02

class TrezorProtocol:
    PACKET_SIZE = 64
    FIRST_PACKET_MAGIC = b'?##'
    NEXT_PACKET_MAGIC = b'?'
    
    @staticmethod
    def pack_first_packet(msg_type: int, data: bytes) -> bytes:
        """Pack first packet according to Trezor protocol"""
        packet = bytearray(TrezorProtocol.PACKET_SIZE)
        
        # Magic constant
        packet[0:3] = TrezorProtocol.FIRST_PACKET_MAGIC
        
        # Message type (2 bytes, big endian)
        packet[3:5] = struct.pack('>H', msg_type)
        
        # Message size (4 bytes, big endian)
        packet[5:9] = struct.pack('>I', len(data))
        
        # First 55 bytes of message
        data_len = min(len(data), 55)
        packet[9:9+data_len] = data[:data_len]

        logger.debug(f"Packed first packet: type={MSG_TYPES.get(msg_type, msg_type)}, size={len(data)}, data_len={data_len}")
        logger.debug(f"Packet hex: {packet.hex()}")
        
        return bytes(packet)
    
    @staticmethod
    def pack_next_packet(data: bytes, offset: int) -> bytes:
        """Pack subsequent packets according to Trezor protocol"""
        packet = bytearray(TrezorProtocol.PACKET_SIZE)
        
        # Magic constant
        packet[0:1] = TrezorProtocol.NEXT_PACKET_MAGIC
        
        # Up to 63 bytes of message data
        data_len = min(len(data) - offset, 63)
        packet[1:1+data_len] = data[offset:offset+data_len]

        logger.debug(f"Packed next packet: offset={offset}, data_len={data_len}")
        logger.debug(f"Packet hex: {packet.hex()}")
        
        return bytes(packet)
    
    @staticmethod
    def read_first_packet(data: bytes) -> tuple[int, int, bytes]:
        """Parse first packet, return (msg_type, msg_size, data)"""
        if data[0:3] != TrezorProtocol.FIRST_PACKET_MAGIC:
            error_msg = f"Invalid magic constant in first packet: expected {TrezorProtocol.FIRST_PACKET_MAGIC.hex()}, got {data[0:3].hex()}"
            logger.error(error_msg)
            raise ValueError(error_msg)
            
        msg_type = struct.unpack('>H', data[3:5])[0]
        msg_size = struct.unpack('>I', data[5:9])[0]
        logger.debug(f"Parsed first packet: type={MSG_TYPES.get(msg_type, msg_type)}, size={msg_size}")
        logger.debug(f"Packet hex: {data.hex()}")
        return msg_type, msg_size, data[9:64]

    @staticmethod
    def read_next_packet(data: bytes) -> bytes:
        """Parse subsequent packet, return data"""
        if data[0:1] != TrezorProtocol.NEXT_PACKET_MAGIC:
            error_msg = f"Invalid magic constant in subsequent packet: expected {TrezorProtocol.NEXT_PACKET_MAGIC.hex()}, got {data[0:1].hex()}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        logger.debug(f"Parsed next packet, hex: {data.hex()}")
        return data[1:64]

    @staticmethod
    def encode_varint(value: int) -> bytes:
        """Encode an integer as a protobuf varint"""
        result = bytearray()
        while value > 0x7F:
            result.append((value & 0x7F) | 0x80)
            value >>= 7
        result.append(value & 0x7F)
        logger.debug(f"Encoded varint: {value} -> {result.hex()}")
        return bytes(result)

    @staticmethod
    def decode_varint(data: bytes, offset: int = 0) -> tuple[int, int]:
        """Decode a protobuf varint, return (value, new_offset)"""
        result = 0
        shift = 0
        start_offset = offset
        while True:
            byte = data[offset]
            result |= (byte & 0x7F) << shift
            offset += 1
            if not (byte & 0x80):
                break
            shift += 7
        logger.debug(f"Decoded varint: {data[start_offset:offset].hex()} -> {result}")
        return result, offset

    @staticmethod
    def pack_protobuf_firmware_erase(length: int) -> bytes:
        """Pack FirmwareErase message according to protobuf format
        
        message FirmwareErase {
            optional uint32 length = 1;
        }
        """
        # Field number 1 (length) with wire type 0 (varint) = 0x08
        result = bytearray([0x08])
        # Append length as varint
        result.extend(TrezorProtocol.encode_varint(length))
        logger.debug(f"Packed FirmwareErase message: length={length}, hex={result.hex()}")
        return bytes(result)

    @staticmethod
    def pack_protobuf_firmware_upload(chunk: bytes) -> bytes:
        """Pack FirmwareUpload message according to protobuf format
        
        message FirmwareUpload {
            required bytes payload = 1;
        }
        """
        # Field 1 (payload) with wire type 2 (length-delimited) = 0x0A
        result = bytearray([0x0A])
        # Append chunk length as varint
        result.extend(TrezorProtocol.encode_varint(len(chunk)))
        # Append chunk bytes
        result.extend(chunk)
        logger.debug(f"Packed FirmwareUpload message: chunk_size={len(chunk)}, hex={result[:20].hex()}...")
        return bytes(result)

    @staticmethod
    def parse_firmware_request(data: bytes) -> tuple[int, int]:
        """Parse FirmwareRequest message from protobuf format
        
        message FirmwareRequest {
            required uint32 offset = 1;
            required uint32 length = 2;
        }
        """
        offset = 0
        chunk_offset = None
        chunk_length = None
        
        while offset < len(data):
            # Read field number and wire type
            field_and_type = data[offset]
            field_number = field_and_type >> 3
            wire_type = field_and_type & 0x07
            offset += 1
            
            if field_number == 1:  # offset field
                chunk_offset, offset = TrezorProtocol.decode_varint(data, offset)
            elif field_number == 2:  # length field
                chunk_length, offset = TrezorProtocol.decode_varint(data, offset)
                
        if chunk_offset is None or chunk_length is None:
            error_msg = "Invalid FirmwareRequest message: missing required fields"
            logger.error(error_msg)
            raise ValueError(error_msg)
            
        logger.debug(f"Parsed FirmwareRequest: offset={chunk_offset}, length={chunk_length}")
        return chunk_offset, chunk_length

class FirmwareUploader:
    def __init__(self, port: str, baudrate: int = 115200):
        """Initialize the uploader with serial port settings"""
        logger.info(f"Initializing serial connection: port={port}, baudrate={baudrate}")
        self.serial = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=5
        )
        logger.debug(f"Serial configuration: {self.serial.get_settings()}")
        
    def _send_message(self, msg_type: int, data: bytes) -> tuple[int, bytes]:
        """Send a message following Trezor protocol, return (response_type, response_data)"""
        start_time = time.time()
        
        # Send first packet
        first_packet = TrezorProtocol.pack_first_packet(msg_type, data)
        self.serial.write(first_packet)
        logger.debug(f"Sent first packet ({len(first_packet)} bytes)")
        time.sleep(PACKET_DELAY)
        
        # Send remaining packets if any
        remaining_data = data[55:]
        offset = 0
        packet_count = 0
        while offset < len(remaining_data):
            packet = TrezorProtocol.pack_next_packet(remaining_data, offset)
            self.serial.write(packet)
            time.sleep(PACKET_DELAY)
            offset += 63
            packet_count += 1
            
        if packet_count > 0:
            logger.debug(f"Sent {packet_count} additional packets")
            
        # Read response
        response = self.serial.read(TrezorProtocol.PACKET_SIZE)
        if len(response) != TrezorProtocol.PACKET_SIZE:
            error_msg = f"No response from device (received {len(response)} bytes)"
            logger.error(error_msg)
            raise Exception(error_msg)
            
        # Parse first response packet
        resp_type, resp_size, resp_data = TrezorProtocol.read_first_packet(response)
        logger.debug(f"Received response: type={MSG_TYPES.get(resp_type, resp_type)}, size={resp_size}")
        
        # Read additional packets if needed
        received_size = len(resp_data)
        packet_count = 0
        while received_size < resp_size:
            packet = self.serial.read(TrezorProtocol.PACKET_SIZE)
            if len(packet) != TrezorProtocol.PACKET_SIZE:
                error_msg = f"Incomplete response from device (expected {TrezorProtocol.PACKET_SIZE} bytes, got {len(packet)})"
                logger.error(error_msg)
                raise Exception(error_msg)
            resp_data += TrezorProtocol.read_next_packet(packet)
            received_size += 63
            packet_count += 1
            
        if packet_count > 0:
            logger.debug(f"Received {packet_count} additional response packets")
            
        elapsed = time.time() - start_time
        logger.debug(f"Message exchange completed in {elapsed:.3f} seconds")
            
        return resp_type, resp_data[:resp_size]
        
    def upload_firmware(self, firmware_file: BinaryIO, callback=None) -> None:
        """Upload firmware to the device using Version 2 protocol
        
        Args:
            firmware_file: Open binary file containing firmware
            callback: Optional progress callback function(progress: float)
        """
        start_time = time.time()
        
        # Read entire firmware into memory
        firmware_data = firmware_file.read()
        total_size = len(firmware_data)
        logger.info(f"Starting firmware upload: size={total_size} bytes")
        
        logger.info("Erasing existing firmware...")
        # Pack length as protobuf message for FirmwareErase
        erase_data = TrezorProtocol.pack_protobuf_firmware_erase(total_size)
        resp_type, response = self._send_message(MSG_FIRMWARE_ERASE, erase_data)
        
        if resp_type != MSG_FIRMWARE_REQUEST:
            error_msg = f"Expected firmware request after erase, got {MSG_TYPES.get(resp_type, resp_type)}"
            logger.error(error_msg)
            raise Exception(error_msg)
            
        logger.info("Uploading firmware in chunks...")
        
        # Handle chunked upload based on device requests
        chunks_sent = 0
        total_bytes_sent = 0
        while True:
            # Parse the request to get chunk offset and length
            time.sleep(1)
            chunk_offset, chunk_length = TrezorProtocol.parse_firmware_request(response)
            
            # Extract and send the requested chunk
            chunk = firmware_data[chunk_offset:chunk_offset + chunk_length]
            upload_data = TrezorProtocol.pack_protobuf_firmware_upload(chunk)
            resp_type, response = self._send_message(MSG_FIRMWARE_UPLOAD, upload_data)
            
            chunks_sent += 1
            total_bytes_sent += chunk_length
            
            if callback:
                progress = (chunk_offset + chunk_length) / total_size * 100
                callback(min(progress, 100))
            
            logger.info(f"Uploaded chunk {chunks_sent}: offset={chunk_offset}, size={chunk_length} ({total_bytes_sent}/{total_size} bytes)")
            
            # Check response type after each chunk upload
            if resp_type == MSG_SUCCESS:
                break
            elif resp_type != MSG_FIRMWARE_REQUEST:
                error_msg = f"Unexpected response type {MSG_TYPES.get(resp_type, resp_type)} after chunk upload"
                logger.error(error_msg)
                raise Exception(error_msg)
        
        elapsed = time.time() - start_time
        logger.info(f"Firmware upload complete! Uploaded {total_size} bytes in {elapsed:.1f} seconds ({total_size/elapsed/1024:.1f} KB/s)")
        
    def close(self):
        """Close the serial connection"""
        logger.debug("Closing serial connection")
        self.serial.close()

def main():
    parser = argparse.ArgumentParser(
        description='Upload firmware over UART following Trezor protocol (Version 2)'
    )
    parser.add_argument('port', help='Serial port (e.g., COM1 or /dev/ttyUSB0)')
    parser.add_argument('firmware', help='Firmware binary file')
    parser.add_argument('--baudrate', type=int, default=115200,
                      help='Baudrate (default: 115200)')
    parser.add_argument('--debug', action='store_true',
                      help='Enable debug logging')
    
    args = parser.parse_args()
    
    if args.debug:
        logger.setLevel(logging.DEBUG)
    
    try:
        with open(args.firmware, 'rb') as f:
            logger.info(f"Opening firmware file: {args.firmware}")
            uploader = FirmwareUploader(args.port, args.baudrate)
            try:
                uploader.upload_firmware(f)
            finally:
                uploader.close()
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return 1
        
    return 0

if __name__ == '__main__':
    exit(main())
