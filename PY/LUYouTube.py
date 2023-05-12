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

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------

#------------------------------------------
# БИБЛИОТЕКИ LU
#------------------------------------------
import LUObjectsYT
import LUFile

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
        TYouTube - 
        """
    luClassName = 'TYouTube'

    #--------------------------------------------------
    # constructor
    #--------------------------------------------------
    def __init__ (self):
        """ Constructor """
    #beginfunction
        super ().__init__ ()
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
