# Automatically generated by pb2py
# fmt: off
# isort:skip_file
from .. import protobuf as p

if __debug__:
    try:
        from typing import Dict, List, Optional  # noqa: F401
        from typing_extensions import Literal  # noqa: F401
        EnumTypeWordRequestType = Literal[0, 1, 2]
    except ImportError:
        pass


class WordRequest(p.MessageType):
    MESSAGE_WIRE_TYPE = 46

    def __init__(
        self,
        *,
        type: Optional[EnumTypeWordRequestType] = None,
    ) -> None:
        self.type = type

    @classmethod
    def get_fields(cls) -> Dict:
        return {
            1: ('type', p.EnumType("WordRequestType", (0, 1, 2,)), None),
        }
