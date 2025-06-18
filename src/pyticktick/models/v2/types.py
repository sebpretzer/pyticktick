"""Pydantic types for TickTick V2 API models.

This module provides custom types that restrict more general types to the specific
values used by the TickTick API. These types are used in Pydantic models to ensure that
both requests and responses conform better to the TickTick API.

For example, all `time_zone` fields in the TickTick API are strings, but they all
represent IANA time zone names. By using the `TimeZoneName`type, we can ensure that only
valid time zone names are used.

There are some custom functions as well to validate some of the types, when Pydantic's
supplied validators are not enough.

!!! warning "Unofficial API"
    These types are part of the unofficial TickTick API. They were created by reverse
    engineering the API. They may be incomplete or inaccurate.
"""

from __future__ import annotations

import re
from datetime import timedelta
from textwrap import dedent
from typing import Annotated, Literal, Optional

from bson import ObjectId as BsonObjectId
from dateutil.rrule import rrulestr
from icalendar import Alarm, Calendar
from pydantic import AfterValidator, BeforeValidator, StringConstraints, conint
from pydantic_extra_types.timezone_name import TimeZoneName as PydanticTimeZoneName

ETag = Annotated[str, StringConstraints(pattern=r"^[a-z0-9]{8}$")]
"""Pydantic type for a TickTick ETag.

This is a string of 8 lowercase alphanumeric characters used to validate the version of
a resource.
"""


def convert_ical_trigger(trigger: str) -> timedelta | None:
    """Converts an iCalendar trigger to a timedelta.

    iCalendar triggers are used in alarms to specify when the alarm will trigger. It
    follows the convention specified in [RFC 5545: Alarm Component Properties - Trigger](https://datatracker.ietf.org/doc/html/rfc5545.html#section-3.8.6.3).

    The icalendar library is a Python parser/generator for iCalendar files. It supports
    parsing alarms, but it does not provide an easy way to extract the timedelta from
    an isolated trigger string. This function works around this limitation.

    Args:
        trigger (str): An iCalendar trigger.

    Returns:
        Optional[timedelta]: The timedelta corresponding to the trigger, or None
            if no trigger is specified.

    Raises:
        ValueError: If the trigger is not a valid iCalendar trigger.
        TypeError: If the trigger is not an Alarm or if the Alarm trigger is not a
            timedelta.
    """
    _trigger = dedent(f"""
    BEGIN:VALARM
    ACTION:DISPLAY
    {trigger}
    END:VALARM
    """).strip()
    try:
        cal = Calendar.from_ical(_trigger)
    except ValueError as e:
        if f"Content line could not be parsed into parts: '{trigger}'" in str(e):
            msg = f"Invalid iCalendar trigger: {trigger}"
            raise ValueError(msg) from e
        raise
    if not isinstance(cal, Alarm):
        msg = f"Invalid iCalendar trigger, expected Alarm, got {type(cal)}"
        raise TypeError(msg)
    if cal.TRIGGER is None:
        return None
    if not isinstance(cal.TRIGGER, timedelta):
        msg = f"Invalid iCalendar trigger, expected timedelta, got {type(cal.TRIGGER)}"
        raise TypeError(msg)
    return cal.TRIGGER


def validate_ical_trigger(trigger: str) -> str:
    """Validates an iCalendar trigger, without converting it to a timedelta.

    Args:
        trigger (str): An iCalendar trigger.

    Returns:
        str: The same input trigger if it is valid.
    """
    convert_ical_trigger(trigger)
    return trigger


ICalTrigger = Annotated[str, BeforeValidator(validate_ical_trigger)]
"""Pydantic type for TickTick reminders, follows the iCalendar convention.

This is the format used by TickTick to represent reminders. It uses the iCalendar
convention for triggers in alarms, as specified in
[RFC 5545: Alarm Component Properties - Trigger](https://datatracker.ietf.org/doc/html/rfc5545.html#section-3.8.6.3).

For all day tasks, the time delta is calculated from midnight of the due date.

See some examples below for the possible values:

- `TRIGGER:PT0S`: at the time
- `TRIGGER:-PT5M`: 5 minutes before
- `TRIGGER:-PT30M`: 30 minutes before
- `TRIGGER:-PT60M`: 1 hour before
- `TRIGGER:-P0DT15H0M0S`: 15 hours before
- `TRIGGER:-P1DT15H0M0S`: 9:00 am the day before, assuming an all-day task
- `TRIGGER:P0DT9H0M0S`: same day at 9:00 am, assuming an all-day task
"""

InboxId = Annotated[str, StringConstraints(pattern=r"^inbox\d+$")]
"""Pydantic type for the Project ID of the user's inbox."""

ObjectId = Annotated[
    str,
    BeforeValidator(str),
    BeforeValidator(BsonObjectId),
    AfterValidator(str),
]
"""Pydantic type for BSON ObjectId.

!!! note
    It is an educated guess that TickTick IDs are [BSON ObjectIds](https://pymongo.readthedocs.io/en/stable/api/bson/objectid.html#bson.objectid.ObjectId).
    This has not been confirmed by TickTick, but we have not seen any evidence to the
    contrary.

Inspired by [pydantic/pydantic#7260 (comment)](https://github.com/pydantic/pydantic/issues/7260#issuecomment-1694724620),
which helps to validate BSON ObjectId in Pydantic models.
"""

Priority = Literal[0, 1, 3, 5]
"""Pydantic type for a TickTick priority.

TickTick priority codes:

1. `0`: None
2. `1`: Low
3. `3`: Medium
4. `5`: High
"""

Progress = Annotated[int, conint(ge=0, le=100)]
"""Pydantic type for the progress of a TickTick checklist task.

This is an integer between 0 and 100, representing the percentage of completion of a
checklist task.
"""

RepeatFrom = Annotated[Literal[0, 1, 2], BeforeValidator(int)]
"""Pydantic type for a TickTick repeat from.

TickTick repeat from codes:

1. `0`: due date
2. `1`: completed date
3. `2`: __unknown to date__
"""

SortOptions = Literal["sortOrder", "dueDate", "tag", "priority", "project", "none"]
"""Pydantic type for TickTick to sort tasks within a project.

This is used not only for sorting tasks, but also for grouping tasks within a project.
"""

Status = Literal[-1, 0, 1, 2]
"""Pydantic type for a TickTick status.

TickTick status codes:

1. `0`: active
2. `1`: completed
3. `2`: completed (used by TickTick's web app)
4. `-1`: abandoned / won't do
"""

Kind = Literal["TEXT", "NOTE", "CHECKLIST"]
"""Pydantic type for a TickTick task.

TickTick provides three kinds of tasks:

    - `TEXT`: a standard task
    - `NOTE`: a note
    - `CHECKLIST`: a checklist

These are used in different contexts. See
[Kinds of Tasks](./../../../explanations/ticktick_api/kinds_of_tasks.md) for more info.

"""


def validate_tt_rrule(rule: str) -> str:
    """Validates a TickTick custom Recurrence Rule (RRULE).

    The default RRULE is specified in [RFC 5545: Property Value Data Types - Recurrence Rule](https://datatracker.ietf.org/doc/html/rfc5545.html#section-3.3.10).
    The default RRULE parser [rrulestr](https://dateutil.readthedocs.io/en/stable/rrule.html#dateutil.rrule.rrulestr)
    works for the majority of the cases, but it does not support certain custom TickTick
    components.

    TickTick added two custom keys to the RRULE: `TT_SKIP` and `TT_WORKDAY`,
    where `TT_SKIP=WEEKEND` skips weekends and `TT_WORKDAY` specifies the first (1) or
    last (-1) workday of the month.

    TickTick also added a custom `ERULE:<RULE>;<RULE>` which repeats tasks on exact
    dates every year.

    Args:
        rule (str): A TickTick custom RRULE to be validated.

    Returns:
        str: The same input rule if it is valid.

    Raises:
        ValueError: If the rule is invalid.
    """
    if re.fullmatch(r"^ERULE:NAME=CUSTOM;BYDATE=(\d{8},)+(\d{8})$", rule):
        return rule

    _rule = rule
    for config in ["TT_SKIP=WEEKEND", "TT_WORKDAY=1", "TT_WORKDAY=-1"]:
        _rule = _rule.replace(f":{config}", "").replace(f";{config}", "")

    try:
        rrulestr(_rule)
    except ValueError as e:
        msg = f"Invalid TickTick RRULE: {rule}"
        raise ValueError(msg) from e

    return rule


TTRRule = Annotated[str, BeforeValidator(validate_tt_rrule)]
"""Pydantic type for a TickTick repeat flag, loosely based on the iCalendar RRULE.

This is the format used by TickTick to represent recurring tasks. It is similar to
the iCalendar RRULE, but with some custom TickTick components. The default RRULE is
specified in [RFC 5545: Property Value Data Types - Recurrence Rule](https://datatracker.ietf.org/doc/html/rfc5545.html#section-3.3.10).
TickTick added some custom keys and rules, specified in `validate_tt_rrule`.
Pydantic currently does not support RRULE as a type ([pydantic/pydantic-extra-types#118](https://github.com/pydantic/pydantic-extra-types/issues/118)).

See some examples below for the possible values:

1. `RRULE:FREQ=WEEKLY;INTERVAL=1;WKST=SU;BYDAY=FR,TH,WE`: repeats every 1 week on Weds,
    Thurs, and Fri
2. `RRULE:FREQ=DAILY;INTERVAL=2`: repeats every 2 days
3. `RRULE:FREQ=DAILY;INTERVAL=15;TT_SKIP=WEEKEND`: repeats every 15 days, skipping
    weekends
4. `RRULE:FREQ=MONTHLY;INTERVAL=1;BYMONTHDAY=20`: repeats every 1 month on the 20th
5. `RRULE:FREQ=MONTHLY;INTERVAL=4;BYDAY=5TU`: repeats every 4 months on the fifth
    Tuesday
6. `RRULE:FREQ=MONTHLY;INTERVAL=2;BYMONTHDAY=1;TT_WORKDAY=1`: repeats every 2 months on
    the 1st workday
7. `RRULE:FREQ=MONTHLY;INTERVAL=2;BYMONTHDAY=-1;TT_WORKDAY=-1`: repeats every 2 months
    on the last workday
8. `ERULE:NAME=CUSTOM;BYDATE=20250731,20250819`: repeats on July 31, 2025 and August 19,
    2025
"""

TagLabel = Annotated[str, StringConstraints(pattern=r"^[^\\\/\"#:*?<>|\s]+$")]
"""Pydantic type for a TickTick tag label.

TickTick tag labels must not contain any of the following characters: `\\/"#:*?<>|` or
whitespace.
"""

TagName = Annotated[str, StringConstraints(pattern=r"^[^\\\/\"#:*?<>|\sA-Z]+$")]
"""Pydantic type for a TickTick tag name.

TickTick tag names must not contain any of the following characters: `\\/"#:*?<>|` or
whitespace and must be lowercase.
"""


TimeZoneName = Annotated[
    Optional[PydanticTimeZoneName],
    BeforeValidator(lambda x: None if isinstance(x, str) and len(x) == 0 else x),
]
"""Pydantic type for a TickTick time zone name.

TickTick time zone names are based on the [IANA Time Zone Database](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List).
For the most part, the type should be aligned with [`pydantic_extra_types.timezone_name.TimeZoneName`](https://docs.pydantic.dev/latest/api/pydantic_extra_types_timezone_name/#pydantic_extra_types.timezone_name.TimeZoneName),
except that TickTick allows an empty string or `None` to represent no time zone.
"""
