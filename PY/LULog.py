"""LULog.py"""
# -*- coding: UTF-8 -*-
__annotations__ ="""
 =======================================================
 Copyright (c) 2023
 Author:
     Lisitsin Y.R.
 Project:
     LU_PY
     Python (LU)
 Module:
     LULog.py

 =======================================================
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import os
import sys
import enum
import codecs
import datetime

import logging
# from logging import StreamHandler, FileHandler
# from logging import Formatter, LogRecord
import logging.config

import ast
import json
import pickle

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
from pythonjsonlogger import jsonlogger
import coloredlogs

#------------------------------------------
# БИБЛИОТЕКА LU 
#------------------------------------------
import LUFile
import LUConsole
import LUDateTime
import LULog
import LUStrDecode

# ===========================================================================
# CONST
# ===========================================================================
"""CONST"""
ctlsNOTSET = ' '
ctlsDEBUG = 'D'
ctlsINFO = 'I'
ctlsWARNING = 'W'
ctlsERROR = 'E'
ctlsCRITICAL = 'C'
ctlsBEGIN = '>'
ctlsEND = '<'
ctlsPROCESS = 'P'
ctlsTEXT = ''

TruncLog = 1
LogPath = ''
Log = 30
LogDir = ''
LogFile = ''

# ДОБАВИТЬ LEVEL
BEGIN = 60
END = 70
PROCESS = 80
TEXT = 90
logging.addLevelName(BEGIN, 'BEGIN')
logging.addLevelName(END, 'END')
logging.addLevelName(PROCESS, 'PROCESS')
logging.addLevelName(TEXT, 'TEXT')

# ===========================================================================
# type
# ===========================================================================
@enum.unique
class TTypeLogString(enum.Enum):
    """TTypeLogString"""
    tlsNOTSET = ctlsNOTSET
    tlsDEBUG = ctlsDEBUG
    tlsINFO = ctlsINFO
    tlsWARNING = ctlsWARNING
    tlsERROR = ctlsERROR
    tlsCRITICAL = ctlsCRITICAL
    tlsBEGIN = ctlsBEGIN
    tlsEND = ctlsEND
    tlsPROCESS = ctlsPROCESS
    tlsTEXT = ctlsTEXT
    @classmethod
    def Empty(cls):
        ...
#endclass

@enum.unique
class TTypeLogCODE (enum.Enum):
    """TTypeLogCODE"""
    tlcOEM = 0
    tlcANSI = 1
    @classmethod
    def Empty (cls):
        ...
#endclass

@enum.unique
class TLogOutput (enum.Enum):
    loStandard = 0
    loTextFile = 1
    @classmethod
    def Empty (cls):
        ...
#endclass

#TLogOutputs = set of TLogOutput;

class TFileMemoLog (object):
    """TFileMemoLog"""
    luClassName = "TFileMemoLog"
    __COLORS = {
        ctlsNOTSET: LUConsole.cS_BOLD + LUConsole.sEND,
        ctlsDEBUG: LUConsole.cFG8_BLUE+LUConsole.sEND,
        ctlsINFO: LUConsole.cFG8_WHITE+LUConsole.sEND,
        ctlsWARNING: LUConsole.cS_BOLD + ';' + LUConsole.cFG8_YELLOW+LUConsole.sEND,
        ctlsERROR: LUConsole.cS_BOLD + ';' + LUConsole.cFG8_RED+LUConsole.sEND,
        ctlsCRITICAL: LUConsole.cS_BOLD + ';' + LUConsole.cFG8_BLACK + ';' + LUConsole.cBG8_RED+LUConsole.sEND,

        ctlsBEGIN: LUConsole.cS_BOLD + ';' + LUConsole.cFG8_GREEN + ';' + LUConsole.cBG8_BLACK+LUConsole.sEND,
        ctlsEND: LUConsole.cS_BOLD + ';' + LUConsole.cFG8_GREEN + ';' + LUConsole.cBG8_BLACK+LUConsole.sEND,
        ctlsPROCESS: LUConsole.cS_BOLD + ';' + LUConsole.cFG8_GREEN + ';' + LUConsole.cBG8_BLACK+LUConsole.sEND,
        ctlsTEXT: LUConsole.cS_BOLD + LUConsole.sEND,
    }

    #--------------------------------------------------
    # constructor
    #--------------------------------------------------
    def __init__(self):
        """Constructor"""
    #beginfunction
        super().__init__()
        self.__FCountLogStrings: int = 200
        self.__FFileName: str = ''
        self.__FStandardOut: bool = True
        self.__FLogCODE: TTypeLogCODE = TTypeLogCODE.tlcANSI
        self.__FLogEnabled: bool = True
        self.__FTruncateDays: int = 3
        self.__FLogStringOEM: str = ''
        self.__FLogStringAnsi: str = ''
        self.__FMemoLog = None                        #TMemo
        self.__FLogStrings: list = list()             #TStringList;
        self.__FLogSave: list = list()                #TStringList;
        self.__FLogCODE = LUFile.cDefaultEncoding
        self.Clear ()
    #endfunction

    #--------------------------------------------------
    # destructor
    #--------------------------------------------------
    def __del__(self):
        """destructor"""
    #beginfunction
        del self.__FLogStringOEM
        del self.__FLogStringAnsi
        del self.__FFileName
        del self.__FLogStrings
        del self.__FLogSave
        LClassName = self.__class__.__name__
        print('{} уничтожен'.format(LClassName))
    #endfunction

    def Clear(self):
        """Clear"""
    #beginfunction
        ...
    #endfunction

    #--------------------------------------------------
    # @property LogCODE
    #--------------------------------------------------
    @property
    # getter
    def LogCODE (self) -> int:
    #beginfunction
        return self.__FLogCODE
    #endfunction
    @LogCODE.setter
    def LogCODE (self, Value: int):
    #beginfunction
        self.__FLogCODE = Value
    #endfunction

    #--------------------------------------------------
    # @property CountLogStrings
    #--------------------------------------------------
    @property
    # getter
    def CountLogStrings (self) -> int:
    #beginfunction
        return self.__FCountLogStrings
    #endfunction
    @CountLogStrings.setter
    def CountLogStrings (self, Value: int):
    #beginfunction
        self.__FCountLogStrings = Value
    #endfunction

    #--------------------------------------------------
    # @property LogEnabled
    #--------------------------------------------------
    # getter
    @property
    def LogEnabled (self) -> bool:
    #beginfunction
        return self.__FLogEnabled
    #endfunction
    @LogEnabled.setter
    def LogEnabled (self, Value: bool):
        #beginfunction
        self.__FLogEnabled = Value
    #endfunction

    #--------------------------------------------------
    # @property Filename
    #--------------------------------------------------
    # getter
    @property
    def FileName (self) -> str:
    #beginfunction
        return self.__FFileName
    #endfunction
    @FileName.setter
    def FileName (self, Value: str):
    #beginfunction
        self.__FFileName = Value
        if len(self.__FFileName) > 0 and LUFile.FileExists (self.__FFileName):
            # FMemoLog.Lines.LoadFromFile (self.__FFileName);
            ...
        #endif
    #endfunction

    #--------------------------------------------------
    # @property StandardOut
    #--------------------------------------------------
    # getter
    @property
    def StandardOut (self) -> bool:
    #beginfunction
        return self.__FStandardOut
    #endfunction
    @StandardOut.setter
    def StandardOut (self, Value: bool):
        #beginfunction
        self.__FStandardOut = Value
    #endfunction

    #--------------------------------------------------
    # @property MemoLog
    #--------------------------------------------------
    # getter
    @property
    def MemoLog (self):
    #beginfunction
        return self.__FMemoLog
    #endfunction
    @MemoLog.setter
    def MemoLog (self, Value):
    #beginfunction
        self.__FMemoLog = Value
        #     if FMemoLog <> nil then
        #     begin
        #         with FMemoLog do
        #         begin
        #             Clear;
        #             Align := alClient;
        #             readonly := True;
        #             TabStop := False;
        #             WantReturns := False;
        #             WantTabs := False;
        #             WordWrap := False;
        #             ParentColor := True;
        #             ScrollBars := ssVertical;
        #             ScrollBars := ssBoth;
        #         end;
        #         if (Filename <> '') and FileExists (Filename) then
        #         begin
        #             try
        #                 FMemoLog.Lines.LoadFromFile (Filename);
        #             except
        #             end;
        #         end;
        #     end;
        ...
    #endfunction

    def _SetMemoLog (self, Value):                             #TMemo
        """_SetMemoLog"""
    #beginfunction
        ...
    #endfunction

    @staticmethod
    def _LogDateStr (ATimeOnly: bool) -> str:
        """LogDateStr"""
    #beginfunction
        LToday: datetime.datetime = LUDateTime.Now ()
        if ATimeOnly:
            LResult = '               ' + LUDateTime.DateTimeStr (ATimeOnly, LToday, LUDateTime.cFormatDateTimeLog01, True)
        else:
            LResult = LUDateTime.DateTimeStr (ATimeOnly, LToday, LUDateTime.cFormatDateTimeLog01, True)
        #endif
        return LResult
    #endfunction

    def _GetLogSave (self, Filename: str) -> list:  #TStringList
        """_GetLogSave"""
        ...

    def _GetLogSaveCurrent (self) -> list:         #TStringList;
        """_GetLogSaveCurrent"""
        LResult = self._GetLogSave (self.__FFileName)
        return LResult

    def TruncateLog (self):
        """TruncateLog"""
    #beginfunction
        # Filename
        ts: list = list()
        if LUFile.FileExists (self.__FFileName):
            # Открыть для чтения
            LEncoding = LUFile.GetFileEncoding (self.__FFileName)
            LFile = open (self.__FFileName, 'r', encoding = LEncoding)
            try:
                # работа с файлом
                for s in LFile:
                    ts.append (s)
                    #file.next()    возвращает следующую строку файла
                #endfor
            finally:
                LFile.close ()
            # TruncateMemo (ts)
            # try
            #     ts.SaveToFile (Filename)
            # except:
            # #endtry
        #endif
        del ts

        # Memo
        ts: list = list()
        if self.__FMemoLog is not None:
            ts.clear()
            # ts.Assign (FMemoLog.Lines)
            # TruncateMemo (ts)
            # FMemoLog.Clear
            # FMemoLog.Lines.Assign (ts)
        #endif
        del ts
    #endfunction

    def _HandlerCONSOLE (self, T: TTypeLogString):
        """_HandlerCONSOLE"""
    #beginfunction
        self.__FLogStrings.clear ()
        self.__FLogStrings.append (self.__FLogStringAnsi)
        for s in self.__FLogStrings:
            if T == TTypeLogString.tlsTEXT:
                _s = s
            else:
                _s = self._LogDateStr (False) + ' ' + T.value + ' ' + s

            LCOLOR = self.__COLORS.get (T.value)
            if LCOLOR is not None:
                LFmt = LUConsole.sBEGIN_oct + LCOLOR + _s + LUConsole.sRESET
            else:
                LFmt = _s
            LUConsole.WriteLN (LFmt)
            # LUConsole.WriteLN (_s, AStyles=(LUConsole.cS_BOLD, LUConsole.cS_ITALIC))
            # LUConsole.WriteLN (_s)
        #endfor
    #endfunction

    def _HandlerFILE (self, T: TTypeLogString):
        """_HandlerFILE"""
    #beginfunction
        s = LUFile.ExpandFileName (self.__FFileName)
        s = LUFile.ExtractFileDir (s)
        if len (s) > 0:
            if not LUFile.DirectoryExists (s):
                LUFile.ForceDirectories (s)
            #endif
        #endif

        self.__FLogStrings.clear ()
        self.__FLogStrings.append (self.__FLogStringAnsi)

        """
        LEncoding = LUFile.GetFileEncoding (self.__FFileName)
        if LEncoding == '':
            LEncoding = LUFile.cDefaultEncoding
            LEncoding = self.__FLogCODE
        # LEncoding = LUStrDecode.cUTF_8
        """
        LEncoding = self.__FLogCODE

        # Откроет для добавления нового содержимого.
        LFile = open (self.__FFileName, 'a+', encoding = LEncoding)
        for s in self.__FLogStrings:
            if T == TTypeLogString.tlsTEXT:
                _s = s
            else:
                _s = self._LogDateStr (False) + ' ' + T.value + ' ' + s
            try:
                # _s = str (s.encode ('utf-8'), 'cp1251')
                # _s = str (s.encode ('cp1251'), 'cp1251')
                _s = str (_s.encode (self.__FLogCODE), self.__FLogCODE)
                LFile.write (_s + '\n')
            except:
                print ('Неправильная кодировка журнала=', LEncoding, s)
        #endfor
        LFile.flush ()
        LFile.close ()
    #endfunction

    def _Execute (self, T: TTypeLogString):
        """_Execute"""
    #beginfunction
        # StandardOut
        if self.__FStandardOut:                 # and isConsole:
            self._HandlerCONSOLE (T)
        #endif
        # Filename
        if self.__FFileName != '':
            self._HandlerFILE (T)
        #endif
        # Memo
        if self.__FMemoLog is not None:
            self.__FLogStrings.clear()
            self.__FLogStrings.append(self.__FLogStringAnsi)
            """
            for s in self.__FLogStrings:
                self.__FMemoLog.add
            #endfor
            """
        #endif
    #endfunction

    def AddLogFile (self, AFileName: str):
        """AddLogFile"""
    #beginfunction
        if LUFile.FileExists (AFileName):
            # Открыть для чтения
            LEncoding = LUFile.GetFileEncoding (AFileName)
            LFile = open (AFileName, 'r', encoding = LEncoding)
            try:
                # работа с файлом
                for s in LFile:
                    self.AddLog (TTypeLogString.tlsTEXT, s.rstrip('\n'))
                    #file.next()    возвращает следующую строку файла
                #endfor
            finally:
                LFile.close ()
        #endif
    #endfunction

    #--------------------------------------------------
    #
    #--------------------------------------------------
    def AddLog (self, T: TTypeLogString, Value: str):
        """AddLog"""
    #beginfunction
        self.__FLogStringOEM = Value
        self.__FLogStringAnsi = Value
        if self.LogEnabled:
            self._Execute(T)
    #endfunction
#endclass

#----------------------------------------------
# TLogging
#----------------------------------------------
# строка формата сообщения
Cstrfmt_04 = '%(asctime)s %(msecs)03d [%(name)s] %(levelno)02d %(levelname)-8s %(module)s %(message)s'

# строка формата времени
Cdatefmt_02 = '%d/%m/%Y %H:%M:%S'
# style
Cstyle_01 = '%'
Cstyle_02 = '{'
Cstyle_03 = '$'
# defaults
Cdefaults = {"ip": '_ip_'}
#-------------------------------------------------
# LOGGING_CONFIG
#-------------------------------------------------
LOGGING_CONFIG = \
{
    'version': 1,
    'disable_existing_loggers': 0,

    'loggers': {
        'root': {
            'handlers': ['CONSOLE'],
            'level': 'DEBUG',
            # 'filters': ['special'],
            'propagate': 1
        },

        'log02': {
            'handlers': ['FILE_01'],
            'level': 'DEBUG',
            'qualname': 'log02',
            'propagate': 0
        }
    },

    'handlers': {
        'CONSOLE': {
            'class': 'logging.StreamHandler',
            'level': logging.INFO,
            'formatter': 'FORMAT_01',
            'stream': 'ext://sys.stdout'
        },

        'FILE_01': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': logging.DEBUG,
            'formatter': 'FORMAT_01',
            'filename': 'LOG\LOGGING_CONFIG.log'
        }
    },

    'formatters': {
        'FORMAT_01': {
            'format': '%(asctime)s %(msecs)03d [%(name)s] %(levelno)02d %(levelname)-8s %(module)s %(message)s',
            'datefmt': '%d/%m/%Y %H:%M:%S',
            'style': '%'
        },
    },
}
#-------------------------------------------------
# TFormatter(logging.Formatter):
#-------------------------------------------------
class TFormatter(logging.Formatter):
    """TFormatter"""
    luClassName = "TFormatter"
    __COLORS = {
        logging.NOTSET: LUConsole.cFG8_BLUE+LUConsole.sEND,
        logging.DEBUG: LUConsole.cFG8_BLUE+LUConsole.sEND,
        logging.INFO: LUConsole.cFG8_WHITE+LUConsole.sEND,
        logging.WARNING: LUConsole.cS_BOLD + ';' + LUConsole.cFG8_YELLOW+LUConsole.sEND,
        logging.ERROR: LUConsole.cS_BOLD + ';' + LUConsole.cFG8_RED+LUConsole.sEND,
        logging.CRITICAL: LUConsole.cS_BOLD + ';' + LUConsole.cFG8_BLACK + ';' + LUConsole.cBG8_RED+LUConsole.sEND,
        LULog.BEGIN: LUConsole.cS_BOLD + ';' + LUConsole.cFG8_GREEN + ';' + LUConsole.cBG8_BLACK + LUConsole.sEND,
        LULog.END: LUConsole.cS_BOLD + ';' + LUConsole.cFG8_GREEN + ';' + LUConsole.cBG8_BLACK + LUConsole.sEND,
        LULog.PROCESS: LUConsole.cS_BOLD + ';' + LUConsole.cFG8_GREEN + ';' + LUConsole.cBG8_BLACK + LUConsole.sEND,
        LULog.TEXT: LUConsole.cS_BOLD + LUConsole.sEND
    }

    #--------------------------------------------------
    # constructor
    #--------------------------------------------------
    def __init__(self, AOldFmt, AUseColor = True, **kwargs):
        """Constructor"""
    #beginfunction
        # logging.Formatter.__init__(self, fmt = None,datefmt = None,style = None,validate = False,defaults = None)
        logging.Formatter.__init__(self, **kwargs)
        if len(AOldFmt) > 0:
            self.__FFORMAT = AOldFmt
        else:
            self.__FFORMAT = kwargs['fmt']
        self.__FUseColor = AUseColor
    #endfunction

    def format(self, record):
        """
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ
            record.levelname = levelname_color
        """
        if self.__FUseColor:
            LCOLOR = self.__COLORS.get(record.levelno)
            LFmt = LUConsole.sBEGIN_oct +  LCOLOR + self.__FFORMAT + LUConsole.sRESET
            # установить новый fmt
            Lformatter = logging.Formatter(LFmt)
            return Lformatter.format (record)
        else:
            return logging.Formatter.format (self, record)
        #endif
    #endfunction
#endclass

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# class TLogging (logging.Logger):
# class ColoredLogger(logging.Logger):
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# ??????????????????????????????????????????????
# class TLogger (logging.getLoggerClass()):
# ??????????????????????????????????????????????

class TLogger (logging.Logger):
    """TLogging"""
    luClassName = "TLogging"

    #--------------------------------------------------
    # constructor
    #--------------------------------------------------
    def __init__(self, ALogerName: str):
        """Constructor"""
    #beginfunction
        super().__init__(ALogerName)
        # Formater
        self.__Fstrfmt = Cstrfmt_04
        self.__Fdatefmt = Cdatefmt_02
        self.__Fdefaults = Cdefaults
        self.__Fstyle = Cstyle_01
        # LEVEL
        self.LEVEL = logging.DEBUG
        # propagate
        self.propagate = True
        self.Clear ()
    #endfunction

    #--------------------------------------------------
    # destructor
    #--------------------------------------------------
    def __del__(self):
        """destructor"""
    #beginfunction
        LClassName = self.__class__.__name__
        print('{} уничтожен'.format(LClassName))
    #endfunction

    def Clear(self):
        """Clear"""
    #beginfunction
        ...
    #endfunction

    #--------------------------------------------------
    # @property LEVEL
    #--------------------------------------------------
    # getter
    @property
    def LEVEL (self):
    #beginfunction
        return self.level
    #endfunction
    @LEVEL.setter
    def LEVEL (self, Value):
    #beginfunction
        self.setLevel (Value)
    #endfunction

    def AddHandlerCONSOLE(self, ALevel):
    #beginfunction
        LHandlerConsole = logging.StreamHandler ()
        LHandlerConsole.setLevel (ALevel)
        LHandlerConsole.set_name ('CONSOLE')
        LHandlerConsole.setStream (sys.stdout)

        # Вариант 0
        # LFormaterConsole = logging.Formatter (fmt=self.__Fstrfmt, datefmt=self.__Fdatefmt,
        #                                          style=self.__Fstyle, validate=True, defaults=self.__Fdefaults)

        LFormaterConsole = TFormatter ('', True, fmt=self.__Fstrfmt, datefmt=self.__Fdatefmt,
                                                 style=self.__Fstyle, validate=True, defaults=self.__Fdefaults)
        LHandlerConsole.setFormatter (LFormaterConsole)
        self.addHandler (LHandlerConsole)
    #endfunction

    def AddHandlerFILE(self, AFileName: str, ALevel):
    #beginfunction
        LHandlerFile = logging.FileHandler (AFileName, mode='a+',
                                            encoding=None, delay=False, errors=None)
        LHandlerFile.setLevel (ALevel)
        LHandlerFile.set_name ('FILE')

        LFormaterFile = logging.Formatter (fmt=self.__Fstrfmt, datefmt=self.__Fdatefmt,
                                               style=self.__Fstyle, validate=True,
                                               defaults = self.__Fdefaults)
        LHandlerFile.setFormatter (LFormaterFile)
        self.addHandler (LHandlerFile)

        # Json
        # LJsonFormatter = jsonlogger.JsonFormatter ()
        # logHandler.setFormatter (LJsonFormatter)
        # logger.addHandler (logHandler)

    #endfunction

"""
    try:
        1/0
    except:
        logger.exception('exception')

    try:
        1/0
    except OSError as e:
        logger.error(e, exc_info=True)
    except:
        logger.error("uncaught exception: %s", traceback.format_exc())
        
    try: 
        c = a / b 
    except Exception as e: 
        logging.error("Exception occurred", exc_info=True) 
        
"""

"""
# logger
logger = logging.getLogger(__name__)
    
    # LEVEL
    NOTSET
    DEBUG - уровень отладочной информации, зачастую помогает при разработке приложения на машине программиста.
    INFO - уровень вспомогательной информации о ходе работы приложения/скрипта.
    WARNING - уровень предупреждения. Например, мы можем предупреждать о том, что та или иная функция будет удалена в будущих версиях вашего приложения.
    ERROR - с таким уровнем разработчики пишут логи с ошибками, например, о том, что внешний сервис недоступен.
    CRITICAL - уровень сообщений после которых работа приложения продолжаться не может.
    
    # УСТАНОВИТЬ LEVEL
    logger.setLevel(logging.DEBUG)
    logger.setLevel(logging.INFO)
    
    # ЗАПИСЬ в logger
    logger.debug('debug')
    logger.info('info')
    logger.warning('warning')
    logger.error('error')
    logger.critical('critical')

    # handler
    Задача класса Handler и его потомков обрабатывать запись сообщений/логов. Т.е. Handler отвечает за то куда будут записаны сообщения. В базовом наборе logging предоставляет ряд готовых классов-обработчиков:
    SteamHandler - запись в поток, например, stdout или stderr.
        handler = StreamHandler(stream=sys.stdout)
    FileHandler - запись в файл, класс имеет множество производных классов с различной функциональностью
        ротация файлов логов по размеру, времени и т.д.)
        handler = StreamHandler(stream=)
    BaseRotatingHandler
        handler = BaseRotatingHandler(filename, mode, encoding=None, delay=False, errors=None
    RotatingFileHandler
        handler = RotatingFileHandler(filename, mode='a', maxBytes=0, backupCount=0, encoding=None,
            delay=False, errors=None
    TimedRotatingFileHandler
        handler = TimedRotatingFileHandler(filename, when='h', interval=1, backupCount=0, encoding=None,
            delay=False, utc=False, atTime=None, errors=None) 
        
    SocketHandler - запись сообщений в сокет по TCP
        handler = SocketHandler(host, port)
    DatagramHandler - запись сообщений в сокет по UDP
        handler = DatagramHandler(host, port)
    SysLogHandler - запись в syslog
        handler = SysLogHandler(address=('localhost', SYSLOG_UDP_PORT), facility=LOG_USER, socktype=socket.SOCK_DGRAM)
    HTTPHandler - запись по HTTP
        handler = HTTPHandler(host, url, method='GET', secure=False, credentials=None, context=None)
    NullHandler = NullHandler
        handler = StreamHandler(stream=)
    WatchedFileHandler
        handler = WatchedFileHandler(filename, mode='a', encoding=None, delay=False, errors=None)
    NTEventLogHandler
        handler = NTEventLogHandler(appname, dllname=None, logtype='Application')
    SMTPHandler
        handler = SMTPHandler(mailhost, fromaddr, toaddrs, subject, credentials=None, secure=None, timeout=1.0)
    MemoryHandler
        handler = BufferingHandler(capacity)¶
    QueueHandler
        handler = QueueHandler(queue)
    QueueListener
        handler = QueueListener(queue, *handlers, respect_handler_level=False)¶
        
    # ДОБАВИТЬ handler
    logger.addHandler(handler)

    # Formatter
    #class logging.Formatter(fmt=None, datefmt=None, style='%', validate=True, *, defaults=None)
    formster = logging.Formatter (fmt=self.strfmt_03,
        datefmt=self.datefmt_02,
        style = '%',
        validate = True,
        defaults = {"ip": None}
        )
    handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))

    Параметр defaults может быть словарем со значениями по умолчанию для использования в настраиваемых полях.
    Например: logging.Formatter('%(ip)s %(message)s', defaults={"ip": None})

    # Filter
    def filter_python(record: LogRecord) -> bool:
        return record.getMessage().find('python') != -1
    logger.addFilter(filter_python)

    # LoggerAdapter
    class CustomLoggerAdapter(LoggerAdapter):
    def process(self, msg, kwargs):
        return f'{msg} from {self.extra["username"]}', kwargs
    
    logger2 = logging.getLogger('adapter')
    logger2.setLevel(logging.DEBUG)

    handler = StreamHandler(stream=sys.stdout)
    handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))

    adapter = CustomLoggerAdapter(logger2, {'username': 'adilkhash'})

    logger2.addHandler(handler)
    adapter.error('failed to save')

    # extra и не только
    logger.debug('debug info', extra={"response": response.text})
    Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s, response: %(response)s')

# Конфигурация logging
Официальная документация рекомендует конфигурировать logging через python-словарь.
Для этого необходимо вызвать функцию logging.config.dictConfig и передать ей специальный словарь.
Схема словаря описана здесь. Я лишь вкратце пробегусь по основным ключам:
version - 
    ключ указывает версию конфига, рекомендуется наличие этого ключа со значением 1, нужно для обратной совместимости в случае, если в будущем появятся новые версии конфигов.
disable_existing_loggers - 
    запрещает или разрешает настройки для существующих логеров (на момент запуска), по умолчанию равен True
formatters - 
    настройки форматов логов
handlers - 
    настройки для обработчиков логов
loggers - 
    настройки существующих логеров

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'default_formatter': {
            'format': '[%(levelname)s:%(asctime)s] %(message)s'
        },
    },

    'handlers': {
        'stream_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'default_formatter',
        },
    },

    'loggers': {
        'my_logger': {
        'handlers': ['stream_handler'],
        'level': 'DEBUG',
        'propagate': True
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('my_logger')
logger.debug('debug log')

# Наследование в logging
    Ещё одним удобным механизмом в logging является "наследование" настроек корневого логера
    его потомками. Наследование задаётся через символ . в названии логера.
    То есть логер с названием my_package.logger1 унаследует все настройки, заданные для my_package.
    Давайте обновим пример выше, добавив в LOGGING_CONFIG настройку для my_package
    
LOGGING_CONFIG['loggers'].update (
    {
    'my_package': {
        'handlers': ['stream_handler'],
        'level': 'DEBUG',
        'propagate': False
        }
    }
)

# Отправляем логи в Telegram
    
    """
#endclass

#-------------------------------------------------
# Функциональное исполнение
#-------------------------------------------------

def GetLogDirLogon () -> str:
    """GetLogDirLogon"""
#beginfunction
    """
    if @LDomain <> ''
        LogDir = LogDir + '\\'+@LDomain
    endif
    s = AddCharR ('_', $USERID, 15)
    LogFile = s + "_" + UCase (@WKSTA)+'.log'
    """
    return ''
#endfunction

def GetLogFileName () -> str:
    """GetLogFileName"""
#beginfunction
    LResult = LUDateTime.Now ().strftime ('%Y%m%d') + '.log'
    return LResult
#endfunction

def GetLogFileNameSufix (ASufix: str) -> str:
    """GetLogFileNameSufix"""
#beginfunction
    LResult = LUDateTime.Now ().strftime ('%Y%m%d') + ASufix + '.log'
    return LResult
#endfunction

#-------------------------------------------------
# LogFileName(ALog: str, ALogDir: str, ALogFile: str) -> str:
#-------------------------------------------------
def LogFileName(ALog: int, ALogDir: str, ALogFile: str) -> str:
    """LogFileName"""
#beginfunction
    LToday: datetime = LUDateTime.Now ()
    match ALog:
        case 1|3|10|30:
            LLogDir = ALogDir
            if len (ALogDir) > 0:
                LLogDir = os.environ['TEMP']
            #endif
            LLogFile = ALogFile
            if ALogFile == '':
                s = LUDateTime.DateTimeStr (False, LToday, LUDateTime.cFormatDateYYMMDD_01)
                LLogFile = s+'.log'
            #endif
            LLogFileName = os.sep.join([LLogDir,LLogFile])
            if ALog == 10 or ALog == 30:
                if LUFile.FileExists(LLogFileName):
                    try:
                        os.remove (LLogFileName)
                    except:
                    # except LUErrors.LUFileError_FileERROR as ERROR:
                        print (f'Ошибка при удалении файла {LLogFileName}')
                    else:
                        ...
                #endif
            #endif
        case _:
            LLogFileName = ""
    #endmatch
    return LLogFileName
#endfunction

#--------------------------------------------------------------------------------
# LogAdd (ALog: int, ALogFile: str, AOpt: str, AMessage: str,
#           AStyles = '', AFG8 = '', ABG8 = '', AFG256 = '', ABG256 = '', AESC = ''):
#--------------------------------------------------------------------------------
def LogAdd (ALog: int, ALogFile: str, AOpt: str, AMessage: str,
            AStyles='', AFG8='', ABG8='', AFG256='', ABG256='', AESC=''):
    """LogAdd"""
#beginfunction
    LToday: datetime = LUDateTime.Now ()
    o = AOpt.upper()
    match o:
        case 'I':
            s = AMessage
        case _:
            s = LUDateTime.DateTimeStr(False, LToday, LUDateTime.cFormatDateTimeLog01)+' '+AOpt+' '+AMessage
    #endmatch

    # Откроет для добавления нового содержимого.
    # LFile = open(ALogFile, 'a+', encoding = 'cp1251')

    LEncoding = LUFile.GetFileEncoding (ALogFile)
    if LEncoding == '':
        LEncoding = LUFile.cDefaultEncoding
    LFile = open (ALogFile, 'a+', encoding = LEncoding)

    match ALog:
        case 1|10:
            LUConsole.WriteLN (s)
            LFile.write (s+'\n')
        case 2:
            LUConsole.WriteLN (s, AStyles=AStyles, AFG8=AFG8, ABG8=ABG8, AFG256=AFG256, ABG256=ABG256, AESC=AESC)
        case 3|30:
            LUConsole.WriteLN (s, AStyles=AStyles, AFG8=AFG8, ABG8=ABG8, AFG256=AFG256, ABG256=ABG256, AESC=AESC)
            LFile.write (s+'\n')
    #endmatch
    LFile.flush ()
    LFile.close ()
#endfunction

#--------------------------------------------------------------------------------
# LogAddFile (ALog: int, ALogFile: str, AOpt: str, AFileName: str,
#            AStyles='', AFG8='', ABG8='', AFG256='', ABG256='', AESC=''):
#--------------------------------------------------------------------------------
def LogAddFile (ALog: int, ALogFile: str, AOpt: str, AFileName: str,
            AStyles='', AFG8='', ABG8='', AFG256='', ABG256='', AESC=''):
    """LogAddFile"""
#beginfunction
    if LUFile.FileExists (AFileName):
        # Открыть для чтения
        # LFile = open (AFileName, 'r', encoding='utf-8')
        # LFile = open (AFileName, 'r', encoding='cp1251')
        # LFile.encoding =

        LEncoding = LUFile.GetFileEncoding (AFileName)
        LFile = open (AFileName, 'r', encoding = LEncoding)
        try:
            # работа с файлом
            for s in LFile:
                Ls = s.split ('\n')[0]
                # Ls = s
                LogAdd (ALog, ALogFile, AOpt, Ls, AStyles, AFG8, ABG8, AFG256, ABG256, AESC)
                #LFile.next()   возвращает следующую строку файла
            #endfor
        finally:
            LFile.close ()
    #endif
#endfunction

#-------------------------------------------------
# GLOBAL
#-------------------------------------------------
def CreateTFileMemoLog (*args, **kwargs) -> TFileMemoLog:
    """CreateTFileMemoLog"""
#beginfunction
    return TFileMemoLog ()
#endfunction

def CreateTLogger (AFileNameINI: str) -> TLogger:
    """CreateTLogging"""
#beginfunction
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    logging.setLoggerClass (TLogger)
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    # читаем конфигурацию из FileNameINI
    # logging.config.fileConfig (AFileNameINI)

    # читаем конфигурацию из FileNameINI
    # logging.basicConfig(filename = AFileNameINI)

    # читаем конфигурацию из словаря
    # logging.config.dictConfig (LOGGING_CONFIG)

    # создаем регистратор
    LResult = TLogger('root')
    return LResult
#endfunction

def list_dict(dicts):
    for k,v in dicts.items():
        try:
            print("key:\t" + k)
            list_dict(v)
        except AttributeError:
            print("value:\t" + str(v))

def CreateLoggerCONFIG (AFileNameCONFIG: str, ALogerName: str) -> logging.Logger:
    """CreateLoggerCONFIG"""
#beginfunction
    # if LUFile.FileExists(AFileNameCONFIG):
    #     # читаем конфигурацию из файла
    #     try:
    #         CONFIG = {}
    #         with open (AFileNameCONFIG, 'r') as FileCONFIG:
    #             json_sample = {}
    #             s = FileCONFIG.read ()
    #             # итерация по строкам
    #             for s in FileCONFIG:
    #                 s = s.strip ()
    #                 if len(s) > 0:
    #                     ...
    #         with open (AFileNameCONFIG, 'rb') as FileCONFIG:
    #             s = FileCONFIG.read ()
    #
    #     except FileNotFoundError:
    #         print ('Невозможно открыть файл')
    # else:
    #     # читаем конфигурацию из словаря
    #     logging.config.dictConfig (LOGGING_CONFIG)
    # #endif

    # читаем конфигурацию из словаря
    logging.config.dictConfig (LOGGING_CONFIG)
    # создаем регистратор
    LResult = logging.getLogger (ALogerName)
    for item in LResult.handlers:
        if type(item) is logging.StreamHandler:
            print (item.formatter._fmt)
            LFormaterConsole = TFormatter (item.formatter._fmt)
            item.setFormatter (LFormaterConsole)
        #endif
    #enfor
    return LResult
#endfunction

def CreateLoggerFILEINI (AFileNameINI: str, ALogerName: str) -> logging.Logger:
    """CreateLoggerFILEINI"""
#beginfunction
    # читаем конфигурацию из файла
    logging.config.fileConfig(AFileNameINI,disable_existing_loggers = False)
    # logging.config.fileConfig (AFileNameINI)
    # создаем регистратор
    LResult = logging.getLogger (ALogerName)

    for item in LResult.handlers:
        if type (item) is logging.StreamHandler:

            # print(item.formatter.datefmt)
            # item.formatter.datefmt = '%H:%M:%S'

            # print(item.formatter.default_msec_format)
            # print(item.formatter.default_time_format)

            # print (item.formatter._fmt)
            # LFormater = logging.Formatter(fmt = '%(message)s')
            # item.setFormatter(LFormater)
            # print (item.formatter._fmt)

            print (item.formatter._fmt)
            LFormaterConsole = TFormatter (item.formatter._fmt)
            item.setFormatter (LFormaterConsole)

            # LJsonFormatter = jsonlogger.JsonFormatter ()
            # logHandler.setFormatter (LJsonFormatter)
            # logger.addHandler (logHandler)

        #endif
    #enfor
    return LResult
#endfunction

def CreateLoggerBASIC (ALevel, AFileNameLOG: str, ALogerName: str) -> logging.Logger:
    """CreateTLoggingCONFIG"""
#beginfunction
    Cdatefmt = '%d/%m/%Y %H:%M:%S'
    Cformat = '%(asctime)s %(msecs)d %(levelno)s %(module)s:%(message)s'
    # читаем конфигурацию из
    if len(AFileNameLOG) > 0:
        logging.basicConfig (level = ALevel, filename = AFileNameLOG, style='%',
                             datefmt = Cdatefmt, format = Cformat)
    else:
        logging.basicConfig (level = ALevel, stream=sys.stdout, style='%',
                             datefmt = Cdatefmt, format = Cformat)
    # создаем регистратор
    LResult = logging.getLogger (ALogerName)
    for item in LResult.handlers:
        if type(item) is logging.StreamHandler:
            print (item.formatter._fmt)
            LFormaterConsole = TFormatter (item.formatter._fmt)
            item.setFormatter (LFormaterConsole)
        #endif
    #enfor
    return LResult
#endfunction

GFileMemoLog = CreateTFileMemoLog ()
GLogger = CreateTLogger ('logging.ini')

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
