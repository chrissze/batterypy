from typing import List
from datetime import date, datetime,timedelta


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


if __name__ == '__main__':

    s3 =  '2020-02-29'

    print(is_iso_date_format(s3))

#    print(date.fromisoformat(s3))