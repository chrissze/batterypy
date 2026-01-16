
from typing import Optional

from datetime import date, datetime, timedelta, timezone


from datetime import date, datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from typing import Optional
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError




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


    
    


def exchange_holidays(year: int) -> list[date]:
    """
    https://www.investopedia.com/ask/answers/06/stockexchangeclosed.asp
    
    If New Year's Day falls on a Saturday, the exchange remains OPEN on the preceding Friday (Dec 31), although Dec31 is a Federal holiday
    
    The NYSE and NASDAQ are open on Veterans Day and Columbus Day (or the day in which they are observed).
    The NYSE and NASDAQ are closed on Good Friday.
    2001-09-11 911
    2001-09-12 911
    2001-09-13 911
    2001-09-14 911
    2004-06-11 honoring President Ronald Reagan

    2007-01-02 Mourning for President Ford
    *2010-12-31 open for year-end accounting, though it is federal holiday
    2012-10-29 Hurricane Sandy
    2012-10-30 Hurricane Sandy
    2018-12-05 George H W Bush
    2025-01-09 closure for President Jimmy Carter's funeral
    """
    
    holidays = [holiday_new_years(year), holiday_martin_luther(year), holiday_washington(year),
        holiday_good_friday(year), holiday_memorial(year), holiday_independence(year), holiday_labor(year),
        holiday_thanksgiving(year), holiday_christmas(year)]

    if year == 2001:
        holidays += [date(2001, 9, 11), date(2001, 9, 12), date(2001, 9, 13), date(2001, 9, 14)]
    elif year == 2004:
        holidays += [date(2004, 6, 11)]
    elif year == 2007:
        holidays += [date(2007, 1, 2)]
    elif year == 2012:
        holidays += [date(2012, 10, 29), date(2012, 10, 30)]
    elif year == 2018:
        holidays += [date(2018, 12, 5)]
    elif year == 2025:
        holidays += [date(2025, 1, 9)]
    
    if year >= 2021:
        holidays += [holiday_juneteenth(year)]
    
    return sorted(holidays)




def federal_holidays(year: int) -> list[date]:
    # Federal holidays do not include Easter
    # New Years Day might be Saturday and falls into 31 Dec, see year 2010
    # https://www.opm.gov/policy-data-oversight/snow-dismissal-procedures/federal-holidays/
    dec31 = date(year, 12, 31)
    holidays = [holiday_new_years(year), holiday_martin_luther(year), holiday_washington(year)
            , holiday_memorial(year), holiday_independence(year), holiday_labor(year)
            , holiday_columbus(year), holiday_veterans(year), holiday_thanksgiving(year), holiday_christmas(year)]
    if is_friday(dec31):
        holidays += [dec31]
    
    if year >= 2021:
        holidays += [holiday_juneteenth(year)]
    
    return sorted(holidays)


def get_gmt_datetime(url: str) -> datetime:
    """
    INDEPENDENT
    Get GMT datetime by internet
    """
    req = Request(url=url, method='HEAD', headers={'User-Agent': 'Mozilla/5.0'})
    with urlopen(req, timeout=5) as response:
        if 'Date' not in response.headers:
            raise Exception('Date is not in response.headers')
        gmt_datetime = parsedate_to_datetime(response.headers['Date'])
        return gmt_datetime


def get_hk_date(url: str) -> date:
    """
    DEPENDS: get_gmt_datetime
    Get HK 'date' by internet
    """

    gmt_datetime = get_gmt_datetime(url)
    
    hk_tz = timezone(timedelta(hours=8))
    
    hk_datetime = gmt_datetime.astimezone(hk_tz)
    
    hk_date = hk_datetime.date()

    return hk_date


def getting_hk_date() -> Optional[date]:
    """
    DEPENDS: get_gmt_datetime, get_hk_date

    returns None when there are http errors or no internet connection at the host.
    """
    websites = [
        'https://google.com',
        'https://cloudflare.com',
        'https://www.apple.com'
    ]

    for url in websites:
        try:
            return get_hk_date(url)
        except (URLError, HTTPError) as e:
            continue
        except Exception as e:
            continue
    return None




def get_third_friday(months: int, base_date: date | None = None):
    """
    DEPENDS: next_friday

    
    EXAMPLES:
    d1: date = date(2027, 12, 1)
    friday: str = get_third_friday(1, d1).strftime("%Y%m%d")
    print(friday)  # '20280121'

    NOTES: 
    
    Do not put base_date=date.today() into default keyword argument, otherwise, every time I import the module, today() will get pull. Set default to None so that today will be computed only on call.

    // is floor division.
    """
    if base_date is None:
        base_date = date.today()

    year = base_date.year + (base_date.month + months - 1) // 12

    month = (base_date.month + months - 1) % 12 + 1

    third_friday = next_friday(date(year, month, 14))

    return third_friday





def get_trading_day() -> date:
    return previous_trading_day(date.today())


def get_trading_day_utc() -> date:
    return previous_trading_day(get_utc_today())


def get_utc_today() -> date:
    t = datetime.utcnow()
    return date(t.year, t.month, t.day)


def gregorian_easter(year: int) -> date:
    century: int = year // 100 + 1
    shifted_epact: int = (11 * (year % 19) + 14 - (3 * century) // 4 + (8 * century + 5) // 25) % 30
    adjusted_epact: int = shifted_epact + 1 if shifted_epact == 0 or (shifted_epact == 1 and year % 19 > 10) \
        else shifted_epact
    
    #pascha_moon = add_days(date(year, 4, 19), - adjusted_epact)
    pascha_moon: date = date(year, 4, 19) - timedelta(days=adjusted_epact)
    easter: date = next_sunday(pascha_moon)
    return easter


def holiday_new_years(year: int) -> date:
    jan1 = date(year, 1, 1)
    if is_sunday(jan1):
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


def holiday_juneteenth(year: int) -> date:
    """
    Since 2021
    """
    jun19 = date(year, 6, 19)
    if is_saturday(jun19):
        return date(year, 6, 18)
    elif is_sunday(jun19):
        return date(year, 6, 20)
    else:
        return jun19




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


def is_federal_holiday(d: date) -> bool:
    return d in federal_holidays(d.year)

def is_trading_day(d: date) -> bool:
    return not (is_weekend(d) or is_exchange_holiday(d))



def is_first_settlement(d: date | str) -> bool:
    """
    This is 1st Friday option settlement.
    """
    if isinstance(d, str):
        d: date = date.fromisoformat(d)
    
    day: int = d.day
    
    if day > 7:
        return False
    
    return is_weekly_settlement(d)



def is_fortnite_settlement(d: date | str) -> bool:
    """
    
    """
    return is_first_settlement(d) or is_monthly_settlement(d)



def is_monthly_settlement(d: date | str) -> bool:
    """
    This is 3rd Friday option settlement.
    """
    if isinstance(d, str):
        d: date = date.fromisoformat(d)
    
    day: int = d.day
    
    if day < 15 or day > 21:
        return False
    
    return is_weekly_settlement(d)



def is_weekly_settlement(d: date | str) -> bool:
    if isinstance(d, str):
        d: date = date.fromisoformat(d)
    next_day: date = d + timedelta(days=1)
    day2: date = d + timedelta(days=2)
    if is_friday(d) and not_exchange_holiday(d):
        return True
    elif is_thursday(d) and is_exchange_holiday(next_day):
        return True
    elif is_wednesday(d) and is_exchange_holiday(next_day) and is_exchange_holiday(day2):
        return True
    else:
        return False



def is_iso_date_format(s: str) -> bool:
    s_list: list[str] = s.split('-')     # ['2020', '02', '29']
    length_list: list[int] = list(map(len, s_list))    # [4, 2, 2]
    date_str: str = "".join(s_list)           #  '20200229'
    is_all_decimal: bool = date_str.isdecimal()
    is422: bool = length_list == [4, 2, 2]

    passtest1: bool = is_all_decimal and is422

    valid_year: bool = 0 < int(s_list[0]) < 10000 if passtest1 else False

    is_leap_year: bool = int(s_list[0]) % 4 == 0 if valid_year else False

    valid_month: bool = 0 < int(s_list[1]) < 13 if passtest1 else False

    month_int: int = int(s_list[1]) if valid_month else 0
    is_large_month: bool = month_int in [1,3,5,7,8,10,12]

    is_feb: bool = month_int == 2

    valid_day: bool = (0 < int(s_list[2]) < 29 + is_leap_year if is_feb
                       else 0 < int(s_list[2]) < 31 + is_large_month if valid_month
                       else False)

    return valid_year and valid_month and valid_day





def last_saturday(d: date) -> date:
    n: int = d.toordinal() % 7 + 1
    return d - timedelta(days=n)


def last_friday(d: date) -> date:
    n = (d.toordinal() + 1) % 7 + 1
    return d - timedelta(days=n)


def last_thursday(d: date) -> date:
    n = (d.toordinal() + 2) % 7 + 1
    return d - timedelta(days=n)



def last_wednesday(d: date) -> date:
    n = (d.toordinal() + 3) % 7 + 1
    return d - timedelta(days=n)


def last_tuesday(d: date) -> date:
    n = (d.toordinal() + 4) % 7 + 1
    return d - timedelta(days=n)


def last_monday(d: date) -> date:
    n = (d.toordinal() + 5) % 7 + 1
    return d - timedelta(days=n)


def last_sunday(d: date) -> date:
    n = (d.toordinal() + 6) % 7 + 1
    return d - timedelta(days=n)



def make_date_list(start: date | str, end: date | str | None = None) -> list[date]:
    """
    ** INDEPENDENT **
    
    USED BY: make_td_list
    """
    if isinstance(start, str):
        start: date = date.fromisoformat(start)
    
    if isinstance(end, str):
        end: date = date.fromisoformat(end)
    elif end is None:
        end: date = date.today()
    
    # diff can be 0 or a negative int; (end - start) is a timedelta
    # start + timedelta(days=diff) == end
    diff: int = (end - start).days
        
    if diff > 0:
        date_list: list[date] = [ start + timedelta(i) for i in range(diff + 1) ]
        return date_list
    else:
        return []
    


def make_fortnite_list(start: date | str, end: date | str | None = None) -> list[date]:
    """
    DEPENDS: make_date_list, is_trading_day
    """
    date_list: list[date] = make_date_list(start=start, end=end) 
    
    fortnite_list: list[date] = [x for x in date_list if is_fortnite_settlement(x)]
    
    return fortnite_list



def make_td_list(start: date | str, end: date | str | None = None, interval='daily') -> list[date]:
    """
    DEPENDS: make_date_list, is_trading_day
    """
    date_list: list[date] = make_date_list(start=start, end=end) 
    
    if interval == 'monthly':
        td_list: list[date] = [x for x in date_list if is_monthly_settlement(x)]
    elif interval == 'fortnite':
        td_list: list[date] = [x for x in date_list if is_fortnite_settlement(x)]
    elif interval == 'weekly':
        td_list: list[date] = [x for x in date_list if is_weekly_settlement(x)]
    else:
        td_list: list[date] = [x for x in date_list if is_trading_day(x)]
    
    return td_list


def make_monthly_list(start: date | str, end: date | str | None = None) -> list[date]:
    """
    DEPENDS: make_date_list, is_trading_day
    """
    date_list: list[date] = make_date_list(start=start, end=end) 
    
    monthly_list: list[date] = [x for x in date_list if is_monthly_settlement(x)]
    
    return monthly_list



def make_weekly_list(start: date | str, end: date | str | None = None) -> list[date]:
    """
    DEPENDS: make_date_list, is_trading_day
    """
    date_list: list[date] = make_date_list(start=start, end=end) 
    
    monthly_list: list[date] = [x for x in date_list if is_weekly_settlement(x)]
    
    return monthly_list



def next_sunday(d: date) -> date:
    """
    If d is Sunday, return d + 7

    If d is Sunday, d.toordinal() % 7 is 0

    """
    days_until_sunday = 7 - (d.toordinal() % 7)
    return d + timedelta(days=days_until_sunday)


def next_monday(d: date) -> date:
    n = (d.toordinal() - 1) % 7
    return d + timedelta(days = 7 - n)


def next_tuesday(d: date) -> date:
    n = (d.toordinal() - 2) % 7
    return d + timedelta(days = 7 - n)

def next_wednesday(d: date) -> date:
    n = (d.toordinal() - 3) % 7
    return d + timedelta(days = 7 - n)


def next_thursday(d: date) -> date:
    n = (d.toordinal() - 4) % 7
    return d + timedelta(days = 7 - n)


def next_friday(d: date) -> date:
    """
    USED BY: get_third_friday

    """
    n = (d.toordinal() - 5) % 7
    return d + timedelta(days = 7 - n)


def next_saturday(d: date) -> date:
    n = (d.toordinal() - 6) % 7
    return d + timedelta(days = 7 - n)
    


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


def not_exchange_holiday(d: date) -> bool:
    return not is_exchange_holiday(d)



def not_federal_holiday(d: date) -> bool:
    return not is_federal_holiday(d)




def not_trading_day(d: date) -> bool:
    return is_weekend(d) or is_exchange_holiday(d)


def not_weekly_settlement(d: date) -> bool:
    return not is_weekly_settlement(d)


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





def this_sunday(d: date) -> date:
    """
    INDEPENDENT

    If the input date d is a Sunday, return the input date, otherwise return the coming Sunday.
    
    .weekday()    Mon is 0, Sun is 6
    """
    days_until_sunday = 6 - d.weekday()  # Days from current day to Sunday
    return d + timedelta(days=days_until_sunday)


def this_monday(d: date) -> date:
    """
    if d is a Monday, return d.
    """
    days_until_monday = (7 - d.weekday()) % 7 
    return d + timedelta(days=days_until_monday)

def this_tuesday(d: date) -> date:
    """
    if d is a Tuesday, return d.
    """
    days_until_tuesday = (8 - d.weekday()) % 7 
    return d + timedelta(days=days_until_tuesday)


def this_wednesday(d: date) -> date:
    """
    if d is a Wednesday, return d.
    """
    days_until_wednesday = (9 - d.weekday()) % 7 
    return d + timedelta(days=days_until_wednesday)

def this_thursday(d: date) -> date:
    """
    if d is a Thursday, return d.
    """
    days_until_thursday = (10 - d.weekday()) % 7 
    return d + timedelta(days=days_until_thursday)


def this_friday(d: date) -> date:
    """
    if d is a Friday, return d.
    """
    days_until_friday = (11 - d.weekday()) % 7 
    return d + timedelta(days=days_until_friday)


def this_saturday(d: date) -> date:
    """
    if d is a Saturday, return d.
    """
    days_until_saturday = (12 - d.weekday()) % 7 
    return d + timedelta(days=days_until_saturday)






if __name__ == '__main__':

    d1 = date(2026, 1, 16)
    d2 = date(2025, 12, 31)
    
    
    #x = holiday_good_friday(2025) 
    
    x = next_sunday(d1)
    
    
    
    print(x)
