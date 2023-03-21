"""LUDateTime.py"""
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
     LUDateTime.py

 =======================================================
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import datetime
# from datetime import *
from calendar import *


#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------

#------------------------------------------
# CONST
#------------------------------------------
"""CONST"""
cFormatDateTimeLog01 = ('%H:%M:%S %f', '%d/%m/%Y %H:%M:%S %f')
cFormatDateTimeLog02 = ('%H%M%S%f', '%Y%m%d %H%M%S%f')
cFormatDateTimeLog03 = ('', '%Y%m%d')
cFormatDateTimeLog04 = ('', '%Y%m%d%H%M%S%f')
cFormatDateTimeLog05 = ('%d/%m/%Y %H:%M:%S %f', '%H:%M:%S %f')
cFormatDateTimeYYMMDD = ('', '%Y/%m/%d')
cFormatDateTimeYYMM = ('', '%Y/%m')

#---------------------------------------------------------------
#
#---------------------------------------------------------------
def Now () -> datetime:
    """DateTimeStr"""
#beginfunction
    LResult = datetime.datetime.now ()
    return LResult
#endfunction

#---------------------------------------------------------------
#
#---------------------------------------------------------------
def DateTimeStr (ATimeOnly: bool, ADateTime: datetime, AFormat: ()) -> str:
    """DateTimeStr"""
#beginfunction
    if ATimeOnly:
        LResult = ADateTime.strftime (AFormat[0])
    else:
        LResult = ADateTime.strftime (AFormat[1])
    #endif
    return LResult
#endfunction

#---------------------------------------------------------------
#
#---------------------------------------------------------------
def DecodeDate (ADateTime: datetime):
    """DecodeDate"""
#beginfunction
    LDate = ADateTime
    LTuple = (LDate.year, LDate.month, LDate.day)
    return LTuple
#endfunction

#---------------------------------------------------------------
#
#---------------------------------------------------------------
def DecodeTime (ADateTime: datetime):
    """DecodeTime"""
#beginfunction
    LTuple = (ADateTime.hour, ADateTime.minute, ADateTime.second, ADateTime.microsecond)
    return LTuple
#endfunction

#---------------------------------------------------------------
#
#---------------------------------------------------------------
def DayOfWeek (ADateTime: datetime):
    """DayOfWeek"""
#beginfunction
    return ADateTime.weekday()
#endfunction

#---------------------------------------------------------------
#
#---------------------------------------------------------------
def DaysInMonth (AYear: int, AMonth: int):
    """DaysInMonth"""
#beginfunction
    return monthrange (AYear, AMonth) [1]
#endfunction

def IsLeapYear(AYear: int) -> bool:
    """IsLeapYear"""
#beginfunction
    # return calendar.isleap(AYear)
    return (AYear % 4 == 0) and ((AYear % 100 != 0) or (AYear % 400 == 0))
#endfunction

def DaysPerMonth(AYear: int, AMonth: int) -> int:
    """DaysPerMonth"""
    LDaysInMonth = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
#beginfunction
    LResult = LDaysInMonth[AMonth]
    if (AMonth == 2) and IsLeapYear(AYear):
        LResult = LResult + 1
    return LResult
#endfunction

#---------------------------------------------------------------
#
#---------------------------------------------------------------
def EncodeDate (AYear: int, AMonth: int, ADay: int) -> datetime:
    """EncodeDate"""
#beginfunction
    return datetime.date(AYear, AMonth, ADay)
#endfunction

#---------------------------------------------------------------
#
#---------------------------------------------------------------
def EncodeTime (AHour: int, AMin: int, ASec: int, AMSec: int) -> datetime:
    """EncodeTime"""
#beginfunction
    return datetime.time(AHour, AMin, ASec, AMSec)
#endfunction

#---------------------------------------------------------------
#
#---------------------------------------------------------------
def EncodeDateTime (AYear: int, AMonth: int, ADay: int, AHour: int, AMin: int, ASec: int, AMSec: int) -> datetime:
    """EncodeDate"""
#beginfunction
    return datetime.datetime(AYear, AMonth, ADay, AHour, AMin, ASec, AMSec)
#endfunction

#---------------------------------------------------------------
#
#---------------------------------------------------------------
def GenerateObjectIDStr (AObjectID: datetime) -> str:
    """GenerateObjectIDStr"""
#beginfunction
    LResult = DateTimeStr (False, AObjectID, cFormatDateTimeLog04)
    return LResult
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
