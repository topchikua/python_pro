import tracemalloc


# TODO: 2. Створити декоратор для заміру пам'яті.


def memory_check(msg):
    print(msg)

    def outer(func):
        def wrapper(*args, **kwargs):
            tracemalloc.start()
            result = func(*args, **kwargs)
            first_size, first_peak = tracemalloc.get_traced_memory()
            print(f"Якщо список генерується з {len(result)} елементів, буде використано {first_size} B")
            tracemalloc.reset_peak()
            return result

        return wrapper

    return outer


@memory_check('Пам\'ять необхідна для обчислень:')
def mylist(n):
    result = [x for x in range(n) if x % 2 == 0]
    return result


mylist(5)
mylist(111)
mylist(65536)
