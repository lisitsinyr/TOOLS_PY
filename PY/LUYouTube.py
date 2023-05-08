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
import pytube.exceptions
from pytube import YouTube
from pytube import Playlist
from pytube import exceptions

#------------------------------------------
# БИБЛИОТЕКИ LU
#------------------------------------------
import LULog
# import LUConst
import LUObjects
import LUObjectsYT
import LUFile
import LUDateTime

# --------------------------------------------
# TYouTubeObjectsItem
# --------------------------------------------
class TYouTubeObjectsItem (object):
    """TYouTubeObjectsItem"""
    luClassName = "TYouTubeObjectsItem"

    #--------------------------------------------------
    # constructor
    #--------------------------------------------------
    def __init__(self):
        """Constructor"""
        super().__init__()
        self.__FYouTubeObject: LUObjectsYT.TYouTubeObject = LUObjectsYT.TYouTubeObject()
    #endfunction

    #--------------------------------------------------
    # destructor
    #--------------------------------------------------
    def __del__(self):
        """destructor"""
        # удалить объект
        del self.__FYouTubeObject
        LClassName = self.__class__.__name__
        s = '{} уничтожен'.format (LClassName)
        # LULog.LoggerTOOLS.log (LULog.DEBUGTEXT, s)
    #endfunction

    #--------------------------------------------------
    # @property YouTubeObject
    #--------------------------------------------------
    # getter
    @property
    def YouTubeObject(self):
    #beginfunction
        return self.__FYouTubeObject
    #endfunction
    @YouTubeObject.setter
    def YouTubeObject(self, Value: LUObjectsYT.TYouTubeObject):
    #beginfunction
        self.__FYouTubeObject = Value
    #endfunction
#endclass

# --------------------------------------------
# TYouTubeObjectsCollection
# --------------------------------------------
class TYouTubeObjectsCollection (list):
    """TObjectsCollection"""
    luClassName = "TYouTubeObjectsCollection"

    #--------------------------------------------------
    # constructor
    #--------------------------------------------------
    def __init__ (self):
        """Constructor"""
    #beginfunction
        super ().__init__ ()
    #endfunction

    #--------------------------------------------------
    # destructor
    #--------------------------------------------------
    def __del__ (self):
        """destructor"""
    #beginfunction
        self.clear()            # удалить все items
        LClassName = self.__class__.__name__
        s = '{} уничтожен'.format (LClassName)
        # LULog.LoggerTOOLS.log (LULog.DEBUGTEXT, s)
    #endfunction

    def AddItem (self) -> TYouTubeObjectsItem:
        """AddItem"""
    #beginfunction
        LYouTubeObjectsItem: TYouTubeObjectsItem = TYouTubeObjectsItem ()
        self.append (LYouTubeObjectsItem)
        return self [self.__len__()-1]
    #endfunction

    def GetItem (self, Index: int) -> TYouTubeObjectsItem:
        """GetItem"""
    #beginfunction
        LResult: TYouTubeObjectsItem = self [Index]
        return LResult
    #endfunction

    def SetItem (self, Index: int, Value: TYouTubeObjectsItem):
        """SetItem"""
    #beginfunction
        self [Index] = Value
    #endfunction

    def FindYouTubeObjectsItemURL (self, AURL: str) -> TYouTubeObjectsItem:
        """Поиск YouTubeObjectsItem по AURL"""
    #beginfunction
        for item in self:
            LYouTubeObjectsItem:TYouTubeObjectsItem = item
            LURL = LYouTubeObjectsItem.YouTubeObject.URL
            if LURL == AURL:
                return LYouTubeObjectsItem
            #endif
        #endfor
        return None
    #endfunction
#endclass

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
        # YouTubeObjectsCollection
        self.__FYouTubeObjectsCollection = TYouTubeObjectsCollection ()

        # self.__FAPPWorkDir = LUos.APPWorkDir ()
        # self.__FAPPWorkDir = LUos.GetCurrentDir ()
        self.__FAPPWorkDir = LUFile.ExtractFileDir(sys.argv[0])
    #endfunction

    #--------------------------------------------------
    # destructor
    #--------------------------------------------------
    def __del__ (self):
        """ destructor """
    #beginfunction
        del self.__FYouTubeObjectsCollection
        LClassName = self.__class__.__name__
        s = '{} уничтожен'.format (LClassName)
        # LULog.LoggerTOOLS.log (LULog.DEBUGTEXT, s)
        #print (s)
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

    #--------------------------------------------------
    # CreateURLItems (self, AURL: str):
    #--------------------------------------------------
    def CreateURLItems (self, AURL: str, AMaxRes: ()):

        def _CreateYOUTUBEObject_Coll (AURL: str, APlayList: str, ANumber: int, ACount: int):
        #beginfunction
            LURL = AURL
            s = 'CreateObject...'
            # self.__FFileMemoLog.AddLog (LULog.TTypeLogString.tlsPROCESS, s)
            LULog.LoggerTOOLS.log(LULog.PROCESS, s)
            s = AURL + ' новый.'
            # self.__FFileMemoLog.AddLog (LULog.TTypeLogString.tlsPROCESS, s)
            LULog.LoggerTOOLS.log(LULog.PROCESS, s)

            LObjectID: datetime = LUDateTime.Now()
            s = LUDateTime.GenerateObjectIDStr (LObjectID)
            # self.__FFileMemoLog.AddLog (LULog.TTypeLogString.tlsPROCESS, LObjectIDStr)
            LULog.LoggerTOOLS.log(LULog.PROCESS, s)

            # LYouTubeObjectItem
            LYouTubeObjectsItem = self.__FYouTubeObjectsCollection.AddItem()
            LYouTubeObjectsItem.YouTubeObject.ID = LObjectID
            LYouTubeObjectsItem.YouTubeObject.SetURL(LURL, AMaxRes, APlayList, ANumber, ACount)
            LYouTubeObjectsItem.YouTubeObject.FONcomplete = LUObjectsYT.ONcomplete
            LYouTubeObjectsItem.YouTubeObject.FONprogress = LUObjectsYT.ONprogress
        #endfunction

        def _CreateYOUTUBEPlaylists (AURL: str):
        #beginfunction
            """
            # ЦИКЛ ОТ i=0 ДО AURLPlaylists.count-1
            """
            ...
        #endfunction

        def _CreateYOUTUBEPlaylist (AURL: str):
        #beginfunction
            LPlaylist = Playlist (AURL)
            Lvideo_urls = LPlaylist.video_urls
            j = len(LPlaylist.video_urls)
            i = 0
            for url in Lvideo_urls:
                i = i + 1
                # CreateObject
                if self.__FYouTubeObjectsCollection.FindYouTubeObjectsItemURL (url) is not None:
                    s = url + ' уже существует.'
                    # self.__FFileMemoLog.AddLog (LULog.TTypeLogString.tlsINFO, s)
                    LULog.LoggerTOOLS.info (s)
                else:
                    _CreateYOUTUBEObject_Coll (url, LPlaylist.title, i, j)
                #endif
            #endfor
        #endfunction

    #beginfunction
        LURI = urlparse (AURL)
        if LURI.hostname.upper () == LUObjectsYT.CYOUTUBE_COM or LURI.hostname.upper () == LUObjectsYT.CYOUTUBE_BE:
            if LUObjectsYT.CYOUTUBE_PLAYLISTS in LURI.path.upper ():
                _CreateYOUTUBEPlaylists (AURL)
            else:
                if LUObjectsYT.CYOUTUBE_PLAYLIST in LURI.path.upper ():
                    _CreateYOUTUBEPlaylist (AURL)
                else:
                    if self.__FYouTubeObjectsCollection.FindYouTubeObjectsItemURL (AURL) is not None:
                        s = AURL + ' уже существует.'
                        LULog.LoggerTOOLS.info (s)
                    else:
                        _CreateYOUTUBEObject_Coll (AURL, '', 0, 0)
                    #endif
                #endif
            #endif
        #endif
    #endfunction
#endclass

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
