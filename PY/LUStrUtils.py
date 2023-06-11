"""LUStrUtils.py"""
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
     LUStrUtils.py

 =======================================================
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import string
import logging

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------

#------------------------------------------
# БИБЛИОТЕКИ LU
#------------------------------------------

#---------------------------------------------------------------
#
#---------------------------------------------------------------

CRLFd = chr(13)+chr(10)
CRLFx = '\x0d'+'\x0a'
CRLF = '\r'+'\n'
"""
\n  Newline
\r  Carriage Return
\r\n    Carriage Return + Line Feed
\v or \x0b  Line Tabulation
\f or \x0c  Form Feed
\x1c    File Separator
\x1d    Group Separator
\x1e    Record Separator
\x85    Next Line (C1 Control Code)
\u2028  Unicode Line Separator
\u2029  Unicode Paragraph Separator
"""

#---------------------------------------------------------------
#
#---------------------------------------------------------------
TSysCharSet = ()
TCharSet = ()

"""
(vi) Коллекции литералов: коллекции литералов в python включают список, кортеж, словарь и наборы.
Список []:
    это список элементов, представленных в квадратных скобках с запятыми между ними.
    Эти переменные могут иметь любой тип данных и также могут быть изменены.
Кортеж ():
    это также список элементов или значений, разделенных запятыми, в круглых скобках.
    Значения могут быть любого типа данных, но не могут быть изменены.
Словарь {}:
    это неупорядоченный набор пар ключ-значение.
Set {}:
    это неупорядоченный набор элементов в фигурных скобках ‘{}’.
"""

"""
String Operators
    + Operator
    * Operator
    in Operator
Built-in String Functions    
    chr()   Converts an integer to a character
    ord()   Converts a character to an integer
    len()   Returns the length of a string
    str()   Returns a string representation of an object
String Indexing
     0  1  2  3  4  5
    -6 -5 -4 -3 -2 -1
String Slicing (Нарезка строк)
    s[2:5]
Specifying a Stride in a String Slice (Указание шага в фрагменте строки)
    [0:6:2]
Interpolating Variables Into a String (Интерполяция переменных в строку)
    f'A dog says {var}!'
Modifying Strings (Изменение строк)
    s = 'foobar'
    s[3] = 'x'              не правильно
    s = s[:3] + 'x' + s[4:] правильно
    s = s.replace('b', 'x') правильно
Built-in String Methods
    Case Conversion
        s.capitalize() 
            returns a copy of s with the first character converted to uppercase and all other characters converted to lowercase:
        s.lower() 
            returns a copy of s with all alphabetic characters converted to lowercase:
        s.swapcase() 
            returns a copy of s with uppercase alphabetic characters converted to lowercase and vice versa:
        s.title() 
            returns a copy of s in which the first letter of each word is converted to uppercase and remaining letters are lowercase:
        s.upper() 
            returns a copy of s with all alphabetic characters converted to uppercase:
    Find and Replace
        s.count(<sub>[, <start>[, <end>]]) 
            returns the number of non-overlapping occurrences of substring <sub> in s:
        s.endswith(<suffix>[, <start>[, <end>]]) 
            returns True if s ends with the specified <suffix> and False otherwise:
        s.find(<sub>[, <start>[, <end>]]) 
            You can use .find() to see if a Python string contains a particular substring. s.find(<sub>) returns the lowest index in s where substring <sub> is found:        
        s.index(<sub>[, <start>[, <end>]])
            This method is identical to .find(), except that it raises an exception if <sub> is not found rather than returning -1:
        s.rfind(<sub>[, <start>[, <end>]])
            returns the highest index in s where substring <sub> is found:
        s.rindex(<sub>[, <start>[, <end>]])
            This method is identical to .rfind(), except that it raises an exception if <sub> is not found rather than returning -1:
        s.startswith(<prefix>[, <start>[, <end>]])
            When you use the Python .startswith() method, s.startswith(<suffix>) returns True if s starts with the specified <suffix> and False otherwise:
    Character Classification
        s.isalnum() 
            returns True if s is nonempty and all its characters are alphanumeric (either a letter or a number), and False
        s.isalpha() 
            returns True if s is nonempty and all its characters are alphabetic, and False otherwise:
        s.isdigit()
            You can use the .isdigit() Python method to check if your string is made of only digits. s.isdigit() returns True if s is nonempty and all its characters are numeric digits, and False otherwise:
        s.isidentifier() 
            returns True if s is a valid Python identifier according to the language definition, and False otherwise:
        s.islower()
            returns True if s is nonempty and all the alphabetic characters it contains are lowercase, and False otherwise. Non-alphabetic characters are ignored:
        s.isprintable() 
            returns True if s is empty or all the alphabetic characters it contains are printable. It returns False if s contains at least one non-printable character. Non-alphabetic characters are ignored:
        s.isspace()
            returns True if s is nonempty and all characters are whitespace characters, and False otherwise.
        s.istitle() returns True if s is nonempty, the first alphabetic character of each word is uppercase, and all other alphabetic characters in each word are lowercase. It returns False otherwise:
        s.isupper() returns True if s is nonempty and all the alphabetic characters it contains are uppercase, and False otherwise. Non-alphabetic characters are ignored:
    String Formatting
        s.center(<width>[, <fill>])
            returns a string consisting of s centered in a field of width <width>. By default, padding consists of the ASCII space character:
        s.expandtabs(tabsize=8)
            replaces each tab character ('\t') with spaces. By default, spaces are filled in assuming a tab stop at every eighth column:
        s.ljust(<width>[, <fill>])
            returns a string consisting of s left-justified in a field of width <width>. By default, padding consists of the ASCII space character:
        s.lstrip([<chars>])
            returns a copy of s with any whitespace characters removed from the left end:
        s.replace(<old>, <new>[, <count>])
            In Python, to remove a character from a string, you can use the Python string .replace() method. s.replace(<old>, <new>) returns a copy of s with all occurrences of substring <old> replaced by <new>:
        s.rjust(<width>[, <fill>])
            returns a string consisting of s right-justified in a field of width <width>. By default, padding consists of the ASCII space character:
        s.rstrip([<chars>])
            returns a copy of s with any whitespace characters removed from the right end:
        s.strip([<chars>])
             is essentially equivalent to invoking s.lstrip() and s.rstrip() in succession. Without the <chars> argument, it removes leading and trailing whitespace:
        s.zfill(<width>)
            returns a copy of s left-padded with '0' characters to the specified <width>:
    Converting Between Strings and Lists
        s.join(<iterable>)
            returns the string that results from concatenating the objects in <iterable> separated by s.
        s.partition(<sep>)
            splits s at the first occurrence of string <sep>. The return value is a three-part tuple consisting of:
        s.rpartition(<sep>)
            functions exactly like s.partition(<sep>), except that s is split at the last occurrence of <sep> instead of the first occurrence:
        s.rsplit(sep=None, maxsplit=-1)
            Without arguments, s.rsplit() splits s into substrings delimited by any sequence of whitespace and returns the substrings as a list:
        s.split(sep=None, maxsplit=-1)
             behaves exactly like s.rsplit(), except that if <maxsplit> is specified, splits are counted from the left end of s rather than the right end:
        s.splitlines([<keepends>])
            splits s up into lines and returns them in a list. Any of the following characters or character sequences is considered to constitute a line boundary:
bytes Objects
    Defining a Literal bytes Object
        b = b'foo bar baz'
        type(b)
    The 'r' prefix may be used on a bytes literal to disable processing of escape sequences, as with strings:
        b = rb'foo\xddbar'
        >>> b
        b'foo\\xddbar'
    Defining a bytes Object With the Built-in bytes() Function
        bytes(<s>, <encoding>)
            converts string <s> to a bytes object, using str.encode() according to the specified <encoding>
        bytes(<size>)
            defines a bytes object of the specified <size>, which must be a positive integer. The resulting bytes object is initialized to null (0x00) bytes:
        bytes(<iterable>)
            defines a bytes object from the sequence of integers generated by <iterable>. <iterable> must be an iterable that generates a sequence of integers n in the range 0 ≤ n ≤ 255:
    Operations on bytes Objects
        The in and not in operators:
        The concatenation (+) and replication (*) operators:
        Indexing and slicing:
            >>> b = b'abcde'
            >>> b[2]
            99
            >>> b[1:3]
            b'bc'
        Built-in functions:
            len(b)
            min(b)
            max(b)
        bytes.fromhex(<s>)
            returns the bytes object that results from converting each pair of hexadecimal digits in <s> to the corresponding byte value. The hexadecimal digit pairs in <s> may optionally be separated by whitespace, which is ignored:
        b.hex()
            returns the result of converting bytes object b into a string of hexadecimal digit pairs. That is, it does the reverse of .fromhex():
    bytearray Objects
        There is no dedicated syntax built into Python for defining a bytearray literal, like the 'b' prefix that may be used to define a bytes object. A bytearray object is always created using the bytearray() built-in function:
            ba = bytearray('foo.bar.baz', 'UTF-8')
            bytearray(6)
                bytearray(b'\x00\x00\x00\x00\x00\x00')
            bytearray([100, 102, 104, 106, 108])
                bytearray(b'dfhjl')
        bytearray objects are mutable. You can modify the contents of a bytearray object using indexing and slicing:
                      
"""
# Алфавиты: все заглавные (A-Z) и строчные (a-z) алфавиты.

# Цифры: все цифры 0-9.
cDigitChars = tuple(string.digits)
cBrackets = ('(', ')', '[', ']', '{', '}')
# Специальные символы (пунктуация)  ” ‘ l ; : ! ~ @ # $ % ^ ` & * ( ) _ + – = { } [ ] \ .
cWordDelimitersFull = tuple(string.punctuation)
cWordDelimiters = ('|', ';')
cWordDelimiter = '|'

#---------------------------------------------------------------
#
#---------------------------------------------------------------
def PrintableStr(s: str) -> str:
    return ''.join(c for c in s if c.isalpha()
                   or c.isnumeric() or c.isspace()
                   or c in string.printable
                   )

#---------------------------------------------------------------
# MakeStr return a string of length N filled with character C. }
#---------------------------------------------------------------
def MakeStr (C: str, N: int) -> str:
    """MakeStr"""
#beginfunction
    LResult = ''
    if (len(C)==1) and (N > 0) and (N < 255):
        LResult = C*N
    return LResult
#endfunction

#---------------------------------------------------------------
#
#---------------------------------------------------------------
def CharFromSet (C: TCharSet) -> str:
    """CharFromSet"""
#beginfunction
    for i in range(0,255,1):
        if chr(i) in C:
            return chr(i)
        #endif
    #endfor
    return '?'
#endfunction

#--------------------------------------------------------------------
# AddChar (Pad, Input, Length):
#--------------------------------------------------------------------
def AddChar (APad, AInput, ALength) -> str:
    """AddChar"""
#beginfunction
    x = len (AInput)
    for i in range (x, ALength, len (APad)):
        AInput = APad + AInput
    #endfor
    LAddChar = AInput
    return LAddChar
#endfunction

#--------------------------------------------------------------------
# AddCharR (Pad, Input, Length):
#--------------------------------------------------------------------
def AddCharR (APad, AInput, ALength):
    """AddCharR"""
#beginfunction
    x = len (AInput)
    for i in range (x, ALength, len (APad)):
        AInput = AInput + APad
    #endfor
    LAddCharR = AInput
    return LAddCharR
#endfunction

#---------------------------------------------------------------
#
#---------------------------------------------------------------
def Trim (s: str) -> str:
    """Trim"""
#beginfunction
    return s.strip()
#endfunction

#---------------------------------------------------------------
#
#---------------------------------------------------------------
def TrimL (s: str) -> str:
    """TrimL"""
#beginfunction
    return s.lstrip()
#endfunction

#---------------------------------------------------------------
#
#---------------------------------------------------------------
def TrimR (s: str) -> str:
    """TrimR"""
#beginfunction
    return s.rstrip()
#endfunction

#---------------------------------------------------------------
#
#---------------------------------------------------------------
def TrimChar (s: str, c: str) -> str:
    """TrimChar"""
#beginfunction
    return s.strip (c)
#endfunction

#---------------------------------------------------------------
#
#---------------------------------------------------------------
def TrimCharL (s: str, c: str) -> str:
    """TrimCharL"""
#beginfunction
    return s.lstrip (c)
#endfunction

#---------------------------------------------------------------
#
#---------------------------------------------------------------
def TrimCharR (s: str, c: str) -> str:
    """TrimCharR"""
#beginfunction
    return s.rstrip (c)
#endfunction

#--------------------------------------------------------------------
# WordCount (String, Delimiter):
#--------------------------------------------------------------------
def WordCount (AString: str, AWordDelims) -> int:
    """WordCount"""
#beginfunction
    LArray = AString.split (AWordDelims)
    LWordCount = len (LArray)
    return LWordCount
#endfunction

#--------------------------------------------------------------------
#ExtractWord (i, String, Delimiter):
#--------------------------------------------------------------------
def ExtractWord (i: int, AString: str, AWordDelims):
    """ExtractWord"""
    #beginfunction
    LArray = AString.split (AWordDelims)
    if (i > 0) and (i <= len(LArray) + 1):
        try:
            LExtractWord = LArray [i-1]
        except IndexError as ERROR:
            LExtractWord = ""
            ...
    else:
        LExtractWord = ""
    #endif
    return LExtractWord
#endfunction

#--------------------------------------------------------------------
#ExistWord (String, Delimiter, Word):
#--------------------------------------------------------------------
def ExistWord (AString: str, AWordDelims, AWord: str):
    """ExistWord"""
#beginfunction
    n = WordCount (AString, AWordDelims)
    for i in range (1, n+1, 1):
        s = ExtractWord (i, AString, AWordDelims)
        if AWord.upper() == s.upper ():
            return True
        #endif
    #endfor
    return False
#endfunction

#---------------------------------------------------------------
#
#---------------------------------------------------------------
def GetParamFromString (AParamName: str, AParamValues: str,
    AParamNames: (), AWordDelims: TCharSet) -> str:
    """GetParamFromString"""
#beginfunction
    LResult = ''
    i = 0
    for ParamName in AParamNames:
        i = i + 1
        if ParamName.upper() == AParamName.upper():
            LResult = Trim (ExtractWord (i, AParamValues, AWordDelims))
            return LResult
        #endif
    #endfor
    return LResult
#endfunction

#---------------------------------------------------------------
#
#---------------------------------------------------------------
def SetParamToString (AParamName: str, AParamValues: str,
    AParamNames: (), AWordDelims: TCharSet, AValue: str):
    """SetParamToString"""
#beginfunction
    LStroka = AParamValues
    s = ''
    i = 0
    for ParamName in AParamNames:
        i = i + 1
        if ParamName.upper() == AParamName.upper():
            s = s + AValue
        else:
            s = s + ExtractWord (i, LStroka, AWordDelims)
        #endif
        if i != len(AParamNames):
            s = s + CharFromSet (AWordDelims)
        #endif
    #endfor
    return s
#endfunction

#---------------------------------------------------------------
# DelChars return a string with all Chr characters removed
#---------------------------------------------------------------
def DelChars (s: str, c: str) -> str:
    """DelChars"""
#beginfunction
    LResult = s.replace(c, '')
    return LResult
#endfunction

#---------------------------------------------------------------
# DelSpace return a string with all white spaces removed.
#---------------------------------------------------------------
def DelSpaces (s: str) -> str:
    """DelSpaces"""
#beginfunction
    LResult = DelChars(s, ' ')
    return LResult
#endfunction

#---------------------------------------------------------------
# DelSpace return a string with all white spaces removed.
#---------------------------------------------------------------
def ReplaceChars (s, sOld, sNew: str) -> str:
    """ReplaceChars"""
#beginfunction
    LResult = s.replace (sOld, sNew)
    return LResult
#endfunction

#---------------------------------------------------------------
#
#---------------------------------------------------------------
def CenterStr (s: str, c: str, ALen: int) -> str:
    """CenterStr"""
#beginfunction
    return s.center (len(s)+ALen, c)
#endfunction

def strtobool (val: str):
    """Convert a string representation of truth to true (1) or false (0).
    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
#beginfunction
    if val.lower() in ('y', 'yes', 't', 'true', 'on', '1'):
        return 1
    elif val.lower() in ('n', 'no', 'f', 'false', 'off', '0'):
        return 0
    else:
        raise ValueError("invalid truth value %r" % (val,))
#endfunction

"""
function IsWild (InputStr, Wilds: string; IgnoreCase: Boolean): Boolean;

    function SearchNext (var Wilds: string): Integer;
    { looking for next *, returns position and string until position }
    begin
        Result := Pos ('*', Wilds);
        if Result > 0 then
            Wilds := Copy (Wilds, 1, Result - 1);
    end;

var
    CWild, CInputWord: Integer; { counter for positions }
    I, LenHelpWilds: Integer;
    MaxInputWord, MaxWilds: Integer; { Length of InputStr and Wilds }
    HelpWilds: string;
begin
    if Wilds = InputStr then
    begin
        Result := True;
        Exit;
    end;
    repeat { delete '**', because '**' = '*' }
        I := Pos ('**', Wilds);
        if I > 0 then
            Wilds := Copy (Wilds, 1, I - 1) + '*' + Copy (Wilds, I + 2, MaxInt);
    until I = 0;
    if Wilds = '*' then
    begin { for fast end, if Wilds only '*' }
        Result := True;
        Exit;
    end;
    MaxInputWord := Length (InputStr);
    MaxWilds := Length (Wilds);
    if IgnoreCase then
    begin { upcase all letters }
        InputStr := AnsiUpperCase (InputStr);
        Wilds := AnsiUpperCase (Wilds);
    end;
    if (MaxWilds = 0) or (MaxInputWord = 0) then
    begin
        Result := False;
        Exit;
    end;
    CInputWord := 1;
    CWild := 1;
    Result := True;
    repeat
        if InputStr[CInputWord] = Wilds[CWild] then
        begin { equal letters }
      { goto next letter }
            Inc (CWild);
            Inc (CInputWord);
            Continue;
        end;
        if Wilds[CWild] = '?' then
        begin { equal to '?' }
      { goto next letter }
            Inc (CWild);
            Inc (CInputWord);
            Continue;
        end;
        if Wilds[CWild] = '*' then
        begin { handling of '*' }
            HelpWilds := Copy (Wilds, CWild + 1, MaxWilds);
            I := SearchNext (HelpWilds);
            LenHelpWilds := Length (HelpWilds);
            if I = 0 then
            begin
        { no '*' in the rest, compare the ends }
                if HelpWilds = '' then
                    Exit; { '*' is the last letter }
        { check the rest for equal Length and no '?' }
                for I := 0 to LenHelpWilds - 1 do
                begin
                    if (HelpWilds[LenHelpWilds - I] <> InputStr
                        [MaxInputWord - I]) and
                        (HelpWilds[LenHelpWilds - I] <> '?') then
                    begin
                        Result := False;
                        Exit;
                    end;
                end;
                Exit;
            end;
      { handle all to the next '*' }
            Inc (CWild, 1 + LenHelpWilds);
            I := FindPart (HelpWilds, Copy(InputStr, CInputWord, MaxInt));
            if I = 0 then
            begin
                Result := False;
                Exit;
            end;
            CInputWord := I + LenHelpWilds;
            Continue;
        end;
        Result := False;
        Exit;
    until (CInputWord > MaxInputWord) or (CWild > MaxWilds);
  { no completed evaluation }
    if CInputWord <= MaxInputWord then
        Result := False;
    if (CWild <= MaxWilds) and (Wilds[MaxWilds] <> '*') then
        Result := False;
end;
"""

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
