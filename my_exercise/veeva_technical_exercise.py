# encoding: utf-8
"""
-------------------------------------------------
Description:    veeva
date:       2021/10/6
author:     lixueji
-------------------------------------------------
"""
from datetime import date


def is_leap_year(year: int)->bool:
    if year % 4 == 0 and year % 100 != 0:
        return True
    elif year % 100 == 0 and year % 400 == 0:
        return True
    return False


# BASIC WAY: BEGIN

def days4month(year: int, month: int)->int:
    if month < 1 or month > 12:
        raise Exception("wrong month")
    if month == 2:
        if is_leap_year(year):
            return 29
        else:
            return 28
    elif month in (1, 3, 5, 7, 8, 10, 12):
        return 31
    else:
        return 30


def dayOfYear(year: int, month: int, day: int)->int:
    days = day
    for m in range(1, month):
        # print(f"month: {m}")
        _days = days4month(year, m)
        days += _days
    print(f"days: {days}")
    return days


# BASIC WAY: END


# use datetime
def dayOfYear_by_datetime(year: int, month: int, day: int)->int:
    dt = date(year, month, day)
    days = (dt - date(dt.year, 1, 1)).days + 1
    # print(f"days: {days}")
    return days


# BETTER WAY: BEGIN

DAYS_MONTHS_WITHOUT_FEB = {
    1: 31, 3: 62, 4: 92, 5: 123, 6: 153, 7: 184, 8: 215, 9: 245, 10: 276, 11: 306
}


# O(1)
def better_dayOfYear(year: int, month: int, day: int)->int:
    _month = month - 1
    feb = 28
    if is_leap_year(year):
        feb = 29
    if _month == 0:
        days = 0
    elif _month == 1:
        days = 31
    elif _month == 2:
        days = 31 + feb
    else:
        days = DAYS_MONTHS_WITHOUT_FEB[_month] + feb
    days += day
    print(f"days: {days}")
    return days

# BETTER WAY: END


def test():
    assert dayOfYear(2016, 1, 3) == 3
    assert dayOfYear(2016, 2, 1) == 32
    assert dayOfYear(2016, 3, 1) == 61
    assert dayOfYear(1990, 3, 1) == 60
    assert dayOfYear(2021, 3, 1) == 60
    params = (2021, 3, 1)
    assert dayOfYear(*params) == dayOfYear_by_datetime(*params)
    params = (2000, 10, 15)
    assert dayOfYear(*params) == dayOfYear_by_datetime(*params)
    params = (1990, 7, 10)
    assert dayOfYear(*params) == dayOfYear_by_datetime(*params)


def test_better():
    assert better_dayOfYear(2016, 1, 3) == 3
    assert better_dayOfYear(2016, 2, 1) == 32
    assert better_dayOfYear(2016, 3, 1) == 61
    assert better_dayOfYear(1990, 3, 1) == 60
    assert better_dayOfYear(2021, 3, 1) == 60
    params = (2021, 3, 1)
    assert better_dayOfYear(*params) == dayOfYear_by_datetime(*params)
    params = (2000, 10, 15)
    assert better_dayOfYear(*params) == dayOfYear_by_datetime(*params)
    params = (1990, 7, 10)
    assert better_dayOfYear(*params) == dayOfYear_by_datetime(*params)


if __name__ == '__main__':
    # test()
    test_better()






