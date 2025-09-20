import io
from prov.model import ProvDocument as ProvDocument
from prov.serializers import Serializer as Serializer
from typing import Any

class ProvNSerializer(Serializer):
    def serialize(self, stream: io.IOBase, **args: Any) -> None: ...
    def deserialize(self, stream: io.IOBase, **args: Any) -> ProvDocument: ...
