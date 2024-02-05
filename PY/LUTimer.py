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
     LUTimer.py

 =======================================================
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import threading

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------

#------------------------------------------
# БИБЛИОТЕКА LU
#------------------------------------------
import LULog

# Create the Worker Thread
class TTimer (threading.Timer):
    """TQTimer"""
    luClassName = 'TTimer'

    #--------------------------------------------------
    # constructor
    #--------------------------------------------------
    # def __init__ (self, AFuction, parent = None):
    def __init__ (self, AInterval, AFunction, *args, **kwargs):
    #beginfunction
        super ().__init__ (AInterval, AFunction, *args, **kwargs)
        self.args = args
        self.kwargs = kwargs

        self.__FFunction = AFunction

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
    def TTimer(self) -> TTimer:
    #beginfunction
        return self
    #endfunction

    # #--------------------------------------------------
    # # start
    # #--------------------------------------------------
    # def start(self):
    #     """start - Запуск таймера"""
    # #beginfunction
    #     s = 'Запуск таймера...'
    #     LULog.LoggerTOOLS.log (LULog.DEBUGTEXT, s)
    #     # self.Function ()
    #     super ().start ()
    # #endfunction

    #--------------------------------------------------
    # run
    #--------------------------------------------------
    def run(self):
        """run - Запуск таймера"""
    #beginfunction
        s = 'run - Запуск таймера...'
        LULog.LoggerTOOLS.debug (s)
        # super ().run()

        # self.Function()

        while not self.__FStopTimer:
            s = 'Выполнение таймера...'
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
