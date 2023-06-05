"""LUQTimer.py"""
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
     LUQTimer.py

 =======================================================
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import psutil

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
import PySide6.QtCore as QtCore
from PySide6.QtCore import QObject, QThread, Signal, Slot, QTimer, QCoreApplication
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget

#------------------------------------------
# БИБЛИОТЕКА LU
#------------------------------------------
import LULog

# Signals must inherit QObject
class MySignals(QObject):
    signal_str = Signal(str)
    signal_int = Signal(int)
#endclass

class TQTimer (QTimer):
    """TQTimer"""
    luClassName = 'TQTimer'

    signals = MySignals ()

    #--------------------------------------------------
    # constructor
    #--------------------------------------------------
    def __init__ (self, parent=None):
    #beginfunction
        QTimer.__init__ (self, parent=parent)
        self.__FStopTimer = False
        self.__Fidle = False
        self.__Fparent = parent
        # self.interval = 1
        self.setInterval (1)

        self.signals.signal_str.connect (parent.update_str_field)
        self.signals.signal_int.connect (parent.update_int_field)

        # self.timeout.connect (self.run_CPU)
    #endfunction

    #--------------------------------------------------
    # destructor
    #--------------------------------------------------
    def __del__ (self):
        """destructor"""
    #beginfunction
        LClassName = self.__class__.__name__
        s = '{} уничтожен'.format (LClassName)
        # LULog.LoggerTOOLS.log (LULog.DEBUGTEXT, s)
        #print (s)
    #endfunction

    #--------------------------------------------------
    # @property QTimer
    #--------------------------------------------------
    # getter
    @property
    def QTimer(self) -> QTimer:
    #beginfunction
        return self
    #endfunction

    #--------------------------------------------------
    # start
    #--------------------------------------------------
    def start(self):
        """start - Запуск таймера..."""
    #beginfunction
        s = 'Запуск таймера ...'
        # LULog.LoggerTOOLS.log (LULog.DEBUGTEXT, s)
        super ().start ()
        self.__Fidle = True
    #endfunction

    #--------------------------------------------------
    # stop
    #--------------------------------------------------
    def stop(self):
        """stop - Остановить таймер..."""
    #beginfunction
        s = 'stop - Остановить таймер...'
        # LULog.LoggerTOOLS.log (LULog.DEBUGTEXT, s)
        super ().stop ()
    #endfunction

    #--------------------------------------------------
    # run_CPU
    #--------------------------------------------------
    def run_CPU(self):
        """run_CPU..."""
    #beginfunction
        s = 'run_CPU...'
        LULog.LoggerTOOLS.debug (s)

        # Do something on the worker thread
        a = 1 + 1
        # Emit signals whenever you want
        self.signals.signal_int.emit (a)
        self.signals.signal_str.emit ("This text comes to Main thread from our Worker thread.")

        while self.__Fidle:
            QCoreApplication.processEvents ()
        #endwhile

        # while 1:
        #     Lval = psutil.cpu_percent ()
        #     self.signals.signal_int.emit (Lval)
        #     self.signals.signal_str.emit ('CPU_VALUE')
        #
        #     # self.emit(QtCore.SIGNAL('CPU_VALUE'), Lval)
        #     QCoreApplication.processEvents ()
        # #endwhile
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
