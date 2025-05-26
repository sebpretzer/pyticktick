import pytest
from pydantic import TypeAdapter

from pyticktick.models.v2 import ICalTrigger, TimeZoneName, TTRRule


@pytest.mark.parametrize(
    "trigger",
    [
        # at the time
        "TRIGGER:-PT0S",
        # 5 minutes before
        "TRIGGER:-PT5M",
        # 30 minutes before
        "TRIGGER:-PT30M",
        # 1 hour before
        "TRIGGER:-PT60M",
        # 1 day before
        "TRIGGER:-PT1440M",
        # 5 days before
        "TRIGGER:-PT7200M",
        # 15 hours before
        "TRIGGER:-P0DT15H0M0S",
        # 1 day before at 9:00 am, assuming an all-day task
        "TRIGGER:-P1DT15H0M0S",
        # same day at 9:00 am, assuming an all-day task
        "TRIGGER:P0DT9H0M0S",
    ],
)
def test_ical_trigger(trigger):
    ta = TypeAdapter(ICalTrigger)
    assert ta.validate_python(trigger) == trigger


@pytest.mark.parametrize(
    "repeat_flag",
    [
        # repeats every 1 week on Weds, Thurs, and Fri
        "RRULE:FREQ=WEEKLY;INTERVAL=1;WKST=SU;BYDAY=FR,TH,WE",
        # repeats every 2 weeks on Mon and Tue
        "RRULE:FREQ=WEEKLY;INTERVAL=2;WKST=SU;BYDAY=MO,TU",
        # repeats every 2 days
        "RRULE:FREQ=DAILY;INTERVAL=2",
        # repeats every 15 days, skipping weekends
        "RRULE:FREQ=DAILY;INTERVAL=15;TT_SKIP=WEEKEND",
        # repeats every 1 month on the 20th
        "RRULE:FREQ=MONTHLY;INTERVAL=1;BYMONTHDAY=20",
        # repeats every 12 months on the 11th, 16th, 20th, skipping weekends
        "RRULE:FREQ=MONTHLY;INTERVAL=12;BYMONTHDAY=20,16,11;TT_SKIP=WEEKEND",
        # repeats every 4 months on the first Friday
        "RRULE:FREQ=MONTHLY;INTERVAL=4;BYDAY=1FR",
        # repeats every 4 months on the fifth Tuesday
        "RRULE:FREQ=MONTHLY;INTERVAL=4;BYDAY=5TU",
        # repeats every 4 months on the last Sunday
        "RRULE:FREQ=MONTHLY;INTERVAL=4;BYDAY=-1SU",
        # repeats every 2 months on the 1st workday
        "RRULE:FREQ=MONTHLY;INTERVAL=2;BYMONTHDAY=1;TT_WORKDAY=1",
        # repeats every 2 months on the last workday
        "RRULE:FREQ=MONTHLY;INTERVAL=2;BYMONTHDAY=-1;TT_WORKDAY=-1",
        # repeats every 2 days, skipping weekends
        "RRULE:FREQ=DAILY;INTERVAL=2;TT_SKIP=WEEKEND",
        # repeats on July 31, 2025 and August 19, 2025
        "ERULE:NAME=CUSTOM;BYDATE=20250731,20250819",
        # repeats on July 31, 2025, August 19, 2025, March 5, 2026, March 23, 2026, July 6, 2026, and July 24, 2026  # noqa: E501, W505
        "ERULE:NAME=CUSTOM;BYDATE=20250731,20250819,20260305,20260323,20260706,20260724",
    ],
)
def test_tt_rule(repeat_flag):
    ta = TypeAdapter(TTRRule)
    assert ta.validate_python(repeat_flag) == repeat_flag


@pytest.mark.parametrize(
    "time_zone",
    [
        "America/New_York",
        "America/Chicago",
        "Africa/Abidjan",
        "Asia/Tokyo",
        "Europe/London",
        "",
        None,
    ],
)
def test_time_zone_name(time_zone):
    ta = TypeAdapter(TimeZoneName)

    if isinstance(time_zone, str) and len(time_zone) == 0:
        _time_zone = None
    else:
        _time_zone = time_zone

    assert ta.validate_python(time_zone) == _time_zone
