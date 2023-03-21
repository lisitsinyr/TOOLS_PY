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

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------

#------------------------------------------
# БИБЛИОТЕКА LU 
#------------------------------------------
import LUFile
import LUConsole
import LUDateTime
import LUStrDecode

# ===========================================================================
# CONST
# ===========================================================================
"""CONST"""
ctlsNone = ' '
ctlsBegin = '>'
ctlsEnd = '<'
ctlsInfo = 'I'
ctlsError = 'E'
ctlsWarning = 'W'
ctlsProcess = 'P'
ctlsText = ''

TruncLog = 1
LogPath = ''
Log = 30
LogDir = ''
LogFile = ''

# ===========================================================================
# type
# ===========================================================================
# class syntax
@enum.unique
class TTypeLogString(enum.Enum):
    """TTypeLogString"""
    tlsNone = ' '
    tlsBegin = '>'
    tlsEnd = '<'
    tlsInfo = 'I'
    tlsError = 'E'
    tlsWarning = 'W'
    tlsProcess = 'P'
    tlsText = ''
    @classmethod
    def Empty(cls):
        ...
#endclass

# class syntax
@enum.unique
class TTypeLogCODE (enum.Enum):
    """TTypeLogCODE"""
    tlcOEM = 0
    tlcANSI = 1
    @classmethod
    def Empty (cls):
        ...
#endclass

# class syntax
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
    # @property TruncateDays
    #--------------------------------------------------
    @property
    # getter
    def TruncateDays (self) -> int:
    #beginfunction
        return self.__FTruncateDays
    #endfunction
    @TruncateDays.setter
    def TruncateDays (self, Value: int):
    #beginfunction
        self.__FTruncateDays = Value
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

    def _Execute (self, T: TTypeLogString):
        """_Execute"""
    #beginfunction
        # StandardOut
        if self.__FStandardOut:                 # and isConsole:
            self.__FLogStrings.clear()
            self.__FLogStrings.append(self.__FLogStringAnsi)
            for s in self.__FLogStrings:
                _s = self._LogDateStr(False)+' '+T.value+' '+s
                # LUConsole.WriteLN (_s, AStyles=('1','3'))
                LUConsole.WriteLN (_s, AStyles = (LUConsole.cS_BOLD, LUConsole.cS_ITALIC))
                # LUConsole.WriteLN (_s)
            #endfor
        #endif

        # Filename
        if self.__FFileName != '':
            s = LUFile.ExpandFileName(self.__FFileName)
            s = LUFile.ExtractFileDir (s)
            if len(s) > 0:
                if not LUFile.DirectoryExists(s):
                    LUFile.ForceDirectories (s)
                #endif
            #endif

            self.__FLogStrings.clear()
            self.__FLogStrings.append(self.__FLogStringAnsi)

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
                _s = self._LogDateStr (False) + ' ' + T.value + ' ' + s
                try:
                    # _s = str (s.encode ('utf-8'), 'cp1251')
                    # _s = str (s.encode ('cp1251'), 'cp1251')
                    _s = str (_s.encode (self.__FLogCODE), self.__FLogCODE)
                    LFile.write(_s + '\n')
                except:
                    print ('Неправильная кодировка журнала=',LEncoding, s)
            #endfor
            LFile.flush()
            LFile.close()
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

    def _SetMemoLog (self, Value):                             #TMemo
        """_SetMemoLog"""
    #beginfunction
        ...
    #endfunction

    @staticmethod
    def _LogDateStr (ATimeOnly: bool) -> str:
        """LogDateStr"""
    #beginfunction
        LToday: datetime = LUDateTime.Now ()
        if ATimeOnly:
            LResult = '               ' + LUDateTime.DateTimeStr (ATimeOnly, LToday, LUDateTime.cFormatDateTimeLog01)
        else:
            LResult = LUDateTime.DateTimeStr (ATimeOnly, LToday, LUDateTime.cFormatDateTimeLog01)
        #endif
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

    def AddFile (self, AFileName: str, ATabCount: int):
        """AddFile"""
    #beginfunction
        if LUFile.FileExists (AFileName):
            # Открыть для чтения
            LEncoding = LUFile.GetFileEncoding (self.__FFileName)
            LFile = open (self.__FFileName, 'r', encoding = LEncoding)
            try:
                # работа с файлом
                for s in LFile:
                    self.SetLogString(TTypeLogString.tlsInfo, ATabCount, s)

                    #file.next()    возвращает следующую строку файла
                #endfor
            finally:
                LFile.close ()
        #endif
        ...
    #endfunction

    #--------------------------------------------------
    #
    #--------------------------------------------------
    def SetLogString (self, T: TTypeLogString, TabCount: int, Value: str):
        """SetLogString"""
    #beginfunction
        if T != TTypeLogString.tlsText:
            s = ' '*TabCount*2 + Value
        else:
            s = Value
        self.__FLogStringOEM = s
        self.__FLogStringAnsi = s
        if self.LogEnabled:
            self._Execute(T)
        ...
    #endfunction


    def _GetLogSave (self, Filename: str) -> list:  #TStringList
        """_GetLogSave"""
        ...

    def _GetLogSaveCurrent (self) -> list:         #TStringList;
        """_GetLogSaveCurrent"""
        LResult = self._GetLogSave (self.__FFileName)
        return LResult

#endclass

"""
procedure TFileMemoLog.TruncateMemo (ATS: TStrings);
var
    Today, LogDay: TDateTime;
    { Delta: TDateTime; }
    s: string;
    Save: Char;
    i: Longint;
    x: Longint;
    Stop: Boolean;
    yy, mm, dd, hh, nn, ss, ms: word;
begin
    Save := FormatSettings.DateSeparator;
    FormatSettings.DateSeparator := '/';
    Today := Now;
    s := DateTimeToStr (Today);
    i := 0;
    Stop := False;
    while (i < ATS.Count) and (not Stop) do
    begin
        s := ExtractWordNew (1, ATS.Strings[i], [' ']) + ' ' +
            ExtractWordNew (2, ATS.Strings[i], [' ']);
        s := ReplaceStr (s, '.', FormatSettings.DateSeparator);
        try
            ms := StrToInt (ExtractWordNew(2, ATS.Strings[i], [' ']));
        except
            ms := 0;
        end;
        try
            LogDay := StrToDateTime (s) + EncodeTime (0, 0, 0, ms);
        except
            LogDay := 0;
        end;
        if LogDay <> 0 then
        begin
            DecodeDate (Today - TruncateDays, yy, mm, dd);
            DecodeTime (Today - TruncateDays, hh, nn, ss, ms);
            { Delta := EncodeDate(yy,mm,dd)+EncodeTime(hh,nn,ss,ms); }
            x := Trunc (Today) - Trunc (LogDay);
            if x > TruncateDays - 1 then
                { if LogDay < Delta then }
                ATS.Delete (i)
            else
            begin
                Stop := True;
                i := ATS.Count;
            end;
        end else begin
            ATS.Delete (i);
        end;
    end;
    FormatSettings.DateSeparator := Save;
end;
"""

"""
function TFileMemoLog.GetLogSave (Filename: string): TStringList;
var
    TSIn: TStringList;
    ProcessEnd: Boolean;
    IB, IE, i, J, IP: Integer;
    Ch: string;

begin
    FLogSave.Clear;
    if FileExists (Filename) then
    begin
        TSIn := TStringList.Create;
        TSIn.LoadFromFile (Filename);
        if TSIn.Count > 0 then
        begin
            i := 0;
            IB := 0;
            IP := 0;
            Ch := ExtractWordNew (4, TSIn.Strings[i], [' ']);
            ProcessEnd := False;
            while not ProcessEnd do
            begin
                if Ch = StlsBegin then
                begin
                    if IB < i then
                    begin
                        { нет символа конца }
                        Ch := StlsEnd;
                        Dec (i);
                    end else begin
                        IB := i;
                        IP := 0;
                    end;
                end;
                if Ch = StlsEnd then
                begin
                    if (i < TSIn.Count) then
                        IE := i
                    else
                    begin
                        IE := i - 1;
                        ProcessEnd := True;
                    end;
                    { Copy strings }
                    if IP > 0 then
                        for J := IB to IE do
                            FLogSave.Add (TSIn.Strings[J]);
                    IB := IE + 1;
                end;
                if Ch = ctlsError then
                    Inc (IP);
                if Ch = ctlsWarning then
                    Inc (IP);
                if Ch = ctlsProcess then
                    Inc (IP);
                { Next string }
                Inc (i);
                if (i < TSIn.Count) then
                    Ch := ExtractWordNew (4, TSIn.Strings[i], [' '])
                else
                    Ch := ctlsEnd;
            end;
        end;
        TSIn.Free;
    end;
    Result := FLogSave;
end;
"""
#endclass

# строка формата сообщения
strfmt = '[%(asctime)s: %(levelname)s] %(message)s'
strfmt = '[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s'
# строка формата времени
datefmt = '%Y-%m-%d %H:%M:%S'

#----------------------------------------------
# TLogging
#----------------------------------------------

class TLogging (logging.Logger):
    """"""
    luClassName = "TLogging"
    
    #--------------------------------------------------
    # constructor
    #--------------------------------------------------
    def __init__(self, ALogerName: str):
        """Constructor"""
    #beginfunction
        super().__init__(ALogerName)
        self.__FFileName: str = ''
        self.__FStandardOut: bool = True

        # self.__FLogger: logging.Logger = logging.getLogger (ALogerName)

        self.__FHandlerConsole: logging.StreamHandler = logging.StreamHandler (stream = sys.stdout)
        self.__FFormaterConsole: logging.Formatter = logging.Formatter (fmt = strfmt, datefmt=datefmt, style='%')
        self.__FHandlerConsole.setFormatter (self.__FFormaterConsole)
        self.addHandler (self.__FHandlerConsole)

        self.__FHandlerFile: logging.StreamHandler = logging.StreamHandler (stream = sys.stdout)
        self.addHandler (self.__FHandlerFile)

        self.setLevel (logging.DEBUG)
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
        # self.__FLogger.setLevel (logging.DEBUG)
        self.setLevel (Value)
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

    """
    DEBUG — уровень отладочной информации, зачастую помогает при разработке приложения на машине программиста.
    INFO — уровень вспомогательной информации о ходе работы приложения/скрипта.
    WARNING — уровень предупреждения. Например, мы можем предупреждать о том, что та или иная функция будет удалена в будущих версиях вашего приложения.
    ERROR — с таким уровнем разработчики пишут логи с ошибками, например, о том, что внешний сервис недоступен.
    CRITICAL — уровень сообщений после которых работа приложения продолжаться не может.
    
    logger.setLevel(logging.DEBUG)
    
    logger.debug('debug')
    logger.info('info')
    logger.warning('warning')
    logger.error('error')
    logger.critical('critical')
    
    try:
        1/0
    except :
        logger.exception('exception')
        
    Handler
        Задача класса Handler и его потомков обрабатывать запись сообщений/логов. Т.е. Handler отвечает за то куда будут записаны сообщения. В базовом наборе logging предоставляет ряд готовых классов-обработчиков:
    SteamHandler — запись в поток, например, stdout или stderr.
    FileHandler — запись в файл, класс имеет множество производных классов с различной функциональностью (ротация файлов логов по размеру, времени и т.д.)
    SocketHandler — запись сообщений в сокет по TCP
    DatagramHandler — запись сообщений в сокет по UDP
    SysLogHandler — запись в syslog
    HTTPHandler — запись по HTTP
    
    StreamHandler
    FileHandler
    NullHandler
    WatchedFileHandler
    BaseRotatingHandler
    RotatingFileHandler
    TimedRotatingFileHandler
    SocketHandler
    DatagramHandler
    SysLogHandler
    NTEventLogHandler
    SMTPHandler
    MemoryHandler
    HTTPHandler
    QueueHandler
    QueueListener
    
    def filter_python(record: LogRecord) -> bool:
        return record.getMessage().find('python') != -1
    
    # Logger
    logger = logging.getLogger(__name__)
    
    logger.setLevel(logging.DEBUG)
    logger.setLevel(logging.INFO)
    
    # Handler
    handler = StreamHandler(stream=sys.stdout)
    
    # Formatter
    handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
    
    # Filter
    logger.addFilter(filter_python)
    
    logger.addHandler(handler)

    logger.debug('debug information')
    
    
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
    Официальная документация рекомендует конфигурировать logging через python-словарь. Для этого необходимо вызвать функцию logging.config.dictConfig и передать ей специальный словарь. Схема словаря описана здесь. Я лишь вкратце пробегусь по основным ключам:

    version — ключ указывает версию конфига, рекомендуется наличие этого ключа со значением 1, нужно для обратной совместимости в случае, если в будущем появятся новые версии конфигов.
    disable_existing_loggers — запрещает или разрешает настройки для существующих логеров (на момент запуска), по умолчанию равен True
    formatters — настройки форматов логов
    handlers — настройки для обработчиков логов
    loggers — настройки существующих логеров
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
    LOGGING_CONFIG['loggers'].update({
      'my_package': {
            'handlers': ['stream_handler'],
            'level': 'DEBUG',
            'propagate': False
        }
    })
    
    # Отправляем логи в Telegram
    
        
    """
#endclass

#-------------------------------------------------
# Фунциональное исполнение
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
                s = LUDateTime.DateTimeStr (False, LToday, LUDateTime.cFormatDateTimeLog03)
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

def CreateTFileMemoLog (*args, **kwargs) -> TFileMemoLog:
    """CreateTFileMemoLog"""
#beginfunction
    return TFileMemoLog ()
#endfunction

def CreateTLogging (*args, **kwargs) -> TLogging:
    """CreateTLogging"""
#beginfunction
    return TLogging('LOGER')
#endfunction

GFileMemoLog = CreateTFileMemoLog ()
GLogging = CreateTLogging ()

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
