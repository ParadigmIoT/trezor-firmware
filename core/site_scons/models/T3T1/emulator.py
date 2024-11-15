from __future__ import annotations

from .. import get_hw_model_as_number


def configure(
    env: dict,
    features_wanted: list[str],
    defines: list[str | tuple[str, str]],
    sources: list[str],
    paths: list[str],
) -> list[str]:

    features_available: list[str] = []
    board = "T3T1/boards/t3t1-unix.h"
    hw_model = get_hw_model_as_number("T3T1")
    hw_revision = 0
    mcu = "STM32U585xx"

    defines += ["FRAMEBUFFER", "DISPLAY_RGB565"]
    features_available.append("framebuffer")
    features_available.append("display_rgb565")
    defines += ["USE_RGB_COLORS=1"]

    defines += [mcu]
    defines += [f'TREZOR_BOARD=\\"{board}\\"']
    defines += [f"HW_MODEL={hw_model}"]
    defines += [f"HW_REVISION={hw_revision}"]
    defines += [f"MCU_TYPE={mcu}"]
    # todo change to blockwise flash when implemented in unix
    defines += ["FLASH_BIT_ACCESS=1"]
    defines += ["FLASH_BLOCK_WORDS=1"]

    if "dma2d" in features_wanted:
        features_available.append("dma2d")
        sources += [
            "embed/trezorhal/unix/dma2d_bitblt.c",
        ]
        defines += ["USE_DMA2D"]

    if "sd_card" in features_wanted:
        features_available.append("sd_card")
        sources += [
            "embed/trezorhal/unix/sdcard.c",
            "embed/extmod/modtrezorio/ff.c",
            "embed/extmod/modtrezorio/ffunicode.c",
        ]
    defines += ["USE_SD_CARD=1"]

    if "sbu" in features_wanted:
        sources += ["embed/trezorhal/unix/sbu.c"]
    defines += ["USE_SBU=1"]

    if "optiga" in features_wanted:
        sources += ["embed/trezorhal/unix/optiga_hal.c"]
        sources += ["embed/trezorhal/unix/optiga.c"]
        features_available.append("optiga")
    defines += ["USE_OPTIGA=1"]

    if "input" in features_wanted:
        sources += ["embed/trezorhal/unix/touch.c"]
        features_available.append("touch")
    defines += ["USE_TOUCH=1"]

    features_available.append("backlight")
    defines += ["USE_BACKLIGHT=1"]

    sources += ["embed/trezorhal/stm32u5/layout.c"]

    return features_available
