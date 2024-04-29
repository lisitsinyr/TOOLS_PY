"""LULog.py"""
# -*- coding: UTF-8 -*-
__annotations__ ="""
 =======================================================
 Copyright (c) 2023-2024
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
import yaml
import json

import inspect
import traceback

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
import pythonjsonlogger
import pythonjsonlogger.jsonlogger
#------------------------------------------
import PySide6.QtWidgets

#------------------------------------------
# БИБЛИОТЕКА LU 
#------------------------------------------
import lyr.LUConst
import lyr.LUFile
import lyr.LUConsole
import lyr.LUDateTime
import lyr.LUos
import lyr.LUParserINI
import lyr.LUDict
import lyr.LUSupport

# import lyr

# ===========================================================================
# CONST
# ===========================================================================
import rich
import rich.console
GConsoleRich = rich.console.Console ()

STATLogging = True

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
ctlsDEBUGTEXT = 'T'
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

# строка формата сообщения
# Cstrfmt_04 = '%(asctime)s %(msecs)03d [%(name)s] %(levelno)02d %(levelname)-8s %(module)s %(message)s'
Cstrfmt_01 = '%(asctime)s [%(name)s] [%(module)-15s] %(levelno)02d %(levelname)-10s %(lineno)04d %(message)s'
Cstrfmt_02 = '%(asctime)s %(name)s %(levelname)-10s %(message)s'
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
CDefaultFileLogYAML = 'logging.YAML'

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
class TTypeSETUPLOG (enum.Enum):
    """TTypeSETUPLOG"""
    tslCONFIG = 0
    tslYAML = 1
    tslINI = 2
    @classmethod
    def Empty (cls):
        ...
#endclass

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
    tlsDEBUGTEXT = ctlsDEBUGTEXT
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

Cbold = 'bold '
Cblue = 'blue'
Cwhite = 'white'
Cyellow = 'yellow'
Cred = 'red'
Cgreen = 'green'
Con = 'on'

Cbold_blue = Cbold+Cblue
Cbold_white = Cbold+Cwhite
Cbold_yellow = Cbold+Cyellow
Cbold_red = Cbold+Cred
Cbold_red_blue = Cbold+Cred+' on '+Cblue
Cbold_green = Cbold+Cred

COLORS_tls = {
    TTypeLogString.tlsNOTSET: lyr.LUConsole.cFG8_BLUE+lyr.LUConsole.sEND,
    TTypeLogString.tlsDEBUG: lyr.LUConsole.cFG8_BLUE+lyr.LUConsole.sEND,
    TTypeLogString.tlsINFO: lyr.LUConsole.cFG8_WHITE+lyr.LUConsole.sEND,
    TTypeLogString.tlsWARNING: lyr.LUConsole.cS_BOLD + ';' + lyr.LUConsole.cFG8_YELLOW+lyr.LUConsole.sEND,
    TTypeLogString.tlsERROR: lyr.LUConsole.cS_BOLD + ';' + lyr.LUConsole.cFG8_RED+lyr.LUConsole.sEND,
    TTypeLogString.tlsCRITICAL: lyr.LUConsole.cS_BOLD + ';' + lyr.LUConsole.cFG8_BLACK + ';' + lyr.LUConsole.cBG8_RED+lyr.LUConsole.sEND,
    TTypeLogString.tlsBEGIN: lyr.LUConsole.cS_BOLD + ';' + lyr.LUConsole.cFG8_GREEN  + lyr.LUConsole.sEND,
    TTypeLogString.tlsEND: lyr.LUConsole.cS_BOLD + ';' + lyr.LUConsole.cFG8_GREEN + lyr.LUConsole.sEND,
    TTypeLogString.tlsPROCESS: lyr.LUConsole.cS_BOLD + ';' + lyr.LUConsole.cFG8_GREEN + lyr.LUConsole.sEND,
    TTypeLogString.tlsDEBUGTEXT: lyr.LUConsole.cS_BOLD + ';' + lyr.LUConsole.cFG8_BLUE+lyr.LUConsole.sEND,
    TTypeLogString.tlsTEXT: lyr.LUConsole.cS_BOLD + ';' + lyr.LUConsole.cFG8_YELLOW+lyr.LUConsole.sEND
}

COLORS_tls_rich = {
    TTypeLogString.tlsNOTSET: Cbold_blue,
    TTypeLogString.tlsDEBUG: Cbold_blue,
    TTypeLogString.tlsINFO: Cbold_white,
    TTypeLogString.tlsWARNING: Cbold_yellow,
    TTypeLogString.tlsERROR: Cbold_red,
    TTypeLogString.tlsCRITICAL: Cbold_red_blue,
    TTypeLogString.tlsBEGIN: Cbold_green,
    TTypeLogString.tlsEND: Cbold_green,
    TTypeLogString.tlsPROCESS: Cbold_green,
    TTypeLogString.tlsDEBUGTEXT: Cbold_blue,
    TTypeLogString.tlsTEXT: Cbold_yellow
}

COLORS = {
    logging.NOTSET: lyr.LUConsole.cFG8_BLUE+lyr.LUConsole.sEND,
    logging.DEBUG: lyr.LUConsole.cFG8_BLUE+lyr.LUConsole.sEND,
    logging.INFO: lyr.LUConsole.cFG8_WHITE+lyr.LUConsole.sEND,
    logging.WARNING: lyr.LUConsole.cS_BOLD + ';' + lyr.LUConsole.cFG8_YELLOW+lyr.LUConsole.sEND,
    logging.ERROR: lyr.LUConsole.cS_BOLD + ';' + lyr.LUConsole.cFG8_RED+lyr.LUConsole.sEND,
    logging.CRITICAL: lyr.LUConsole.cS_BOLD + ';' + lyr.LUConsole.cFG8_BLACK + ';' + lyr.LUConsole.cBG8_RED+lyr.LUConsole.sEND,
    BEGIN: lyr.LUConsole.cS_BOLD + ';' + lyr.LUConsole.cFG8_GREEN + lyr.LUConsole.sEND,
    END: lyr.LUConsole.cS_BOLD + ';' + lyr.LUConsole.cFG8_GREEN + lyr.LUConsole.sEND,
    PROCESS: lyr.LUConsole.cS_BOLD + ';' + lyr.LUConsole.cFG8_GREEN + lyr.LUConsole.sEND,
    DEBUGTEXT: lyr.LUConsole.cS_BOLD + ';' + lyr.LUConsole.cFG8_BLUE+lyr.LUConsole.sEND,
    TEXT: lyr.LUConsole.cS_BOLD + ';' + lyr.LUConsole.cFG8_YELLOW+lyr.LUConsole.sEND
}

COLORS_rich = {
    logging.NOTSET: Cbold_blue,
    logging.DEBUG: Cbold_blue,
    logging.INFO: Cbold_white,
    logging.WARNING: Cbold_yellow,
    logging.ERROR: Cbold_red,
    logging.CRITICAL: Cbold_red_blue,
    BEGIN: Cbold_green,
    END: Cbold_green,
    PROCESS: Cbold_green,
    DEBUGTEXT: Cbold_blue,
    TEXT: Cbold_yellow
}

#TLogOutputs = set of TLogOutput;

class TFileMemoLog (object):
    """TFileMemoLog"""
    luClassName = "TFileMemoLog"

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
        self.__FLogCODE = lyr.LUFile.cDefaultEncoding
        self.__FConsoleRich = rich.console.Console()

        # self.__FLogger: logging.Logger = CreateLoggerFILEINI (CDefaultFileLogINI, 'root')

        self.Clear ()
    #endfunction

    #--------------------------------------------------
    # destructor
    #--------------------------------------------------
    def __del__(self):
        """destructor"""
    #beginfunction
        del self.__FLogStrings
        del self.__FLogSave
        LClassName = self.__class__.__name__
        s = '{} уничтожен'.format (LClassName)
        #print (s)
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
    #beginfunction
        ...
    #endfunction

    def _GetLogSaveCurrent (self) -> list:         #TStringList;
    #beginfunction
        """_GetLogSaveCurrent"""
        LResult = self._GetLogSave (self.__FFileName)
        return LResult
    #endfunction

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
            except:
                s = f'TruncateLog: Неправильная кодировка журнала!'
                LoggerTOOLS.error (s)
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

        # if self.FUseColor:

        self.__FLogStrings.clear ()
        self.__FLogStrings.append (self.__FLogStringAnsi)
        for s in self.__FLogStrings:
            if T == TTypeLogString.tlsTEXT:
                _s = s
            else:
                _s = self._LogDateStr (False) + ' ' + str(T.value) + ' ' + s
            if not LUSupport.ISTerminal ():
                LCOLOR = COLORS_tls.get (T)
                if LCOLOR is not None:
                    LFmt = LUConsole.sBEGIN_oct + LCOLOR + _s + LUConsole.sRESET
                else:
                    LFmt = _s
                LUConsole.WriteLN (LFmt)
            else:
                LCOLOR = COLORS_tls_rich.get (T)
                LFmt = _s
                if len(LCOLOR) > 0:
                    LFmt = '[' + LCOLOR + ']' + _s
                else:
                    LFmt = s
                self.__FConsoleRich.print (LFmt)
            #endif
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

        for s in self.__FLogStrings:
            if T == TTypeLogString.tlsTEXT:
                _s = s
            else:
                _s = self._LogDateStr (False) + ' ' + str(T.value) + ' ' + s
            #endif
            try:
                LEncoding = self.__FLogCODE

                # LEncoding = LUFile.GetFileEncoding (self.__FFileName)
                # if LEncoding == '':
                #     LEncoding = LUFile.cDefaultEncoding

                LEncoding = LUFile.cDefaultEncoding
                with open (self.__FFileName, 'a+', encoding = LEncoding) as LFile:

                    # _s = str (s.encode ('utf-8'), 'cp1251')
                    # _s = str (s.encode ('cp1251'), 'cp1251')

                    # _s = str (_s.encode (self.__FLogCODE), self.__FLogCODE)

                    LFile.write (_s + '\n')

                #endwith
            except:
                s = f'_HandlerFILE: Неправильная кодировка журнала!'
                LoggerTOOLS.error (s)
            #endtry
        #endfor
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

    def AddLogFile (self, AFileName: str):
        """AddLogFile"""
    #beginfunction
        if LUFile.FileExists (AFileName):
            LEncoding = LUFile.GetFileEncoding (AFileName)
            if LEncoding == '':
                LEncoding = LUFile.cDefaultEncoding
            try:
                # работа с файлом
                with open (AFileName, 'r', encoding = LEncoding) as LFile:
                    for s in LFile:
                        self.AddLog (TTypeLogString.tlsTEXT, s.rstrip('\n'))
                    #endfor
                #endwith
            except:
                self.AddLog (TTypeLogString.tlsERROR, AFileName)
                s = f'AddLogFile: Неправильная кодировка журнала!'
                LoggerTOOLS.error (s)

        #endif
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
    def __init__(self, parent, **kwargs):
    # def __init__ (self, parent):
        """Constructor"""
    #beginfunction
        logging.Handler.__init__(self, **kwargs)
        # super ().__init__ ()

        self.__Fwidget = None
        # self.__Fwidget = PySide6.QtWidgets.QPlainTextEdit (parent)
        # self.__Fwidget.setReadOnly (True)
    #endfunction

    #--------------------------------------------------
    # @property widget
    #--------------------------------------------------
    # getter
    @property
    def widget (self):
    #beginfunction
        return self.__Fwidget
    #endfunction
    @widget.setter
    def widget (self, Value):
    #beginfunction
        self.__Fwidget = Value
    #endfunction


    def emit(self, record):
        if self.widget is None:
            super (THandler, self).emit (record)
        else:
            msg = self.format (record)
            self.widget.appendPlainText (msg)
        #endif
#endclass

#-------------------------------------------------
# class TStreamHandler(logging.StreamHandler):
#-------------------------------------------------
class TStreamHandler(logging.StreamHandler):
    """TStreamHandler"""
    luClassName = "TStreamHandler"
    #--------------------------------------------------
    # constructor
    #--------------------------------------------------
    def __init__(self, *args, **kwargs):
        """Constructor"""
    #beginfunction
        logging.StreamHandler.__init__(self, *args, **kwargs)
        self.name = 'CONSOLE'
        self.FAPPGUI = False

        self.__FConsoleRich = rich.console.Console()

        self.__FWidget:PySide6.QtWidgets.QPlainTextEdit = None
        # self.__Fwidget = PySide6.QtWidgets.QPlainTextEdit (parent)
        # self.__Fwidget = PySide6.QtWidgets.QPlainTextEdit ()
        # self.__Fwidget.setReadOnly (True)

    #endfunction

    # def __new__(cls, clsname, bases, attrs):
    #     newclass = super(cls, MetaClass).__new__(cls, clsname, bases, attrs)
    #     register(newclass)  # here is your register function
    #     return newclass

    #--------------------------------------------------
    # @property widget
    #--------------------------------------------------
    # getter
    @property
    def Widget (self):
    #beginfunction
        return self.__FWidget
    #endfunction
    @Widget.setter
    def Widget (self, Value):
    #beginfunction
        self.__FWidget = Value
    #endfunction

    #--------------------------------------------------
    # emit
    #--------------------------------------------------
    def emit(self, record):
        """emit"""
    #beginfunction
        if type(self.formatter) is TFormatter:
            LFormatter: TFormatter = self.formatter
            # widget
            if not self.Widget is None:
                b = LFormatter.FUseColor
                LFormatter.FUseColor = False
                msg = LFormatter.format (record)
                self.Widget.appendPlainText (msg)
                # self.widget.document().end()
                self.Widget.verticalScrollBar().setValue (self.Widget.verticalScrollBar().maximum ())
                LFormatter.FUseColor = b
            #endif

            if LFormatter.FUseColor:
                # self.emit(record)
                try:
                    msg = self.format(record)
                    stream = self.stream
                    # issue 35046: merged two stream.writes into one.
                    if not lyr.LUSupport.IsTerminal ():
                        stream.write(msg + self.terminator)
                        self.flush()
                    else:
                        msg = self.format (record)
                        if not self.FAPPGUI:
                            #rich.print (msg)
                            self.__FConsoleRich.print(msg)
                        #endif
                    #endif
                except RecursionError:  # See issue 36272
                    raise
                except Exception:
                    self.handleError(record)
                #endtry
            #endif
        else:
            super(TStreamHandler, self).emit(record)
        #endif
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
        #print(record.color)
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

    #--------------------------------------------------
    # constructor
    #--------------------------------------------------
    def __init__ (self, AUseColor = True, **kwargs):
        """Constructor"""
    #beginfunction
        #class logging.Formatter(fmt=None, datefmt=None, style='%', validate=True, *, defaults=None)
        logging.Formatter.__init__(self, **kwargs)
        self.FUseColor = AUseColor
    #endfunction

    def _SetColor(self, AFmt: str, ALevelNo: int) -> str:
        """_SetColor"""
    #beginfunction
        if self.FUseColor:
            if not lyr.LUSupport.IsTerminal ():
                LCOLOR = COLORS.get (ALevelNo)
                LFmt = lyr.LUConsole.sBEGIN_oct + LCOLOR + AFmt + lyr.LUConsole.sRESET
                return LFmt
            else:
                LCOLOR = COLORS_rich.get (ALevelNo)
                _s = AFmt
                LFmt = _s
                LFmt = '[' + LCOLOR + ']' + _s
                if len(LCOLOR) > 0:
                    LFmt = '[' + LCOLOR + ']' + _s
                else:
                    LFmt = _s
                return LFmt
        else:
            return AFmt
        #endif
    #endfunction

    def format(self, record):
        """format"""
    #beginfunction
        # отдельный атрибут
        # LLevelname = record.levelname
        # record.levelname = '_'+LLevelname+'_'

        Ldatefmt = self.datefmt
        if self.FUseColor:
            if record.levelno == TEXT:
                # установить новый fmt
                Lfmt = self._SetColor ('%(message)s', record.levelno)
            else:
                Lfmt = self._SetColor (self._fmt, record.levelno)
            #endif
        else:
            if record.levelno == TEXT:
                # установить новый fmt
                Lfmt = '%(message)s'
            else:
                Lfmt = self._fmt
            #endif
        #endif
        # установить новый fmt
        Lformatter = logging.Formatter (Lfmt, Ldatefmt)
        s = Lformatter.format (record)
        return s
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

def AddHandlerCONSOLE (ALogger: logging.Logger, ALevel: int, Astrfmt: str, Adatefmt: str,
                    Astyle: str, Adefaults):
    """AddFileHandler"""

#beginfunction
    LHandler = TStreamHandler ()
    LHandler.setLevel (ALevel)
    LHandler.set_name ('CONSOLE')
    LHandler.setStream (sys.stdout)
    LFormater = TFormatter (fmt=Astrfmt, datefmt=Adatefmt,
                                            style=Astyle, validate=True, defaults=Adefaults)
    LHandler.setFormatter (LFormater)
    ALogger.addHandler (LHandler)
#endfunction

def AddHandlerFILE (ALogger: logging.Logger, AFileName: str, ALevel: int, Astrfmt: str, Adatefmt: str,
                    Astyle: str, Adefaults):
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
    luClassName = "TLogger"

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
        self.propagate = False
        AddHandlerCONSOLE (self, self.LEVEL, self.__Fstrfmt, self.__Fdatefmt, self.__Fstyle, self.__Fdefaults)
        self.Clear ()
    #endfunction

    #--------------------------------------------------
    # destructor
    #--------------------------------------------------
    def __del__(self):
        """destructor"""
    #beginfunction
        LClassName = self.__class__.__name__
        s = '{} уничтожен'.format(LClassName)
        #print (s)
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

    def AddHandlerCONSOLE(self, ALevel: int):
    #beginfunction
        # AddHandlerCONSOLE (self, ALevel, self.__Fstrfmt, self.__Fdatefmt, self.__Fstyle, self.__Fdefaults)
        # LHandler = logging.StreamHandler ()
        # LHandler.setLevel (ALevel)
        # LHandler.set_name ('CONSOLE')
        # LHandler.setStream (sys.stdout)
        # LFormater = TFormatter (fmt=self.__Fstrfmt, datefmt=self.__Fdatefmt,
        #                                         style=self.__Fstyle, validate=True, defaults=self.__Fdefaults)
        # LHandler.setFormatter (LFormater)
        # self.addHandler (LHandler)
        ...
    #endfunction

    def AddHandlerFILE(self, AFileName: str, ALevel: int):
    #beginfunction
        LHandler = logging.FileHandler (AFileName, mode='a+',
                                        encoding=LUFile.cDefaultEncoding, delay=False, errors=None)
        LHandler.setLevel (ALevel)
        LHandler.set_name ('FILE')
        LFormater = TFormatter (AUseColor = False,
                                fmt=self.__Fstrfmt, datefmt=self.__Fdatefmt,
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
        LFormater = TFormatterJSON (AUseColor = False,
                                    fmt=self.__Fstrfmt, datefmt=self.__Fdatefmt,
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
            if len (ALogDir) == 0:
                # LLogDir = os.environ['TEMP']
                LLogDir = LUFile.GetTempDir()
            #endif
            LLogFile = ALogFile
            if ALogFile == '':
                s = LUDateTime.DateTimeStr (False, LToday, LUDateTime.cFormatDateYYMMDD_01, False)
                LLogFile = s+'.log'
            #endif
            LLogFileName = s.path.join([LLogDir, LLogFile])
            if ALog == 10 or ALog == 30:
                if LUFile.FileExists(LLogFileName):
                    try:
                        LUFile.FileDelete(LLogFileName)
                    except:
                    # except LUErrors.LUFileError_FileERROR as ERROR:
                        s = f'Ошибка при удалении файла {LLogFileName}'
                        LoggerTOOLS.error (s)
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
def LogAdd (ALog: int, ALogFile: str, AOpt: TTypeLogString, AMessage: str):
    """LogAdd"""

    def _WriteConsole(_s, T):
    #beginfunction
        if not LUSupport.ISTerminal ():
            LCOLOR = COLORS_tls.get (T)
            if LCOLOR is not None:
                LFmt = LUConsole.sBEGIN_oct + LCOLOR + _s + LUConsole.sRESET
            else:
                LFmt = _s
            LUConsole.WriteLN (LFmt)
        else:
            LCOLOR = COLORS_tls_rich.get (T)
            LFmt_default = _s
            LFmt = '[' + LCOLOR + ']' + _s
            GConsoleRich.print (LFmt)
        #endif
    #endfunction

    def _WriteFile(_s):
    #beginfunction

        LEncoding = LUFile.GetFileEncoding (ALogFile)
        if LEncoding == '':
            LEncoding = LUFile.cDefaultEncoding

        LEncoding = LUFile.cDefaultEncoding
        # sWIN = s.encode (encoding = 'UTF-8').decode(encoding = 'ANSI')
        # sWIN = s.encode (encoding = 'WINDOWS-1251').decode(encoding = 'UTF-8')
        # Это работает !!!!!!!!!!!!!!!!!
        try:
            with open (ALogFile, 'a+', encoding = LEncoding) as LFile:
                LFile.write (_s+'\n')
        except:
            _s = f'_WriteFile: Неправильная кодировка журнала!'
            LoggerTOOLS.error (_s)
        #endtry
    #endfunction

#beginfunction
    LToday = LUDateTime.Now ()
    if AOpt == TTypeLogString.tlsTEXT:
        s = AMessage
    else:
        s = LUDateTime.DateTimeStr(False, LToday, LUDateTime.cFormatDateTimeLog01, True)+' '+\
            AOpt.value+' '+AMessage
    match ALog:
        case 1|10:
            _WriteConsole (s, AOpt)
            _WriteFile (s)
        case 2:
            _WriteConsole (s, AOpt)
        case 3|30:
            _WriteConsole (s, AOpt)
            _WriteFile (s)
    #endmatch
#endfunction

#--------------------------------------------------------------------------------
# LogAddFile (ALog: int, ALogFile: str, AOpt: str, AFileName: str,
#            AStyles='', AFG8='', ABG8='', AFG256='', ABG256='', AESC=''):
#--------------------------------------------------------------------------------
def LogAddFile (ALog: int, ALogFile: str, AOpt: TTypeLogString, AFileName: str):
    """LogAddFile"""
#beginfunction
    if LUFile.FileExists (AFileName):
        try:
            LEncoding = LUFile.GetFileEncoding (AFileName)
            if LEncoding == '':
                LEncoding = LUFile.cDefaultEncoding
            with open (AFileName, 'r', encoding = LEncoding) as LFile:
                for s in LFile:
                    Ls = s.split ('\n')[0]
                    LogAdd (ALog, ALogFile, AOpt, Ls)
                #endfor
            #endwith
        except:
            s = f'LogAddFile: Неправильная кодировка журнала!'+AFileName
            LoggerTOOLS.error (s)
        #endtry
    #endif
#endfunction

#-------------------------------------------------
# GLOBAL
#-------------------------------------------------
def SetFormatterForLogger (ALogger: logging.Logger):
    """SetFormatterForLogger"""
#beginfunction
    for item in ALogger.handlers:
        if type (item.formatter) is pythonjsonlogger.jsonlogger.JsonFormatter:
            item.formatter.json_ensure_ascii = False
        #endif
        if type (item) is logging.StreamHandler or type (item) is TStreamHandler:
            # if LUSupport.ISTerminal ():
            #     TStreamHandler(item).setLevel(logging.CRITICAL)
            #     # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            #     ...
            # #endif
            Lfmt = item.formatter._fmt
            Ldatefmt = item.formatter.datefmt
            LFormaterConsole = TFormatter (fmt = Lfmt, datefmt = Ldatefmt)
            item.setFormatter (LFormaterConsole)
        #endif
    #enfor
#endfunction

def PrintHandlers (ALogger: logging.Logger):
    """Printhandlers"""
#beginfunction
    for item in ALogger.root.handlers:
        s = f'{item.name}={item}'
        # LoggerTOOLS.info(s)
        if type(item) is logging.StreamHandler:
            LoggerTOOLS.info ('logging.StreamHandler='+s)
            # Lfmt = item.formatter._fmt
            # Ldatefmt = item.formatter.datefmt
            # LFormaterConsole = TFormatter (AUseColor=True, fmt=Lfmt, datefmt=Ldatefmt)
            ...
        #endif
        if type (item) is TStreamHandler:
            LoggerTOOLS.info ('TStreamHandler='+s)
            # Lfmt = item.formatter._fmt
            # Ldatefmt = item.formatter.datefmt
            # LFormaterConsole = TFormatter (AUseColor=True, fmt=Lfmt, datefmt=Ldatefmt)
            ...
        #endif
    #enfor
#endfunction

def GetHandler (ALogger: logging.Logger, ANameHandler: str):
    """Printhandlers"""
#beginfunction
    for item in ALogger.root.handlers:
        s = f'{item.name}={item}'
        # LoggerTOOLS.info(s)
        if item.name == ANameHandler:
            return item
        #endif
    #enfor
#endfunction

def WinToUnix (Astr: str) -> str:
    """WinToUnix"""
#beginfunction
    LOSInfo = LUos.TOSInfo ()
    print ('HostName      = ' + LOSInfo.node)
    print ('OS            = ' + LOSInfo.system)
    # print ('OS            = ' + LOSInfo.uname.system)
    match LOSInfo.system.upper ():
        case 'LINUX':
            Lstr = os.path.abspath (Astr).replace ("\\", "/")
        case 'WINDOWS':
            Lstr = Astr
        case _:
            # print ('INFO: Only LINUX or WINDOWS')
            Lstr = Astr
    #endmatch
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
            'handlers': [
                'CONSOLE',
                'FILE_01'
            ],
            'level': 'DEBUG',
            'propagate': 1
        },
        'log01': {
            'handlers': [
                'FILE_01'
            ],
            'level': 'DEBUG',
            'propagate': 0,
            'qualname': 'log01'
        },
        'log02': {
            'handlers': [
                'FILE_02'
            ],
            'level': 'DEBUG',
            'propagate': 0,
            'qualname': 'log02'
        }
    },
    'handlers': {
        'CONSOLE': {
            # 'class': 'logging.StreamHandler',
            'class': 'LULog.TStreamHandler',
            'level': 'DEBUG',
            'formatter': 'FORMAT_01',
            'stream': 'ext://sys.stdout'
        },
        'FILE_01': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'FORMAT_01',
            'maxBytes': 10000000,
            'backupCount': 5,
            'filename': 'LOGGING_CONFIG.log'
        },
        'FILE_02': {
            # 'class': 'logging.handlers.TimedRotatingFileHandler',
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'FORMAT_json',
            # 'interval': 'M',
            'maxBytes': 1024,
            'backupCount': 5,
            'filename': 'LOGGING_CONFIG_json.log'
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

#-------------------------------------------------
# CreateLoggerCONFIG
#-------------------------------------------------
def CreateLoggerCONFIG (AFileNameCONFIG: str, ALogerName: str,
                        ADirectoryLOG: str, AFileNameLOG: str, AFileNameLOGjson: str) -> logging.Logger:
    """CreateLoggerCONFIG"""
#beginfunction
    global CONFIG
    CONFIG = {}

    LPath = LUFile.ExtractFileDir(__file__)
    LFileNameCONFIG = os.path.join (LPath, AFileNameCONFIG)
    if LUFile.FileExists(LFileNameCONFIG):
        # читаем конфигурацию из файла
        try:
            with open (LFileNameCONFIG, 'r') as FileCONFIG:
                CONFIG = json.load(FileCONFIG)
            #endwith
        except FileNotFoundError as ERROR:
            print ('Невозможно открыть файл', ERROR)
            GLULogger.error('Невозможно открыть файл')
        #endtry
    else:
        CONFIG = copy.deepcopy (LOGGING_CONFIG)
    #endif
    #-------------------------------------------------------------------
    # CONFIG = copy.deepcopy (LOGGING_CONFIG)
    #-------------------------------------------------------------------

    if AFileNameLOG == '':
        LOptionValue_01 = CONFIG['handlers']['FILE_01']['filename']
        print ('LOptionValue_01:',LOptionValue_01)
        LFileNameLOG = LUFile.ExtractFileName (LOptionValue_01)
    else:
        LFileNameLOG = LUFile.ExtractFileName (AFileNameLOG)
    #endif
    print('LFileNameLOG:',LFileNameLOG)

    if AFileNameLOGjson == '':
        LOptionValue_02 = CONFIG['handlers']['FILE_02']['filename']
        print ('LOptionValue_02:',LOptionValue_02)
        LFileNameLOGjson = LUFile.ExtractFileName (LOptionValue_02)
    else:
        LFileNameLOGjson = LUFile.ExtractFileName (AFileNameLOGjson)
    #endif
    print('LFileNameLOGjson:',LFileNameLOGjson)

    if ADirectoryLOG == '':
        # log будет создан в текущем каталоге (по умолчанию)
        LDirectoryLOG = LUos.GetCurrentDir ()
    else:
        # log будет создан в ADirectoryLOG
        LDirectoryLOG = LUFile.ExpandFileName (ADirectoryLOG)
    #endif
    # print('LDirectoryLOG:',LDirectoryLOG)
    if not LUFile.DirectoryExists (LDirectoryLOG):
        LUFile.ForceDirectories(LDirectoryLOG)
    #endif

    # установить имена log файлов в CONFIG
    LOptionValue_01 = os.path.join (LDirectoryLOG, LFileNameLOG)
    print('LOptionValue_01:', LOptionValue_01)
    CONFIG ['handlers'] ['FILE_01'] ['filename'] = LOptionValue_01

    LOptionValue_02 = os.path.join (LDirectoryLOG, LFileNameLOGjson)
    print('LOptionValue_02:', LOptionValue_02)
    CONFIG ['handlers'] ['FILE_02'] ['filename'] = LOptionValue_02

    if len(CONFIG) > 0:
        #-------------------------------------------------------------------
        LFileNameCONFIG = os.path.join (LUos.GetCurrentDir (), CDefaultFileLogCONFIG)
        LUDict.SaveDictSTR (CONFIG, LFileNameCONFIG)
        #-------------------------------------------------------------------
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

#-------------------------------------------------
# CreateLoggerYAML
#-------------------------------------------------
def CreateLoggerYAML (AFileNameYAML: str, ALogerName: str, ADirectoryLOG: str, AFileNameLOG: str, AFileNameLOGjson: str) -> logging.Logger:
    """CreateLoggerFILEYAML"""
#beginfunction
    global CONFIG_YAML
    CONFIG_YAML = {}

    LPath = LUFile.ExtractFileDir(__file__)
    LFileNameYAML = os.path.join (LPath, AFileNameYAML)
    if LUFile.FileExists (LFileNameYAML):
        # читаем конфигурацию из файла
        try:
            with (open (LFileNameYAML, 'r') as FileCONFIG_YAML):
                CONFIG_YAML = yaml.load(FileCONFIG_YAML, Loader=yaml.FullLoader)
            #endwith
        except FileNotFoundError as ERROR:
            print ('Невозможно открыть файл', ERROR)
            GLULogger.error ('Невозможно открыть файл')
        #endtry
    else:
        CONFIG_YAML = copy.deepcopy (LOGGING_CONFIG)
    #endif
    #-------------------------------------------------------------------
    # CONFIG_YAML = copy.deepcopy (LOGGING_CONFIG)
    #-------------------------------------------------------------------

    if AFileNameLOG == '':
        LOptionValue_01 = CONFIG_YAML ['handlers'] ['FILE_01'] ['filename']
        print ('LOptionValue_01:', LOptionValue_01)
        LFileNameLOG = LUFile.ExtractFileName (LOptionValue_01)
    else:
        LFileNameLOG = LUFile.ExtractFileName (AFileNameLOG)
    #endif
    print ('LFileNameLOG:', LFileNameLOG)

    if AFileNameLOGjson == '':
        LOptionValue_02 = CONFIG_YAML ['handlers'] ['FILE_02'] ['filename']
        print ('LOptionValue_02:', LOptionValue_02)
        LFileNameLOGjson = LUFile.ExtractFileName (LOptionValue_02)
    else:
        LFileNameLOGjson = LUFile.ExtractFileName (AFileNameLOGjson)
    #endif
    print ('LFileNameLOGjson:', LFileNameLOGjson)

    if ADirectoryLOG == '':
        # log будет создан в текущем каталоге (по умолчанию)
        LDirectoryLOG = LUos.GetCurrentDir ()
    else:
        # log будет создан в ADirectoryLOG
        LDirectoryLOG = LUFile.ExpandFileName (ADirectoryLOG)
    #endif
    # print('LDirectoryLOG:',LDirectoryLOG)
    if not LUFile.DirectoryExists (LDirectoryLOG):
        LUFile.ForceDirectories(LDirectoryLOG)
    #endif

    # установить имена log файлов в CONFIG
    LOptionValue_01 = os.path.join (LDirectoryLOG, LFileNameLOG)
    print('LOptionValue_01:', LOptionValue_01)
    CONFIG_YAML ['handlers'] ['FILE_01'] ['filename'] = LOptionValue_01

    LOptionValue_02 = os.path.join (LDirectoryLOG, LFileNameLOGjson)
    print('LOptionValue_02:', LOptionValue_02)
    CONFIG_YAML ['handlers'] ['FILE_02'] ['filename'] = LOptionValue_02

    if len (CONFIG_YAML) > 0:
        #-------------------------------------------------------------------
        LFileNameYAML = os.path.join (LUos.GetCurrentDir (), CDefaultFileLogYAML)
        LUDict.SaveDictSTR (CONFIG_YAML, LFileNameYAML)
        #-------------------------------------------------------------------
        # читаем конфигурацию из словаря
        logging.config.dictConfig (CONFIG_YAML)
        # создаем регистратор
        LResult = logging.getLogger (ALogerName)
        # установить форматер
        SetFormatterForLogger (LResult)
        return LResult
    else:
        return None
    #endif

#endfunction

#-------------------------------------------------
# CreateLoggerFILEINI
#-------------------------------------------------
def CreateLoggerFILEINI (AFileNameINI: str, ALogerName: str,
                         ADirectoryLOG: str, AFileNameLOG: str, AFileNameLOGjson: str) -> logging.Logger:
    """CreateLoggerFILEINI"""
#beginfunction
    LDirectoryLOG = ADirectoryLOG

    # читаем конфигурацию из файла INI
    LFileNameINI = lyr.LUFile.ExpandFileName (AFileNameINI)
    if lyr.LUFile.FileExists (LFileNameINI):
        # существует файл, который можно редактировать
        SetEditINI = True
        LPathINI = LUFile.ExtractFileDir (LFileNameINI)
        LFileNameINI = os.path.join (LPathINI, LUFile.ExtractFileName (AFileNameINI))
    else:
        LPathINI = lyr.LUos.GetCurrentDir ()
        LFileNameINI = os.path.join (LPathINI, lyr.LUFile.ExtractFileName (AFileNameINI))
        # print ('LFileNameINI: ', LFileNameINI)
        if lyr.LUFile.FileExists (LFileNameINI):
            # существует файл в текущем каталоге, который можно редактировать
            SetEditINI = True
        else:
            # берем имя файла из проекта, если оно есть
            LPathINI = lyr.LUFile.ExtractFileDir (__file__)
            LFileNameINI = os.path.join (LPathINI, lyr.LUFile.ExtractFileName (AFileNameINI))
            SetEditINI = False
        #endif
    #endif
    # print ('LPathINI:',LPathINI)
    # print ('LFileNameINI:',LFileNameINI)

    if not SetEditINI:
        pass
    else:
        LINIFile = LUParserINI.TINIFile ()
        LINIFile.FileNameINI = LFileNameINI
        LOptionName = 'args'
        if AFileNameLOG == '':
            LSectionName_01 = 'handler_FILE_01'
            LOptionValue_01 = LINIFile.GetOption(LSectionName_01, LOptionName)
            print ('LOptionValue_01:',LOptionValue_01)
            LFileNameLOG = LUFile.ExtractFileName (LOptionValue_01.split([',', '('])[0])
        else:
            LFileNameLOG = LUFile.ExtractFileName (AFileNameLOG)
        #endif
        # print('LFileNameLOG:',LFileNameLOG)
        if AFileNameLOGjson == '':
            LSectionName_02 = 'handler_FILE_02'
            LOptionValue_02 = LINIFile.GetOption(LSectionName_02, LOptionName)
            print ('LOptionValue_02:',LOptionValue_02)
            LFileNameLOGjson = LUFile.ExtractFileName (LOptionValue_02.split([',', '('])[0])
        else:
            LFileNameLOGjson = LUFile.ExtractFileName (AFileNameLOGjson)
        #endif
        # print('LFileNameLOGjson:',LFileNameLOGjson)

        # установить имена log файлов в ini
        LOptionValue_01 = "('" + os.path.join (LDirectoryLOG, LFileNameLOG) + "',)"
        if LUos.GOSInfo.system == 'Windows':
            LOptionValue_01 = LOptionValue_01.replace ('\\', "\\\\")
        #endif
        if LUos.GOSInfo.system == 'Linux':
            raise 'Linux не поддерживается'
        #endif
        # print(LOptionValue_01)

        LINIFile.SetOption ('handler_FILE_01', LOptionName, LOptionValue_01)
        LOptionValue_02 = "('" + os.path.join (LDirectoryLOG, LFileNameLOGjson) + "',)"

        if LUos.GOSInfo.system == 'Windows':
            LOptionValue_02 = LOptionValue_02.replace ("\\", "\\\\")
        #endif
        if LUos.GOSInfo.system == 'Linux':
            raise 'Linux не поддерживается'
        #endif
        # print(LOptionValue_02)

        LINIFile.SetOption ('handler_FILE_02', LOptionName, LOptionValue_02)
        LINIFile.UpdateFileINI ()
    #endif

    if ADirectoryLOG == '':
        # log будет создан в текущем каталоге (по умолчанию)
        LDirectoryLOG = LUos.GetCurrentDir ()
    else:
        # log будет создан в ADirectoryLOG
        LDirectoryLOG = lyr.LUFile.ExpandFileName (ADirectoryLOG)
    #endif
    # print('LDirectoryLOG:',LDirectoryLOG)
    if not lyr.LUFile.DirectoryExists (LDirectoryLOG):
        lyr.LUFile.ForceDirectories(LDirectoryLOG)
    #endif

    print(LFileNameINI)
    logging.config.fileConfig (LFileNameINI, disable_existing_loggers=True, encoding=lyr.LUFile.cDefaultEncoding)
    # logging.config.fileConfig (LFileNameINI, disable_existing_loggers=True, encoding='cp1251')

    # создаем регистратор
    LResult = logging.getLogger (ALogerName)
    # установить форматер
    SetFormatterForLogger (LResult)

    return LResult
#endfunction

#-------------------------------------------------
# CreateLoggerBASIC
#-------------------------------------------------
def CreateLoggerBASIC (ALevel, AFileNameLOG: str, ALogerName: str) -> logging.Logger:
    """CreateTLoggingCONFIG"""
#beginfunction
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

#-------------------------------------------------
# LoggerTLogger
#-------------------------------------------------
def CreateTLogger (ALogerName: str) -> TLogger:
    """CreateTLogging"""
#beginfunction
    logging.setLoggerClass (TLogger)
    # создаем регистратор
    LResult = TLogger(ALogerName)
    SetFormatterForLogger (LResult)
    return LResult
#endfunction

#-------------------------------------------------
# FileMemoLog
#-------------------------------------------------
def CreateTFileMemoLog () -> TFileMemoLog:
    """CreateTFileMemoLog"""
#beginfunction
    LFileMemoLog = TFileMemoLog ()
    return LFileMemoLog
#endfunction

#-------------------------------------------------
# Инициализация системы logging
#-------------------------------------------------
GLoggerFILEINI = None
GLoggerCONFIG = None
LoggerTOOLS = None
LoggerAPPS = None
LoggerTLogger = None
FileMemoLog = None

def STARTLogging (T: TTypeSETUPLOG, ADirectoryLOG: str, AFileNameLOG: str, AFileNameLOGjson: str) -> None:
    """STARTLogging"""
#beginfunction
    global STATLogging
    STATLogging = False
    # print (sys._getframe (0).f_code.co_name, '...')

    # print (inspect.currentframe().f_code.co_name, '...')
    # print (inspect.stack () [0] [3], '...')
    # print (traceback.extract_stack () [-1].name, '...')

    global GLoggerFILEINI
    global GLoggerCONFIG
    global LoggerTOOLS
    global LoggerAPPS
    global LoggerTLogger
    global FileMemoLog

    AddLevelName ()

    match T:
        case TTypeSETUPLOG.tslCONFIG:
            GLoggerCONFIG = CreateLoggerCONFIG (CDefaultFileLogCONFIG, 'root', ADirectoryLOG, AFileNameLOG,
                                                AFileNameLOGjson)
        case TTypeSETUPLOG.tslYAML:
            GLoggerYAML = CreateLoggerYAML (CDefaultFileLogYAML, 'root', ADirectoryLOG, AFileNameLOG,
                                                AFileNameLOGjson)
        case TTypeSETUPLOG.tslINI:
            GLoggerFILEINI = CreateLoggerFILEINI (CDefaultFileLogINI, 'root', ADirectoryLOG, AFileNameLOG,
                                                  AFileNameLOGjson)
        case _:
            ...
    #endmatch

    #-------------------------------------------------
    # GLoggerBASIC = CreateLoggerBASIC (logging.DEBUG, 'LOG\\' + CDefaultFileLogFILEBASIC, 'root')
    # GLoggerBASIC = CreateLoggerBASIC (logging.DEBUG, '', 'root')
    #-------------------------------------------------

    #-------------------------------------------------
    # LoggerTOOLS
    #-------------------------------------------------
    CLoggerTOOLS = 'TOOLS__'
    LoggerTOOLS = logging.getLogger (CLoggerTOOLS)
    LoggerTOOLS.disabled = False
    # print('LoggerTOOLS' in vars () or 'LoggerTOOLS' in globals ())
    # print('LoggerTOOLS' in vars ())
    # print('LoggerTOOLS' in globals ())
    # if not ('LoggerTOOLS' in vars () or 'LoggerTOOLS' in globals ()):
    #     CLoggerTOOLS = 'TOOLS__'
    #     LoggerTOOLS = logging.getLogger (CLoggerTOOLS)
    # #endif

    #-------------------------------------------------
    # LoggerAPPS
    #-------------------------------------------------
    CLoggerAPPS = 'APPS___'
    LoggerAPPS = logging.getLogger(CLoggerAPPS)

    #-------------------------------------------------
    # LoggerTLogger
    #-------------------------------------------------
    CTLogger = 'TLOGGER'
    LoggerTLogger = CreateTLogger (CTLogger)

    #-------------------------------------------------
    # FileMemoLog
    #-------------------------------------------------
    FileMemoLog = CreateTFileMemoLog ()

    #-------------------------------------------------
    # Отключить журнал 'chardet.charsetprober'
    #-------------------------------------------------
    logger = logging.getLogger('chardet.charsetprober')
    logger.setLevel(logging.INFO)
    logger = logging.getLogger('chardet.universaldetector')
    logger.setLevel(logging.INFO)
    #-------------------------------------------------
    # Отключить журнал 'pytube.extract'
    #-------------------------------------------------
    logger = logging.getLogger('pytube.extract')
    logger.setLevel(logging.INFO)
    #-------------------------------------------------
    # Отключить журнал 'pytube.streams'
    #-------------------------------------------------
    logger = logging.getLogger('pytube.streams')
    logger.setLevel(logging.INFO)
    #-------------------------------------------------
    # Отключить журнал 'pytube.cipher'
    #-------------------------------------------------
    logger = logging.getLogger('pytube.cipher')
    logger.setLevel(logging.INFO)
    #-------------------------------------------------
    # Отключить журнал 'pytube.helpers'
    #-------------------------------------------------
    logger = logging.getLogger('pytube.helpers')
    logger.setLevel(logging.INFO)

    STATLogging = True
#endfunction

#-------------------------------------------------
# Выключить систему logging
#-------------------------------------------------
def STOPLogging () -> None:
    """STOPLogging"""
#beginfunction
    global STATLogging
    global LoggerTOOLS
    STATLogging = False
    # LoggerTOOLS.disabled = True# Выключить систему logging для логгирования
#endfunction

#-------------------------------------------------
# LoggerTOOLS_AddLevel
#-------------------------------------------------
def LoggerTOOLS_AddLevel (ALevel, Astr):
#beginfunction
    if STATLogging:
        try:
            LoggerTOOLS.log(ALevel, Astr)
        except:
            ...
        #endtry
    else:
        print("INFO: система не включена для записи логов")
    #endif
#endfunction

#-------------------------------------------------
# LoggerTOOLS_AddDebug
#-------------------------------------------------
def LoggerTOOLS_AddDebug (Astr):
#beginfunction
    if STATLogging:
        try:
            LoggerTOOLS.debug(Astr)
        except:
            ...
        #endtry
    else:
        print("INFO: система не включена для записи логов")
    #endif
#endfunction

#-------------------------------------------------
# LoggerTOOLS_AddError
#-------------------------------------------------
def LoggerTOOLS_AddError (Astr):
#beginfunction
    if STATLogging:
        try:
            LoggerTOOLS.error(Astr)
        except:
            ...
        #endtry
    else:
        print("INFO: система не включена для записи логов")
    #endif
#endfunction

#-------------------------------------------------
# LoggerAPPS_AddLevel
#-------------------------------------------------
#LULog.LoggerAPPS.log
def LoggerAPPS_AddLevel (ALevel, Astr):
#beginfunction
    if STATLogging:
        try:
            LoggerAPPS.log(ALevel, Astr)
        except:
            ...
        #endtry
    else:
        print("INFO: система не включена для записи логов")
    #endif
#endfunction

#-------------------------------------------------
# LoggerAPPS_AddInfo
#-------------------------------------------------
#LULog.LoggerAPPS.info
def LoggerAPPS_AddInfo (Astr):
#beginfunction
    if STATLogging:
        try:
            LoggerAPPS.info(Astr)
        except:
            ...
        #endtry
    else:
        print("INFO: система не включена для записи логов")
    #endif
#endfunction

#-------------------------------------------------
# LoggerAPPS_AddError
#-------------------------------------------------
#LULog.LoggerAPPS.error
def LoggerAPPS_AddError (Astr):
#beginfunction
    if STATLogging:
        try:
            LoggerAPPS.error(Astr)
        except:
            ...
        #endtry
    else:
        print("INFO: система не включена для записи логов")
    #endif
#endfunction

#-------------------------------------------------
# LoggerAPPS_AddDebug
#-------------------------------------------------
#LULog.LoggerAPPS.debug
def LoggerAPPS_AddDebug (Astr):
#beginfunction
    if STATLogging:
        try:
            LoggerAPPS.debug(Astr)
        except:
            ...
        #endtry
    else:
        print("INFO: система не включена для записи логов")
    #endif
#endfunction

#-------------------------------------------------
# main
#-------------------------------------------------
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
    STOPLogging ()
#endif

#endmodule
