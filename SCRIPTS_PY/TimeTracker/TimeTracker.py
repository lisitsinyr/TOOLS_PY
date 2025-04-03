"""TimeTracker.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2025
 Author:
     Lisitsin Y.R.
 Project:
     SCRIPTS_PY
 Module:
     TimeTracker.py
 =======================================================
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import os
import sys
import argparse
import logging
import shutil
import filecmp
import psutil
import time

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
import random
import string
import tkinter as tk
import pyperclip
import requests # Импортируем библиотеку requests для выполнения HTTP- запросов
import urllib.request as urllib2
import json

from pynput import mouse, keyboard
import time
import json

#------------------------------------------
# БИБЛИОТЕКА lyrpy
#------------------------------------------
import lyrpy.LUos as LUos
import lyrpy.LUDoc as LUDoc
import lyrpy.LULog as LULog
import lyrpy.LUConst as LUConst
import lyrpy.LUDoc as LUDoc
import lyrpy.LULog as LULog
import lyrpy.LUFile as LUFile
import lyrpy.LUParserARG as LUParserARG

TASKS_FILE = r"D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\PROJECTS_PY\SCRIPTS_PY\SRC\00.TEST\TimeTrackertime_tracker.json"

#------------------------------------------
# load_tasks () -> None:
#------------------------------------------
def load_tasks () -> None:
    """load_tasks"""
    """Загружает список задач из файла."""
#beginfunction
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print("Ошибка чтения файла. Начинаем с пустого списка.")
        return {}
#endfunction

#------------------------------------------
# save_tasks (tasks) -> None
#------------------------------------------
def save_tasks (tasks) -> None:
    """save_tasks"""
    """Сохраняет список задач в файл."""
#beginfunction
    with open(TASKS_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4)
#endfunction

#------------------------------------------
# start_task (tasks) -> None:
#------------------------------------------
def start_task (tasks) -> None:
    """start_task"""
    """Начинает отслеживать задачу."""
#beginfunction
    task_name = input("Введите название задачи: ").strip()
    if task_name in tasks:
        print(f"Задача '{task_name}' уже существует.Продолжение отслеживания.")
    else:
        print(f"Начато отслеживание задачи '{task_name}'.")
    tasks[task_name] = tasks.get(task_name, 0)
    start_time = time.time()
    input("Нажмите Enter, чтобы остановить отслеживание...")
    elapsed_time = time.time() - start_time
    tasks[task_name] += round(elapsed_time)
    print(f"Задача '{task_name}' обновлена:{tasks[task_name]} секунд.")
#endfunction

#------------------------------------------
# view_tasks (tasks) -> None:
#------------------------------------------
def view_tasks (tasks) -> None:
    """view_tasks"""
    """Отображает список задач и потраченное время."""
#beginfunction
    if not tasks:
        print("Нет задач для отображения.")
    else:
        print("\nСписок задач:")
        for task, seconds in tasks.items():
            print(f"{task}: {seconds // 60} минут {seconds % 60} секунд")
#endfunction

#------------------------------------------
# reset_task (tasks) -> None:
#------------------------------------------
def reset_task (tasks) -> None:
    """reset_task"""
    """Сбрасывает время отслеживания задачи."""
#beginfunction
    task_name = input("Введите название задачи для сброса: ").strip()
    if task_name in tasks:
        tasks[task_name] = 0
        print(f"Время задачи '{task_name}' сброшено.")
    else:
        print(f"Задача '{task_name}' не найдена.")
#endfunction

#------------------------------------------
def main ():
    """main"""
#beginfunction
    global text_result
    global pass_length
    global lbl_alert
    global events

    LUConst.SET_LIB(__file__)

    LULog.STARTLogging (LULog.TTypeSETUPLOG.tslINI, 'console', LUConst.GDirectoryLOG, LUConst.GFileNameLOG,
                        LUConst.GFileNameLOGjson)
    LULog.LoggerTOOLS.level = logging.INFO

    LPath = LUFile.ExtractFileDir(__file__)
    print(f'LPath: {LPath}')

    #--------------------------------------------------------------
    # 
    #--------------------------------------------------------------
    tasks = load_tasks()
    print("Программа: Трекер времени задач")
    while True:
        print("\nМеню:")
        print("1. Начать задачу")
        print("2. Просмотреть задачи")
        print("3. Сбросить задачу")
        print("4. Выйти")
        choice = input("Выберите действие (1-4): ").strip()

        if choice == "1":
            start_task(tasks)
            save_tasks(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            reset_task(tasks)
            save_tasks(tasks)
        elif choice == "4":
            print("Выход из программы. До свидания!")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")
    
    LULog.STOPLogging ()
#endfunction

#------------------------------------------
#
#------------------------------------------
#beginmodule
if __name__ == "__main__":
    main ()
# endif

# endmodule
