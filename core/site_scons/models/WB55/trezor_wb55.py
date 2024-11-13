from __future__ import annotations

from .. import get_hw_model_as_number
from ..stm32wb55_common import stm32wb55_common_files


def configure(
    env: dict,
    features_wanted: list[str],
    defines: list[str | tuple[str, str]],
    sources: list[str],
    paths: list[str],
) -> list[str]:
    features_available: list[str] = []
    board = "WB55/boards/trezor_wb55.h"
    display = "st7789v.c"
    hw_model = get_hw_model_as_number("WB55")
    hw_revision = 0
    features_available.append("disp_i8080_16bit_dw")

    defines += ["DISPLAY_RGB565"]
    features_available.append("display_rgb565")
    defines += ["USE_RGB_COLORS=1"]

    mcu = "STM32WB55xx"
    linker_script = """embed/trezorhal/stm32wb55/linker/{target}.ld"""

    stm32wb55_common_files(env, defines, sources, paths)

    env.get("ENV")[
        "CPU_ASFLAGS"
    ] = "-mthumb -mcpu=cortex-m4 -mfloat-abi=hard -mfpu=fpv4-sp-d16"
    env.get("ENV")[
        "CPU_CCFLAGS"
    ] = "-mthumb -mcpu=cortex-m4 -mfloat-abi=hard -mfpu=fpv4-sp-d16 -mtune=cortex-m4 "
    env.get("ENV")["RUST_TARGET"] = "thumbv7em-none-eabihf"

    defines += [mcu]
    defines += [f'TREZOR_BOARD=\\"{board}\\"']
    defines += [f"HW_MODEL={hw_model}"]
    defines += [f"HW_REVISION={hw_revision}"]

    sources += ["embed/trezorhal/xdisplay_legacy.c"]
    sources += ["embed/trezorhal/stm32wb55/xdisplay/st-7789/display_nofb.c"]
    sources += ["embed/trezorhal/stm32wb55/xdisplay/st-7789/display_driver.c"]
    sources += ["embed/trezorhal/stm32wb55/xdisplay/st-7789/display_io.c"]
    sources += ["embed/trezorhal/stm32wb55/xdisplay/st-7789/display_panel.c"]
    sources += [
        "embed/trezorhal/stm32wb55/xdisplay/st-7789/panels/lhs200kb-if21.c",
    ]

    sources += ["embed/trezorhal/stm32wb55/backlight_pwm.c"]
    features_available.append("backlight")
    defines += ["USE_BACKLIGHT=1"]

    if "input" in features_wanted:
        sources += ["embed/trezorhal/stm32wb55/i2c_bus.c"]
        sources += ["embed/trezorhal/stm32wb55/touch/ft6x36.c"]
        sources += ["embed/trezorhal/stm32wb55/touch/panels/lhs200kb-if21.c"]
        features_available.append("touch")
        # sources += ["embed/trezorhal/stm32wb55/button.c"]
        # features_available.append("button")
    defines += ["USE_TOUCH=1"]
    defines += ["USE_I2C=1"]
    # defines += ["USE_BUTTON=1"]

    if "sd_card" in features_wanted:
        sources += ["embed/trezorhal/stm32wb55/sdcard.c"]
        sources += ["embed/extmod/modtrezorio/ff.c"]
        sources += ["embed/extmod/modtrezorio/ffunicode.c"]
        features_available.append("sd_card")
    defines += ["USE_SD_CARD=1"]

    # if "ble" in features_wanted:
    #     sources += ["embed/trezorhal/stm32wb55/ble/ble_hal.c"]
    #     sources += ["embed/trezorhal/stm32wb55/ble/dfu.c"]
    #     sources += ["embed/trezorhal/stm32wb55/ble/fwu.c"]
    #     sources += ["embed/trezorhal/stm32wb55/ble/ble.c"]
    #     sources += ["embed/trezorhal/stm32wb55/ble/messages.c"]
    #     sources += [
    #         "vendor/micropython/lib/stm32lib/STM32WBxx_HAL_Driver/Src/stm32wbxx_hal_uart.c"
    #     ]
    #     features_available.append("ble")
    # defines += ["USE_BLE=1"]

    if "ble" in features_wanted or "sd_card" in features_wanted:
        sources += [
            "vendor/micropython/lib/stm32lib/STM32WBxx_HAL_Driver/Src/stm32wbxx_hal_dma.c"
        ]

    if "sbu" in features_wanted:
        sources += ["embed/trezorhal/stm32wb55/sbu.c"]
        features_available.append("sbu")
    defines += ["USE_SBU=1"]

    if "usb" in features_wanted:
        sources += [
            "embed/trezorhal/stm32wb55/usb/usb_class_hid.c",
            "embed/trezorhal/stm32wb55/usb/usb_class_vcp.c",
            "embed/trezorhal/stm32wb55/usb/usb_class_webusb.c",
            "embed/trezorhal/stm32wb55/usb/usb.c",
            "embed/trezorhal/stm32wb55/usb/usbd_conf.c",
            "embed/trezorhal/stm32wb55/usb/usbd_core.c",
            "embed/trezorhal/stm32wb55/usb/usbd_ctlreq.c",
            "embed/trezorhal/stm32wb55/usb/usbd_ioreq.c",
            "vendor/micropython/lib/stm32lib/STM32WBxx_HAL_Driver/Src/stm32wbxx_ll_usb.c",
        ]
        features_available.append("usb")

    if "dma2d" in features_wanted:
        defines += ["USE_DMA2D"]
        sources += ["embed/trezorhal/stm32u5/dma2d_bitblt.c"]
        sources += [
            "vendor/micropython/lib/stm32lib/STM32WBxx_HAL_Driver/Src/stm32wbxx_hal_dma2d.c",
        ]
        features_available.append("dma2d")

    env.get("ENV")["TREZOR_BOARD"] = board
    env.get("ENV")["MCU_TYPE"] = mcu
    env.get("ENV")["LINKER_SCRIPT"] = linker_script

    return features_available
