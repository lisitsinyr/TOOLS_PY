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
     LUQThread.py

 =======================================================
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import psutil

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
from PySide6.QtCore import QObject, QThread, Signal, Slot
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget

#------------------------------------------
# БИБЛИОТЕКА LU
#------------------------------------------
import LULog

# Signals must inherit QObject
class MySignals(QObject):
    signal_str = Signal(str)
    signal_int = Signal(int)

# Create the Worker Thread
class TQThread (QThread):
    """TQThread"""
    luClassName = 'TQThread'

    #--------------------------------------------------
    # constructor
    #--------------------------------------------------
    # def __init__ (self, AFuction, parent = None):
    def __init__ (self, *args, **kwargs):
    #beginfunction
        # QThread.__init__ (self, parent)
        super ().__init__ (*args, **kwargs)
        self.args = args
        self.kwargs = kwargs

        # self.Function = AFuction

        # # Instantiate signals and connect signals to the slots
        # self.signals = MySignals ()
        # self.signals.signal_str.connect (parent.update_str_field)
        # self.signals.signal_int.connect (parent.update_int_field)

        self.__FStopThread = False
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
    # @property QThread
    #--------------------------------------------------
    # getter
    @property
    def QThread(self) -> QThread:
    #beginfunction
        return self
    #endfunction

    #--------------------------------------------------
    # run
    #--------------------------------------------------
    def run(self):
        """Запуск потока"""
    #beginfunction
        s = 'run - Запуск потока...'
        LULog.LoggerTOOLS.debug (s)
        # self.Function()
        super ().run()
        while not self.__FStopThread:
            s = 'Выполнение потока...'
            # LULog.LoggerTOOLS.debug (s)
            continue
        #endwhile

        # # Do something on the worker thread
        # a = 1 + 1
        # # Emit signals whenever you want
        # self.signals.signal_int.emit (a)
        # self.signals.signal_str.emit ("This text comes to Main thread from our Worker thread.")

        # while 1:
        #     Lval = psutil.cpu_percent ()
        #     # self.emit(QtCore.SIGNAL('CPU_VALUE'), Lval)
        #     ...
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
