# Automatically generated by pb2py
# fmt: off
# isort:skip_file
import protobuf as p

from .PrevInput import PrevInput

if __debug__:
    try:
        from typing import Dict, List, Optional  # noqa: F401
        from typing_extensions import Literal  # noqa: F401
    except ImportError:
        pass


class TxAckPrevInputWrapper(p.MessageType):

    def __init__(
        self,
        *,
        input: PrevInput,
    ) -> None:
        self.input = input

    @classmethod
    def get_fields(cls) -> Dict:
        return {
            2: ('input', PrevInput, p.FLAG_REQUIRED),
        }
