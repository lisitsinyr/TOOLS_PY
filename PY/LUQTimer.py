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
import timer

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
# import PySide6.QtCore as QtCore

from PySide6.QtCore import (
    QObject, QThread, Signal, Slot, QTimer, QCoreApplication,
    QEventLoop, QTime, QTimer, Slot
    )
from PySide6.QtWidgets import (
    QApplication, QPushButton, QVBoxLayout, QWidget,
    QLCDNumber
    )

#------------------------------------------
# БИБЛИОТЕКА LU
#------------------------------------------
import LULog

# blocking.py
def wait(milliseconds, /):
    timer = QTimer()
    timer.start(milliseconds)
    wait_for_event(timer.timeout)
def wait_for_event(event, /):
    loop = QEventLoop()
    event.connect(loop.quit)
    loop.exec()


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

class DigitalClock(QLCDNumber):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSegmentStyle(QLCDNumber.Filled)
        self.setDigitCount(8)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_time)
        self.timer.start(1000)

        self.show_time()

        self.setWindowTitle("Digital Clock")
        self.resize(250, 60)

    @Slot (str, name = 'show_time')
    def show_time(self):
        time = QTime.currentTime()
        text = time.toString("hh:mm:ss")

        # Blinking effect
        if (time.second() % 2) == 0:
            text = text.replace(":", " ")

        self.display(text)
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
