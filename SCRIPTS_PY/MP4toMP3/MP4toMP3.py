"""MP4toMP3.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2025
 Author:
     Lisitsin Y.R.
 Project:
     SCRIPTS_PY
 Module:
     MP4toMP3.py
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
import pyspeedtest

import moviepy
# from moviepy.editor import VideoFileClip

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
    # 🔹 Укажите путь к видеофайлу
    video_path = r"M:\VIDEO\РУССКИЕ\СССР\А\_Адьютант его превосходительства - 1969 - СССР - (мелодрама, приключения, военный)\Адьютант его превосходительства_1969_01.avi"
    audio_path = r"P:\MEDIA\AUDIO [КИНО]\РУССКИЕ\СССР\Адьютант его превосходительства - 1969 - СССР - (мелодрама, приключения, военный)\Адьютант его превосходительства_1969_01.mp3"
    # 🔹 Загружаем видео
    video = moviepy.VideoFileClip(video_path)
    # 🔹 Извлекаем аудиодорожку
    audio = video.audio
    audio.write_audiofile(audio_path)
    print(f"✅ Аудио сохранено как {audio_path}")

    # 🔹 Укажите путь к видеофайлу
    video_path = r"M:\VIDEO\РУССКИЕ\СССР\А\_Адьютант его превосходительства - 1969 - СССР - (мелодрама, приключения, военный)\Адьютант его превосходительства_1969_02.avi"
    audio_path = r"P:\MEDIA\AUDIO [КИНО]\РУССКИЕ\СССР\Адьютант его превосходительства - 1969 - СССР - (мелодрама, приключения, военный)\Адьютант его превосходительства_1969_02.mp3"
    # 🔹 Загружаем видео
    video = moviepy.VideoFileClip(video_path)
    # 🔹 Извлекаем аудиодорожку
    audio = video.audio
    audio.write_audiofile(audio_path)
    print(f"✅ Аудио сохранено как {audio_path}")

        # 🔹 Укажите путь к видеофайлу
    video_path = r"M:\VIDEO\РУССКИЕ\СССР\А\_Адьютант его превосходительства - 1969 - СССР - (мелодрама, приключения, военный)\Адьютант его превосходительства_1969_03.avi"
    audio_path = r"P:\MEDIA\AUDIO [КИНО]\РУССКИЕ\СССР\Адьютант его превосходительства - 1969 - СССР - (мелодрама, приключения, военный)\Адьютант его превосходительства_1969_03.mp3"
    # 🔹 Загружаем видео
    video = moviepy.VideoFileClip(video_path)
    # 🔹 Извлекаем аудиодорожку
    audio = video.audio
    audio.write_audiofile(audio_path)
    print(f"✅ Аудио сохранено как {audio_path}")

    # 🔹 Укажите путь к видеофайлу
    video_path = r"M:\VIDEO\РУССКИЕ\СССР\А\_Адьютант его превосходительства - 1969 - СССР - (мелодрама, приключения, военный)\Адьютант его превосходительства_1969_04.avi"
    audio_path = r"P:\MEDIA\AUDIO [КИНО]\РУССКИЕ\СССР\Адьютант его превосходительства - 1969 - СССР - (мелодрама, приключения, военный)\Адьютант его превосходительства_1969_04.mp3"
    # 🔹 Загружаем видео
    video = moviepy.VideoFileClip(video_path)
    # 🔹 Извлекаем аудиодорожку
    audio = video.audio
    audio.write_audiofile(audio_path)
    print(f"✅ Аудио сохранено как {audio_path}")

    # 🔹 Укажите путь к видеофайлу
    video_path = r"M:\VIDEO\РУССКИЕ\СССР\А\_Адьютант его превосходительства - 1969 - СССР - (мелодрама, приключения, военный)\Адьютант его превосходительства_1969_05.avi"
    audio_path = r"P:\MEDIA\AUDIO [КИНО]\РУССКИЕ\СССР\Адьютант его превосходительства - 1969 - СССР - (мелодрама, приключения, военный)\Адьютант его превосходительства_1969_05.mp3"
    # 🔹 Загружаем видео
    video = moviepy.VideoFileClip(video_path)
    # 🔹 Извлекаем аудиодорожку
    audio = video.audio
    audio.write_audiofile(audio_path)
    print(f"✅ Аудио сохранено как {audio_path}")

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
