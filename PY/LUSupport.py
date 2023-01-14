#===============================================================
# LUSupport.py
#===============================================================
# WriteLN($c,$s)
# Pause()
# pause2(optional $delay, optional $prompt)
# LogFileName($Log, $LogDir, $LogFile)
# LogAdd ($Log, $LogFile, $Opt, $Message)
# LogAddFile ($Log, $LogFile, $Opt, $FileName, optional $Color)
# GetFolderCU($FolderName)
# SetFolderCU($FolderName, $Value)
# GetFolderLM($FolderName)
# SetFolderLM($FolderName, $Value)
# fnAllSpecialFolders()
# PasswdFromKbd(optional $Prompt)
#--------------------------------------------------------------------

import os
import sys
import time

#-------------------------------------------------
# Write($c,$s)
#-------------------------------------------------
def Write (AColor, s):
#beginfunction
#   COLOR $c
#'b' - синий цвет
#'g' - зеленый цвет
#'r' - красный цвет
#'c' - голубой цвет
#'m' - пурпурный цвет
#'y' - желтый цвет
#'k' - черный цвет
#'w' - белый цвет

#\033[4m — подчёркнутый;
#\033[37m — белая надпись;
#\033[44m — синий фон;
#{} — заменится на «Python 3»;
#\033[0m — сброс к начальным значениям.

    sys.stdout.write (s)
#endfunction

#-------------------------------------------------
# WriteLN($c,$s)
#-------------------------------------------------
def WriteLN (AColor, s):
#beginfunction
#   COLOR $Color
    sys.stdout.write (s+'\n')
#endfunction

#-------------------------------------------------
# Write (c, s)
#-------------------------------------------------
def Write (AColor, s):
#beginfunction
#   COLOR $Color
    print (s)
#endfunction

#--------------------------------------------------------------------------------
# WriteStr ($FileName, $Str)
#--------------------------------------------------------------------------------
def WriteStr (AFileName, AStr, AColor=''):
#beginfunction
    #SaveColor = @Color
    #$Res=RedirectOutput($FileName, 0)
    #if $Color COLOR $Color #endif
    sys.stdout.write (AStr+'\n')
    #if $Color COLOR $SaveColor #endif
    #------------------------------------------------------------
    #if $FileName
    #   $Handle = FreeFileHandle
    #   if Open ($Handle, $FileName, 1+4) = 0
    #      $Res = WriteLine ($Handle, $Str)
    #      if $Res
    #         $Res = Close ($Handle)
    #      #endif
    #   #endif
    #else
    #   $Res=RedirectOutput("")
    #   $s ?   
    ##endif
    #$WriteStr = $Res
    #--------------------------------------------------------------
#endfunction

#-------------------------------------------------
# ReadParam($Title,$Default)
#-------------------------------------------------
def ReadParam (ATitle: str, ADefault: str)->str:
#beginfunction
    #WriteLN ("w/n",  "")
    WriteLN ("w+/n", "Введите ("+ATitle+")["+ADefault+"]: ")
    LReadParam: str = input ("")
    #if (LReadParam is None) or (LReadParam == ''):
    if LReadParam == "":
       LReadParam = ADefault
    #endif
    return LReadParam
    #WriteLN ("w/n",  "")
#endfunction

#--------------------------------------------------------------------
# Pause(optional $prompt)
#--------------------------------------------------------------------
def Pause (Aprompt: str = ''):
#beginfunction
    if Aprompt == '':
        Aprompt="Press any key to continue "
    #endif
    if Aprompt != '':
        WriteLN (Aprompt)
    #endif
    x = sys.stdin.read (1)
#endfunction

#--------------------------------------------------------------------
# pause2(optional $delay, optional $prompt)
#--------------------------------------------------------------------
def pause2 (delay=0,prompt=''):
    loop = 0
    counter = 0
    interval = 0
#beginfunction
    #$Res=RedirectOutput("")
    pause = -1
    if prompt == '':
        prompt = "Press any key to continue"
    #endif
    if prompt != '':
        WriteLN(prompt)
    #endif
    if delay > 0:
        Interval = 0.2
        delay = delay + 1
        while pause == -1 and delay > 1.0 + interval:
            delay = delay - interval
            counter = "[" + int(delay) + "]:"
            Write (counter)
            sleep (interval)
            #for loop in range (1, len(counter), 1):
            #    Write (chr(8)+" "+chr(8))
            #endfor
            #if kbhit():
            pause = sys.stdin.read(1)
            #endif
        #endwhile
    else:
        pause = sys.stdin.read(1)
    #endif
#endfunction 

#-------------------------------------------------
# LogFileName($Log, $LogDir, $LogFile)
#-------------------------------------------------
def LogFileName(Log, LogDir, LogFile):
#beginfunction
    match Log:
        case 1,3,10,30:
            if LogDir == None:
                LogDir = os.environ['USERPROFILE']
                LogDir = os.environ['TEMP']
            #endif
            if LogFile == '':
                #a = Split(@DATE,"/")
                #LogFile = Join (a,"")+".log"
                LogFile = os.sep.join([a, ".log"])
            #endif
            LogFileName = LogDir+"/"+LogFile
            if Log == 10 or Log == 30:
               os.remove (LogFileName)
            #endif
        case _:
            Log = 2
            LogFileName = ""
    #endmatch
    return LogFileName
#endfunction

#--------------------------------------------------------------------------------
# LogAdd ($Log, $LogFile, $Opt, $Message, optional $Color)
#--------------------------------------------------------------------------------
def LogAdd (ALog, ALogFile, AOpt, AMessage, AColor=''):
#beginfunction
    o = AOpt.upper()
    match o:
        case "I":
            s = AMessage
        case _:
            s = "@DATE @TIME"+" "+AOpt+" "+AMessage
    #endmatch

    match ALog:
        case 1, 10:
            #$=RedirectOutput($LogFile,0)=0
            WriteLN (s)
            #$=RedirectOutput("")
        case 2:
            #if $Color COLOR $Color #endif
            WriteLN (s)
        case 3, 30:
            #$=RedirectOutput($LogFile,0)=0
            WriteLN (s)
            #$=RedirectOutput("")
            #if $Color COLOR $Color #endif
            WriteLN (s)
           #if $Color COLOR W/N #endif
    #endmatch
#endfunction

#--------------------------------------------------------------------------------
# LogAddFile ($Log, $LogFile, $Opt, $FileName, optional $Color)
#--------------------------------------------------------------------------------
#def LogAddFile ($Log, $LogFile, $Opt, $FileName, optional $Color)
##beginfunction
#   if EXIST ($FileName)
#      $Handle = FreeFileHandle
#      if Open ($Handle, $FileName, 2) = 0
#         $Str = ReadLine ($Handle)
#         while @ERROR = 0
#            LogAdd ($Log, $LogFile, $Opt, $Str, $Color)
#            $Str = ReadLine ($Handle)
#         loop
#         $Res = Close ($Handle)
#      #endif
#   #endif
#endfunction

#--------------------------------------------------------------------------------
# GetFolderCU($FolderName)
#--------------------------------------------------------------------------------
#def GetFolderCU($FolderName)
#   Dim $s
##beginfunction
#   $s = "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
#   $GetFolderCU = ReadString($S, $FolderName)
#endfunction

#--------------------------------------------------------------------------------
# SetFolderCU($FolderName, $Value)
#--------------------------------------------------------------------------------
#def SetFolderCU($FolderName, $Value)
#   Dim $s
##beginfunction
#   $s = "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
#   $SetFolderCU = WriteString($S, $FolderName, $Value, REG_SZ)
#endfunction

#--------------------------------------------------------------------------------
# GetFolderLM($FolderName)
#--------------------------------------------------------------------------------
#def GetFolderLM($FolderName)
#   Dim $s
##beginfunction
#   $s = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
#   $GetFolderLM = ReadString($S, $FolderName)
#endfunction

#--------------------------------------------------------------------------------
# SetFolderLM($FolderName, $Value)
#--------------------------------------------------------------------------------
#def SetFolderLM($FolderName, $Value)
#   Dim $s
##beginfunction
#   $s = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
#   $SetFolderLM = WriteString($S, $FolderName, $Value, REG_SZ)
#endfunction

#--------------------------------------------------------------------------------
# fnAllSpecialFolders()
#--------------------------------------------------------------------------------
def fnAllSpecialFolders():
    sAllFolders = ""
    objWshShell = ""
    Folder = ""
    nul = ""

    global AllUsersDesktop
    global AllUsersStartMenu
    global AllUsersPrograms
    global AllUsersStartup
    global AppData
    global Desktop
    global Favorites
    global Fonts
    global MyDocuments
    global NetHood
    global PrintHood
    global Programs
    global Recent
    global SendTo
    global StartMenu
    global Startup
    global Templates
#    $sAllFolders="AllUsersDesktop AllUsersStartMenu AllUsersPrograms AllUsersStartup "+
#       "AppData Desktop Favorites Fonts MyDocuments NetHood PrintHood Programs Recent "+
#       "SendTo StartMenu Startup Templates"
#    objWshShell = CreateObject("WScript.Shell")
#    if @ERROR Exit(1) #endif
#    For Each $Folder in Split($sAllFolders)
#       $nul=Execute("$"+$Folder+" = $$objWshShell.SpecialFolders($$Folder)")
#    #endfor
#    objWshShell = ''
#    return (0)
#endfunction

#--------------------------------------------------------------------------------
# fnGetM(OPTIONAL $sM,OPTIONAL $lTO)
#--------------------------------------------------------------------------------
#def fnGetM(OPTIONAL $sM,OPTIONAL $lTO)
#   Dim $X,$lT,$lTC
#begifunction
#   Do
#      $lT=@Ticks
#      Sleep 0.05
#      if KbHit()
#         Get $X
#         if Asc($X)>32
#            $fnGetM=$fnGetM+$X
#            if $sM $sM Else $X #endif
#         #endif
#         if Instr($X,Chr(8)) AND LEN($fnGetM)>0
#            Chr(8) Chr(32) Chr(8)
#            $fnGetM=Left($fnGetM,LEN($fnGetM)-1)
#         #endif
#         $lTC=0
#      #endif
#      if $lTO
#         if $lTC < $lTO*1000
#            $lTC=$lTC+@Ticks-$lT
#         Else
#            $fnGetM=""
#         ? Exit 121
#         #endif
#      #endif
#   Until Instr($X,Chr(13))
#   ? Exit 0
#endfunction

#------------------------------------------------------
# PrintGeneralTitle ($LLog, $LFile)
#------------------------------------------------------
#def PrintGeneralTitle (LLog, LFile):
##beginfunction
#   LogAdd ($LLog, $LFile, "I", "===========================================")
#   LogAdd ($LLog, $LFile, "I", "Текущее время = " + @Date+" "+@Time)
#   LogAdd ($LLog, $LFile, "I", "===========================================")
#   LogAdd ($LLog, $LFile, "I", "UserID        = " + $USERID)
#   LogAdd ($LLog, $LFile, "I", "FullName      = " + @FullName+" ("+@Comment+")")
#   LogAdd ($LLog, $LFile, "I", "PCUser        = " + %COMPUTERNAME%+" ("+Trim(@CPU)+" "+@MHz+")")
#   LogAdd ($LLog, $LFile, "I", "HostName      = " + @HostName)
#   LogAdd ($LLog, $LFile, "I", "OS            = " + @ProductType+" "+@DOS+" ("+@Build+")")
#   LogAdd ($LLog, $LFile, "I", "CompName      = " + @WKSTA)
#
#   LogAdd ($LLog, $LFile, "I", "DomainPC      = " + @Domain)
#   LogAdd ($LLog, $LFile, "I", "DomainUser    = " + @LDomain)
#   LogAdd ($LLog, $LFile, "I", "LServer       = " + @LServer)
#
#   LogAdd ($LLog, $LFile, "I", "StartDir      = " + @StartDir)
#   LogAdd ($LLog, $LFile, "I", "ScriptExe     = " + @ScriptExe)
#   LogAdd ($LLog, $LFile, "I", "Kix           = " + @Kix)
#
#   LogAdd ($LLog, $LFile, "I", "KxlDir        = " + $KxlDir)
#   LogAdd ($LLog, $LFile, "I", "LogFile       = " + $LFile)
#   LogAdd ($LLog, $LFile, "I", "Debug         = " + $Debug)
#   LogAdd ($LLog, $LFile, "I", "===========================================")
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

#-------------------------------------------------
# Memory
#-------------------------------------------------
#def Memory
#beginfunction
#  $objWMIService = GetObject("winmgmts:"+"{impersonationLevel=impersonate}!\\" + @WKSTA + "\root\cimv2")
#  $colCSItems = $objWMIService.ExecQuery("SELECT * FROM Win32_ComputerSystem")
#  For Each $objCSItem In $colCSItems
#     $Memory = $Memory + $objCSItem.TotalPhysicalMemory
#  Next
#endfunction
