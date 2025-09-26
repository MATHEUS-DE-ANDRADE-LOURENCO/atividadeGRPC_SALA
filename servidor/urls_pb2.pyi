from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class EncurtarUrlRequest(_message.Message):
    __slots__ = ("url_longa",)
    URL_LONGA_FIELD_NUMBER: _ClassVar[int]
    url_longa: str
    def __init__(self, url_longa: _Optional[str] = ...) -> None: ...

class EncurtarUrlResponse(_message.Message):
    __slots__ = ("sucesso", "url_curta", "msg_erro")
    SUCESSO_FIELD_NUMBER: _ClassVar[int]
    URL_CURTA_FIELD_NUMBER: _ClassVar[int]
    MSG_ERRO_FIELD_NUMBER: _ClassVar[int]
    sucesso: bool
    url_curta: str
    msg_erro: str
    def __init__(self, sucesso: bool = ..., url_curta: _Optional[str] = ..., msg_erro: _Optional[str] = ...) -> None: ...

class ObterUrlLongaRequest(_message.Message):
    __slots__ = ("codigo_curto",)
    CODIGO_CURTO_FIELD_NUMBER: _ClassVar[int]
    codigo_curto: str
    def __init__(self, codigo_curto: _Optional[str] = ...) -> None: ...

class ObterUrlLongaResponse(_message.Message):
    __slots__ = ("sucesso", "url_longa", "msg_erro")
    SUCESSO_FIELD_NUMBER: _ClassVar[int]
    URL_LONGA_FIELD_NUMBER: _ClassVar[int]
    MSG_ERRO_FIELD_NUMBER: _ClassVar[int]
    sucesso: bool
    url_longa: str
    msg_erro: str
    def __init__(self, sucesso: bool = ..., url_longa: _Optional[str] = ..., msg_erro: _Optional[str] = ...) -> None: ...
