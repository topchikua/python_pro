from heapq import nsmallest
from operator import itemgetter
import functools
import requests


# TODO: 1. Реалізувати LFU алгоритм для кешування. За базу берем існуючий декоратор.Написати для фетчування URL-ів.
#  Додати можливість указати максимум елементів в кеші.

class Counter(dict):
    """Відображає, де значення за замовчуванням дорівнюють нулю"""

    def __missing__(self, key):
        return 0


def lfu_cache(maxsize=100):
    def decorating_function(user_function):
        cache = {}  # зіставлення аргументів з результатами
        use_count = Counter()  # кількість звернень до кожного ключа
        kwd_mark = object()  # окремі позиційні та ключові аргументи

        @functools.wraps(user_function)
        def wrapper(*args, **kwargs):
            key = args
            if kwargs:
                key += (kwd_mark,) + tuple(sorted(kwargs.items()))
            use_count[key] += 1
            # отримати запис кешу або створити, якщо не знайдено
            try:
                result = cache[key]
                wrapper.hits += 1
            except KeyError:
                result = user_function(*args, **kwargs)
                cache[key] = result
                wrapper.misses += 1
                # видаляємо найменш використовуваний запис в пам'яті
                if len(cache) > maxsize:
                    for key, _ in nsmallest(maxsize // 10,
                                            use_count.iteritems(),
                                            key=itemgetter(1)):
                        del cache[key], use_count[key]
            return result

        def clear():
            cache.clear()
            use_count.clear()
            wrapper.hits = wrapper.misses = 0

        wrapper.hits = wrapper.misses = 0
        wrapper.clear = clear
        print(wrapper)
        return wrapper

    return decorating_function


@lfu_cache(maxsize=100)
def fetch_url(url, first_n=100):
    """Fetch a given url"""
    res = requests.get(url)
    return res.content[:first_n] if first_n else res.content


fetch_url('https://google.com')
fetch_url('https://google.com')
fetch_url('https://ithillel.ua')
fetch_url('https://dou.ua')
fetch_url('https://ain.ua')
fetch_url('https://youtube.com')
