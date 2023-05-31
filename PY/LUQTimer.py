"""LUThread.py"""
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
from PySide6.QtCore import QObject, QThread, Signal, Slot, QTimer
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

# Create the Worker Thread
class TQTimer (QTimer):
    """TQTimer"""
    luClassName = 'TQTimer'

    #--------------------------------------------------
    # constructor
    #--------------------------------------------------
    def __init__ (self, parent = None):
    #beginfunction
        QTimer.__init__ (self, parent=parent)

        # # Instantiate signals and connect signals to the slots
        # self.signals = MySignals ()
        # self.signals.signal_str.connect (parent.update_str_field)
        # self.signals.signal_int.connect (parent.update_int_field)

        self.__FStopTimer = False

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
    # @property TQTimer
    #--------------------------------------------------
    # getter
    @property
    def TQTimer(self) -> TQTimer:
    #beginfunction
        return self
    #endfunction

    #--------------------------------------------------
    # start
    #--------------------------------------------------
    def start(self):
        """start - Запуск таймера..."""
    #beginfunction
        s = 'Запуск потока...'
        LULog.LoggerTOOLS.log (LULog.DEBUGTEXT, s)
        # self.Function ()
        super ().start ()
    #endfunction

    #--------------------------------------------------
    # stop
    #--------------------------------------------------
    def stop(self):
        """stop - Остановить таймер..."""
    #beginfunction
        s = 'stop - Остановить таймер...'
        LULog.LoggerTOOLS.log (LULog.DEBUGTEXT, s)
        # self.Function ()
        super ().stop ()
    #endfunction

    # #--------------------------------------------------
    # # run
    # #--------------------------------------------------
    # def run(self):
    #     """run - Запуск таймера..."""
    # #beginfunction
    #     s = 'run - Запуск таймера...'
    #     LULog.LoggerTOOLS.debug (s)
    #     # self.Function()
    #     while not self.__FStopTimer:
    #         s = 'Выполнение таймера...'
    #         # LULog.LoggerTOOLS.debug (s)
    #         continue
    #     #endwhile
    #
    #     # # Do something on the worker thread
    #     # a = 1 + 1
    #     # # Emit signals whenever you want
    #     # self.signals.signal_int.emit (a)
    #     # self.signals.signal_str.emit ("This text comes to Main thread from our Worker thread.")
    #
    #     # while 1:
    #     #     Lval = psutil.cpu_percent ()
    #     #     # self.emit(QtCore.SIGNAL('CPU_VALUE'), Lval)
    #     #     ...
    #     # #endwhile
    # #endfunction

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
