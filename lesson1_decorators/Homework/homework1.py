import functools
import requests


# TODO: 1. Реалізувати LFU алгоритм для кешування. За базу берем існуючий декоратор.Написати для фетчування URL-ів.
#  Додати можливість указати максимум елементів в кеші.


def lfu_cache(func, maxsize=100):
    cache = {}
    cache_count = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key_arg = args[0]
        if key_arg in cache:
            result = cache[key_arg]
            cache_count[key_arg] += 1
        else:
            if len(cache) == maxsize:
                min_key, min_count = sorted(cache_count.items(), key=lambda item: item[1])[0]
                cache.pop(min_key)
                cache_count.pop(min_key)
            result = func(*args, **kwargs)
            cache[key_arg] = result
            cache_count[key_arg] = 1
            return result

    return wrapper


@lfu_cache
def fetch_url(url, first_n=100):
    """Fetch a given url"""
    res = requests.get(url)
    fetch_result = res.content[:first_n] if first_n else res.content
    return fetch_result


fetch_url('https://telegram.org/')
fetch_url('https://telegram.org/')
fetch_url('https://google.com')
fetch_url('https://ithillel.ua')
fetch_url('https://dou.ua')
fetch_url('https://ain.ua')
fetch_url('https://ain.ua')
