"""EXIFread.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2025
 Author:
     Lisitsin Y.R.
 Project:
     SCRIPTS_PY
 Module:
     EXIFread.py
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
from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS

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
# get_exif(filename)
#------------------------------------------
def get_exif(filename):
    """get_exif"""
#beginfunction
    image = Image.open(filename)
    exif = image._getexif()
    if exif:
        for tag, value in exif.items():
            decoded = TAGS.get(tag, tag)
            print(f"{decoded}: {value}")
        #endfor
    else:
        print("EXIF data not found")
    #endif
#endfunction

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

    #-------------------------------------------------
    # Отключить журнал 'pytube.helpers'
    #-------------------------------------------------
    logger = logging.getLogger('PIL.TiffImagePlugin')
    logger.setLevel(logging.INFO)

    get_exif(LPath+r'\EXIFread.jpg')
    
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


