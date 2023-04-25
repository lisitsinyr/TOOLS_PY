"""LUParserARG.py"""
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
     LUParserARG.py

 =======================================================
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import sys
import argparse
import logging

# re - Regular expression operations
import re

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------

#------------------------------------------
# БИБЛИОТЕКА LU
#------------------------------------------
# from LULog import LULogger
import LULog

#------------------------------------------
# Разбор аргументов
#------------------------------------------
cSwitchChars = ('-', '/')

class TArgParser (argparse.ArgumentParser):
    """TArgParser"""
    luClassName = 'TArgParser'

    #--------------------------------------------------
    # constructor
    #--------------------------------------------------
    def __init__ (self, **kwargs):
        """ Constructor """
    #beginfunction
        super ().__init__ (**kwargs)
        self.__FArgs: argparse.Namespace = None
        self.__FArgsUnknown: argparse.Namespace = None
        self.__FArgsDICT = {}
        ...
    #endfunction

    #--------------------------------------------------
    # destructor
    #--------------------------------------------------
    def __del__ (self):
        """ destructor """
    #beginfunction
        LClassName = self.__class__.__name__
        s = '{} уничтожен'.format (LClassName)
        # LULog.LoggerTOOLS.log (LULog.DEBUGTEXT, s)
        print (s)
    #endfunction

    #--------------------------------------------------
    # @property ArgParser
    #--------------------------------------------------
    # getter
    @property
    def ArgParser(self):
    #beginfunction
        return self
    #endfunction

    #--------------------------------------------------
    # @property ArgsDICT
    #--------------------------------------------------
    @property
    # getter
    def ArgsDICT (self):
    #beginfunction
        return self.__FArgsDICT
    #endfunction
    @ArgsDICT.setter
    def ArgsDICT (self, Value):
    #beginfunction
        self.__FArgsDICT = Value
    #endfunction

    #--------------------------------------------------
    # @property Args
    #--------------------------------------------------
    @property
    # getter
    def Args (self) -> argparse.Namespace:
    #beginfunction
        return self.__FArgs
    #endfunction
    @Args.setter
    def Args (self, Value: argparse.Namespace):
    #beginfunction
        self.__FArgs = Value
    #endfunction

    #--------------------------------------------------
    # @property ArgsUnknown
    #--------------------------------------------------
    @property
    # getter
    def ArgsUnknown (self) -> argparse.Namespace:
    #beginfunction
        return self.__FArgsUnknown
    #endfunction
    @ArgsUnknown.setter
    def ArgsUnknown (self, Value: argparse.Namespace):
    #beginfunction
        self.__FArgsUnknown = Value
    #endfunction

    def Clear (self):
    #beginfunction
        ...
    #endfunction

    def ReadARGS (self, AARGS: dict):
        def GetARG (AARGName, AARGValue):
        #beginfunction
            LResult = AARGS.get (AARGName).get (AARGValue)
            # try:
            #     LResult = AARGS [AARGName] [AARGValue]
            # except:
            #     LResult = None
            # #endtry
            return LResult
        #endfunction

    #beginfunction
        for name, value in AARGS.items ():
            # print (f"{name}={value}")
            LArg = self.add_argument (GetARG (name, 'name'),
                                      dest = GetARG (name, 'dest'),
                                      type = GetARG (name, 'type'),
                                      default = GetARG (name, 'default'),
                                      help = GetARG (name, 'help'),
                                      action = GetARG (name, 'action'),
                                      choices = GetARG (name, 'choices')
                                      )
            print (LArg)
        #endfor

        # GArgParser.Args = GArgParser.ArgParser.parse_args (['-ld', '1'], namespace = C)

        # self.Args = self.ArgParser.parse_args ()
        self.Args, self.ArgsUnknown = self.parse_known_args ()
        print (self.Args)

        self.ArgsDICT = vars (self.Args)
        print (self.ArgsDICT)

        # for item in self.Args:
        #     ...
        # GArgParser.ArgsDICT = {'-ld': GArgParser.Args.ld, '-lf': GArgParser.Args.lf,
        #                    '-lfj': GArgParser.Args.lfj, '-ini': GArgParser.Args.ini}

    #endfunction
#endclass

"""
--------------------------------------
ArgumentParser objects
--------------------------------------
class argparse.ArgumentParser(prog=None, usage=None, description=None,
    epilog=None, parents=[], formatter_class=argparse.HelpFormatter,
    prefix_chars='-', fromfile_prefix_chars=None, argument_default=None,
    conflict_handler='error', add_help=True, allow_abbrev=True, exit_on_error=True)

    prog - имя программы (по умолчанию: os.path.basename(sys.argv[0]))
    usage - Строка, описывающая использование программы (по умолчанию: генерируется из аргументов, добавленных в парсер)
    description - текст для отображения перед аргументом help (по умолчанию без текста)
    epilog - текст для отображения после справки аргумента (по умолчанию без текста)
    parents - список объектов ArgumentParser, чьи аргументы также должны быть включены
    formatter_class - класс для настройки вывода справки
    prefix_chars - набор символов, которые предшествуют необязательным аргументам (по умолчанию: «-»).
    fromfile_prefix_chars - набор символов, которые префиксируют файлы,
        из которых должны быть прочитаны дополнительные аргументы (по умолчанию: нет)
    argument_default - глобальное значение по умолчанию для аргументов (по умолчанию: None)
    conflict_handler - стратегия разрешения конфликтующих опций (обычно ненужных)
    add_help - добавить параметр -h/--help в парсер (по умолчанию: True)
    allow_abbrev - позволяет сокращать длинные параметры, если аббревиатура недвусмысленна. (по умолчанию: Истина)
    exit_on_error - определяет, завершается ли ArgumentParser с информацией об ошибке при возникновении ошибки.
        (по умолчанию: Истина)
"""

"""
--------------------------------------
The add_argument() method
ArgumentParser.add_argument(name or flags...[, action][, nargs]
    [, const][, default][, type][, choices][, required][, help][, metavar][, dest])
--------------------------------------
    name or flags - либо имя, либо список строк параметров, например. foo или -f, --foo.
    action - основной тип действия, которое необходимо предпринять, когда этот аргумент встречается в командной строке.
        'store', 'store_const', 'store_true', 'append', 'append_const', 'count', 'help', 'version'
    nargs - количество аргументов командной строки, которые следует использовать.
        int, '?', '*', '+', or argparse.REMAINDER
    const - постоянное значение, необходимое для выбора некоторых действий и nargs.
    default - значение, создаваемое, если аргумент отсутствует в командной строке и если он
        отсутствует в объекте пространства имен. Defaults to None.
    type - Тип, в который должен быть преобразован аргумент командной строки.
        int, float, argparse.FileType('w'), or callable function
    choices - последовательность допустимых значений аргумента.
        ['foo', 'bar'], range(1, 10), or Container instance
    required - можно ли опустить параметр командной строки (только необязательные параметры).
        True or False
    help - Краткое описание того, что делает аргумент.
    metavar - имя аргумента в сообщениях об использовании.
    dest - имя атрибута, который будет добавлен к объекту, возвращаемому функцией parse_args().
    
    LArg = GArgParser.add_argument (
        '-ld', dest='ld',
        type=str, default='',
        help = 'log dir',
        
        action='store', required=True,
        # action='store_const', const=True
        # action='store_true',
        # action='store_false',

        nargs = '+',
        # nargs = '?', const='',

        # choices=[],
        metavar = 'LDM'
    )
"""

"""
--------------------------------------
The parse_args() method
--------------------------------------
ArgumentParser.parse_args(args=None, namespace=None)
    args - Список строк для разбора. Значение по умолчанию берется из sys.argv.
    namespace - Объект для получения атрибутов. По умолчанию используется новый пустой объект пространства имен.
----------------------------------
"""

""" Работа со параметрами программы """

def __GetCmdLineArg (ASwitch: str, ASwitchChars: (), AIgnoreCase: bool) -> str:
    """__GetCmdLineArg"""
#beginfunction
    i = 0
    for s in sys.argv:
        i = i + 1
        if len(ASwitchChars) == 0 or ((s[0] in ASwitchChars) and (len(s) > 1)):
            s = re.split('|'.join(ASwitchChars), s)[1]
            if AIgnoreCase:
                if s.upper() == ASwitch.upper():
                    if i < len(sys.argv):
                        s = sys.argv[i]
                        if s[0] in ASwitchChars:
                            return ''
                        else:
                            return s
                        #endif
                    #endif
                #endif
            else:
                if s == ASwitch:
                    i = i + 1
                    if i <= len(sys.argv):
                        s = sys.argv[i]
                        if s[0] in ASwitchChars:
                            return ''
                        else:
                            return s
                        #endif
                    #endif
                #endif
            #endif
    #endfor
    return ''
#endfunction

def FindCmdLineSwitch (ASwitch: str, ASwitchChars: (), AIgnoreCase: bool) -> bool:
    """FindCmdLineSwitch"""
#beginfunction
    i = 0
    for s in sys.argv:
        i = i + 1
        if len(ASwitchChars) == 0 or ((s[0] in ASwitchChars) and (len(s) > 1)):
            s = re.split('|'.join(ASwitchChars), s)[1]
            if AIgnoreCase:
                if s.upper() == ASwitch.upper():
                    return True
                #endif
            else:
                if s == ASwitch:
                    return True
                #endif
            #endif
        #endif
    #endfor
    return False
#endfunction

#---------------------------------------------------------
# GetParam (AParamName: str, ADefaultValue: str) -> str:
#---------------------------------------------------------
def GetParam (AParamName: str, ADefaultValue: str) -> str:
    """GetParam"""
#beginfunction
    LResult = ADefaultValue
    if FindCmdLineSwitch (AParamName, cSwitchChars, True):
        LParamValue: str = __GetCmdLineArg (AParamName, cSwitchChars, True)
        LResult = LParamValue
    #endif
    return LResult
#endfunction

def CreateTArgParser (AProg: str, ADescrption: str) -> TArgParser:
    """CreateTArgParser"""
#beginfunction
    LResult = TArgParser (prog = AProg, description=ADescrption, prefix_chars='-/',
                          usage = None, epilog = None, parents = [], formatter_class = argparse.HelpFormatter,
                          fromfile_prefix_chars = None, argument_default = None,
                          conflict_handler = 'error', add_help = True, allow_abbrev = True, exit_on_error = True)
    return LResult
#endfunction

GArgParser = CreateTArgParser ('LUArgParser', 'Параметры')

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
