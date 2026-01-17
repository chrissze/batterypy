from datetime import date

from batterypy.cal import holiday_good_friday, next_sunday, is_friday, is_trading_day, parse_date





def test_holiday_good_friday():
    d25 = holiday_good_friday(2025)
    d26 = holiday_good_friday(2026)
    d27 = holiday_good_friday(2027)
    d28 = holiday_good_friday(2028)
    d29 = holiday_good_friday(2029)
    d30 = holiday_good_friday(2030)
    
    assert d25 == date(2025, 4, 18)
    assert d26 == date(2026, 4, 3)
    assert d27 == date(2027, 3, 26)
    assert d28 == date(2028, 4, 14)
    assert d29 == date(2029, 3, 30)
    assert d30 == date(2030, 4, 19)





def test_is_friday():
    d04 = date(2004, 12, 31)
    d10 = date(2010, 12, 31)
    d21 = date(2021, 12, 31)
    d27 = date(2027, 12, 31)
    
    assert is_friday(d04)
    assert is_friday(d10)
    assert is_friday(d21)
    assert is_friday(d27)




def test_is_trading_day():
    d2025 = date(2025, 4, 18)
    d911 = date(2001, 9, 11)  # Tue
    d912 = date(2001, 9, 12)
    d913 = date(2001, 9, 13)
    d914 = date(2001, 9, 14)
    d915 = date(2001, 9, 15)
    d916 = date(2001, 9, 16)
    d917 = date(2001, 9, 17)  # Monday
    
    d04 = date(2004, 12, 31)
    d10 = date(2010, 12, 31)
    d21 = date(2021, 12, 31)
    d27 = date(2027, 12, 31)
    
    
    assert not is_trading_day(d2025)
    assert not is_trading_day(d911)
    assert not is_trading_day(d912)
    assert not is_trading_day(d913)
    assert not is_trading_day(d914)
    assert not is_trading_day(d915)
    assert not is_trading_day(d916)
    assert is_trading_day(d917)

    assert is_trading_day(d04)
    assert is_trading_day(d10)
    assert is_trading_day(d21)
    assert is_trading_day(d27)
    




def test_next_sunday():
    d = date(2025, 4, 13)
    d1 = date(2026, 1, 1)
    d2 = date(2026, 1, 2)
    d3 = date(2026, 1, 3)
    d4 = date(2026, 1, 4)
    d5 = date(2026, 1, 5)
    d6 = date(2026, 1, 6)
    d7 = date(2026, 1, 7)
    
    assert next_sunday(d) == date(2025, 4, 20)
    assert next_sunday(d1) == date(2026, 1, 4)
    assert next_sunday(d2) == date(2026, 1, 4)
    assert next_sunday(d3) == date(2026, 1, 4)
    assert next_sunday(d4) == date(2026, 1, 11)
    assert next_sunday(d5) == date(2026, 1, 11)
    assert next_sunday(d6) == date(2026, 1, 11)
    assert next_sunday(d7) == date(2026, 1, 11)
    



def test_parse_date():
    s1 = '2001-01-01'
    s10 = '  2001-01-01  '
    
    s2 = '20020202'
    s20 = '  20020202    '

    s3 = '690101'
    s4 = '  681231  '
    
    sx = '68131'
    
    assert parse_date(s1) == date(2001, 1, 1)
    assert parse_date(s10) == date(2001, 1, 1)
    
    assert parse_date(s2) == date(2002, 2, 2)
    assert parse_date(s20) == date(2002, 2, 2)
    
    assert parse_date(s3) == date(1969, 1, 1)
    assert parse_date(s4) == date(2068, 12, 31)
    
    assert parse_date(sx) is None
    