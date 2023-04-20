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
import datetime
import copy
import logging
import logging.config

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
from pythonjsonlogger import jsonlogger
import pythonjsonlogger

#------------------------------------------
# БИБЛИОТЕКА LU 
#------------------------------------------
import LUConst
import LUFile
import LUConsole
import LUDateTime

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
DEBUGTEXT = 11
BEGIN = 21
END = 22
PROCESS = 23
TEXT = 24

# LULogger = logging.getLogger(__name__)
# GLULogger = logging.getLogger(__name__)

# строка формата сообщения
# Cstrfmt_04 = '%(asctime)s %(msecs)03d [%(name)s] %(levelno)02d %(levelname)-8s %(module)s %(message)s'
Cstrfmt_01 = '%(asctime)s [%(name)s] [%(module)-15s] %(levelno)02d %(levelname)-10s %(lineno)03d %(message)s'
Cstrfmt_02 = '%(asctime)s %(name)s %(levelname)s %(message)s'
# строка формата времени
Cdatefmt_01 = '%d/%m/%Y %H:%M:%S'
# style
Cstyle_01 = '%'
Cstyle_02 = '{'
Cstyle_03 = '$'
# defaults
Cdefaults = {"ip": '_ip_'}

def AddLevelName():
#beginfunction
    logging.addLevelName(DEBUGTEXT, 'DEBUGTEXT')
    logging.addLevelName(BEGIN, 'BEGIN')
    logging.addLevelName(END, 'END')
    logging.addLevelName(PROCESS, 'PROCESS')
    logging.addLevelName(TEXT, 'TEXT')
#endfunction

CDefaultFileLogINI = 'logging.ini'
CDefaultFileLogCONFIG = 'logging.CONFIG'

CDefaultFileLog = 'LOGGING.log'
CDefaultFileLogFILEINI = 'LOGGING_FILEINI.log'
CDefaultFileLogFILEINI_json = 'LOGGING_FILEINI_json.log'

CDefaultFileLogFILECONFIG = 'LOGGING_CONFIG.log'
CDefaultFileLogFILECONFIG_json = 'LOGGING_FILECONFIG_json.log'

CDefaultFileLogFILEBASIC = 'LOGGING_BASIC.log'

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
        s = '{} уничтожен'.format (LClassName)
        LUConst.LULogger.log (DEBUGTEXT, s)
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
            LResult = ' '*15 + LUDateTime.DateTimeStr (ATimeOnly, LToday, LUDateTime.cFormatDateTimeLog01, True)
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
                _s = self._LogDateStr (False) + ' ' + str(T.value) + ' ' + s
            LCOLOR = self.__COLORS.get (T.value)
            if LCOLOR is not None:
                LFmt = LUConsole.sBEGIN_oct + LCOLOR + _s + LUConsole.sRESET
            else:
                LFmt = _s
            LUConsole.WriteLN (LFmt)
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
        LEncoding = self.__FLogCODE
        # Откроет для добавления нового содержимого.
        LFile = open (self.__FFileName, 'a+', encoding = LEncoding)
        for s in self.__FLogStrings:
            if T == TTypeLogString.tlsTEXT:
                _s = s
            else:
                _s = self._LogDateStr (False) + ' ' + str(T.value) + ' ' + s
            try:
                # _s = str (s.encode ('utf-8'), 'cp1251')
                # _s = str (s.encode ('cp1251'), 'cp1251')
                _s = str (_s.encode (self.__FLogCODE), self.__FLogCODE)
                LFile.write (_s + '\n')
            except:
                s = f'Неправильная кодировка журнала={s}'
                LUConst.LULogger.log (DEBUGTEXT, s)
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

#-------------------------------------------------
# TLogRecord(logging.LogRecord):
#-------------------------------------------------
class TLogRecord(logging.LogRecord):
    """TLogRecord"""
    luClassName = "TLogRecord"
    #--------------------------------------------------
    # constructor
    #--------------------------------------------------
    #class logging.LogRecord(name, level, pathname, lineno, msg, args, exc_info, func=None, sinfo=None)
    def __init__(self, **kwargs):
        """Constructor"""
    #beginfunction
        logging.LogRecord.__init__(self, **kwargs)
    #endfunction
#endclass

#-------------------------------------------------
# THandler(logging.Handler):
#-------------------------------------------------
class THandler(logging.Handler):
    """THandler"""
    luClassName = "THandler"
    #--------------------------------------------------
    # constructor
    #--------------------------------------------------
    #class logging.Handler
    def __init__(self, **kwargs):
        """Constructor"""
    #beginfunction
        logging.Handler.__init__(self, **kwargs)
    #endfunction
#endclass

#-------------------------------------------------
# TFilter(logging.Filter):
#-------------------------------------------------
class TFilter(logging.Filter):
    """TFilter"""
    luClassName = "TFilter"
    COLOR = {
        "DEBUG": "BLUE",
        "INFO": "WHITE",
        "WARNING": "YELLOW",
        "ERROR": "RED",
        "CRITICAL": "RED",
        "DEBUGTEXT": "RED",
        "BEGIN": "RED",
        "END": "RED",
        "PROCESS": "RED",
        "TEXT": "RED"
    }
    #--------------------------------------------------
    # constructor
    #--------------------------------------------------
    #class logging.Filter (name='')
    def __init__(self, **kwargs):
        """Constructor"""
    #beginfunction
        logging.Filter.__init__(self, **kwargs)
    #endfunction

    def filter(self, record):
    #beginfunction
        record.color = self.COLOR[record.levelname]
        # print(record.color)
        return True
    #endfunction
#endclass

# #-------------------------------------------------
# # TFilter(logging.Filter):
# #-------------------------------------------------
# # Фильтр, который вводит контекстную информацию в журнал.
# # Вместо того, чтобы использовать фактическую контекстуальную информацию, мы
# # просто используем случайные данные в этой демонстрации.
# from random import choice
#
# class TFilter (logging.Filter):
#     """TFilter"""
#     luClassName = "TFilter"
#     USERS = ['jim', 'fred', 'sheila']
#     IPS = ['123.231.231.123', '127.0.0.1', '192.168.0.1']
#     def filter(self, record):
#     #beginfunction
#         record.ip = choice(TFilter.IPS)
#         record.user = choice(TFilter.USERS)
#         return True
#     #endfunction
# #endclass
#
# def Test ():
# #beginfunction
#     levels = (logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL)
#     logging.basicConfig(level=logging.DEBUG,
#                         format='%(asctime)-15s %(name)-5s %(levelname)-8s IP: %(ip)-15s User: %(user)-8s %(message)s')
#     a1 = logging.getLogger('a.b.c')
#     a2 = logging.getLogger('d.e.f')
#     f = TFilter()
#     a1.addFilter(f)
#     a2.addFilter(f)
#     a1.debug('A debug message')
#     a1.info('An info message with %s', 'some parameters')
#     for x in range(10):
#         lvl = choice(levels)
#         lvlname = logging.getLevelName(lvl)
#         a2.log(lvl, 'A message at %s level with %d %s', lvlname, 2, 'parameters')
# #endfunction

#-------------------------------------------------
# TAdapter(logging.LoggerAdapter):
#-------------------------------------------------
class TAdapter(logging.LoggerAdapter):
    """TAdapter"""
    luClassName = "TAdapter"
    #--------------------------------------------------
    # constructor
    #--------------------------------------------------
    #class logging.LoggerAdapter(logger, extra)
    def __init__(self, **kwargs):
        """Constructor"""
    #beginfunction
        # logging.LoggerAdapter.__init__(self, logger = None, extra = None)
        logging.LoggerAdapter.__init__(self, **kwargs)
    #endfunction

    def process(self, msg, kwargs):
        my_context = kwargs.pop('id', self.extra['id'])
        return '[%s] %s' % (my_context, msg), kwargs
#endclass

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
        BEGIN: LUConsole.cS_BOLD + ';' + LUConsole.cFG8_GREEN  + LUConsole.sEND,
        END: LUConsole.cS_BOLD + ';' + LUConsole.cFG8_GREEN + LUConsole.sEND,
        PROCESS: LUConsole.cS_BOLD + ';' + LUConsole.cFG8_GREEN + LUConsole.sEND,
        DEBUGTEXT: LUConsole.cS_BOLD + ';' + LUConsole.cFG8_BLUE+LUConsole.sEND,
        TEXT: LUConsole.cS_BOLD + LUConsole.sEND
    }

    #--------------------------------------------------
    # constructor
    #--------------------------------------------------
    def __init__ (self, AUseColor = True, **kwargs):
        """Constructor"""
    #beginfunction
        #class logging.Formatter(fmt=None, datefmt=None, style='%', validate=True, *, defaults=None)
        logging.Formatter.__init__(self, **kwargs)
        self.__FUseColor = AUseColor
    #endfunction

    def _SetColor(self, Afmt: str, ALevelNo: int) -> str:
        """_SetColor"""
    #beginfunction
        if self.__FUseColor:
            LCOLOR = self.__COLORS.get (ALevelNo)
            LFmt = LUConsole.sBEGIN_oct + LCOLOR + Afmt + LUConsole.sRESET
            return LFmt
        else:
            return Afmt
        #endif
    #endfunction

    def format(self, record):
        """format"""
    #beginfunction

        # отдельный атрибут
        # LLevelname = record.levelname
        # record.levelname = '_'+LLevelname+'_'

        if record.levelno == TEXT:
            # установить новый fmt
            Lfmt = self._SetColor ('%(message)s', record.levelno)
            Ldatefmt = self.datefmt
            # установить новый fmt
            Lformatter = logging.Formatter(Lfmt)
            return Lformatter.format (record)
        #endif
        if self.__FUseColor:
            Lfmt = self._SetColor (self._fmt, record.levelno)
            Ldatefmt = self.datefmt
            # установить новый fmt
            Lformatter = logging.Formatter(Lfmt, Ldatefmt)
            return Lformatter.format (record)
        else:
            return logging.Formatter.format (self, record)
        #endif
    #endfunction
#endclass

#-------------------------------------------------
# TFormatterJSON(jsonlogger.JsonFormatter):
#-------------------------------------------------
class TFormatterJSON(pythonjsonlogger.jsonlogger.JsonFormatter):
    """TFormatterJSON"""
    luClassName = "TFormatterJSON"

    #--------------------------------------------------
    # constructor
    #--------------------------------------------------
    #class jsonlogger.JsonFormatter(*args, **kwargs)
    def __init__(self, *args, **kwargs):
        """Constructor"""
    #beginfunction
        super(TFormatterJSON, self).__init__(*args, **kwargs)
        self.json_ensure_ascii = False
        ...
    #endfunction

    def format(self, record):
        """format"""
    #beginfunction
        return super().format(record)
    #endfunction
#endclass

def AddHandlerFile (ALogger: logging.Logger, AFileName: str, ALevel, Astrfmt: str, Adatefmt: str,
                    Astyle: str, Adefaults: str):
    """AddFileHandler"""
#beginfunction
    LHandler = logging.FileHandler (AFileName, mode='a+',
                                    encoding=LUFile.cDefaultEncoding, delay=False, errors=None)
    LHandler.setLevel (ALevel)
    LHandler.set_name ('FILE')
    LFormater = TFormatter (fmt=Astrfmt, datefmt=Adatefmt,
                                    style=Astyle, validate=True, defaults=Adefaults)
    LHandler.setFormatter (LFormater)
    ALogger.addHandler (LHandler)
#endfunction

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
        self.__FFileName: str = ''
        # Formater
        self.__Fstrfmt = Cstrfmt_01
        self.__Fdatefmt = Cdatefmt_01
        self.__Fstyle = Cstyle_01
        self.__Fdefaults = Cdefaults
        # LEVEL
        self.LEVEL = logging.DEBUG
        # propagate
        self.propagate = True
        AddLevelName ()
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
    # @property FileName
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
            ...
        #endif
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
        LHandler = logging.StreamHandler ()
        LHandler.setLevel (ALevel)
        LHandler.set_name ('CONSOLE')
        LHandler.setStream (sys.stdout)
        LFormater = TFormatter (fmt=self.__Fstrfmt, datefmt=self.__Fdatefmt,
                                                style=self.__Fstyle, validate=True, defaults=self.__Fdefaults)
        LHandler.setFormatter (LFormater)
        self.addHandler (LHandler)
    #endfunction

    def AddHandlerFILE(self, AFileName: str, ALevel):
    #beginfunction
        LHandler = logging.FileHandler (AFileName, mode='a+',
                                        encoding=LUFile.cDefaultEncoding, delay=False, errors=None)
        LHandler.setLevel (ALevel)
        LHandler.set_name ('FILE')
        LFormater = TFormatter (fmt=self.__Fstrfmt, datefmt=self.__Fdatefmt,
                                                 style=self.__Fstyle, validate=True, defaults=self.__Fdefaults)
        LHandler.setFormatter (LFormater)
        self.addHandler (LHandler)
    #endfunction

    def AddHandlerFILE_JSON(self, AFileName: str, ALevel):
    #beginfunction
        LHandler = logging.FileHandler (AFileName, mode='a+',
                                        encoding=LUFile.cDefaultEncoding, delay=False, errors=None)
        LHandler.setLevel (ALevel)
        LHandler.set_name ('FILE_JSON')
        LFormater = TFormatterJSON (fmt=self.__Fstrfmt, datefmt=self.__Fdatefmt,
                                                 style=self.__Fstyle, validate=True, defaults=self.__Fdefaults)
        LFormater.json_ensure_ascii = False
        LHandler.setFormatter (LFormater)
        self.addHandler (LHandler)
    #endfunction
#endclass

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
    logger.exception('error')
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
    formster = logging.Formatter (fmt=self.strfmt_03, datefmt=self.datefmt_02, style = '%', validate = True,
        defaults = {"ip": None} )
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

Available format attributes:
args        You shouldn’t need to format this yourself.
    The tuple of arguments merged into msg to produce message, or a dict whose values are used for the merge (when there is only one argument, and it is a dictionary).
exc_info    You shouldn’t need to format this yourself.
    Exception tuple (à la sys.exc_info) or, if no exception has occurred, None.
msg         You shouldn’t need to format this yourself.
    The format string passed in the original logging call. Merged with args to produce message, or an arbitrary object (see Using arbitrary objects as messages).
stack_info  You shouldn’t need to format this yourself.
    Stack frame information (where available) from the bottom of the stack in the current thread, up to and including the stack frame of the logging call which resulted in the creation of this record.

%(msg)s         Message passed to logging call (same as %(message)s)
%(hostname)s    System hostname
%(username)s    System username
%(programname)s System programname

%(asctime)s     Time as human-readable string, when logging call was issued
%(created)f     Time as float when logging call was issued
%(filename)s    File name
%(funcName)s    Name of function containing the logging call
%(levelname)s   Text logging level
%(levelno)s     Integer logging level
%(lineno)d      Line number where the logging call was issued
%(message)s     Message passed to logging call (same as %(msg)s)
%(module)s      File name without extension where the logging call was issued
%(msecs)d       Millisecond part of the time when logging call was issued
%(name)s        Logger name
%(pathname)s    Full pathname to file containing the logging call
%(process)d     Process ID
%(processName)s Process name
%(relativeCreated)d - Time as integer in milliseconds when logging call was issued, relative to the time when logging module was loaded
%(thread)d      Thread ID
%(threadName)s  Thread name

%(asctime)s     Human-readable time when the LogRecord was created. By default this is of the form ‘2003-07-08 16:49:45,896’ (the numbers after the comma are millisecond portion of the time).
%(created)f     Time when the LogRecord was created (as returned by time.time()).
%(filename)s    Filename portion of pathname.
%(funcName)s    Name of function containing the logging call.
%(levelname)s   Text logging level for the message ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').
%(levelno)s     Numeric logging level for the message (DEBUG, INFO, WARNING, ERROR, CRITICAL).
%(lineno)d      Source line number where the logging call was issued (if available).
%(message)s     The logged message, computed as msg % args. This is set when Formatter.format() is invoked.
%(module)s      Module (name portion of filename).
%(msecs)d       Millisecond portion of the time when the LogRecord was created.
%(name)s        Name of the logger used to log the call.
%(pathname)s    Full pathname of the source file where the logging call was issued (if available).
%(process)d     Process ID (if available).
%(processName)s Process name (if available).
%(relativeCreated)d    Time in milliseconds when the LogRecord was created, relative to the time the logging module was loaded.
%(thread)d      Thread ID (if available).
%(threadName)s  Thread name (if available).

Emoji
You can use colors for text as others mentioned in their answers to have colorful text with a background or foreground color.
But you can use emojis instead! for example, you can use ⚠️ for warning messages and 🛑 for error messages.
Or simply use these notebooks as a color:

print("📕: error message")
print("📙: warning message")
print("📗: ok status message")
print("📘: action message")
print("📓: canceled status message")
print("📔: Or anything you like and want to recognize immediately by color")

🎁 Bonus:
This method also helps you to quickly scan and find logs directly in the source code.

How to open emoji picker?
mac os: control + command + space
windows: win + .
linux: control + . or control + ;

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
                s = LUDateTime.DateTimeStr (False, LToday, LUDateTime.cFormatDateYYMMDD_01, True)
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
            s = LUDateTime.DateTimeStr(False, LToday, LUDateTime.cFormatDateTimeLog01, True)+' '+AOpt+' '+AMessage
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
def CreateTFileMemoLog () -> TFileMemoLog:
    """CreateTFileMemoLog"""
#beginfunction
    return TFileMemoLog ()
#endfunction

def CreateTLogger (ALogerName: str) -> TLogger:
    """CreateTLogging"""
#beginfunction
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    logging.setLoggerClass (TLogger)
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # создаем регистратор
    LResult = TLogger(ALogerName)
    return LResult
#endfunction

def SetFormatterForLogger (ALogger: logging.Logger):
    """SetFormatterForLogger"""
#beginfunction
    for item in ALogger.handlers:
        if type (item.formatter) is pythonjsonlogger.jsonlogger.JsonFormatter:
            item.formatter.json_ensure_ascii = False
        #endif
        if type (item) is logging.StreamHandler:
            Lfmt = item.formatter._fmt
            Ldatefmt = item.formatter.datefmt
            LFormaterConsole = TFormatter (AUseColor = True, fmt = Lfmt, datefmt = Ldatefmt)
            item.setFormatter (LFormaterConsole)
        #endif
    #enfor
#endfunction

#-------------------------------------------------
# LOGGING_CONFIG
#-------------------------------------------------
LOGGING_CONFIG = \
{
    'version': 1,
    'disable_existing_loggers': 1,
    'loggers': {
        'root': {
            'handlers': ['CONSOLE', 'FILE_01'],
            'level': 'DEBUG',
            'propagate': 1
        },

        'log02': {
            'handlers': ['FILE_02'],
            'level': 'DEBUG',
            'qualname': 'log02',
            'propagate': 0
        }
    },
    'handlers': {
        'CONSOLE': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'FORMAT_01',
            'stream': 'ext://sys.stdout'
        },
        'FILE_01': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'FORMAT_01',
            'maxBytes': 10000000,
            'backupCount': 5,
            'filename': 'LOG\LOGGING_CONFIG.log'
        },
        'FILE_02': {
            # 'class': 'logging.handlers.TimedRotatingFileHandler',
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'FORMAT_json',
            # 'interval': 'M',
            'maxBytes': 10000000,
            'backupCount': 5,
            'filename': 'LOG\LOGGING_CONFIG_json.log'
        }
    },
    'formatters': {
        'FORMAT_01': {
            'format': Cstrfmt_01,
            'datefmt': Cdatefmt_01
        },
        'FORMAT_json': {
            'class': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': Cstrfmt_01,
            'datefmt': Cdatefmt_01
        }
    },
}

def CreateLoggerCONFIG (AFileNameCONFIG: str, ALogerName: str) -> logging.Logger:
    """CreateLoggerCONFIG"""
#beginfunction
    CONFIG = {}

    # LUDict.SaveDictSTR (LOGGING_CONFIG, AFileNameCONFIG)
    # if LUFile.FileExists(AFileNameCONFIG):
    #     # читаем конфигурацию из файла
    #     try:
    #         with open (AFileNameCONFIG, 'r') as FileCONFIG:
    #             CONFIG = json.load(FileCONFIG)
    #         #endwith
    #     except FileNotFoundError as ERROR:
    #         print ('Невозможно открыть файл', ERROR)
    #         GLULogger.error('Невозможно открыть файл')
    #     #endtry
    # else:
    #     CONFIG = copy.deepcopy (LOGGING_CONFIG)
    # #endif

    CONFIG = copy.deepcopy (LOGGING_CONFIG)
    if len(CONFIG) > 0:
        # AddLevelName ()
        # читаем конфигурацию из словаря
        logging.config.dictConfig (CONFIG)
        # создаем регистратор
        LResult = logging.getLogger (ALogerName)
        # установить форматер
        SetFormatterForLogger (LResult)
        return LResult
    else:
        return None
#endfunction

def CreateLoggerFILEINI (AFileNameINI: str, ALogerName: str) -> logging.Logger:
    """CreateLoggerFILEINI"""
#beginfunction
    # AddLevelName ()
    # читаем конфигурацию из файла
    logging.config.fileConfig(AFileNameINI, disable_existing_loggers=True,
                              encoding = LUFile.cDefaultEncoding)
    # создаем регистратор
    LResult = logging.getLogger (ALogerName)
    # установить форматер
    SetFormatterForLogger (LResult)
    return LResult
#endfunction

def CreateLoggerBASIC (ALevel, AFileNameLOG: str, ALogerName: str) -> logging.Logger:
    """CreateTLoggingCONFIG"""
#beginfunction
    # AddLevelName ()
    # читаем конфигурацию из
    if len(AFileNameLOG) > 0:
        logging.basicConfig (level = ALevel, filename = AFileNameLOG, style='%',
                             datefmt = Cdatefmt_01, format = Cstrfmt_01)
    else:
        logging.basicConfig (level = ALevel, stream=sys.stdout, style='%',
                             datefmt = Cdatefmt_01, format = Cstrfmt_01)
    # создаем регистратор
    LResult = logging.getLogger (ALogerName)
    # установить форматер
    SetFormatterForLogger (LResult)
    return LResult
#endfunction

def PrintHandlers (ALogger: logging.Logger):
    """Printhandlers"""
#beginfunction
    for item in ALogger.root.handlers:
        print (item)
        if type(item) is logging.StreamHandler:
            Lfmt = item.formatter._fmt
            Ldatefmt = item.formatter.datefmt
            LFormaterConsole = TFormatter (AUseColor=True, fmt=Lfmt, datefmt=Ldatefmt)
            # item.setFormatter (LFormaterConsole)
        #endif
    #enfor

AddLevelName ()

GFileMemoLog = CreateTFileMemoLog ()
GLogger = CreateTLogger ('root')

GLULogger = CreateLoggerCONFIG (CDefaultFileLogCONFIG, 'root')

# GLULogger = CreateLoggerFILEINI (CDefaultFileLogINI, 'root')

# GLULogger = CreateLoggerBASIC (logging.DEBUG, 'LOG\\' + CDefaultFileLogFILEBASIC, 'root')
# GLULogger = CreateLoggerBASIC (logging.DEBUG, '', 'root')

LUConst.LULogger.disabled = False

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
else:
    ...
#endif

#endmodule
