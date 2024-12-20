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

## Using STM32CubeProgrammer

1. Install [STM32CubeProgrammer](https://www.st.com/en/development-tools/stm32cubeprog.html).
2. Connect the DISC2 device via ST-Link or J-Link in Hot Plug mode. If connecting via J-Link, connect via J-Link JTAG connector to CN3 with jumpers on JP1, JP4 (CHGR), JP2, JP3, and JP6. Connect USB ST-LINK (micro-b) for power.
3. Open STM32CubeProgrammer and select the `core/build/prodtest/combined.bin` file.
4. Flash the selected file to the DISC2 device.

> **Warning:** TZEN will be enabled after flashing. This is normal and will allow future reflashing using the process described above.

## Using J-Link

1. Create a `script.jlink` file with the following contents:
    ```sh
    Device STM32U5A9NJ
    if swd
    speed auto
    loadfile core/build/prodtest/combined.bin 0x0c004000
    r
    g
    exit
    ```
    Replace `core/build/prodtest/combined.bin` with the actual path to your `combined.bin` file if it differs.
2. Connect via J-Link JTAG connector to CN3 with jumpers on JP1, JP4 (CHGR), JP2, JP3, and JP6. Connect USB ST-LINK (micro-b) for power.
3. Run the script using the following command:
    ```sh
    ./JLink.exe -CommanderScript ./script.jlink
    ```

# Enabling System View and RTT

To enable System View and RTT for debugging, follow these steps:
1. Follow the [System View Instructions](https://docs.trezor.io/trezor-firmware/core/systemview/index.html). These instructions apply to DISC2 as well.
2. Add the following to SConscript.firmware
```python3
SYSTEM_VIEW = ARGUMENTS.get('SYSTEM_VIEW', '0')
if FEATURE_FLAGS["SYSTEM_VIEW"]:
    SOURCE_MOD += [
        'embed/sys/systemview/stm32/config/SEGGER_SYSVIEW_Config_NoOS.c',
        'embed/sys/systemview/stm32/segger/SEGGER_SYSVIEW.c',
        'embed/sys/systemview/stm32/segger/SEGGER_RTT.c',
        'embed/sys/systemview/stm32/segger/SEGGER_RTT_ASM_ARMv7M.S',
        'embed/sys/systemview/stm32/segger/Syscalls/SEGGER_RTT_Syscalls_GCC.c',
        'embed/sys/systemview/systemview.c',
    ]
    CPPPATH_MOD += [
        'embed/sys/systemview/inc',
        'embed/sys/systemview/stm32/config',
        'embed/sys/systemview/stm32/segger',
    ]
    CPPDEFINES_MOD += ['SYSTEM_VIEW']
    CCFLAGS_MOD += '-DSYSTEM_VIEW '
```
> **Warning:** If `PYOPT` is used to build, then USB connection will not work as expected.
```

3. Rebuild using the build instructions mentioned above, but replace the 4th command with:
    ```sh
    make -j build PYOPT=0 BITCOIN_ONLY=1 V=1 VERBOSE=1 TREZOR_MODEL=DISC2 BOOTLOADER_DEVEL=1 SYSTEM_VIEW=1
    ```


# Open in Ozone

1. To debug firmware in Ozone J-Link debugger, open trezor.jdebug file