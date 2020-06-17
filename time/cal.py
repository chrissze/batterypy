from typing import Any, Dict, List, Optional
from datetime import date, datetime,timedelta
from timeit import default_timer


def add_days(d: date, i: int) -> date:
    return d + timedelta(days=i)


def add_trading_days(d: date, i: int) -> date:
    n = i
    day = d
    if i > 0:
        while n > 0:
            day = next_trading_day(day)
            n -= 1
        return day
    elif i < 0:
        while n < 0:
            day = previous_trading_day(day)
            n += 1
        return day
    else:
        return d


def date_range(start: Optional[date] = None, end: Optional[date]=None, period: Optional[int]=None) -> List[date]:
    result: List[date] = []
    i: Optional[int] = period
    d: date = start
    if start is not None and end is not None and period is None:
        if start <= end:
            while d <= end:
                result.append(d)
                d += timedelta(days=1)
            return result
        else:
            return []

    elif start is not None and end is None and period is not None:
        if period > 0:
            while i > 0:
                result.append(d)
                d += timedelta(days=1)
                i -= 1
            return result
        elif period < 0:
            while i < 0:
                result.append(d)
                d -= timedelta(days=1)
                i += 1
            return result
        else:
            return []
    else:
        return []



def tdate_range(start: Optional[date] = None, end: Optional[date]=None, period: Optional[int]=None) -> List[date]:
    normal = date_range(start=start, end=end, period=period)
    result = [x for x in normal if is_trading_day(x)]
    return result


def date_length(start: date, end: date) -> int:
    if end >= start:
        return len(date_range(start=start, end=end))

    else:
        return -(len(date_range(start=end, end=start)))

def tdate_length(start: date, end: date) -> int:
    if end >= start:
        return len(tdate_range(start=start, end=end))

    else:
        return -(len(tdate_range(start=end, end=start)))


def exchange_holidays(year: int) -> List[date]:
    """https://www.investopedia.com/ask/answers/06/stockexchangeclosed.asp
    The NYSE and NASDAQ are open on Veterans Day and Columbus Day (or the day in which they are observed).
    The NYSE and NASDAQ are closed on Good Friday.
    """
    dec31 = date(year, 12, 31)
    holidays = [holiday_new_years(year), holiday_martin_luther(year), holiday_washington(year),
        holiday_good_friday(year), holiday_memorial(year), holiday_independence(year), holiday_labor(year),
        holiday_thanksgiving(year), holiday_christmas(year)]
    if is_friday(dec31):
        return holidays + [dec31]
    else:
        return holidays



def federal_holidays(year: int) -> List[date]:
    # Federal holidays do not include Easter
    # New Years Day might be Saturday and falls into 31 Dec, see year 2010
    # https://www.opm.gov/policy-data-oversight/snow-dismissal-procedures/federal-holidays/
    dec31 = date(year, 12, 31)
    holidays = [holiday_new_years(year), holiday_martin_luther(year), holiday_washington(year)
            , holiday_memorial(year), holiday_independence(year), holiday_labor(year)
            , holiday_columbus(year), holiday_veterans(year), holiday_thanksgiving(year), holiday_christmas(year)]
    if is_friday(dec31):
        return holidays + [dec31]
    else:
        return holidays


def get_trading_day() -> date:
    return previous_trading_day(date.today())


def get_trading_day_utc() -> date:
    return previous_trading_day(get_utc_today())


def get_utc_today() -> date:
    t = datetime.utcnow()
    return date(t.year, t.month, t.day)


def gregorian_easter(year: int) -> date:
    century = year // 100 + 1
    shifted_epact = (11 * (year % 19) + 14 - (3 * century) // 4 + (8 * century + 5) // 25) % 30
    adjusted_epact = shifted_epact + 1 if shifted_epact == 0 or (shifted_epact == 1 and year % 19 > 10) \
        else shifted_epact
    pascha_moon = add_days(date(year, 4, 19), - adjusted_epact)
    easter = next_sunday(pascha_moon)
    return easter


def holiday_new_years(year: int) -> date:
    jan1 = date(year, 1, 1)
    if is_saturday(jan1):
        return add_days(jan1, -1)
    elif is_sunday(jan1):
        return date(year, 1, 2)
    else:
        return jan1


def holiday_martin_luther(year: int) -> date:
    return next_monday(date(year, 1, 14))


def holiday_washington(year: int) -> date:
    return next_monday(date(year, 2, 14))


def holiday_good_friday(year: int) -> date:
    return last_friday(gregorian_easter(year))


def holiday_memorial(year: int) -> date:
    return last_monday(date(year, 6, 1))


def holiday_independence(year: int) -> date:
    july4 = date(year, 7, 4)
    if is_saturday(july4):
        return date(year, 7, 3)
    elif is_sunday(july4):
        return date(year, 7, 5)
    else:
        return july4


def holiday_labor(year: int) -> date:
    return next_monday(date(year, 8, 31))


def holiday_columbus(year: int) -> date:
    return next_monday(date(year, 10, 7))


def holiday_veterans(year: int) -> date:
    nov11 = date(year, 11, 11)
    if is_saturday(nov11):
        return date(year, 11, 10)
    elif is_sunday(nov11):
        return date(year, 11, 12)
    else:
        return nov11


def holiday_thanksgiving(year: int) -> date:
    return next_thursday(date(year, 11, 21))


def holiday_christmas(year: int) -> date:
    dec25 = date(year, 12, 25)
    if is_saturday(dec25):
        return date(year, 12, 24)
    elif is_sunday(dec25):
        return date(year, 12, 26)
    else:
        return dec25


def is_monday(d: date) -> bool: return d.isoweekday() == 1


def is_tuesday(d: date) -> bool: return d.isoweekday() == 2


def is_wednesday(d: date) -> bool: return d.isoweekday() == 3


def is_thursday(d: date) -> bool: return d.isoweekday() == 4


def is_friday(d: date) -> bool: return d.isoweekday() == 5


def is_saturday(d: date) -> bool: return d.isoweekday() == 6


def is_sunday(d: date) -> bool: return d.isoweekday() == 7


def is_weekend(d: date) -> bool: return is_saturday(d) or is_sunday(d)


def is_weekday(d: date) -> bool: return not is_weekend(d)


def is_exchange_holiday(d: date) -> bool:
    return d in exchange_holidays(d.year)


def not_exchange_holiday(d: date) -> bool:
    return not is_exchange_holiday(d)


def is_federal_holiday(d: date) -> bool:
    return d in federal_holidays(d.year)


def not_federal_holiday(d: date) -> bool:
    return not is_federal_holiday(d)


def is_trading_day(d: date) -> bool:
    return not (is_weekend(d) or is_exchange_holiday(d))


def not_trading_day(d: date) -> bool:
    return is_weekend(d) or is_exchange_holiday(d)


def is_weekly_close(d: date) -> bool:
    tomorrow = add_days(d, 1)
    if is_friday(d) and not_exchange_holiday(d):
        return True
    elif is_thursday(d) and is_exchange_holiday(tomorrow):
        return True
    else:
        return False


def not_weekly_close(d: date) -> bool:
    return not is_weekly_close(d)


def last_saturday(d: date) -> date:
    n = d.toordinal() % 7 + 1
    return add_days(d, -n)


def last_friday(d: date) -> date:
    n = (d.toordinal() + 1) % 7 + 1
    return add_days(d, -n)


def last_thursday(d: date) -> date:
    n = (d.toordinal() + 2) % 7 + 1
    return add_days(d, -n)


def last_wednesday(d: date) -> date:
    n = (d.toordinal() + 3) % 7 + 1
    return add_days(d, -n)


def last_tuesday(d: date) -> date:
    n = (d.toordinal() + 4) % 7 + 1
    return add_days(d, -n)


def last_monday(d: date) -> date:
    n = (d.toordinal() + 5) % 7 + 1
    return add_days(d, -n)


def last_sunday(d: date) -> date:
    n = (d.toordinal() + 6) % 7 + 1
    return add_days(d, -n)


def next_sunday(d: date) -> date:
    n = d.toordinal() % 7
    return add_days(d, 7 - n)


def next_monday(d: date) -> date:
    n = (d.toordinal() - 1) % 7
    return add_days(d, 7 - n)


def next_tuesday(d: date) -> date:
    n = (d.toordinal() - 2) % 7
    return add_days(d, 7 - n)

def next_wednesday(d: date) -> date:
    n = (d.toordinal() - 3) % 7
    return add_days(d, 7 - n)


def next_thursday(d: date) -> date:
    n = (d.toordinal() - 4) % 7
    return add_days(d, 7 - n)


def next_friday(d: date) -> date:
    n = (d.toordinal() - 5) % 7
    return add_days(d, 7 - n)


def next_saturday(d: date) -> date:
    n = (d.toordinal() - 6) % 7
    return add_days(d, 7 - n)


def next_trading_day(d: date) -> date:
    if is_trading_day(day1 := add_days(d, 1)):
        return day1
    elif is_trading_day(day2 := add_days(d, 2)):
        return day2
    elif is_trading_day(day3 := add_days(d, 3)):
        return day3
    elif is_trading_day(day4 := add_days(d, 4)):
        return day4
    else:
        return add_days(d, 5)


def previous_trading_day(d: date) -> date:
    if is_trading_day(pday1 := add_days(d, -1)):
        return pday1
    elif is_trading_day(pday2 := add_days(d, -2)):
        return pday2
    elif is_trading_day(pday3 := add_days(d, -3)):
        return pday3
    elif is_trading_day(pday4 := add_days(d, -4)):
        return pday4
    else:
        return add_days(d, -5)


if __name__ == '__main__':
    d1 = date(2020,1,1)
    d2 = date(2020,12,31)
    d3 = date(2019,1,2)
    d4 = date(2019,1,7)

    dd1 = tdate_length(start=d3, end=d4)
    print(dd1)
    print(default_timer())