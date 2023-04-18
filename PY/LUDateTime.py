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
import time
from calendar import *
import logging

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------

#------------------------------------------
# БИБЛИОТЕКИ LU
#------------------------------------------
import LUStrUtils

# LULogger = logging.getLogger(__name__)

#------------------------------------------
# CONST
#------------------------------------------
# cFormatDateTimeLog01 = ('%H:%M:%S %f', '%d/%m/%Y %H:%M:%S %f')
# cFormatDateTimeLog02 = ('%H%M%S%f', '%Y%m%d %H%M%S%f')
# cFormatDateTimeLog03 = ('', '%Y%m%d')
# cFormatDateTimeLog04 = ('', '%Y%m%d%H%M%S%f')
# cFormatDateTimeLog05 = ('%d/%m/%Y %H:%M:%S %f', '%H:%M:%S %f')

cFormatDateTimeLog01 = ('%H:%M:%S', '%d/%m/%Y %H:%M:%S')
cFormatDateTimeLog02 = ('%H%M%S', '%Y%m%d %H%M%S')
cFormatDateTimeLog04 = ('', '%Y%m%d%H%M%S%f')
cFormatDateTimeLog05 = ('%d/%m/%Y %H:%M:%S', '%H:%M:%S')

cFormatDateYYMMDD_01 = ('', '%Y%m%d')
cFormatDateYYMMDD_02 = ('', '%Y/%m/%d')
cFormatDateYYMM_01 = ('', '%Y/%m')
cFormatDateYYMM_02 = ('', '%Y\\%m')

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
    else:
        if Amsecs:
            LResult = ADateTime.strftime (AFormat[1]+' '+smsecs)
        else:
            LResult = ADateTime.strftime (AFormat[1])
    #endif
    return LResult
#endfunction

#---------------------------------------------------------------
#
#---------------------------------------------------------------
def DecodeDate (ADateTime: datetime.datetime):
    """DecodeDate"""
#beginfunction
    LDate = ADateTime
    LTuple = (LDate.year, LDate.month, LDate.day)
    return LTuple
#endfunction

#---------------------------------------------------------------
#
#---------------------------------------------------------------
def EncodeDate (AYear: int, AMonth: int, ADay: int) -> datetime.date:
    """EncodeDate"""
#beginfunction
    return datetime.date(AYear, AMonth, ADay)
#endfunction

#---------------------------------------------------------------
#
#---------------------------------------------------------------
def DecodeTime (ADateTime: datetime.datetime):
    """DecodeTime"""
#beginfunction
    LTuple = (ADateTime.hour, ADateTime.minute, ADateTime.second, ADateTime.microsecond)
    return LTuple
#endfunction

#---------------------------------------------------------------
#
#---------------------------------------------------------------
def EncodeTime (AHour: int, AMin: int, ASec: int, AMSec: int) -> datetime.time:
    """EncodeTime"""
#beginfunction
    return datetime.time(AHour, AMin, ASec, AMSec)
#endfunction

#---------------------------------------------------------------
#
#---------------------------------------------------------------
def EncodeDateTime (AYear: int, AMonth: int, ADay: int, AHour: int, AMin: int, ASec: int, AMSec: int) -> datetime.datetime:
    """EncodeDate"""
#beginfunction
    return datetime.datetime(AYear, AMonth, ADay, AHour, AMin, ASec, AMSec)
#endfunction

#---------------------------------------------------------------
#
#---------------------------------------------------------------
def DayOfWeek (ADateTime: datetime.datetime):
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
def GenerateObjectIDStr (AObjectID: datetime.datetime) -> str:
    """GenerateObjectIDStr"""
#beginfunction
    LResult = DateTimeStr (False, AObjectID, cFormatDateTimeLog04,Amsecs = False)
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
