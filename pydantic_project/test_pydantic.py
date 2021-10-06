# encoding: utf-8
"""
-------------------------------------------------
Description:    test_pydantic
date:       2021/9/2 18:00
author:     lixueji
-------------------------------------------------
"""
from datetime import datetime
from pprint import pprint
from typing import List, Optional
from pydantic import BaseModel, validator, ValidationError


class User(BaseModel):
    id: int
    name = 'John Doe'
    signup_ts: Optional[datetime] = None
    friends: List[int] = []


# data = {
#     'id': '123',
#     'signup_ts': '2019-06-01 12:22',
#     'friends': [1, 2, '3'],
# }
# user = User(**data)
#
# pprint(user)


# data = {
#     'id': 0,
#     'name': 'test',
#     'friends': [1, None],
# }
# user = User(**data)
#
# print(user)


class Parameter(BaseModel):
    jid: str
    check: Optional[str] = None
    date: str
    timezone: int

    @validator('date')
    def check_date(cls, v):
        try:
            return str2dt(v)
        except Exception as e:
            raise e
        #     raise ValidationError(f'wrong date: {v}')


def str2dt(string: str, format_str="%Y-%m-%d"):
    return datetime.strptime(string, format_str).date()


data = {
    'jid': '2131',
    # 'check': ['sad'],
    # 'date': '2021-08-31',
    'date': '2021-08-31',
    'timezone': '100',
}
p = Parameter(**data)

print(p.dict())
print(p.date)




