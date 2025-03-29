"""QRCode.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2025
 Author:
     Lisitsin Y.R.
 Project:
     SCRIPTS_PY
 Module:
     QRCode.py
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

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
import qrcode
from qrcode.constants import ERROR_CORRECT_H

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
def main ():
    """main"""
#beginfunction
    LUConst.SET_LIB(__file__)

    LULog.STARTLogging (LULog.TTypeSETUPLOG.tslINI, 'console', LUConst.GDirectoryLOG, LUConst.GFileNameLOG,
                        LUConst.GFileNameLOGjson)
    LULog.LoggerTOOLS.level = logging.INFO

    LPath = LUFile.ExtractFileDir(__file__)
    print(f'LPath: {LPath}')

    # Создаем объект QR-кода
    qr = qrcode.QRCode(
        version=1,          # Размер (1-40). Автоматически подбирается, если не указано
        error_correction=ERROR_CORRECT_H,  # Уровень коррекции ошибок (H — высокий)
        box_size=10,        # Размер одного "пикселя" QR-кода (в пикселях)
        border=4            # Поля вокруг QR-кода (по умолчанию 4)
    )

    # Добавляем данные
    # Добавление нескольких данных
    qr.add_data('Скоро Катя придет!')
    qr.add_data("Строка 1")
    qr.add_data("Строка 2")
    qr.make(fit=True)       # Автоматически подбирает размер при необходимости

    # Генерируем изображение
    img = qr.make_image(
        fill_color="black",  # Цвет "черных" блоков
        back_color="white"   # Цвет фона
    )

    img = qr.make_image(
        fill_color="green",  # Зеленые блоки
        back_color="yellow"  # Желтый фон
    )
    # Сохраняем
    img.save(LPath+r'\QRCode.png')    

    # Отображение QR-кода
    # img.show()  # Показывает QR-код в стандартном просмотрщике изображений

    LULog.STOPLogging ()
#endfunction

#------------------------------------------
#
#------------------------------------------
#beginmodule
if __name__ == "__main__":
    main()
#endif

#endmodule


