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
     LUThread.py

 =======================================================
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import psutil

import threading
import logging

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------

#------------------------------------------
# БИБЛИОТЕКА LU
#------------------------------------------
import LULog

# class ScheduleThread (threading.Thread):
#     @classmethod
#     def run (cls):
#         while not cease_continuous_run.is_set ():
#             schedule.run_pending ()
#             time.sleep (interval)

# threading.Thread.name
#threading.active_count() количество живых потоков,
#threading.current_thread() текущий поток,
#threading.excepthook() обрабатывает неперехваченные исключения в потоках,
#threading.get_ident() идентификатор текущего потока,
#threading.get_native_id() интегральный идентификатор текущего потока,
#threading.enumerate() список объектов всех живых потоков,
#threading.main_thread() объект основной потока,
#threading.TIMEOUT_MAX максимально значение для тайм-аута блокировки.

#threading.active_count():
#Функция threading.active_count() возвращает количество живых потоков - объектов threading.Thread().
#Возвращенное количество равно длине списка, возвращаемого функцией threading.enumerate().

#threading.get_ident():
#Функция threading.get_ident() возвращает идентификатор текущего потока. Это ненулевое целое число.

#threading.enumerate():
#Функция threading.enumerate() возвращает список объектов threading.Thread() всех живых потоков.

class TThread (threading.Thread):
    """TThread"""
    luClassName = 'TThread'

    #--------------------------------------------------
    # constructor
    #--------------------------------------------------
    def __init__ (self, *args, **kwargs):
    # def __init__ (self, group = None, target = None,
    #                            name = None, args = (),
    #                            kwargs = {}, *, daemon = None):

        """Constructor"""
    #beginfunction
        super ().__init__ (*args, **kwargs)
        # super ().__init__ (group = group, target = target,
        #                        name = name,
        #                         *args,
        #                        **kwargs,
        #                         daemon = daemon)
        #
        self.args = args
        self.kwargs = kwargs
        # print ('args=',args)
        # print ('kwargs=',kwargs)
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
    # @property Thread
    #--------------------------------------------------
    # getter
    @property
    def Thread(self) -> threading.Thread:
    #beginfunction
        return self
    #endfunction

    # #--------------------------------------------------
    # # start
    # #--------------------------------------------------
    # def start(self):
    #     """start - Запуск потока"""
    # #beginfunction
    #     s = 'start - Запуск потока...'
    #     LULog.LoggerTOOLS.log (LULog.DEBUGTEXT, s)
    #     # self.Function ()
    #     super ().start ()
    # #endfunction

    #--------------------------------------------------
    # run
    #--------------------------------------------------
    def run(self):
        """run - Запуск потока"""
    #beginfunction
        s = 'run - Запуск потока...'
        LULog.LoggerTOOLS.debug (s)
        super ().run()
        while not self.__FStopThread:
            s = 'Выполнение потока...'
            # LULog.LoggerTOOLS.debug (s)
            continue
        #endwhile
    #endfunction

    #--------------------------------------------------
    # StartThread
    #--------------------------------------------------
    def StartThread(self):
        """StartThread"""
    #beginfunction
        s = 'StartThread...'
        LULog.LoggerTOOLS.debug (s)
        self.__FStopThread = False
        self.run()
    #endfunction
    #--------------------------------------------------
    # StopThread
    #--------------------------------------------------
    def StopThread(self):
        """StopThread"""
    #beginfunction
        s = 'StopThread...'
        LULog.LoggerTOOLS.debug (s)
        self.__FStopThread = True
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
