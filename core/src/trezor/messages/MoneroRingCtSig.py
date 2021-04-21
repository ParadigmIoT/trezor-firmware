# Automatically generated by pb2py
# fmt: off
# isort:skip_file
import protobuf as p

if __debug__:
    try:
        from typing import Dict, List, Optional  # noqa: F401
        from typing_extensions import Literal  # noqa: F401
    except ImportError:
        pass


class MoneroRingCtSig(p.MessageType):

    def __init__(
        self,
        *,
        txn_fee: Optional[int] = None,
        message: Optional[bytes] = None,
        rv_type: Optional[int] = None,
    ) -> None:
        self.txn_fee = txn_fee
        self.message = message
        self.rv_type = rv_type

    @classmethod
    def get_fields(cls) -> Dict:
        return {
            1: ('txn_fee', p.UVarintType, None),
            2: ('message', p.BytesType, None),
            3: ('rv_type', p.UVarintType, None),
        }
