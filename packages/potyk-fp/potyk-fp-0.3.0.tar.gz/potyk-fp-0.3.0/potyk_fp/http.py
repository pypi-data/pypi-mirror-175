import dataclasses
from typing import Callable, Tuple, Union, Any, TypeVar, Generic, Optional, Protocol

__all__ = [
    'Json', 'StatusCode', 'Response',
    'HttpRes', 'WithToJson',
]

Json = Union[dict, list]
StatusCode = Code = int
Response = Tuple[Json, StatusCode]
IdType = TypeVar('IdType')
HttpResT = TypeVar('HttpResT')


@dataclasses.dataclass
class MsgResp:
    msg: str = ''


@dataclasses.dataclass
class IdResp(Generic[IdType]):
    id: IdType


class WithToJson(Protocol):
    def to_json(self):
        ...


@dataclasses.dataclass()
class HttpRes(Generic[HttpResT]):
    success: bool
    resp: HttpResT
    code: Optional[int] = None

    def __post_init__(self):
        self.code = self.code or (200 if self.success else 400)

    @classmethod
    def ok(cls, resp=None, code=None, **kwargs):
        return cls(success=True, resp=resp or {}, code=code)

    @classmethod
    def err(cls, resp=None, code=None, **kwargs):
        return cls(success=False, resp=resp or {}, code=code)

    @classmethod
    def ok_msg(cls, msg='', code=None):
        return cls.ok(MsgResp(msg), code)

    @classmethod
    def err_msg(cls, msg='', code=None):
        return cls.err(MsgResp(msg), code)

    @classmethod
    def ok_id(cls, id_: IdType, code=None):
        return cls.ok(IdResp(id_), code)

    def and_then(self, res: Callable[[], 'HttpRes']):
        return res() if self.success else self

    def or_else(self, res: Callable[[], 'HttpRes']):
        return self if self.success else res()

    @property
    def as_response(self) -> Response:
        return (
            self.resp.to_json() if hasattr(self.resp, 'to_json') else
            (dataclasses.asdict(self.resp) if dataclasses.is_dataclass(self.resp) else
             self.resp),
            self.code
        )


def test_HttpRes():
    assert HttpRes.ok_msg('ok').as_response == ({'msg': 'ok'}, 200)
    assert HttpRes.err_msg('err').as_response == ({'msg': 'err'}, 400)
    assert HttpRes.ok_id('ok').as_response == ({'id': 'ok'}, 200)
    assert HttpRes.ok_id('ok').and_then(lambda: HttpRes.ok_msg('sam')).as_response == ({'msg': 'sam'}, 200)
    assert HttpRes.err_msg('err').and_then(lambda: HttpRes.ok_id('sam')).as_response == ({'msg': 'err'}, 400)
    assert HttpRes.ok_id('ok').or_else(lambda: HttpRes.ok_msg('sam')).as_response == ({'id': 'ok'}, 200)
    assert HttpRes.err_msg('err').or_else(lambda: HttpRes.ok_id('sam')).as_response == ({'id': 'sam'}, 200)

    class WithToJson:
        def to_json(self):
            return {'op': 'oppa'}

    assert HttpRes.ok(WithToJson()).as_response == ({'op': 'oppa'}, 200)
    assert HttpRes.ok([{'ass': 'tities'}]).as_response == ([{'ass': 'tities'}], 200)
