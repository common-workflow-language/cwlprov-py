from typing import Any

class BaseFetchTransport:
    config: Any
    keychain: Any
    kwargs: Any
    def __init__(self, config, keychain, **kwargs) -> None: ...
    @classmethod
    def fetch(cls, url, output_path, **kwargs) -> None: ...
    @classmethod
    def cleanup(cls) -> None: ...
