"""LUObjects.py"""
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
     LUObjects.py

 =======================================================
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import logging
#from enum import Enum, unique
import enum

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------

#------------------------------------------
# БИБЛИОТЕКИ LU
#------------------------------------------
import LULog
import LUConst

# LULogger = logging.getLogger(__name__)

# ===========================================================================
# type
# otUsers, otTask, otTasks, otDirectory, otEMail, otFile, otMonth, otUser 
# ===========================================================================
# class syntax
@enum.unique
class TObjectTypeClass(enum.Enum):
    """TObjectTypeClass"""
    otNone = 0
    otYouTubeObject = 1
    @classmethod
    def Empty(cls):
        ...
#endclass

class TObjects (object):
    """TObjects"""
    luClassName = "TObjects"
    
    #--------------------------------------------------
    # constructor
    #--------------------------------------------------
    def __init__(self):
        """ Constructor """
    #beginfunction
        super().__init__()
        self.__FTag: int = 0
        self.__FObjectType: TObjectTypeClass = TObjectTypeClass.otNone
        self.Clear()
    #endfunction

    #--------------------------------------------------
    # destructor
    #--------------------------------------------------
    def __del__(self):
        """ destructor """
    #beginfunction
        LClassName = self.__class__.__name__  
        s = '{} уничтожен'.format (LClassName)
        LUConst.LULogger.log (LULog.DEBUGTEXT, s)
    #endfunction

    def Clear(self):
    #beginfunction
        self.Tag = 0
        self.ObjectType = TObjectTypeClass.otNone
    #endfunction

    #--------------------------------------------------
    # @property Tag
    #--------------------------------------------------
    # getter
    @property
    def Tag(self) -> int:
    #beginfunction
        return self.__FTag
    #endfunction
    @Tag.setter
    def Tag(self, Value: int):
    #beginfunction
        self.__FTag = Value
    #endfunction

    #--------------------------------------------------
    # @property ObjectType
    #--------------------------------------------------
    # getter
    @property
    def ObjectType(self) -> TObjectTypeClass:
    #beginfunction
        return self.__FObjectType
    #endfunction
    @ObjectType.setter
    def ObjectType(self, Value: TObjectTypeClass):
    #beginfunction
        self.__FObjectType = Value
    #endfunction

# --------------------------------------------
# TObjectsItem
# --------------------------------------------
class TObjectsItem (object):
    """TObjectsItem"""
    luClassName = "TObjectsItem"

    #--------------------------------------------------
    # constructor
    #--------------------------------------------------
    def __init__(self):
        """ Constructor """
        super().__init__()
        self.__FObjects: TObjects = TObjects ()

    #--------------------------------------------------
    # destructor
    #--------------------------------------------------
    def __del__(self):
        """ destructor """
        # удалить объект
        del self.__FObjects
        LClassName = self.__class__.__name__
        s = '{} уничтожен'.format (LClassName)
        LUConst.GLULogger.log (LULog.DEBUGTEXT, s)

    #--------------------------------------------------
    # @property Objects
    #--------------------------------------------------
    # getter
    @property
    def Objects(self):
    #beginfunction
        return self.__FObjects
    #endfunction
    @Objects.setter
    def Objects(self, Value: TObjects):
    #beginfunction
        self.__FObjects: TObjects = Value
    #endfunction
#endclass

# --------------------------------------------
# TObjectsCollection
# --------------------------------------------
class TObjectsCollection (list):
    """TObjectsCollection"""
    luClassName = "TObjectsCollection"
    
    #--------------------------------------------------
    # constructor
    #--------------------------------------------------
    def __init__ (self):
        """ Constructor """
        super ().__init__ ()

    #--------------------------------------------------
    # destructor
    #--------------------------------------------------
    def __del__(self):
        """ destructor """
        self.clear()            # удалить все items
        LClassName = self.__class__.__name__
        s = '{} уничтожен'.format (LClassName)
        LUConst.LULogger.log (LULog.DEBUGTEXT, s)

    def AddItem(self) -> TObjectsItem:
        LObjectsItem: TObjectsItem = TObjectsItem()
        self.append (LObjectsItem)
        return self[self.__len__()-1]

    def GetItem(self, Index: int) -> TObjectsItem:
    #beginfunction
        LResult: TObjectsItem = self[Index]
        return LResult
    #endfunction

    def SetItem(self, Index: int, Value: TObjectsItem):
    #beginfunction
        self[Index] = Value
    #endfunction
#endclass

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
