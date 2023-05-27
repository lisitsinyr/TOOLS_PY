"""LUSheduler.py"""
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
     LUSheduler.py

 =======================================================
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import datetime
from calendar import monthrange
import threading
import logging
import time
#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------

#------------------------------------------
# БИБЛИОТЕКИ LU
#------------------------------------------
import LULog
import LUConst
import LUStrUtils
import LUDateTime

minNN = 0
maxNN = 59
minHH = 0
maxHH = 23
minDW = 1
maxDW = 7
minMM = 1
maxMM = 12
minDD = 1
maxDD = 31
DelimPattern = ' '
DelimItem = ','
DelimItems = '-'
"""
------------------------------------------------------------------
 NN-NN    HH-HH     DD-DD     MM-MM     DW-DW     [Program]
 NN,NN,.. HH,HH,... DD,DD,... MM,MM,... DW,DW,... [Program]
 *        *         *         *         *         [Program]
------------------------------------------------------------------
"""

def NotifyFileEvent():
#beginfunction
    ...
#endfunction
TNotifyFileEvent = NotifyFileEvent

# --------------------------------------------
# TObjectsItem
# --------------------------------------------
class TShedulerEventItem (object):
    """TShedulerEventItem"""
    luClassName = 'TShedulerEventItem'

    @staticmethod
    def IsBitOn (Value: int, Bit: int) -> bool:
    #beginfunction
        # return n & (1<<b))
        LResult = (Value & (1<<Bit)) != 0
        return LResult
    #endfunction

    @staticmethod
    def TurnBitOn (Value: int, Bit: int) -> int:
    #beginfunction
        #return value | (1<<bit)
        LResult = Value | (1<<Bit)
        return LResult
    #endfunction

    @staticmethod
    def TurnBitOff (Value: int, Bit: int) -> int:
    #beginfunction
        # return value & ~(1<<bit)
        LResult = Value & ~ (1<<Bit)
        return LResult
    #endfunction

    #--------------------------------------------------
    # constructor
    #--------------------------------------------------
    def __init__(self):
        """ Constructor """
        super().__init__()
        self.__FDD: int = 0
        self.__FMM: int = 0
        self.__FDW: int = 0
        self.__FHH: int = 0
        self.__FNN1: int = 0
        self.__FNN2: int = 0
        self.__FList: () = list ()
        self.__FNameEvent: str = ''
        self.Clear()

    #--------------------------------------------------
    # destructor
    #--------------------------------------------------
    def __del__(self):
        """ destructor """
    #beginfunction
        # удалить объект
        del self.__FList
        LClassName = self.__class__.__name__
        s = '{} уничтожен'.format (LClassName)
        # LUConst.LULogger.log (LULog.DEBUGTEXT, s)
        #print (s)
    #endfunction

    def Clear(self):
    #beginfunction
        ...
    #endfunction

    #--------------------------------------------------
    # @property NameEvent
    #--------------------------------------------------
    # getter
    @property
    def NameEvent(self):
    #beginfunction
        return self.__FNameEvent
    #endfunction
    @NameEvent.setter
    def NameEvent(self, Value: str):
    #beginfunction
        self.__FNameEvent: str = Value
    #endfunction

    def GetXX (self) -> ():
    #beginfunction
        return self.__FNN1,self.__FNN2,self.__FHH,self.__FDD,self.__FMM,self.__FDW
    #endfunction

    #--------------------------------------------------
    # @property NN
    #--------------------------------------------------
    # property NN [Index: Integer]: Boolean read GetNN write SetNN;
    def GetNN (self, Index: int) -> bool:
    #beginfunction
        LResult = False
        if (Index >= minNN) and (Index <= maxNN):
            if Index <= 31:
                LResult = self.IsBitOn (self.__FNN1, Index)
            else:
                LResult = self.IsBitOn (self.__FNN2, Index-32)
            #endif
        #endif
        return LResult
    #endfunction
    def SetNN (self, Index: int, Value: bool):
    #beginfunction
        if (Index >= minNN) and (Index <= maxNN):
            if Index <= 31:
                if Value:
                    self.__FNN1 = self.TurnBitOn (self.__FNN1, Index)
                else:
                    self.__FNN1 = self.TurnBitOff (self.__FNN1, Index)
                #endif
            else:
                if Value:
                    self.__FNN2 = self.TurnBitOn (self.__FNN2, Index-32)
                else:
                    self.__FNN2 = self.TurnBitOff (self.__FNN2, Index-32)
                #endif
            #endif
        #endif
    #endfunction

    #--------------------------------------------------
    # @property HH
    #--------------------------------------------------
    # property HH [Index: Integer]: Boolean read GetHH write SetHH;
    def GetHH (self, Index: int) -> bool:
    #beginfunction
        LResult = False
        if (Index >= minHH) and (Index <= maxHH):
            LResult = self.IsBitOn (self.__FHH, Index)
        return LResult
    #endfunction
    def SetHH (self, Index: int, Value: bool):
    #beginfunction
        if (Index >= minHH) and (Index <= maxHH):
            if Value:
                self.__FHH = self.TurnBitOn (self.__FHH, Index)
            else:
                self.__FHH = self.TurnBitOff (self.__FHH, Index)
            #endif
        #endif
    #endfunction

    #--------------------------------------------------
    # @property DD
    #--------------------------------------------------
    # property DD [Index: Integer]: Boolean read GetDD write SetDD;
    def GetDD (self, Index: int) -> bool:
    #beginfunction
        LResult = False
        if (Index >= minDD-1) and (Index <= maxDD-1):
            LResult = self.IsBitOn (self.__FDD, Index)
        return LResult
    #endfunction
    def SetDD (self, Index: int, Value: bool):
    #beginfunction
        if (Index >= minDD-1) and (Index <= maxDD-1):
            if Value:
                self.__FDD = self.TurnBitOn (self.__FDD, Index)
            else:
                self.__FDD = self.TurnBitOff (self.__FDD, Index)
            #endif
        #endif
    #endfunction

    #--------------------------------------------------
    # @property MM
    #--------------------------------------------------
    # property MM [Index: Integer]: Boolean read GetMM write SetMM;
    def GetMM (self, Index: int) -> bool:
    #beginfunction
        LResult = False
        if (Index >= minMM-1) and (Index <= maxMM-1):
            LResult = self.IsBitOn (self.__FMM, Index)
        return LResult
    #endfunction
    def SetMM (self, Index: int, Value: bool):
    #beginfunction
        if (Index >= minMM-1) and (Index <= maxMM-1):
            if Value:
                self.__FMM = self.TurnBitOn (self.__FMM, Index)
            else:
                self.__FMM = self.TurnBitOff (self.__FMM, Index)
            #endif
        #endif
    #endfunction

    #--------------------------------------------------
    # @property DW
    #--------------------------------------------------
    # property DW [Index: Integer]: Boolean read GetDW write SetDW;
    def GetDW (self, Index: int) -> bool:
    #beginfunction
        LResult = False
        if (Index >= minDW-1) and (Index <= maxDW-1):
            LResult = self.IsBitOn (self.__FDW, Index)
        return LResult
    #endfunction
    def SetDW (self, Index: int, Value: bool):
    #beginfunction
        if (Index >= minDW-1) and (Index <= maxDW-1):
            if Value:
                self.__FDW = self.TurnBitOn (self.__FDW, Index)
            else:
                self.__FDW = self.TurnBitOff (self.__FDW, Index)
            #endif
        #endif
    #endfunction

    #--------------------------------------------------
    # @property XXString
    #--------------------------------------------------
    # property XXString[XXName: string]: string read GetXXString;
    def GetXXString (self, XXName: str) -> str:
    #beginfunction
        LResult = ''
        if XXName.upper() == 'DD':
            for i in range (0, maxDD):
                if self.GetDD(i):
                    LResult = LResult+LUStrUtils.AddChar(' ', str(i+1), 2)+','
                else:
                    LResult = LResult + 'xx' + ','
                #endif
            #endfor
        #endif
        if XXName.upper() == 'MM':
            for i in range (0, maxMM):
                if self.GetMM(i):
                    LResult = LResult+LUStrUtils.AddChar(' ', str(i+1), 2)+','
                else:
                    LResult = LResult + 'xx' + ','
                #endif
            #endfor
        #endif
        if XXName.upper() == 'DW':
            for i in range (0, maxDW):
                if self.GetDW(i):
                    LResult = LResult+LUStrUtils.AddChar(' ', str(i+1), 2)+','
                else:
                    LResult = LResult + 'xx' + ','
                #endif
            #endfor
        #endif
        if XXName.upper() == 'HH':
            for i in range (0, maxHH+1):
                if self.GetHH(i):
                    LResult = LResult+LUStrUtils.AddChar(' ', str(i), 2)+','
                else:
                    LResult = LResult + 'xx' + ','
                #endif
            #endfor
        #endif
        if XXName.upper() == 'NN':
            for i in range (0, maxNN+1):
                if self.GetNN(i):
                    LResult = LResult+LUStrUtils.AddChar(' ', str(i), 2)+','
                else:
                    LResult = LResult + 'xx' + ','
                #endif
            #endfor
        #endif
        # удалить последний символ ',' в строке
        LResult = LResult [:-1]
        return LResult
    #endfunction

    def CreateList (self, Pattern: str, Lmin: int, Lmax: int):
    #var
    #   i, j, WCount, i11, i12: Integer;
    #   S1, S11, S12: string;
    #beginfunction
        self.__FList.clear()
        if Pattern == '*':
            for j in range (Lmin, Lmax+1):
                # self.__FList.append (str(j))
                self.__FList.append (j)
        else:
            WCount = LUStrUtils.WordCount(Pattern, DelimItem)
            for i in range (1, WCount+1):
                s1 = LUStrUtils.ExtractWord (i, Pattern, DelimItem)
                s11 = LUStrUtils.ExtractWord (1, s1, DelimItems)
                s12 = LUStrUtils.ExtractWord (2, s1, DelimItems)
                try:
                    i11 = int(s11)
                except:
                    i11 = -1
                #endtry
                if i11 > Lmax: i11 = Lmax #endif
                try:
                    i12 = int(s12)
                except:
                    i12 = i11
                #endtry
                if i12 > Lmax: i12 = Lmax #endif
                if i11 >= 0 and i12 >= 0:
                    # for j in range (i11, i12 + 1): self.__FList.append (str (j))
                    for j in range (i11, i12 + 1): self.__FList.append (j)
                #endif
            #endfor
        #endif
    #endfunction

    # def NewPatterns (self, Patterns: str):
    # #beginfunction
    #    self.__FDD = 0
    #    self.__FMM = 0
    #    self.__FDW = 0
    #    self.__FHH = 0
    #    self.__FNN1 = 0
    #    self.__FNN2 = 0
    #    self.AddPatterns (Patterns)
    # #endfunction

    def AddPatterns (self, Patterns: str):
    #beginfunction
        self.__FDD = 0
        self.__FMM = 0
        self.__FDW = 0
        self.__FHH = 0
        self.__FNN1 = 0
        self.__FNN2 = 0
        # NN
        self.CreateList (LUStrUtils.ExtractWord (1, Patterns, DelimPattern), minNN, maxNN)
        for item in self.__FList:
            # self.SetNN(self.__FList.index(item), True)
            self.SetNN(item, True)
        # HH
        self.CreateList (LUStrUtils.ExtractWord (2, Patterns, DelimPattern), minHH, maxHH)
        for item in self.__FList:
            # self.SetHH (self.__FList.index(item), True)
            self.SetHH (item, True)
        # DD
        self.CreateList (LUStrUtils.ExtractWord (3, Patterns, DelimPattern), minDD, maxDD)
        for item in self.__FList:
            # self.SetDD (self.__FList.index(item), True)
            self.SetDD (item-1, True)
        # MM
        self.CreateList (LUStrUtils.ExtractWord (4, Patterns, DelimPattern), minMM, maxMM)
        for item in self.__FList:
            # self.SetMM (self.__FList.index(item), True)
            self.SetMM (item-1, True)
        # DW
        self.CreateList (LUStrUtils.ExtractWord (5, Patterns, DelimPattern), minDW, maxDW)
        for item in self.__FList:
            # self.SetDW (self.__FList.index (item), True)
            self.SetDW (item-1, True)
    #endfunction
#endclass

# --------------------------------------------
# TSheduler
# --------------------------------------------
# TSheduler = class (TTimer)
class TSheduler (threading.Thread):
    """TSheduler"""
    luClassName = 'TSheduler'

    #--------------------------------------------------
    # constructor
    #--------------------------------------------------
    def __init__ (self, *args, **kwargs):
        """Constructor"""
    #beginfunction
        super ().__init__ (*args, **kwargs)
        self.args = args
        self.kwargs = kwargs
        #
        self.FStopThread = False
        #
        self.__FShedulerEvents = list ()
        #
        self.__FNameEvents = list ()
        # 'Следующий сеанс: ', self.DTEvents
        self.__FDTEvents: datetime = 0
        #
        self.__FEnable: bool = True
        #
        self.__FOnSheduler: TNotifyFileEvent = None
        #
        self.__FOnShedulerEvent:TShedulerEventItem = None
    #endfunction

    #--------------------------------------------------
    # destructor
    #--------------------------------------------------
    def __del__(self):
        """destructor"""
    #beginfunction
        # удалить объект
        del self.__FShedulerEvents
        del self.__FNameEvents
        LClassName = self.__class__.__name__
        s = '{} уничтожен'.format(LClassName)
        # LUConst.LULogger.log (LULog.DEBUGTEXT, s)
    #endfunction

    #--------------------------------------------------
    # @property OnSheduler
    #--------------------------------------------------
    # getter
    @property
    def OnSheduler(self) -> TNotifyFileEvent:
    #beginfunction
        return self.__FOnSheduler
    #endfunction
    @OnSheduler.setter
    def OnSheduler(self, Value: str):
    #beginfunction
        self.__FOnSheduler: TNotifyFileEvent = Value
    #endfunction

    #--------------------------------------------------
    # @property Enable
    #--------------------------------------------------
    # getter
    @property
    def Enable(self) -> bool:
    #beginfunction
        return self.__FEnable
    #endfunction
    @Enable.setter
    def Enable(self, Value: bool):
    #beginfunction
        self.__FEnable: bool = Value
        if Value:
            self.__CreateNextEvent ()
        #endif
    #endfunction

    # #--------------------------------------------------
    # # @property ShedulerEvents
    # #--------------------------------------------------
    # # getter
    # @property
    # def ShedulerEvents(self):
    # #beginfunction
    #     return self.__FShedulerEvents
    # #endfunction
    # @ShedulerEvents.setter
    # def ShedulerEvents(self, Value: ()):
    # #beginfunction
    #     self.__FShedulerEvents: () = Value
    # #endfunction

    #--------------------------------------------------
    # @property OnShedulerEvent
    #--------------------------------------------------
    # getter
    @property
    def OnShedulerEvent(self) -> TShedulerEventItem:
    #beginfunction
        return self.__FOnShedulerEvent
    #endfunction
    @OnShedulerEvent.setter
    def OnShedulerEvent(self, Value:TShedulerEventItem):
    #beginfunction
        self.__FOnShedulerEvent = Value
    #endfunction

    #--------------------------------------------------
    # @property ShedulerEventItem
    #--------------------------------------------------
    def GetShedulerEventItem(self, ANameEvent: str) -> TShedulerEventItem:
    #beginfunction
        for item in self.__FShedulerEvents:
            if item.NameEvent == ANameEvent:
                return item
            #endif
        #endfor
        return None
    #endfunction

    # #--------------------------------------------------
    # # @property NameEvents
    # #--------------------------------------------------
    # # getter
    # @property
    # def NameEvents(self) -> list:
    # #beginfunction
    #     self.CreateNextEvent (LUDateTime.Now ())
    #     return self.__FNameEvents
    # #endfunction

    #--------------------------------------------------
    # @property DTEvents
    #--------------------------------------------------
    # getter
    @property
    def DTEvents(self) -> datetime:
    #beginfunction
        return self.__FDTEvents
    #endfunction

    #--------------------------------------------------
    # run
    #--------------------------------------------------
    def run(self):
        """Запуск потока"""
    #beginfunction
        s = 'Запуск потока TSheduler...'
        LULog.LoggerTOOLS.debug (s)
        super ().run()
        if self.__FDTEvents == 0:
            self.__CreateNextEvent ()
        #endif
        while not self.FStopThread:
            s = 'Выполнение потока TSheduler...'
            # LULog.LoggerTOOLS.debug (s)
            if self.Enable:
                LPresent1 = LUDateTime.Now ()
                LYear, LMonth, LDay = LUDateTime.DecodeDate (LPresent1)
                LHour, LMin, LSec, LMSec = LUDateTime.DecodeTime (LPresent1)
                LDTEvents1 = LUDateTime.EncodeDateTime (LYear, LMonth, LDay, LHour, LMin, 0, 0)
                LDTEvents2 = self.DTEvents
                if LDTEvents1 == LDTEvents2:
                    self.__Second ()
                    # 'Следующий сеанс: ', self.DTEvents
                    self.__CreateNextEvent ()
                #endif
            #endif
            continue
        #endwhile
    #endfunction

    def __CreateNextEvent (self):
        """__CreateNextEvent"""
    #beginfunction
        LPresent: datetime = LUDateTime.Now ()
        LYear, LMonth, LDay = LUDateTime.DecodeDate (LPresent)
        LHour, LMin, LSec, LMSec = LUDateTime.DecodeTime (LPresent)
        LMin = LMin + 1
        self.__FNameEvents.clear()
        # Year
        for LYear in range (LYear,LYear+1):
            # Month
            for LMonth in range (LMonth, maxMM):
                # MaxDDWork = DateUtils.DaysInMonth (Present)
                MaxDDWork = monthrange (LYear, LMonth)[1]
                # Day of Month
                for LDay in range (LDay, MaxDDWork):
                    LDayWeek = LUDateTime.DayOfWeek (LUDateTime.EncodeDate(LYear,LMonth,LDay))
                    LDayWeek = LDayWeek + 1
                    if LDayWeek == 0:
                        LDayWeek = 7
                    #endif
                    # Hour
                    for LHour in range (LHour, maxHH):
                        # Min
                        for LMin in range (LMin, maxNN):
                            # Check List Sheduler
                            for item in  self.__FShedulerEvents:
                                self.OnShedulerEvent:TShedulerEventItem = item
                                if self.OnShedulerEvent.GetDD (LDay) and\
                                     self.OnShedulerEvent.GetDW (LDayWeek) and\
                                     self.OnShedulerEvent.GetMM (LMonth) and\
                                     self.OnShedulerEvent.GetHH (LHour) and\
                                     self.OnShedulerEvent.GetNN (LMin):
                                     self.__FNameEvents.append (self.OnShedulerEvent.NameEvent)
                                #endif
                            #endfor
                            if len(self.__FNameEvents) > 0:
                                break
                            #endif
                        #endfor
                        if len(self.__FNameEvents) == 0:
                            LMin = minNN
                        else:
                            break
                        #endif
                    #endfor
                    if len(self.__FNameEvents) == 0:
                        LHour = minHH
                    else:
                        break
                    #endif
                #endfor
                if len(self.__FNameEvents) == 0:
                    LDay = minDD
                else:
                    break
                #endif
            #endfor
            if len(self.__FNameEvents) == 0:
                LMonth = minMM
            else:
                break
            #endif
        #endfor
        if len(self.__FNameEvents) > 0:
            D = LUDateTime.EncodeDate (LYear, LMonth, LDay)
            T = LUDateTime.EncodeTime (LHour, LMin, 0, 0)
            self.__FDTEvents = datetime.datetime.combine (D, T)
            self.__FDTEvents = LUDateTime.EncodeDateTime (LYear, LMonth, LDay, LHour, LMin, 0, 0)
        else:
            self.__FDTEvents = LPresent
        #endif
        s = 'Следующий сеанс: ' + str (self.__FDTEvents)
        # LULog.LoggerTOOLS.debug (s)
    #endfunction
    
    def __Second (self):
        """Second"""
    #beginfunction
        s = 'Second...'
        # LULog.LoggerTOOLS.debug (s)
        if self.Enable:
            LPresent: datetime = LUDateTime.Now()
            LHour, LMin, LSec, LMSec = LUDateTime.DecodeTime (LPresent)
            # Check List Sheduler
            LYear, LMonth, LDay = LUDateTime.DecodeDate (LPresent)
            LDayWeek = LUDateTime.DayOfWeek (LPresent)
            LDayWeek = LDayWeek + 1
            if LDayWeek == 0:
                LDayWeek = 7
            for item in self.__FShedulerEvents:
                LEvent: TShedulerEventItem = item
                bDay = LEvent.GetDD (LDay)
                bDayWeek = LEvent.GetDW (LDayWeek)
                bMonth = LEvent.GetMM (LMonth)
                bHour = LEvent.GetHH (LHour)
                bMin = LEvent.GetNN (LMin)
                if bDay and bDayWeek and bMonth and bHour and bMin:
                    self.OnShedulerEvent = item
                    if self.OnSheduler is not None:
                        self.OnSheduler (LEvent)
                    #endif
                #endif
            #endfor
        #endif
    #endfunction

    def __CreateShedulerEvent(self) -> TShedulerEventItem:
    #beginfunction
        LResult: TShedulerEventItem = TShedulerEventItem()
        self.__FShedulerEvents.append(LResult)
        return LResult
    #endfunction

    def __DeleteEvent (self, ANameEvent: str):
    #beginfunction
        for item in self.__FShedulerEvents:
            if item.NameEvent == ANameEvent:
                self.__FShedulerEvents.remove(item)
                break
            #endif
        #endfor
    #endfunction

    def AddEvent (self, ANameEvent:str, APatterns: str) -> TShedulerEventItem:
        """AddEvent"""
    #beginfunction
        LEvent:TShedulerEventItem = None
        for item in self.__FShedulerEvents:
            if item.NameEvent == ANameEvent:
                LEvent: TShedulerEventItem = item
                break
            #endif
        #endfor

        if LEvent is not None and LEvent.NameEvent == ANameEvent:
            LEvent.AddPatterns (APatterns)
        else:
            LEvent:TShedulerEventItem = self.__CreateShedulerEvent()
            LEvent.NameEvent = ANameEvent
            LEvent.AddPatterns (APatterns)
        #endif
        return LEvent
    #endfunction

    @staticmethod
    def PrintEvent (AEvent: TShedulerEventItem):
        """PrintEvent"""
    #beginfunction
        LULog.LoggerTOOLS.debug (AEvent.NameEvent)
        s = f'NN={AEvent.GetXXString ("NN")}'
        LULog.LoggerTOOLS.debug (s)
        s = f'HH={AEvent.GetXXString ("HH")}'
        LULog.LoggerTOOLS.debug (s)
        s = f'DD={AEvent.GetXXString ("DD")}'
        LULog.LoggerTOOLS.debug (s)
        s = f'MM={AEvent.GetXXString ("MM")}'
        LULog.LoggerTOOLS.debug (s)
        s = f'DW={AEvent.GetXXString ("DW")}'
        LULog.LoggerTOOLS.debug (s)
    #endfunction
#endclass

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

