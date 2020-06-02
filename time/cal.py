from typing import List
from datetime import date, datetime,timedelta


def adddays(d: date, i: int) -> date:
    return d + timedelta(days=i)


def addtradingdays(d: date, i: int) -> date:
    n = i
    day = d
    if i > 0:
        while n > 0:
            day = nexttradingday(day)
            n -= 1
        return day
    elif i < 0:
        while n < 0:
            day = previoustradingday(day)
            n += 1
        return day
    else:
        return d


def exchangeholidays(year: int) -> List[date]:
    return federalholidays(year) + [holidaygoodfriday(year)]


def federalholidays(year: int) -> List[date]:
    # Federal holidays do not include Easter
    # New Years Day might be Saturday and falls into 31 Dec, see year 2010
    # https://www.opm.gov/policy-data-oversight/snow-dismissal-procedures/federal-holidays/
    dec31 = date(year, 12, 31)
    holidays = [holidaynewyears(year), holidaymartinluther(year), holidaywashington(year)
            , holidaymemorial(year), holidayindependence(year), holidaylabor(year)
            , holidaycolumbus(year), holidayveterans(year), holidaythanksgiving(year), holidaychristmas(year)]
    if isfriday(dec31):
        return holidays + [dec31]
    else:
        return holidays


def gettradingday() -> date:
    return previoustradingday(date.today())


def gettradingdayutc() -> date:
    return previoustradingday(getutctoday())


def getutctoday() -> date:
    t = datetime.utcnow()
    return date(t.year, t.month, t.day)


def gregorianeaster(year: int) -> date:
    century = year // 100 + 1
    shifted_epact = (11 * (year % 19) + 14 - (3 * century) // 4 + (8 * century + 5) // 25) % 30
    adjusted_epact = shifted_epact + 1 if shifted_epact == 0 or (shifted_epact == 1 and year % 19 > 10) \
        else shifted_epact
    pascha_moon = adddays(date(year, 4, 19), - adjusted_epact)
    easter = nextsunday(pascha_moon)
    return easter


def holidaynewyears(year: int) -> date:
    jan1 = date(year, 1, 1)
    if issaturday(jan1):
        return adddays(jan1, -1)
    elif issunday(jan1):
        return date(year, 1, 2)
    else:
        return jan1


def holidaymartinluther(year: int) -> date:
    return nextmonday(date(year, 1, 14))


def holidaywashington(year: int) -> date:
    return nextmonday(date(year, 2, 14))


def holidaygoodfriday(year: int) -> date:
    return lastfriday(gregorianeaster(year))


def holidaymemorial(year: int) -> date:
    return lastmonday(date(year, 6, 1))


def holidayindependence(year: int) -> date:
    july4 = date(year, 7, 4)
    if issaturday(july4):
        return date(year, 7, 3)
    elif issunday(july4):
        return date(year, 7, 5)
    else:
        return july4


def holidaylabor(year: int) -> date:
    return nextmonday(date(year, 8, 31))


def holidaycolumbus(year: int) -> date:
    return nextmonday(date(year, 10, 7))


def holidayveterans(year: int) -> date:
    nov11 = date(year, 11, 11)
    if issaturday(nov11):
        return date(year, 11, 10)
    elif issunday(nov11):
        return date(year, 11, 12)
    else:
        return nov11


def holidaythanksgiving(year: int) -> date:
    return nextthursday(date(year, 11, 21))


def holidaychristmas(year: int) -> date:
    dec25 = date(year, 12, 25)
    if issaturday(dec25):
        return date(year, 12, 24)
    elif issunday(dec25):
        return date(year, 12, 26)
    else:
        return dec25


def ismonday(d: date) -> bool: return d.isoweekday() == 1


def istuesday(d: date) -> bool: return d.isoweekday() == 2


def iswednesday(d: date) -> bool: return d.isoweekday() == 3


def isthursday(d: date) -> bool: return d.isoweekday() == 4


def isfriday(d: date) -> bool: return d.isoweekday() == 5


def issaturday(d: date) -> bool: return d.isoweekday() == 6


def issunday(d: date) -> bool: return d.isoweekday() == 7


def isweekend(d: date) -> bool: return issaturday(d) or issunday(d)


def isweekday(d: date) -> bool: return not isweekend(d)


def isexchangeholiday(d: date) -> bool:
    return d in exchangeholidays(d.year)


def isnotexchangeholiday(d: date) -> bool:
    return not isexchangeholiday(d)


def isfederalholiday(d: date) -> bool:
    return d in federalholidays(d.year)


def isnotfederalholiday(d: date) -> bool:
    return not isfederalholiday(d)


def istradingday(d: date) -> bool:
    return not (isweekend(d) or isexchangeholiday(d))


def isnottradingday(d: date) -> bool:
    return isweekend(d) or isexchangeholiday(d)


def isweeklyclose(d: date) -> bool:
    tomorrow = adddays(d, 1)
    if isfriday(d) and isnotexchangeholiday(d):
        return True
    elif isthursday(d) and isexchangeholiday(tomorrow):
        return True
    else:
        return False


def isnotweeklyclose(d: date) -> bool:
    return not isweeklyclose(d)


def lastsaturday(d: date) -> date:
    n = d.toordinal() % 7 + 1
    return adddays(d, -n)


def lastfriday(d: date) -> date:
    n = (d.toordinal() + 1) % 7 + 1
    return adddays(d, -n)


def lastthursday(d: date) -> date:
    n = (d.toordinal() + 2) % 7 + 1
    return adddays(d, -n)


def lastwednesday(d: date) -> date:
    n = (d.toordinal() + 3) % 7 + 1
    return adddays(d, -n)


def lasttuesday(d: date) -> date:
    n = (d.toordinal() + 4) % 7 + 1
    return adddays(d, -n)


def lastmonday(d: date) -> date:
    n = (d.toordinal() + 5) % 7 + 1
    return adddays(d, -n)


def lastsunday(d: date) -> date:
    n = (d.toordinal() + 6) % 7 + 1
    return adddays(d, -n)


def nextsunday(d: date) -> date:
    n = d.toordinal() % 7
    return adddays(d, 7 - n)


def nextmonday(d: date) -> date:
    n = (d.toordinal() - 1) % 7
    return adddays(d, 7 - n)


def nexttuesday(d: date) -> date:
    n = (d.toordinal() - 2) % 7
    return adddays(d, 7 - n)

def nextwednesday(d: date) -> date:
    n = (d.toordinal() - 3) % 7
    return adddays(d, 7 - n)


def nextthursday(d: date) -> date:
    n = (d.toordinal() - 4) % 7
    return adddays(d, 7 - n)


def nextfriday(d: date) -> date:
    n = (d.toordinal() - 5) % 7
    return adddays(d, 7 - n)


def nextsaturday(d: date) -> date:
    n = (d.toordinal() - 6) % 7
    return adddays(d, 7 - n)


def nexttradingday(d: date) -> date:
    day1 = adddays(d, 1)
    day2 = adddays(d, 2)
    day3 = adddays(d, 3)
    day4 = adddays(d, 4)
    if istradingday(day1):
        return day1
    elif istradingday(day2):
        return day2
    elif istradingday(day3):
        return day3
    else:
        return day4


def previoustradingday(d: date) -> date:
    pday1 = adddays(d, -1)
    pday2 = adddays(d, -2)
    pday3 = adddays(d, -3)
    pday4 = adddays(d, -4)
    if istradingday(pday1):
        return pday1
    elif istradingday(pday2):
        return pday2
    elif istradingday(pday3):
        return pday3
    else:
        return pday4


if __name__ == '__main__':
    d1 = date(2018,12,31)
    d2 = date(2019,1,1)
    d3 = date(2019,1,2)
    d4 = date(2019,1,3)
    d5 = date(2019,1,4)
    d6 = date(2019,1,5)
    d7 = date(2019,1,6)
    d1a = date(2019,1,7)
    d2a = date(2019,1,8)
    d3a = date(2019,1,9)
    d4a = date(2019,1,10)
    d5a = date(2019,1,11)
    d6a = date(2019,1,12)
    d7a = date(2019,1,13)
    print(addtradingdays(date(2019,1,1), 250) )
    print(isexchangeholiday(d1))
