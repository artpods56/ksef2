from collections.abc import Sequence
from datetime import datetime, timezone
from enum import Enum, StrEnum
from zoneinfo import ZoneInfo
from camel_converter import to_camel


def to_aware_datetime(dt: str | datetime) -> datetime:
    if isinstance(dt, datetime):
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=ZoneInfo("Europe/Warsaw"))
        return dt.astimezone(timezone.utc)
    else:
        return to_aware_datetime(datetime.fromisoformat(dt))


def lookup[_K, _V](mapping: dict[_K, _V], key: _K, label: str) -> _V:
    try:
        return mapping[key]
    except KeyError:
        expected = ", ".join(str(k) for k in mapping)
        raise ValueError(f"Unknown {label}: {key}. Expected one of: {expected}")


def get_matching_enum(
    value: str, enums: Sequence[type[StrEnum]]
) -> type[StrEnum] | None:
    matches: list[type[StrEnum]] = []
    for enum_cls in enums:
        if any(member.value == value for member in enum_cls):
            matches.append(enum_cls)
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        names = ", ".join(e.__name__ for e in matches)
        raise ValueError(
            f"Ambiguous enum mapping for {value!r}. Matches: {names}. "
            "Pass the explicit StrEnum value instead of a string."
        )
    return None


def to_camel_enum[_V: str, _T: Enum](value: _V, enum: type[_T]) -> _T:
    try:
        return enum(to_camel(value))
    except ValueError:
        raise ValueError(f"{value} is not a valid {enum.__name__}") from None
