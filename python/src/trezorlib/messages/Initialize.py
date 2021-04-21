# Automatically generated by pb2py
# fmt: off
# isort:skip_file
from .. import protobuf as p

if __debug__:
    try:
        from typing import Dict, List, Optional  # noqa: F401
        from typing_extensions import Literal  # noqa: F401
    except ImportError:
        pass


class Initialize(p.MessageType):
    MESSAGE_WIRE_TYPE = 0

    def __init__(
        self,
        *,
        session_id: Optional[bytes] = None,
    ) -> None:
        self.session_id = session_id

    @classmethod
    def get_fields(cls) -> Dict:
        return {
            1: ('session_id', p.BytesType, None),
        }
