
# STANDARD LIBS
from datetime import date, datetime,timedelta
from typing import List, Tuple





def is_iso_date_format(s: str) -> bool:
    s_list: List[str] = s.split('-')     # ['2020', '02', '29']
    length_list: List[int] = list(map(len, s_list))    # [4, 2, 2]
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




def make_date_ranges(FROM: date, TO: date, years: int) -> List[Tuple[date, date]]:    
    """
    This function returns a list of tuples. 'years' parameter is the maximum time length of each tuple.
    'years' parameter can be 1 or more. 

        FROM = date(2019, 7, 1)
        TO = date(2023, 9, 30)
        xs = make_date_ranges(FROM, TO, 2)

        # xs will be [(datetime.date(2019, 7, 1), datetime.date(2020, 12, 31)), (datetime.date(2021, 1, 1), datetime.date(2022, 12, 31)), (datetime.date(2023, 1, 1), datetime.date(2023, 9, 30))]
    """
    if years < 1 or TO < FROM:
        return []

    ranges = []
    range_start = FROM
    range_end = date(FROM.year + (years - 1), 12, 31)

    while range_end < TO:
        date_tuple = (range_start, range_end)
        ranges.append(date_tuple)
        range_start = date(range_end.year + 1, 1, 1)
        range_end = date(range_end.year + years, 12, 31)
    else:
        date_tuple = (range_start, TO)
        ranges.append(date_tuple)

    return ranges





if __name__ == '__main__':

    s3 =  '2020-02-29'

    print(is_iso_date_format(s3))

#    print(date.fromisoformat(s3))