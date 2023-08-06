from typing import Iterator, Tuple, Type, TypeVar

from named import get_name

from enum_extensions.enums import Enum
from enum_extensions.string import concat_comma_space, maps, tick

__all__ = ("unique",)

ET = TypeVar("ET", bound=Type[Enum])

ALIASES_FOUND = "aliases found in {}: {}"


def unique(enum: ET) -> ET:
    """Ensures that the enumeration does not have aliases.

    Example:
        ```python
        from enum_extensions import Enum, unique

        @unique
        class Color(Enum):
            RED = 1
            GREEN = 2
            BLUE = 3
            R, G, B = RED, GREEN, BLUE
        ```

        ```python
        Traceback (most recent call last):
          ...
        ValueError: aliases found in `Color`: `R` -> `RED`, `G` -> `GREEN`, `B` -> `BLUE`
        ```

    Arguments:
        enum: The enumeration to check.

    Raises:
        ValueError: Aliases were found.

    Returns:
        The enumeration checked.
    """
    duplicates = concat_comma_space(
        maps(tick(name), tick(member_name)) for name, member_name in find_duplicates(enum)
    )

    if duplicates:
        raise ValueError(ALIASES_FOUND.format(tick(get_name(enum)), duplicates))

    return enum


def find_duplicates(enum: Type[Enum]) -> Iterator[Tuple[str, str]]:
    for name, member in enum.members.items():
        if name != member.name:
            yield (name, member.name)
