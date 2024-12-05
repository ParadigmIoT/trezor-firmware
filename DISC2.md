# Prerequisites

Follow all instructions for setting up the environment and initial build at:

1. [Core Build Instructions](https://docs.trezor.io/trezor-firmware/core/build/index.html)
2. [Embedded Build Instructions](https://docs.trezor.io/trezor-firmware/core/build/embedded.html)

# Discovery 2 Build Instructions

To build for the Discovery 2 DK, follow these steps:

1. `poetry shell`
2. `cd core`
3. `make -j clean`
4. `make -j build TREZOR_MODEL=DISC2 BOOTLOADER_DEVEL=1`
5. `make -j combine_fw TREZOR_MODEL=DISC2`

# Flashing Instructions

1. Install STM32CubeProgrammer
2. Connect to DISC2 over ST-Link or J-Link in Hot Plug mode
3. Select the `core/build/prodtest/combined.bin` file to flash on DISC2

> **Warning:** TZEN will be enabled after flashing. This is normal and will allow future reflashing with the process described above.

# Enabling System View and RTT

To enable System View and RTT for debugging, follow these steps:

1. Follow the [System View Instructions](https://docs.trezor.io/trezor-firmware/core/systemview/index.html). These instructions apply to DISC2 as well.
2. Rebuild using the build instructions mentioned above, but replace the 4th command with:
    ```sh
    make -j build PYOPT=0 BITCOIN_ONLY=1 V=1 VERBOSE=1 TREZOR_MODEL=DISC2 BOOTLOADER_DEVEL=1 SYSTEM_VIEW=1
    ```