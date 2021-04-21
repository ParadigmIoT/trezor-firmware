# Automatically generated by pb2py
# fmt: off
# isort:skip_file
from .. import protobuf as p

if __debug__:
    try:
        from typing import Dict, List, Optional  # noqa: F401
        from typing_extensions import Literal  # noqa: F401
        EnumTypeRecoveryDeviceType = Literal[0, 1]
    except ImportError:
        pass


class RecoveryDevice(p.MessageType):
    MESSAGE_WIRE_TYPE = 45

    def __init__(
        self,
        *,
        word_count: Optional[int] = None,
        passphrase_protection: Optional[bool] = None,
        pin_protection: Optional[bool] = None,
        language: Optional[str] = None,
        label: Optional[str] = None,
        enforce_wordlist: Optional[bool] = None,
        type: Optional[EnumTypeRecoveryDeviceType] = None,
        u2f_counter: Optional[int] = None,
        dry_run: Optional[bool] = None,
    ) -> None:
        self.word_count = word_count
        self.passphrase_protection = passphrase_protection
        self.pin_protection = pin_protection
        self.language = language
        self.label = label
        self.enforce_wordlist = enforce_wordlist
        self.type = type
        self.u2f_counter = u2f_counter
        self.dry_run = dry_run

    @classmethod
    def get_fields(cls) -> Dict:
        return {
            1: ('word_count', p.UVarintType, None),
            2: ('passphrase_protection', p.BoolType, None),
            3: ('pin_protection', p.BoolType, None),
            4: ('language', p.UnicodeType, None),
            5: ('label', p.UnicodeType, None),
            6: ('enforce_wordlist', p.BoolType, None),
            8: ('type', p.EnumType("RecoveryDeviceType", (0, 1,)), None),
            9: ('u2f_counter', p.UVarintType, None),
            10: ('dry_run', p.BoolType, None),
        }
