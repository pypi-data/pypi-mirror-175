from builtins import hasattr as has_attribute
from builtins import setattr as set_attribute
from itertools import chain
from typing import Any, Iterable, Iterator, Type, TypeVar

from named import get_type_name
from typing_extensions import Never

from enum_extensions.constants import (
    DELETE,
    DOUBLE_UNDER,
    GET,
    MODULE,
    REDUCE,
    SET,
    TWO,
    UNDER,
    UNKNOWN,
)
from enum_extensions.string import tick
from enum_extensions.typing import Namespace

__all__ = (
    "get_frame",
    "is_descriptor",
    "is_double_under_name",
    "make_namespace_unpicklable",
    "make_type_unpicklable",
    "once",
    "prepend",
)

try:
    from sys import _getframe as get_frame

except ImportError:  # pragma: no cover
    from types import FrameType as Frame

    class GetFrame(BaseException):
        pass

    NO_TRACEBACK = "no traceback to get the frame from"
    NO_CALLER_FRAME = "can not get the caller frame"
    CALL_STACK_NOT_DEEP_ENOUGH = "call stack is not deep enough"

    def get_frame(depth: int = 0) -> Frame:  # type: ignore
        try:
            raise GetFrame()

        except GetFrame as error:
            traceback = error.__traceback__

            if traceback is None:
                raise ValueError(NO_TRACEBACK) from None

            current = traceback.tb_frame

            frame = current.f_back

            if frame is None:
                raise ValueError(NO_CALLER_FRAME) from None

            for _ in range(depth):
                frame = frame.f_back

                if frame is None:
                    raise ValueError(CALL_STACK_NOT_DEEP_ENOUGH) from None

            return frame


T = TypeVar("T")


def is_descriptor(item: Any) -> bool:
    return has_attribute(item, GET) or has_attribute(item, SET) or has_attribute(item, DELETE)


FOUR = TWO + TWO  # heh


def is_double_under_name(name: str) -> bool:
    under = UNDER
    double_under = DOUBLE_UNDER
    two = TWO
    four = FOUR

    return (
        len(name) > four
        and name[:two] == double_under
        and name[-two:] == double_under
        and name[two] != under
        and name[~two] != under
    )


NOT_PICKLABLE = "{} instance is not picklable"


def make_namespace_unpicklable(namespace: Namespace) -> None:
    def error_on_reduce(instance: T, protocol: int) -> Never:
        raise TypeError(NOT_PICKLABLE.format(tick(get_type_name(instance))))

    namespace[REDUCE] = error_on_reduce
    namespace[MODULE] = UNKNOWN


def make_type_unpicklable(type: Type[T]) -> None:
    def error_on_reduce(instance: T, protocol: int) -> Never:
        raise TypeError(NOT_PICKLABLE.format(tick(get_type_name(instance))))

    set_attribute(type, REDUCE, error_on_reduce)
    set_attribute(type, MODULE, UNKNOWN)


def once(item: T) -> Iterator[T]:
    yield item  # pragma: no cover  # ???


def prepend(item: T, iterable: Iterable[T]) -> Iterator[T]:
    return chain(once(item), iterable)
