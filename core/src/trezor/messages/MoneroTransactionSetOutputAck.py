# Automatically generated by pb2py
# fmt: off
# isort:skip_file
import protobuf as p

from .MoneroTransactionRsigData import MoneroTransactionRsigData

if __debug__:
    try:
        from typing import Dict, List, Optional  # noqa: F401
        from typing_extensions import Literal  # noqa: F401
    except ImportError:
        pass


class MoneroTransactionSetOutputAck(p.MessageType):
    MESSAGE_WIRE_TYPE = 512

    def __init__(
        self,
        *,
        tx_out: Optional[bytes] = None,
        vouti_hmac: Optional[bytes] = None,
        rsig_data: Optional[MoneroTransactionRsigData] = None,
        out_pk: Optional[bytes] = None,
        ecdh_info: Optional[bytes] = None,
    ) -> None:
        self.tx_out = tx_out
        self.vouti_hmac = vouti_hmac
        self.rsig_data = rsig_data
        self.out_pk = out_pk
        self.ecdh_info = ecdh_info

    @classmethod
    def get_fields(cls) -> Dict:
        return {
            1: ('tx_out', p.BytesType, None),
            2: ('vouti_hmac', p.BytesType, None),
            3: ('rsig_data', MoneroTransactionRsigData, None),
            4: ('out_pk', p.BytesType, None),
            5: ('ecdh_info', p.BytesType, None),
        }
