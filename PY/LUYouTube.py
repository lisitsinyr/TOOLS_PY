"""LUYouTube.py"""
# -*- coding: UTF-8 -*-
__annotations__ ="""
 =======================================================
 Copyright (c) 2023
 Author:
     Lisitsin Y.R.
 Project:
     LU_PY
     Python (LU)
 Module:
     LUYouTube.py

 =======================================================
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import sys
import logging
import datetime
from typing import BinaryIO
from urllib.parse import urlparse

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
from pytube import YouTube
from pytube import Playlist
from pytube import exceptions

#------------------------------------------
# БИБЛИОТЕКИ LU
#------------------------------------------
import LUConst
import LUObjects
import LUObjectsYouTube
import LULog
import LUFile
import LUos
import LUDateTime

# LULogger = logging.getLogger(__name__)

class TYouTube(object):
    """TYouTube"""
    __annotations__ = \
        """
        TPParams - Параметры проекта
        """
    luClassName = 'TYouTube'

    #--------------------------------------------------
    # constructor
    #--------------------------------------------------
    def __init__ (self, **kwargs):
        """ Constructor """
    #beginfunction
        super ().__init__ (**kwargs)
        # ObjectsCollection
        self.__FObjectsCollection = LUObjects.TObjectsCollection ()
        # YouTubeObjectsCollection
        self.__FYouTubeObjectsCollection = LUObjectsYouTube.TYouTubeObjectsCollection ()
        # # Params
        # self.__FParams: YOUTUBE_Params.TParams = YOUTUBE_Params.TParams()

        self.__FAPPWorkDir = LUos.APPWorkDir ()
        self.__FAPPWorkDir = LUos.GetCurrentDir ()
        self.__FAPPWorkDir = LUFile.ExtractFileDir(sys.argv[0])

        # Журнал
        self.__FFileMemoLog: LULog.TFileMemoLog  = LULog.TFileMemoLog ()
        # LLogDir = self.__Fargs.log
        LLogDir = ''
        if len (LLogDir) == 0:
            LLogDir = LUFile.IncludeTrailingBackslash(self.__FAPPWorkDir) + 'LOG'
        else:
            LLogDir = LUFile.ExpandFileName (LLogDir)
        #endif
        LLogDir = LUFile.GetDirNameYYMM (LLogDir, LUDateTime.Now())
        self.__FFileMemoLog.FileName = LUFile.IncludeTrailingBackslash (LLogDir)+'_'+LULog.GetLogFileName ()
    #endfunction

    #--------------------------------------------------
    # destructor
    #--------------------------------------------------
    def __del__ (self):
        """ destructor """
    #beginfunction
        # self.__FObjectsCollection
        del self.__FObjectsCollection
        # self.__FYouTubeObjectsCollection
        del self.__FYouTubeObjectsCollection
        LClassName = self.__class__.__name__
        print('{} уничтожен'.format(LClassName))
    #endfunction

    #--------------------------------------------------
    # @property YouTubeObjectsCollection
    #--------------------------------------------------
    # getter
    @property
    def YouTubeObjectsCollection (self):
    #beginfunction
        return self.__FYouTubeObjectsCollection
    #endfunction

    def _CreateYOUTUBEPlaylists (self, AURL: str):
    #beginfunction
        """
        # ЦИКЛ ОТ i=0 ДО AURLPlaylists.count-1
        """
        ...
    #endfunction

    def _CreateYOUTUBEPlaylist (self, AURL: str):
    #beginfunction
        LPlaylist = Playlist (AURL)
        Lvideo_urls = LPlaylist.video_urls
        j = len(LPlaylist.video_urls)
        i = 0
        for url in Lvideo_urls:
            i = i + 1
            # CreateObject
            if self.__FYouTubeObjectsCollection.FindYouTubeObjectsItemURL (url) is not None:
                self.__FFileMemoLog.AddLog (LULog.TTypeLogString.tlsINFO, url + ' уже существует.')
            else:
                self._CreateYOUTUBEObject (url, LPlaylist.title, i, j)
            #endif
        #endfor
    #endfunction

    def _ONprogress(self, stream, chunk, bytes_remaining):
    #beginfunction
        s = '_ONprogress'
        # print (s)
        # print (stream.filesize)
        # print (len(chunk))
        # print (bytes_remaining)
        LUConst.GLULogger.info (s)
    #endfunction

    def _ONcomplete(self, stream, file_path):
    #beginfunction
        s = '_ONcomplete'
        # print (s)
        # print (stream)
        # print (file_path)
        LUConst.GLULogger.info (s)
    #endfunction

    def _CreateYOUTUBEObject_Coll (self, AURL: str, APlayList: str, ANumber: int, ACount: int):
    #beginfunction
        LURL = AURL
        s = 'CreateObject...'
        self.__FFileMemoLog.AddLog (LULog.TTypeLogString.tlsINFO, s)
        LUConst.GLULogger.info (s)
        s = AURL + ' новый.'
        self.__FFileMemoLog.AddLog (LULog.TTypeLogString.tlsINFO, s)
        LUConst.GLULogger.info (s)
        LObjectID: datetime = LUDateTime.Now()
        LObjectIDStr: str = LUDateTime.GenerateObjectIDStr (LObjectID)
        self.__FFileMemoLog.AddLog (LULog.TTypeLogString.tlsINFO, LObjectIDStr)

        # LYouTubeObjectItem
        LYouTubeObjectsItem = self.__FYouTubeObjectsCollection.AddItem()
        LYouTubeObjectsItem.YouTubeObject.ID = LObjectID
        LYouTubeObjectsItem.YouTubeObject.SetURL(LURL, APlayList, ANumber, ACount)
        LYouTubeObjectsItem.YouTubeObject.FONcomplete = self._ONcomplete
        LYouTubeObjectsItem.YouTubeObject.FONprogress = self._ONprogress
    #endfunction

    def _CreateYOUTUBEObject (self, AURL: str, APlayList: str, ANumber: int, ACount: int) -> LUObjectsYouTube.TYouTubeObject:
    #beginfunction
        LURL = AURL
        s = 'CreateObject...'
        self.__FFileMemoLog.AddLog (LULog.TTypeLogString.tlsINFO, s)
        LUConst.GLULogger.info (s)
        s = AURL + ' новый.'
        self.__FFileMemoLog.AddLog (LULog.TTypeLogString.tlsINFO, s)
        LUConst.GLULogger.info (s)
        LObjectID: datetime = LUDateTime.Now()
        LObjectIDStr: str = LUDateTime.GenerateObjectIDStr (LObjectID)
        self.__FFileMemoLog.AddLog (LULog.TTypeLogString.tlsINFO, LObjectIDStr)

        # LYouTubeObjectItem
        LYouTubeObject = LUObjectsYouTube.TYouTubeObject()
        LYouTubeObject.ID = LObjectID
        LYouTubeObject.SetURL(LURL, APlayList, ANumber, ACount)
        LYouTubeObject.FONcomplete = self._ONcomplete
        LYouTubeObject.FONprogress = self._ONprogress
        return LYouTubeObject
    #endfunction

    #--------------------------------------------------
    # CreateURLItems (self, AURL: str):
    #--------------------------------------------------
    def CreateURLItems (self, AURL: str):
    #beginfunction
        LURI = urlparse (AURL)
        if LURI.hostname.upper () == LUObjectsYouTube.CYOUTUBE_COM or LURI.hostname.upper () == LUObjectsYouTube.CYOUTUBE_BE:
            if LUObjectsYouTube.CYOUTUBE_PLAYLISTS in LURI.path.upper():
                self._CreateYOUTUBEPlaylists (AURL)
            else:
                if LUObjectsYouTube.CYOUTUBE_PLAYLIST in LURI.path.upper():
                    self._CreateYOUTUBEPlaylist (AURL)
                else:
                    if self.__FYouTubeObjectsCollection.FindYouTubeObjectsItemURL (AURL) is not None:
                        self.__FFileMemoLog.AddLog (LULog.TTypeLogString.tlsINFO, AURL + ' уже существует.')
                    else:
                        self._CreateYOUTUBEObject_Coll (AURL, '', 0, 0)
                    #endif
                #endif
            #endif
        #endif
    #endfunction

    def _CheckPlaylists (self, AURL: str) -> list:
    #beginfunction
        LURLs: list = list()
        LURLs.clear()
        """
        # ЦИКЛ ОТ i=0 ДО AURLPlaylists.count-1
        """
        return LURLs
    #endfunction

    def _CheckYOUTUBEPlaylist (self, AURL: str) -> list:
    #beginfunction
        LURLs: list = list()
        LURLs.clear()
        LPlaylist = Playlist (AURL)
        Lvideo_urls = LPlaylist.video_urls
        j = len(LPlaylist.video_urls)
        i = 0
        for url in Lvideo_urls:
            i = i + 1
            LURLs.append(self._CreateYOUTUBEObject (url, LPlaylist.title, i, j))
        #endfor
        return LURLs
    #endfunction

    #--------------------------------------------------
    # CreateURLs (self, AURL: str) -> list:
    #--------------------------------------------------
    def CreateURLs (self, AURL: str) -> list:
    #beginfunction
        LURI = urlparse (AURL)
        if LURI.hostname.upper() == LUObjectsYouTube.CYOUTUBE_COM or LURI.hostname.upper() == LUObjectsYouTube.CYOUTUBE_BE:
            if LUObjectsYouTube.CYOUTUBE_PLAYLISTS in LURI.path.upper():
                LURLs = self._CheckPlaylists (AURL)
                return LURLs
            else:
                if LUObjectsYouTube.CYOUTUBE_PLAYLIST in LURI.path.upper():
                    LURLs = self._CheckYOUTUBEPlaylist (AURL)
                    return LURLs
                else:
                    LURLs: list = list ()
                    LURLs.clear ()
                    LURLs.append (self._CreateYOUTUBEObject (AURL, '', 0, 0))
                    return LURLs
                #endif
            #endif
        #endif
    #endfunction
#endclass

# def progress_func (stream, file_handler: BinaryIO, bytes_remaining: int):
def progress_func (stream, chunk: bytes, bytes_remaining: int):
#beginfunction
    print ('progress_func...')
    # print (stream)
    # print (stream.filesize)
    # print (len(chunk))
    # print (bytes_remaining)
    ...
#endfunction

def complete_func (stream, Afile_path: str):
#beginfunction
    print ('complete_func...')
    # print (stream)
    # print (Afile_path)
    ...
#endfunction

#------------------------------------------
#
#------------------------------------------
def DownloadURL (AURL:str, APATH:str, AMaxRes: (), type='video', file_extension = 'mp4',
                 skip_existing = False, filename_prefix=''):
    """DownloadURL"""
#beginfunction
    LURLYouTube: YouTube = YouTube (AURL, on_progress_callback=progress_func, on_complete_callback=complete_func)
    for res in AMaxRes:

        try:
            LStreams = LURLYouTube.streams.filter (type = type, file_extension = file_extension, res = res)
        except BaseException as ERROR:
            s = f'filter={ERROR}'
            # print (s)
            LUConst.GLULogger.error (s)
        #endtry

        if len (LStreams) > 0:
            i = 0
            for LStream in LStreams:
                print (LStream)
                i = i + 1
                Lfilename_prefix = filename_prefix+str (i) + '. '
                try:
                    LFileName  = LStream.download (APATH, skip_existing=skip_existing, filename_prefix=Lfilename_prefix)
                    # print ("Видео успешно загружено: ", LFileName)
                except BaseException as ERROR:
                    print('LoadYouTubeVideo=', ERROR)
                #endtry
            #endfor
            # если по фильтру есть хотя бы один поток
            break
        #endif
    #endfor

    del LURLYouTube
#endfunction

#------------------------------------------
#
#------------------------------------------
def LoadYouTubeVideo (AURL:str, ASAVE_PATH:str):
    """LoadYouTubeVideo1"""
#beginfunction
    try:
        LURLYouTube: YouTube = YouTube(AURL, on_progress_callback=progress_func, on_complete_callback=complete_func)
        # все потоки
        LStreams = LURLYouTube.streams
        # все потоки progressive
        LStreams = LURLYouTube.streams.filter (progressive = True)
        # все потоки video, mp4, 480p
        LStreams = LURLYouTube.streams.filter (type='video', file_extension = 'mp4', res = '480p')
        for LStream in LStreams:
            # print (LStream)
            LFileName  = LStream.download (ASAVE_PATH, skip_existing = False, filename_prefix=LStream.itag)
            # print ("Видео успешно загружено: ", LFileName)
        #endfor
    except BaseException as ERROR:
        print('LoadYouTubeVideo=', ERROR)
    #endtry

    del LURLYouTube
#endfunction

#------------------------------------------
#
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
