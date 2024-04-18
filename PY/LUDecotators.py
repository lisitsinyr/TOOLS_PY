"""LUsys.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2023
 Author:
     Lisitsin Y.R.
 Project:
     LU_PY
     Python (LU)
 Module:
     LUDecotators.py

 =======================================================
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import time
import logging
from functools import wraps
import smtplib
import traceback
from email.mime.text import MIMEText

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------

#------------------------------------------
# БИБЛИОТЕКИ LU
#------------------------------------------
import LULog

#---------------------------------------------------------------
# TIMING
#---------------------------------------------------------------
def TIMING(func):
    #beginfunction
    def wrapper(*args, **kwargs):
    #beginfunction
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        s = f"Функция {func.__name__} работала {end_time - start_time} секунд..."
        LULog.LoggerTOOLS_AddLevel (LULog.DEBUGTEXT, s)
        return result
    return wrapper
    #endfunction
#endfunction

#---------------------------------------------------------------
# retry
#---------------------------------------------------------------
"""
1. Декоратор retry
В проектах по обработке данных и разработке программного обеспечения очень много случаев, когда мы зависим от внешних систем. Не всё всегда находятся под нашим контролем.
Иногда происходят неожиданное событие, во время которых нам бы хотелось, чтобы внешняя система сама исправляла возникнувшие ошибки и перезапускалась.
Я предпочитаю реализовывать эту логику с помощью декоратора retry, который позволяет повторно выполнять программу через N-ное количество времени.
"""
def retry(max_tries=3, delay_seconds=1):
    def decorator_retry(func):
        @wraps(func)
        def wrapper_retry(*args, **kwargs):
            tries = 0
            while tries < max_tries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    tries += 1
                    if tries == max_tries:
                        raise e
                    time.sleep(delay_seconds)
        return wrapper_retry
    return decorator_retry
@retry(max_tries=5, delay_seconds=2)
def call_dummy_api():
    response = None
    # response = requests.get("https://jsonplaceholder.typicode.com/todos/1")
    return response

#---------------------------------------------------------------
# memoize
#---------------------------------------------------------------
"""
2. Результаты функции кэширования
Некоторые части нашего кода редко меняют своё поведение. Тем не менее, если такое всё-таки произойдёт, это может отнять большую часть наших вычислительных мощностей. В таких ситуациях мы можем использовать декоратор для кэширования вызовов функций
Функция будет запущена только один раз, если входные данные совпадают. При каждом последующем запуске результаты будут извлекаться из кэша. Следовательно, нам не нужно будет постоянно выполнять дорогостоящие вычисления.
"""
def memoize(func):
    cache = {}
    def wrapper(*args):
        if args in cache:
            return cache[args]
        else:
            result = func(*args)
            cache[args] = result
            return result
    return wrapper

#---------------------------------------------------------------
# email_on_failure
#---------------------------------------------------------------
"""
5. Декоратор Notification
Наконец, очень полезным декоратором в производственных системах является декоратор Notification.
Ещё раз, даже при нескольких повторных попытках хорошо протестированная кодовая база может потерпеть неудачу. И когда это произойдет, нам нужно сообщить кому-нибудь об этом, чтобы принять быстрые меры.
Это не ново, если вы когда-либо создавали конвейер данных и надеялись, что он всегда будет работать без перебоев.
Следующий декоратор отправляет электронное письмо всякий раз, когда выполнение внутренней функции завершается неудачей. В вашем случае это не обязательно должно быть уведомление по электронной почте. Вы можете настроить его для отправки уведомлений Teams / slack:
"""
def email_on_failure (sender_email, password, recipient_email):
    def decorator (func):
        def wrapper (*args, **kwargs):
            try:
                return func (*args, **kwargs)
            except Exception as e:
                # format the error message and traceback
                err_msg = f"Error: {str (e)}\n\nTraceback:\n{traceback.format_exc ()}"

                # create the email message
                message = MIMEText (err_msg)
                message ['Subject'] = f"{func.__name__} failed"
                message ['From'] = sender_email
                message ['To'] = recipient_email

                # send the email
                with smtplib.SMTP_SSL ('smtp.gmail.com', 465) as smtp:
                    smtp.login (sender_email, password)
                    smtp.sendmail (sender_email, recipient_email, message.as_string ())

                # re-raise the exception
                raise

        return wrapper
    return decorator

#---------------------------------------------------------------
# my_function
#---------------------------------------------------------------
@email_on_failure (sender_email = 'your_email@gmail.com', password = 'your_password',
                   recipient_email = 'recipient_email@gmail.com')
def my_function ():
    # code that might fail
    ...

#---------------------------------------------------------------
# timeit
#---------------------------------------------------------------
"""
To overcome this, created the @timeit decorator which allows you to measure the execution time of the method/function by just adding the @timeit decorator on the method.
@timeit decorator:
"""
def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print ('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
        return result
    return timed

#---------------------------------------------------------------
# get_all_employee_details
#---------------------------------------------------------------
# Adding decorator to the method
@timeit
def get_all_employee_details(**kwargs):
    print ('employee details')
# The code will look like this after removing the redundant code.
# logtime_data = {}
# employees = Employee.get_all_employee_details(log_time=logtime_data)
# Hurray!! All that messy code is gone and now it looks simple and clear.
# log_time and log_name are optional. Make use of them accordingly when needed.

#---------------------------------------------------------------
# timeit
#---------------------------------------------------------------
def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper

@timeit
def calculate_something(num):
    """
    Simple function that returns sum of all numbers up to the square of num.
    """
    total = sum((x for x in range(0, num**2)))
    return total

class Calculator:
    @timeit
    def calculate_something(self, num):
        """
        an example function that returns sum of all numbers up to the square of num
        """
        total = sum((x for x in range(0, num**2)))
        return total

    def __repr__(self):
        return f'calc_object:{id(self)}'

#---------------------------------------------------------------
#
#---------------------------------------------------------------
"""
01.Свойства @property
Декоратор @property облегчает создание свойств в классах Python. Свойства выглядят как обычные атрибуты (поля) класса, но при их чтении вызывается геттер (getter), при записи – сеттер (setter), а при удалении – делитер (deleter). Геттер и делитер опциональны.

02.Статические и классовые методы
Методы могут быть не только у экземпляра класса, но и у самого класса, которые вызываются без какого-то экземпляра (без self). Декораторы @staticmethod и @classmethod как раз делают метод таким (статическим или классовым). Эти декораторы встроены и видны без import.

Статический метод – это способ поместить функцию в класс, если она логически относится к этому классу. Статический метод ничего не знает о классе, из которого его вызвали.

class Foo:
    @staticmethod
    def help():
        print('help for Foo class')
Foo.help()

Классовый метод напротив знает, из какого класса его вызывают. Он принимает неявный первый аргумент (обычно его зовут cls), который содержит вызывающий класс. Классовые методы прекрасно подходят, когда нужно учесть иерархию наследования. Пример: метод group создает список из нескольких людей. Причем для Person – список Person, а для Worker – список Worker. Со @staticmethod такое бы не вышло:

class Person:
    @classmethod
    def group(cls, n):
        # cls именно тот класс, который вызвал
        return [cls() for _ in range(n)]
    def __repr__(self):
        return 'Person'
class Worker(Person):
    def __repr__(self):
        return 'Worker'
print(Person.group(3))
# [Person, Person, Person]
print(Worker.group(2))
# [Worker, Worker]

03.@contextmanager
Этот декоратор позволяет получить из генератора – контекст менеджер. Находится в стандартном модуле contextlib. Пример открытие файла.

from contextlib import contextmanager
@contextmanager
def my_open(name, mode='r'):
    # тут код для получения ресурса
    f = open(name, mode)
    print('Файл открыт:', name)
    try:
        yield f
    finally:
        # Code to release resource, e.g.:
        f.close()
        print('Файл закрыт:', name)
# использование
with my_open('1.txt', 'w') as f:
    f.write('Hello')
    f.fooooo()  # <- error
# Файл открыт: 1.txt
# Traceback (most recent call last):
# Файл закрыт: 1.txt

В этом генераторе есть единственный yield – он возвращает как раз нужный ресурс. Все, что до него – код захвата ресурса (будет выполнен в методе __enter__), например, открытие файла. Мы оборачиваем yield в try/finally, чтобы если даже в блоке кода with произойдет ошибка, то исключение выбросится из yield, но код закрытия файла в блоке finally будет выполнен в любом случае. Код закрытия выполняется в методе __exit__ менеджера контекста.

Асинхронная версия этого декоратора – @asynccontextmanager. Пример:

from contextlib import asynccontextmanager
@asynccontextmanager
async def get_connection():
    conn = await acquire_db_connection()
    try:
        yield conn
    finally:
        await release_db_connection(conn)
# использование
async def get_all_users():
    async with get_connection() as conn:
        return conn.query('SELECT ...')
        
@functools.wraps
Декоратор @functools.wraps полезен при разработке других декораторов. Передает имя, документацию и прочую мета-информацию из декорируемой функции к ее обертке. Подробнее в статье про декораторы.

@atexit.register
Декоратор @atexit.register регистрирует функцию для вызова ее при завершении работы процесса Python.

import atexit
@atexit.register
def goodbye():
    print("You are now leaving the Python sector.")
Измерение времени @timeit
Переходим к самописным декораторам.

Этот декоратор измеряет время выполнения функции, которую декорирует.

import time
from functools import wraps
def timeit(method):
    @wraps(method)
    def timed(*args, **kw):
        ts = time.monotonic()
        result = method(*args, **kw)
        te = time.monotonic()
        ms = (te - ts) * 1000
        all_args = ', '.join(tuple(f'{a!r}' for a in args)
                             + tuple(f'{k}={v!r}' for k, v in kw.items()))
        print(f'{method.__name__}({all_args}): {ms:2.2f} ms')
        return result
    return timed
# использование:
@timeit
def slow_func(x, y, sleep):
    time.sleep(sleep)
    return x + y
slow_func(10, 20, sleep=2)
# печатает: slow_func(10, 20, sleep=2): 2004.65 ms

Как видите, нам не нужно вмешиваться в код функции, не нужно каждый раз писать измеритель времени, декоратор отлично экономит нашу работу: надо измерить время – дописали @timeit и видим все, как на ладони.        

Повторитель
Повторяет вызов функции n раз, возвращает последний результат.

from functools import wraps
def repeat(_func=None, *, num_times=2):
    def decorator_repeat(func):
        @wraps(func)
        def wrapper_repeat(*args, **kwargs):
            value = None
            for _ in range(num_times):
                value = func(*args, **kwargs)
            return value
        return wrapper_repeat
    if _func is None:
        return decorator_repeat
    else:
        return decorator_repeat(_func)
@repeat(num_times=5)
def foo():
    print('текст')
"""

"""    
Замедлитель
Замедляет исполнение функции на нужное число секунд. Бывает полезно для отладки.

from functools import wraps
import time
def slow_down(seconds=1):
    def _slow_down(func):
        # Sleep 1 second before calling the function
        @wraps(func)
        def wrapper_slow_down(*args, **kwargs):
            time.sleep(seconds)
            return func(*args, **kwargs)
        return wrapper_slow_down
    return _slow_down
@slow_down(seconds=0.5)
def foo():
    print('foo')
def bar():
    foo()  # каждый foo по полсекунды
    foo()

Помощник для отладки
Этот декоратор будет логгировать все вызовы функции и печатать ее аргументы и возвращаемое значение.

from functools import wraps
# Печатает сигнатуру вызова и возвращаемое значение
import functools
def debug(func):
    @wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {value!r}")
        return value
    return wrapper_debug
@debug
def testee(x, y):
    print(x + y)
"""


#------------------------------------------
def main ():
#beginfunction
    ...
#endfunction

#------------------------------------------
#
#------------------------------------------
#beginmodule
if __name__ == "__main__":
    main()
#endif

#endmodule
