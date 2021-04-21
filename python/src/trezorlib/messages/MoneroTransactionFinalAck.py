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


class MoneroTransactionFinalAck(p.MessageType):
    MESSAGE_WIRE_TYPE = 518

    def __init__(
        self,
        *,
        cout_key: Optional[bytes] = None,
        salt: Optional[bytes] = None,
        rand_mult: Optional[bytes] = None,
        tx_enc_keys: Optional[bytes] = None,
        opening_key: Optional[bytes] = None,
    ) -> None:
        self.cout_key = cout_key
        self.salt = salt
        self.rand_mult = rand_mult
        self.tx_enc_keys = tx_enc_keys
        self.opening_key = opening_key

    @classmethod
    def get_fields(cls) -> Dict:
        return {
            1: ('cout_key', p.BytesType, None),
            2: ('salt', p.BytesType, None),
            3: ('rand_mult', p.BytesType, None),
            4: ('tx_enc_keys', p.BytesType, None),
            5: ('opening_key', p.BytesType, None),
        }
