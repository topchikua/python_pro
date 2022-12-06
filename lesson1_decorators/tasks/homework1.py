import pathlib
import os
import random
import time
import timeit
import functools
from collections import OrderedDict
import requests
import sys
import psutil
import tracemalloc

from time import sleep

"""1. Реалізувати LFU алгоритм для кешування. За базу берем існуючий декоратор.Написати для фетчування юерелів. Додати можливість указати максимум елементів в кеші.
https://uk.wikipedia.org/wiki/%D0%9D%D0%B0%D0%B9%D0%BC%D0%B5%D0%BD%D1%88_%D0%A7%D0%B0%D1%81%D1%82%D0%BE_%D0%92%D0%B8%D0%BA%D0%BE%D1%80%D0%B8%D1%81%D1%82%D0%B0%D0%BD%D0%B8%D0%B9_LFU

2. Створити декоратор для заміру пам'яті.

3. Створити окремий гіт репозиторій для домашніх завдань (github).
Окрема гілка, окрема папка. Пул ріквест на main."""


def cache(max_limit=64):
    def internal(f):
        @functools.wraps(f)
        def deco(*args, **kwargs):
            cache_key = (args, tuple(kwargs.items()))
            if cache_key in deco._cache:
                # переносимо в кінець списку
                deco._cache.move_to_end(cache_key, last=True)
                return deco._cache[cache_key]
            result = f(*args, **kwargs)
            # видаляємо якшо досягли ліміта
            if len(deco._cache) >= max_limit:
                # видаляємо перший елемент
                deco._cache.popitem(last=False)
            deco._cache[cache_key] = result
            return result

        deco._cache = OrderedDict()
        return deco

    return internal


@cache
def fetch_url(url, first_n=100):
    """Fetch a given url"""
    res = requests.get(url)
    return res.content[:first_n] if first_n else res.content


link = 'https://uk.wikipedia.org/wiki/%D0%9D%D0%B0%D0%B9%D0%BC%D0%B5%D0%BD%D1%88_%D0%A7%D0%B0%D1%81%D1%82%D0%BE_%D0%92%D0%B8%D0%BA%D0%BE%D1%80%D0%B8%D1%81%D1%82%D0%B0%D0%BD%D0%B8%D0%B9_LFU'
print(fetch_url(link))

print('System memory:', psutil.virtual_memory())
print(psutil.virtual_memory().active)
