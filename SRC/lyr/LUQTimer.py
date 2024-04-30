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

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
from  PySide6 import QtCore

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
# import LULog

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

        self.FQTimerName: str = ''

        self.interval = 1
        # self.setInterval (1)

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
        # LULog.LoggerTOOLS_AddLevel (LULog.DEBUGTEXT, s)
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
        s = 'Запуск таймера '+self.FQTimerName+'...'
        LULog.LoggerTOOLS_AddLevel (LULog.DEBUGTEXT, s)
        super ().start ()
        self.__Fidle = True
    #endfunction

    #--------------------------------------------------
    # stop
    #--------------------------------------------------
    def stop(self):
        """stop - Остановить таймер..."""
    #beginfunction
        s = 'Остановка таймера '+self.FQTimerName+'...'
        LULog.LoggerTOOLS_AddLevel (LULog.DEBUGTEXT, s)
        super ().stop ()
    #endfunction

    #--------------------------------------------------
    # __run_TEST
    #--------------------------------------------------
    @QtCore.Slot (str, name = '__run_TEST')
    def __run_TEST(self):
        """__run_TEST..."""
    #beginfunction
        s = '__run_TEST...'
        # LULog.LoggerTOOLS_AddDebug (s)

        # Do something on the worker thread

        # Emit signals whenever you want
        a = 1 + 1
        self.signals.signal_int.emit (a)
        self.signals.signal_str.emit ("This text comes to Main thread from our Worker thread.")

        # while self.__Fidle:
        #     QCoreApplication.processEvents ()
        # #endwhile

        QCoreApplication.processEvents ()
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

#---------------------------------------------------------
# main
#---------------------------------------------------------
def main ():
#beginfunction
    ...
#endfunction

#---------------------------------------------------------
#
#---------------------------------------------------------
#beginmodule
if __name__ == "__main__":
    main()
#endif

#endmodule
