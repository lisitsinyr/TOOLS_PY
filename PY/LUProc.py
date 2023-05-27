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

cProcessWork = 'Main: Идет процесс обработки...'
cProcessStop = 'Main: Процесс обработки остановлен...'
cProcessSetup = 'Setup...'
cProcessAbout = 'About...'
cProcessHelp = 'Help...'
cProcessDeleteAll = 'DeleteAll...'

cProcessBegin = '********* Начало **********************************'
cProcessEnd = '********* Конец ***********************************'

@enum.unique
class TStatApplication(enum.Enum):
    """TStatApplication"""
    saRunning    = enum.auto ()
    saBreak    = enum.auto ()
    # saMain     = enum.auto ()
    # saTest     = enum.auto ()
    # saSheduler = enum.auto ()
    # saSetup    = enum.auto ()
    # saAbout    = enum.auto ()
    # saHelp     = enum.auto ()
    # saAction   = enum.auto ()
    # saSend     = enum.auto ()
    # saRefresh  = enum.auto ()
    # saViewLog  = enum.auto ()
    # saFree     = enum.auto ()
    # saStart    = enum.auto ()
    # saStop     = enum.auto ()
    # saAddWidget = enum.auto ()
#endclass
CStatApplication = {
    TStatApplication.saRunning:  'saRunning',
    TStatApplication.saBreak:    'saBreak'
    # TStatApplication.saMain: 'saMain',
    # TStatApplication.saTest: 'saTest',
    # TStatApplication.saSheduler: 'saSheduler',
    # TStatApplication.saSetup: 'saSetup',
    # TStatApplication.saAbout: 'saAbout',
    # TStatApplication.saHelp: 'saHelp',
    # TStatApplication.saAction: 'saAction',
    # TStatApplication.saSend: 'saSend',
    # TStatApplication.saRefresh: 'saRefresh',
    # TStatApplication.saViewLog: 'saViewLog',
    # TStatApplication.saFree: 'saFree',
    # TStatApplication.saStart: 'saStart',
    # TStatApplication.saStop: 'saStop',
    # TStatApplication.saAddWidget: 'saAddWidget'
    }

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
