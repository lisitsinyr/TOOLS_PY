"""LUErrors.py"""
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
     LUErrors.py

 =======================================================
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import logging

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------

class LUFileError_FileERROR(Exception):
    """Ошибки в модуле LUFile при обработке файла"""
    """
    Атрибуты:
        AFileName: 
        AMessage: объяснение ошибки
    """

    def __init__(self, AFileName: str, AMessage="Файл не существует."):
        self.__FFileName: str = AFileName
        self.__FMessage: str = AMessage
        super().__init__(self.__FMessage)

    # переопределяем метод '__str__'
    def __str__(self):
        return f'{self.__FFileName} -> {self.__FMessage}'

    #--------------------------------------------------
    # @property Message
    #--------------------------------------------------
    # getter
    @property
    def Message(self):
    #beginfunction
        return self.__FMessage
    #endfunction
    @Message.setter
    def Message(self, Value: str):
    #beginfunction
        self.__FMessage: str = Value
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

