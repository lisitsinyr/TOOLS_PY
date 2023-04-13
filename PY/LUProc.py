"""LUProc.py"""
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
     LUProc.py

 =======================================================
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import enum
#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------

#------------------------------------------
# БИБЛИОТЕКИ LU
#------------------------------------------

LULogger = logging.getLogger(__name__)

cProcessWork = 'Идет процесс обработки ...'
cProcessStop = 'Процесс обработки остановлен.'
cProcessBegin = '********* Начало **********************************'
cProcessEnd = '********* Конец ***********************************'

@enum.unique
class TStatApplication(enum.Enum):
    """TStatApplication"""
    caBreak    = enum.auto ()
    caMain     = enum.auto ()
    caTest     = enum.auto ()
    caSheduler = enum.auto ()
    caSetup    = enum.auto ()
    caAbout    = enum.auto ()
    saAction   = enum.auto ()
    caSend     = enum.auto ()
    caRefresh  = enum.auto ()
    caViewLog  = enum.auto ()
    caFree     = enum.auto ()
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
