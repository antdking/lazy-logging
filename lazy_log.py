from typing import Callable, cast, Any, TypeVar, Generic


__all__ = [
    'lazy_log',
    'LazyLog',
]


_T = TypeVar('_T')

_UNSET = cast(Any, object())


def lazy_log(func: Callable[..., _T], *args: Any, **kwargs: Any) -> _T:
    return cast(_T, LazyLog(func, *args, **kwargs))


def _proxy(attr_name: str) -> Callable:
    def inner(self: 'LazyLog', *args: Any, **kwargs: Any) -> Any:
        return getattr(self.get_result(), attr_name)(*args, **kwargs)

    return inner


class LazyLog(Generic[_T]):
    __slots__ = (
        'func',
        'args',
        'kwargs',
        '__result',
    )

    def __init__(self, func: Callable[..., _T], *args: Any, **kwargs: Any) -> None:
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.__result = _UNSET  # type: _T

    def get_result(self) -> _T:
        if self.__result is _UNSET:
            self.__result = self.func(*self.args, **self.kwargs)
        return self.__result

    def __getattr__(self, item):
        result = self.get_result()
        if hasattr(result, '__getattr__'):
            return result.__getattr__(item)
        else:
            return getattr(result, item)

    __repr__ = _proxy('__repr__')
    __str__ = _proxy('__str__')
    __bytes__ = _proxy('__bytes__')
    __format__ = _proxy('__format__')

    # These might not be needed, and could cause some issues potentially down the road.
    __lt__ = _proxy('__lt__')
    __le__ = _proxy('__le__')
    __eq__ = _proxy('__eq__')
    __ne__ = _proxy('__ne__')
    __gt__ = _proxy('__gt__')
    __ge__ = _proxy('__ge__')

    __hash__ = _proxy('__hash__')

    __bool__ = _proxy('__bool__')

    __dir__ = _proxy('__dir__')

    __len__ = _proxy('__len__')
    __length_hint__ = _proxy('__length_hint__')
    __getitem__ = _proxy('__getitem__')
    __missing__ = _proxy('__missing__')
    __iter__ = _proxy('__iter__')
    __reversed__ = _proxy('__reversed__')
    __contains__ = _proxy('__contains__')

    __neg__ = _proxy('__neg__')
    __pos__ = _proxy('__pos__')
    __abs__ = _proxy('__abs__')
    __invert__ = _proxy('__invert__')

    __complex__ = _proxy('__complex__')
    __int__ = _proxy('__int__')
    __float__ = _proxy('__float__')
    __round__ = _proxy('__round__')
    __index__ = _proxy('__index__')
