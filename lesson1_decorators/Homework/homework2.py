from datetime import datetime
import tracemalloc


# TODO: 2. Створити декоратор для заміру пам'яті.


def memory_check(msg='Повідомлення не отримано, дефолтний текст...'):
    print(msg)

    def outer(func):
        def wrapper(*args, **kwargs):
            tracemalloc.start()
            result = func(*args, **kwargs)
            first_size, first_peak = tracemalloc.get_traced_memory()
            print(f"{datetime.now()}\nПри виконанні функції: {func.__name__}, \nбуде використано {first_size}B\n")
            tracemalloc.reset_peak()
            return result

        return wrapper

    return outer


@memory_check(msg='Пам\'ять необхідна для обчислень:')
def mylist(n):
    result = [x for x in range(n) if x % 2 == 0]
    return result


mylist(1)
mylist(111)
mylist(65536)
