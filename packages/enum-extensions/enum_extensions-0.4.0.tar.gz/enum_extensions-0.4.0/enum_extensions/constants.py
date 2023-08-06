__all__ = (
    "EMPTY",
    "UNDER",
    "DOUBLE_UNDER",
    "TWO",
    "COMMA",
    "SPACE",
    "COMMA_SPACE",
    "PIPE",
    "TICK",
    "DEFAULT_ENCODING",
    "DEFAULT_ERRORS",
    "UNKNOWN",
    "DIRECT_CALLER",
    "NESTED_CALLER",
    "GET",
    "SET",
    "DELETE",
    "DOCUMENTATION",
    "NAME",
    "QUALIFIED_NAME",
    "MODULE",
    "NEW",
    "NEW_MEMBER",
    "REDUCE",
    "ENUM_GENERATE_NEXT_VALUE",
    "ENUM_IGNORE",
    "ENUM_START",
    "ENUM_NAME",
    "ENUM_TYPE",
    "ENUM_VALUE",
    "ENUM_DOCUMENTATION",
    "ENUM_PRESERVE",
    "MEMBER_MAPPING_PRIVATE",
    "UNKNOWN_PRIVATE",
    "BOUNDARY_PRIVATE",
    "INVALID_NAMES",
    "OBJECT_NEW",
    "USELESS_NEW",
    "OBJECT_DIR",
)

EMPTY = str()

UNDER = "_"
DOUBLE_UNDER = UNDER + UNDER

TWO = 2

COMMA = ","
SPACE = " "

COMMA_SPACE = COMMA + SPACE

PIPE = "|"

TICK = "`{}`"

MAPS = "{} -> {}"

DEFAULT_REVERSE = False
DEFAULT_BOUND = True

DEFAULT_ENCODING = "utf-8"
DEFAULT_ERRORS = "strict"

UNKNOWN = "<unknown>"

DIRECT_CALLER = 1
NESTED_CALLER = 2

GET = "__get__"
SET = "__set__"
DELETE = "__delete__"

DOCUMENTATION = "__doc__"
NAME = "__name__"
QUALIFIED_NAME = "__qualname__"
MODULE = "__module__"
NEW = "__new__"
NEW_MEMBER = "__new_member__"

REDUCE = "__reduce_ex__"

PICKLE_METHODS = frozenset(("__getnewargs_ex__", "__getnewargs__", "__reduce_ex__", "__reduce__"))

ENUM_GENERATE_NEXT_VALUE = "enum_generate_next_value"
ENUM_IGNORE = "enum_ignore"
ENUM_START = "enum_start"

ENUM_NAME = "__enum_name__"
ENUM_TYPE = "__enum_type__"
ENUM_VALUE = "__enum_value__"

ENUM_DOCUMENTATION = "An enumeration."

ENUM_PRESERVE = ("__format__", "__repr__", "__str__", "__reduce_ex__")

MEMBER_MAPPING_PRIVATE = "_member_mapping"

UNKNOWN_PRIVATE = "_unknown"
BOUNDARY_PRIVATE = "_boundary"

MRO = "mro"

INVALID_NAMES = frozenset((MRO, EMPTY))

OBJECT_NEW = object.__new__

USELESS_NEW = {OBJECT_NEW}

OBJECT_DIR = object.__dir__
