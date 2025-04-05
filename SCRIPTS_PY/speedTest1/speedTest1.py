"""speedTest1.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2025
 Author:
     Lisitsin Y.R.
 Project:
     SCRIPTS_PY
 Module:
     speedTest1.py
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

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
import speedtest

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

#------------------------------------------
# func_pass ()
#------------------------------------------
def func_pass():
    """func_pass"""
#beginfunction
    pass
#endfunction

def test_download_speed() -> float:
    """Проверяет скорость загрузки в Mbps"""
    test = speedtest.Speedtest()
    speed = test.download() / 10**6  # Перевод из бит/с в Мбит/с
    return round(speed, 2)

def test_upload_speed() -> float:
    """Проверяет скорость выгрузки в Mbps"""
    test = speedtest.Speedtest()
    speed = test.upload() / 10**6
    return round(speed, 2)

def test_ping() -> float:
    """Проверяет пинг в мс"""
    test = speedtest.Speedtest()
    test.get_best_server()
    return round(test.results.ping, 2)

def speed_test() -> None:
    """Основная функция для вывода результатов теста скорости интернета"""
    try:
        print("🔍 Запуск теста скорости интернета...")
        down_speed = test_download_speed()
        up_speed = test_upload_speed()
        ping = test_ping()

        print(f"📥 Download Speed: {down_speed} Mbps")
        print(f"📤 Upload Speed: {up_speed} Mbps")
        print(f"📡 Ping: {ping} ms")
    except Exception as e:
        print(f"⚠️ Ошибка при проверке скорости: {e}")

#------------------------------------------
def main ():
    """main"""
#beginfunction
    LUConst.SET_LIB(__file__)

    LULog.STARTLogging (LULog.TTypeSETUPLOG.tslINI, 'console', LUConst.GDirectoryLOG, LUConst.GFileNameLOG,
                        LUConst.GFileNameLOGjson)
    LULog.LoggerTOOLS.level = logging.INFO

    LPath = LUFile.ExtractFileDir(__file__)
    print (f'LPath: {LPath}')

    #--------------------------------------------------------------
    # 
    #--------------------------------------------------------------
    speed_test()

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
