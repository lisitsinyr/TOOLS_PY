"""LUDateTime.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2023-2024
 Author:
     Lisitsin Y.R.
 Project:
     LU_PY
     Python (LU)
 Module:
     LUDateTime.py

 =======================================================
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import datetime
import time
import calendar
import logging
import platform

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------

#------------------------------------------
# БИБЛИОТЕКИ LU
#------------------------------------------
import lyrpy.LUSupport as LUSupport

#------------------------------------------
# CONST
#------------------------------------------
cFormatDateTimeLog01 = ('%H:%M:%S', '%d/%m/%Y %H:%M:%S')
cFormatDateTimeLog02 = ('%H%M%S', '%Y%m%d %H%M%S')
cFormatDateTimeLog04 = ('', '%Y%m%d%H%M%S%f')
cFormatDateTimeLog05 = ('%d/%m/%Y %H:%M:%S', '%H:%M:%S')

cFormatDateYYMMDD_01 = ('', '%Y%m%d')
cFormatDateYYMM_01 = ('', '%Y%m')

if platform.system() == 'Windows':
    cFormatDateYYMMDD_02 = ('', r'%Y\%m\%d')
    cFormatDateYYMM_02 = ('', r'%Y\%m')
#endif
if platform.system() == 'Linux':
    cFormatDateYYMMDD_02 = ('', r'%Y/%m/%d')
    cFormatDateYYMM_02 = ('', r'%Y/%m')
#endif

#---------------------------------------------------------------
# Now
#---------------------------------------------------------------
def Now () -> datetime:
    """Now"""
#beginfunction
    LResult = datetime.datetime.now ()
    return LResult
#endfunction

#---------------------------------------------------------------
# DateTimeStr
#---------------------------------------------------------------
def DateTimeStr (ATimeOnly: bool, ADateTime: datetime.datetime, AFormat: (), Amsecs: bool) -> str:
    """DateTimeStr"""
#beginfunction
    msecs = ADateTime.microsecond
    msecs = msecs // 1000
    smsecs = LUStrUtils.AddChar('0', str(msecs), 3)
    # ct = time.time ()
    # msecs = int((ct - int(ct)) * 1000) + 0.0 # see gh-89047
    if ATimeOnly:
        if Amsecs:
            LResult = ADateTime.strftime (AFormat[0]+' '+smsecs)
        else:
            LResult = ADateTime.strftime (AFormat [0])
        #endif
    else:
        if Amsecs:
            LResult = ADateTime.strftime (AFormat[1]+' '+smsecs)
        else:
            LResult = ADateTime.strftime (AFormat[1])
        #endif
    #endif
    return LResult
#endfunction

#---------------------------------------------------------------
# DecodeDate
#---------------------------------------------------------------
def DecodeDate (ADateTime: datetime.datetime):
    """DecodeDate"""
#beginfunction
    LDate = ADateTime
    LTuple = (LDate.year, LDate.month, LDate.day)
    return LTuple
#endfunction

#---------------------------------------------------------------
# EncodeDate
#---------------------------------------------------------------
def EncodeDate (AYear: int, AMonth: int, ADay: int) -> datetime.date:
    """EncodeDate"""
#beginfunction
    return datetime.date(AYear, AMonth, ADay)
#endfunction

#---------------------------------------------------------------
# DecodeTime
#---------------------------------------------------------------
def DecodeTime (ADateTime: datetime.datetime):
    """DecodeTime"""
#beginfunction
    LTuple = (ADateTime.hour, ADateTime.minute, ADateTime.second, ADateTime.microsecond)
    return LTuple
#endfunction

#---------------------------------------------------------------
# EncodeTime
#---------------------------------------------------------------
def EncodeTime (AHour: int, AMin: int, ASec: int, AMSec: int) -> datetime.time:
    """EncodeTime"""
#beginfunction
    return datetime.time(AHour, AMin, ASec, AMSec)
#endfunction

#---------------------------------------------------------------
# EncodeDateTime
#---------------------------------------------------------------
def EncodeDateTime (AYear: int, AMonth: int, ADay: int, AHour: int, AMin: int, ASec: int, AMSec: int) -> datetime.datetime:
    """EncodeDate"""
#beginfunction
    return datetime.datetime(AYear, AMonth, ADay, AHour, AMin, ASec, AMSec)
#endfunction

#---------------------------------------------------------------
# DayOfWeek
#---------------------------------------------------------------
def DayOfWeek (ADateTime: datetime.date):
    """DayOfWeek"""
#beginfunction
    return ADateTime.weekday()
#endfunction

#---------------------------------------------------------------
# DaysInMonth
#---------------------------------------------------------------
def DaysInMonth (AYear: int, AMonth: int):
    """DaysInMonth"""
#beginfunction
    return monthrange (AYear, AMonth) [1]
#endfunction

#---------------------------------------------------------------
# IsLeapYear
#---------------------------------------------------------------
def IsLeapYear(AYear: int) -> bool:
    """IsLeapYear"""
#beginfunction
    return (AYear % 4 == 0) and ((AYear % 100 != 0) or (AYear % 400 == 0))
#endfunction

#---------------------------------------------------------------
# DaysPerMonth
#---------------------------------------------------------------
def DaysPerMonth(AYear: int, AMonth: int) -> int:
    """DaysPerMonth"""
    LDaysInMonth = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
#beginfunction
    LResult = LDaysInMonth[AMonth]
    if (AMonth == 2) and IsLeapYear(AYear):
        LResult = LResult + 1
    #endif
    return LResult
#endfunction

#---------------------------------------------------------------
# GenerateObjectIDStr
#---------------------------------------------------------------
def GenerateObjectIDStr (AObjectID: datetime.datetime) -> str:
    """GenerateObjectIDStr"""
#beginfunction
    LResult = DateTimeStr (False, AObjectID, cFormatDateTimeLog04,Amsecs = False)
    return LResult
#endfunction

#---------------------------------------------------------------
# main
#---------------------------------------------------------------
def main ():
#beginfunction
    print('main LUDatTime.py ...')
#endfunction

#------------------------------------------
#
#------------------------------------------
#beginmodule
if __name__ == "__main__":
    main()
#endif

#endmodule
