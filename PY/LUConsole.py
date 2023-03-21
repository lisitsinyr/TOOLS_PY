"""LUConsole.py"""
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
     LUConsole.py

 =======================================================
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import sys
import enum

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
from colorama import Fore, Back, Style

#------------------------------------------
# БИБЛИОТЕКИ LU
#------------------------------------------

#------------------------------------------
# CONST
#------------------------------------------
sBEGIN_hex = '\x1b['
sBEGIN_Unicode = '\u001b'
sBEGIN_oct = '\33['
sBEGIN = sBEGIN_hex
sEND = 'm'
sRESET = sBEGIN_oct+'0'+sEND          # сброс к начальным значениям
sRESET_1 = sBEGIN_oct+'0'+';'+sEND      # вернуться к начальному стилю
sRESET_2 = sBEGIN_oct+sEND

sR = '\r'
sB = '\b' # символ возврата

sERASE_LINE = '\x1b[2K' # erase line command
sCURSOR_UP_ONE = '\033[K'

#{} — заменится на «Python 3»;

# \033[ 01; 03; 04; 07; '__'; '__' m

#--------------------------------------
# Изменения стиля (Styles)
#--------------------------------------
cS_BOLD       = '01' # Жирный
cS_02         = '02' # Блеклый
cS_ITALIC     = '03' # Курсив
cS_UNDERLINE  = '04' # Подчёркнутый
cS_05         = '05' # Мигание
cS_06         = '06'
cS_REVERSE    = '07' # Реверс
cS_08         = '08'
cS_09         = '09' # Зачёркнутый
@enum.unique
class cStyles(enum.Enum):
    """cStyles"""
    BOLD       = cS_BOLD
    ITALIC     = cS_ITALIC
    UNDERLINE  = cS_UNDERLINE
    REVERSE    = cS_REVERSE
#endclass
#--------------------------------------
cStylesList = [cStyles.BOLD, cStyles.ITALIC, cStyles.UNDERLINE, cStyles.REVERSE]

#--------------------------------------
# Изменения цвета шрифта
#--------------------------------------
cFG8_BLACK      = '30' # Чёрный
cFG8_RED        = '31' # Красный
cFG8_GREEN      = '32' # Зелёный
cFG8_YELLOW     = '33' # Жёлтый
cFG8_BLUE       = '34' # Синий
cFG8_MAGENTA    = '35' # Фиолетовый (пурпурный цвет)
cFG8_CYAN       = '36' # Бирюзовый (голубой цвет)
cFG8_WHITE      = '37' # Белый
@enum.unique
class cFG8(enum.Enum):
    """cFG8"""
    BLACK   = cFG8_BLACK
    RED     = cFG8_RED
    GREEN   = cFG8_GREEN
    YELLOW  = cFG8_YELLOW
    BLUE    = cFG8_BLUE
    MAGENTA = cFG8_MAGENTA
    CYAN    = cFG8_CYAN
    WHITE   = cFG8_WHITE
#endclass
#--------------------------------------
cFG8List = [cFG8.BLACK, cFG8.RED, cFG8.GREEN, cFG8.YELLOW, cFG8.BLUE, cFG8.MAGENTA, cFG8.CYAN, cFG8.WHITE]

#--------------------------------------
# Изменения цвета фона
#--------------------------------------
cBG8_BLACK      = '40' # Чёрный
cBG8_RED        = '41' # Красный
cBG8_GREEN      = '42' # Зелёный
cBG8_YELLOW     = '43' # Жёлтый
cBG8_BLUE       = '44' # Синий
cBG8_MAGENTA    = '45' # Фиолетовый (пурпурный цвет)
cBG8_CYAN       = '46' # Бирюзовый (голубой цвет)
cBG8_WHITE      = '47' # Белый
@enum.unique
class cBG8(enum.Enum):
    """cBG8"""
    BLACK   = cBG8_BLACK
    RED     = cBG8_RED
    GREEN   = cBG8_GREEN
    YELLOW  = cBG8_YELLOW
    BLUE    = cBG8_BLUE
    MAGENTA = cBG8_MAGENTA
    CYAN    = cBG8_CYAN
    WHITE   = cBG8_WHITE
#endclass
#--------------------------------------
cBG8List = [cBG8.BLACK, cBG8.RED, cBG8.GREEN, cBG8.YELLOW, cBG8.BLUE, cBG8.MAGENTA, cBG8.CYAN, cBG8.WHITE]

#--------------------------------------
# Избранные цвета 8
#--------------------------------------
# красный текст - для обозначения ошибок
# \033[ 01; 03; 04; 07; '__'; '__' m
ERROR_ESC = '\033['+'31'+'m'
ERROR_s = ''
ERROR_cFG8 = cFG8_RED
ERROR_cBG8 = ''
# жирный красный текст - для обозначения критических ошибок
ERROR_CRITICAL_ESC = '\033['+'01'+'31'+'m'
ERROR_CRITICAL_s = cS_BOLD
ERROR_CRITICAL_cFG8 = cFG8_RED
ERROR_CRITICAL_cBG8 = ''
# зеленый текст - успешное выполнение
SUCCESS_ESC = '\033['+'32'+'m'
SUCCESS_s = ''
SUCCESS_cFG8 = cFG8_GREEN
SUCCESS_sBG8 = ''
# красный курсив - текст ошибки
ERROR_TEXT_ESC = '\033['+'03'+'31'+'m'
ERROR_TEXT_s = cS_ITALIC
ERROR_TEXT_cFG8 = cFG8_RED
ERROR_TEXT_cBG8 = ''
# выделение основного, как будто жёлтым маркером
MARKER_ESC = '\033['+'43'+'m'
MARKER_s = ''
MARKER_cFG8 = ''
MARKER_cBG8 = cBG8_YELLOW
# жирный белый на черном
BOLD_ESC = '\033['+'01'+'31'+'40'+'m'
BOLD_s = cS_BOLD
BOLD_cFG8 = cFG8_WHITE
BOLD_cBG8 = cBG8_BLACK

#--------------------------------------
# Больше цветов: аж целых 256
# Совсем много цветов
# Этот формат не всегда поддерживается стандартными консолями.
#--------------------------------------
# Некоторые будут негодовать: "256 цветов и нет моего любимого терракотового, какой ужас!".
# Для таких ценителей существует формат, который уже поддерживает 24 битные цвета (3 канала RGB по 256 градаций).
# Для не ценителей поясню, что терракотовый кодируется как — (201, 100, 59) или #c9643b.
# Синтаксис в этом формате выглядит вот так:
# цвет текста
# \33[+38;2;⟨r⟩;⟨g⟩;⟨b⟩ m
# цвет фона
# \33[+48;2;⟨r⟩;⟨g⟩;⟨b⟩ m
#--------------------------------------
# \033[ 01; 03; 04; 07; 38;05;222; 48;05;22 m
#--------------------------------------
# Изменения цвета шрифта
#--------------------------------------
sFG256_BEGIN = '38;05;'
#--------------------------------------
# Изменения цвета фона
#--------------------------------------
sBG256_BEGIN = '48;05;'
#--------------------------------------
#--------------------------------------
# Избранные цвета 256
#--------------------------------------
sFG256_01 = '38;05;'+'15'
sBG256_01 = '48;05;'+'21'
sColor256_01 = sBEGIN_oct+cS_BOLD+';'+sFG256_01+';'+sBG256_01+sEND

#--------------------------------------
# colorama
#--------------------------------------
# список доступных фронтальных цветов
#--------------------------------------
FOREGROUND = [Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
#--------------------------------------
# список доступных фоновых цветов
#--------------------------------------
BACKGROUND = [Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE]
#
BRIGHTNESS = [Style.DIM, Style.NORMAL, Style.BRIGHT]

#-------------------------------------------------
# ISTerminal () -> bool:
#-------------------------------------------------
def ISTerminal () -> bool:
    """ISTerminal"""
#beginfunction
    return sys.stdout.isatty ()
#endfunction

#-------------------------------------------------
# GetTupleStr (ATuple:()):
#-------------------------------------------------
def GetTupleStr (ATuple:()):
    """GetTupleStr"""
#beginfunction
    LResult = ''
    i = 0
    j = 0
    if type(ATuple) is tuple:
        for r in ATuple:
            i = i + 1
            if r != '':
                j = j + 1
                if j == 1:
                    LResult = LResult + r
                else:
                    LResult = LResult + ';' + r
    else:
        if len (ATuple) > 0:
            LResult = LResult + ATuple
    return LResult
#endfunction

#-------------------------------------------------
# FormatColorStr (s, AStyles:()='', AFG8:str='', ABG8:str='', AFG256:str='', ABG256:str='', AESC:str=''):
#-------------------------------------------------
def FormatColorStr (s, **kwargs) -> str:
    """FormatColorStr"""
#beginfunction
    AStyles:() = kwargs.get('AStyles')
    AFG8:str = kwargs.get ('AFG8')
    ABG8:str = kwargs.get ('ABG8')
    AFG256:str = kwargs.get ('AFG256')
    ABG256:str = kwargs.get ('ABG256')
    AESC:str = kwargs.get ('AESC')

    LResult = ''
    if  AESC is not None:
        LResult = LResult + AESC + s + sRESET
    else:
        LStyles = GetTupleStr (AStyles)
        # --------------------------------------------
        if len(LStyles) > 0 \
                or AFG8 is not None or ABG8 is not None \
                or AFG256 is not None or ABG256 is not None:
            LResult = sBEGIN
        if len (LStyles) > 0:
            LResult = LResult + LStyles
        # --------------------------------------------
        if AFG8 is not None:
            if len (LStyles) > 0:
                LResult = LResult + ';' + AFG8
            else:
                LResult = LResult + AFG8
        if ABG8 is not None:
            if len (LStyles) > 0:
                LResult = LResult + ';' + ABG8
            else:
                LResult = LResult + AFG8
        # --------------------------------------------
        if AFG256 is not None:
            if len (LStyles) > 0:
                LResult = LResult + ';' + sFG256_BEGIN + AFG256
            else:
                LResult = LResult + sFG256_BEGIN +AFG256
        if ABG256 is not None:
            if len (LStyles) > 0:
                LResult = LResult + ';' + sBG256_BEGIN + ABG256
            else:
                LResult = LResult + sBG256_BEGIN + AFG256
        # --------------------------------------------
        if len (LResult) > 0:
            LResult = LResult + sEND + s + sRESET
        else:
            LResult = s

    return LResult
#endfunction

#-------------------------------------------------
# Write (s, AStyles:()='', AFG8:str='', ABG8:str='', AFG256:str='', ABG256:str='', AESC:str=''):
#-------------------------------------------------
def Write (s, **kwargs):
    """Write"""
#beginfunction
    _s = s
    if ISTerminal():
        sys.stdout.write (_s)
    else:
        if len(kwargs):
            _s = FormatColorStr(_s, **kwargs)
        #endif
        sys.stdout.write (_s)
    #endif
    sys.stdout.flush ()
#endfunction

#-------------------------------------------------
# WriteLN (s, AStyles:()='', AFG8:str='', ABG8:str='', AFG256:str='', ABG256:str='', AESC:str=''):
#-------------------------------------------------
def WriteLN (s, **kwargs):
    """WriteLN"""
#beginfunction
    Write (s, **kwargs)
    sys.stdout.write ('\n')
    sys.stdout.flush ()
#endfunction

#-------------------------------------------------
# ClearLine():
#-------------------------------------------------
def ClearLine():
    """ClearLine"""
#beginfunction
    sys.stdout.write(sCURSOR_UP_ONE)
    sys.stdout.write(sERASE_LINE+'\r')
#endfunction

#-------------------------------------------------
# ReadParam($Title,$Default)
#-------------------------------------------------
def ReadParam (ATitle: str, ADefault: str) -> str:
    """ReadParam"""
#beginfunction
    WriteLN ('Введите ('+ATitle+')['+ADefault+']: ', AStyles=cS_ITALIC, AFG8=cFG8_RED, ABG8=cBG8_WHITE)
    LReadParam: str = input ("")
    if LReadParam == "":
       LReadParam = ADefault
    #endif
    return LReadParam
#endfunction

#--------------------------------------------------------------------
# Pause(optional $prompt)
#--------------------------------------------------------------------
def Pause (Aprompt: str = ''):
    """Pause"""
#beginfunction
    if Aprompt == '':
        Aprompt="Press any key to continue "
    #endif
    if Aprompt != '':
        WriteLN (Aprompt, AStyles=cS_ITALIC, AFG8=cFG8_RED, ABG8=cBG8_WHITE)
    #endif
    x = sys.stdin.read (1)
#endfunction

#--------------------------------------------------------------------
# pause2(optional $delay, optional $prompt)
#--------------------------------------------------------------------
def pause2 (ADelay:int=0, Aprompt:str=''):
    """pause2"""
#beginfunction
    LDelay = ADelay
    LPrompt = Aprompt
    LLoop = 0
    LCounter = 0
    LInterval = 0.2
    LPause = -1
    if Aprompt == '':
        LPrompt = "Press any key to continue"
    #endif
    if LPrompt != '':
        WriteLN(LPrompt)
    #endif
    if LDelay > 0:
        LDelay = LDelay + 1
        while LPause == -1 and LDelay > 1.0 + LInterval:
            LDelay = LDelay - LInterval
            #LCounter = "[" + int(LDelay) + "]:"
            #Write (LCounter)
            #sleep (LInterval)
            #for loop in range (1, len(LCounter), 1):
            #    Write (chr(8)+" "+chr(8))
            #endfor
            #if kbhit():
                #LPause = sys.stdin.read(1)
            #endif
        #endwhile
    else:
        LPause = sys.stdin.read(1)
    #endif
#endfunction 

#------------------------------------------------------
# PasswdFromKbd(optional $Prompt)
#------------------------------------------------------
#def PasswdFromKbd(Prompt = ''):
##beginfunction
#    WriteLN ("w/n",  "")
#    WriteLN ("w+/n", "$Admin_Password_Desc")
#    PasswdFromKbd = fnGetM("*")
#endfunction

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
