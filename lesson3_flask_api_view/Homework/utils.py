import requests as requests

from http import HTTPStatus
from typing import List, Dict

from faker import Faker
from flask import Flask, request, jsonify, Response


def get_students(count: int) -> List[Dict[str, str]]:
    students_list = []
    fake_student = Faker('UK')
    for i in range(count):
        students_list.append(
            {
                'first_name': fake_student.first_name(),
                'last_name': fake_student.last_name(),
                'email': fake_student.free_email(),
                'password': fake_student.password(),
                'birthday': fake_student.date_of_birth(minimum_age=16,
                                                       maximum_age=50).strftime('%d,%m,%Y')
            }
        )

    return students_list


def get_rates(currency: str):
    url = "https://bitpay.com/api/rates"
    result = requests.get(url, {})
    if result.status_code not in (HTTPStatus.OK,):
        return Response(
            "ERROR: Something went wrong",
            status=result.status_code
        )
    result = result.json()
    for coin in result:
        if coin['code'] == currency.upper():
            result = coin['rate']
            return result

    return f'Sorry, the specified exchange rate of <b>"{currency}"</b> - is not available'


def get_symbol(currency: str):
    url = "https://bitpay.com/currencies"
    result = requests.get(url, {})
    if result.status_code not in (HTTPStatus.OK,):
        return Response(
            "ERROR: Something went wrong",
            status=result.status_code
        )
    result = result.json()
    for value in result['data']:
        if value['code'] == currency.upper():
            result = value['symbol']
            return result

    return f'Sorry, the specified symbol of <b>"{currency}"</b> currency - is not available'
