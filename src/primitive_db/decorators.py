import functools
from time import monotonic


def handle_db_errors(func):
    """
    Декоратор для обработки ошибок БД
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print("""Ошибка: Файл данных не найден. 
Возможно, база данных не инициализирована. 
Попробуйте снова:""")
        except KeyError as e:
            print(f"""Ошибка: Таблица или столбец {e} не найден. 
Попробуйте снова:""")
        except ValueError as e:
            print(f"""Ошибка валидации: {e}
Попробуйте снова:""")
        except Exception as e:
            print(f"""Произошла непредвиденная ошибка: {e}
Попробуйте снова:""")
    return wrapper

def confirm_action(action_name):
    """
    Декоратор для подтверждения действия пользователя
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            answer = input(f'Вы уверены, что хотите выполнить "{action_name}"?[y/n]:\n')
            if answer.lower() != "y":
                print("Операция отменена")
                return None
            return func(*args, **kwargs)
        return wrapper
    return decorator

def log_time(func):
    """
    Измерение времени работы функции
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func_start = monotonic()
        try:
            return func(*args, **kwargs)
        finally:
            func_end =  monotonic() - func_start
            print(f"{func.__name__} выполнилась за {func_end:.3f} секунд")
    return wrapper

def create_cacher():
    """
    Возвращает функцию кэширования, хранящую кэш в замыкании
    """
    cache = {}
    def cache_result(key, value_func):
        """
        Функция проверяет наличие кэша, 
        при необходимости записывает или выводит его
        """
        if key in cache:
            return cache[key]
        result = value_func()
        cache[key] = result
        return result

    return cache_result