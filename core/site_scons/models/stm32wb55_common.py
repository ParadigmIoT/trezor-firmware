from __future__ import annotations


def stm32wb55_common_files(env, defines, sources, paths):
    defines += [
        ("STM32_HAL_H", '"<stm32wbxx.h>"'),
        ("FLASH_BLOCK_WORDS", "1"),
        ("FLASH_BIT_ACCESS", "1"),
        ("CONFIDENTIAL", ""),
    ]

    paths += [
        "embed/trezorhal/stm32wb55",
        "vendor/micropython/lib/cmsis/inc",
        "vendor/micropython/lib/stm32lib/STM32WBxx_HAL_Driver/Inc",
        "vendor/micropython/lib/stm32lib/CMSIS/STM32WBxx/Include",
    ]

    sources += [
        "vendor/micropython/lib/stm32lib/STM32WBxx_HAL_Driver/Src/stm32wbxx_hal.c",
        "vendor/micropython/lib/stm32lib/STM32WBxx_HAL_Driver/Src/stm32wbxx_hal_cortex.c",
        "vendor/micropython/lib/stm32lib/STM32WBxx_HAL_Driver/Src/stm32wbxx_hal_flash.c",
        "vendor/micropython/lib/stm32lib/STM32WBxx_HAL_Driver/Src/stm32wbxx_hal_flash_ex.c",
        "vendor/micropython/lib/stm32lib/STM32WBxx_HAL_Driver/Src/stm32wbxx_hal_gpio.c",
        "vendor/micropython/lib/stm32lib/STM32WBxx_HAL_Driver/Src/stm32wbxx_hal_i2c.c",
        # "vendor/micropython/lib/stm32lib/STM32WBxx_HAL_Driver/Src/stm32wbxx_hal_ltdc.c",
        "vendor/micropython/lib/stm32lib/STM32WBxx_HAL_Driver/Src/stm32wbxx_hal_pcd.c",
        "vendor/micropython/lib/stm32lib/STM32WBxx_HAL_Driver/Src/stm32wbxx_hal_pcd_ex.c",
        "vendor/micropython/lib/stm32lib/STM32WBxx_HAL_Driver/Src/stm32wbxx_hal_pwr.c",
        "vendor/micropython/lib/stm32lib/STM32WBxx_HAL_Driver/Src/stm32wbxx_hal_rcc.c",
        "vendor/micropython/lib/stm32lib/STM32WBxx_HAL_Driver/Src/stm32wbxx_hal_rcc_ex.c",
        # "vendor/micropython/lib/stm32lib/STM32WBxx_HAL_Driver/Src/stm32wbxx_hal_sd.c",
        "vendor/micropython/lib/stm32lib/STM32WBxx_HAL_Driver/Src/stm32wbxx_hal_spi.c",
        # "vendor/micropython/lib/stm32lib/STM32WBxx_HAL_Driver/Src/stm32wbxx_hal_sram.c",
        # "vendor/micropython/lib/stm32lib/STM32WBxx_HAL_Driver/Src/stm32wbxx_hal_sdram.c",
        "vendor/micropython/lib/stm32lib/STM32WBxx_HAL_Driver/Src/stm32wbxx_hal_tim.c",
        "vendor/micropython/lib/stm32lib/STM32WBxx_HAL_Driver/Src/stm32wbxx_hal_tim_ex.c",
        # "vendor/micropython/lib/stm32lib/STM32WBxx_HAL_Driver/Src/stm32wbxx_ll_fmc.c",
        # "vendor/micropython/lib/stm32lib/STM32WBxx_HAL_Driver/Src/stm32wbxx_ll_sdmmc.c",
    ]

    sources += [
        "embed/trezorhal/stm32wb55/applet.c",
        "embed/trezorhal/stm32wb55/board_capabilities.c",
        "embed/trezorhal/stm32wb55/bootutils.c",
        "embed/trezorhal/stm32wb55/entropy.c",
        "embed/trezorhal/stm32wb55/flash.c",
        "embed/trezorhal/stm32wb55/flash_otp.c",
        "embed/trezorhal/stm32wb55/fwutils.c",
        "embed/trezorhal/stm32wb55/layout.c",
        "embed/trezorhal/stm32wb55/monoctr.c",
        "embed/trezorhal/stm32wb55/mpu.c",
        "embed/trezorhal/stm32wb55/option_bytes.c",
        "embed/trezorhal/stm32wb55/pvd.c",
        "embed/trezorhal/stm32wb55/random_delays.c",
        "embed/trezorhal/stm32wb55/reset_flags.c",
        "embed/trezorhal/stm32wb55/rng.c",
        "embed/trezorhal/stm32wb55/secret.c",
        "embed/trezorhal/stm32wb55/startup_init.c",
        "embed/trezorhal/stm32wb55/syscall.c",
        "embed/trezorhal/stm32wb55/syscall_dispatch.c",
        "embed/trezorhal/stm32wb55/syscall_probe.c",
        "embed/trezorhal/stm32wb55/syscall_stubs.c",
        "embed/trezorhal/stm32wb55/syscall_verifiers.c",
        "embed/trezorhal/stm32wb55/system.c",
        "embed/trezorhal/stm32wb55/systask.c",
        "embed/trezorhal/stm32wb55/systick.c",
        "embed/trezorhal/stm32wb55/systimer.c",
        "embed/trezorhal/stm32wb55/time_estimate.c",
        "embed/trezorhal/stm32wb55/unit_properties.c",
        "embed/trezorhal/stm32wb55/vectortable.S",
    ]

    # boardloader needs separate assembler for some function unencumbered by various FW+bootloader hacks
    # this helps to prevent making a bug in boardloader which may be hard to fix since it's locked with write-protect
    env_constraints = env.get("CONSTRAINTS")
    if env_constraints and "limited_util_s" in env_constraints:
        sources += [
            "embed/trezorhal/stm32wb55/limited_util.S",
        ]
    else:
        sources += [
            "embed/trezorhal/stm32wb55/util.S",
        ]

    env.get("ENV")["SUFFIX"] = "stm32wb55"
    env.get("ENV")["LINKER_SCRIPT"] = """embed/trezorhal/stm32wb55/linker/{target}.ld"""
