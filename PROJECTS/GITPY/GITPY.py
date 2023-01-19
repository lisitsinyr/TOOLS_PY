#===============================================================
# GITPY.py
# GITPY.py "-PYDir='%PYDir%'" -Command=%1 -P1=%2 -P2=%3 -P5=%4 -P6=%5
#===============================================================

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import os
import sys
import subprocess

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
import argparse

#------------------------------------------
# Разбор аргументов
#------------------------------------------
parser = argparse.ArgumentParser(description='Параметры')
#parser.add_argument('-PYDir', type=str, nargs='?', default='', dest='PYDir', help='Библиотека LU')
#args = parser.parse_args()
#print('-PYDir  = '+args.PYDir)
#------------------------------------------
#PYDir: str = 'D:\\PROJECTS_LYR\\CHECK_LIST\\05_DESKTOP\\02_Python\\PROJECTS_PY\\TOOLS_PY\\PY'
#if args.PYDir != "":
#    PYDir = args.PYDir
#endif
#sys.path.append(PYDir)

#------------------------------------------
#БИБЛИОТЕКА LU
#------------------------------------------
import LUConst
#import LUFile
#import LUDateTime
import LUSupport
#import LUArray
#import LUIniFiles
#import APPTools
#------------------------------------------

#------------------------------------------
# Глобальные переменные 1
#------------------------------------------
LUConst.Log = 30
LUConst.LogDir = 'D:\\WORK'
LUConst.LogFile = "GIT.log"
LUConst.LogFile = LUSupport.LogFileName (LUConst.Log, LUConst.LogDir, LUConst.LogFile)

#------------------------------------------
# Глобальные переменные 2
#------------------------------------------
D_APP = "C:\\Program Files\\Git\\bin"
APP = "git.exe"
GITCommand: str = ""
P1: str = ""
P2: str = ""
P3: str = ""
P4: str = ""
P5: str = ""
#------------------------------------------
Dir: str = os.getcwd ()
#------------------------------------------

#-------------------------------------------------
# Display_Error
#-------------------------------------------------
def Display_Error (AError: int):
#beginFunction
    match AError:
        case 0:
            LUSupport.LogAdd(LUConst.Log, LUConst.LogFile, "I", "00 Нет ошибок")
        case _:
            LUSupport.LogAdd(LUConst.Log, LUConst.LogFile, "I", str(AError)+" неопределенная ошибка")
    #endmatch
#EndFunction

#-------------------------------------------------
# Display_Error
#-------------------------------------------------
def RUN_GIT ():
    global GITCommand
    global P1
    global P2
    global P3
    global P4
    global P5
#beginFunction
    LProgram = D_APP+"\\"+APP
    ProgramGIT = D_APP + "\\" + APP

    LProgramARG = ""
    if GITCommand != "":
        LProgram = LProgram+" "+GITCommand
        LProgramARG = GITCommand
    #endif
    if P1 != "":
        LProgram = LProgram+" "+P1
        LProgramARG = GITCommand+" "+P1
    #endif
    if P2 != "":
        LProgram = LProgram+" "+P2
        LProgramARG = GITCommand + " " + P2
    #endif
    LUSupport.LogAdd(LUConst.Log, LUConst.LogFile, "I", LProgram)

    LUSupport.WriteLN ("w/n",  LProgram)

    #Shell Program

    result = subprocess.run([ProgramGIT, LProgramARG], capture_output=True, text=True, check=True)
    #print("stdout:", result.stdout)
    #print("stderr:", result.stderr)
    #print(result.check_returncode())

    #result = subprocess.Popen([ProgramGIT, GITCommand, P1, P2, P3, P4, P5])

    LUSupport.LogAdd(LUConst.Log, LUConst.LogFile, "I", " ")
    #if @Error > 0
    #    Display_Error(@Error)
    #endif
#EndFunction

#-------------------------------------------------
# ClearParam ():
#-------------------------------------------------
def ClearParam ():
    global GITCommand
    global P1
    global P2
#beginFunction
    GITCommand = ""
    P1 = ""
    P2 = ""
#EndFunction

#-------------------------------------------------
# Command_git_init ():
#-------------------------------------------------
def Command_git_init ():
    global GITCommand
    global P1
    global P2
#beginFunction
    GITCommand = "init"
    P1 = ""
    P2 = ""
    RUN_GIT ()
    ClearParam ()
#EndFunction

#-------------------------------------------------
# Command_git_status ():
#-------------------------------------------------
def Command_git_status ():
    global GITCommand
    global P1
    global P2
#beginFunction
    GITCommand = "status"
    P1 = ""
    P2 = ""
    RUN_GIT ()
    ClearParam ()
#EndFunction

#-------------------------------------------------
# Command_ERROR_add_files ():
#-------------------------------------------------
def Command_ERROR_add_files ():
#beginFunction
    os.system('CLS')
    LUSupport.WriteLN ("w/n",  APP+" "+GITCommand)
    LUSupport.WriteLN ("w/n",  "A|<files>|<dir>")
    LUSupport.WriteLN ("w/n",  "")
    #git add . добавляет в индекс все файлы.
#EndFunction

#-------------------------------------------------
# Command_git_add ():
#-------------------------------------------------
def Command_git_add ():
    global GITCommand
    global P1
    global P2
#beginFunction
    GITCommand = "add"
    P1_s = "A|<files>|<dir>"
    Command_ERROR_add_files()
    P1 = LUSupport.ReadParam (P1_s+"|Q","")
    if P1.upper () != "Q":
       RUN_GIT ()
    #endwhile
    ClearParam ()
#EndFunction

#-------------------------------------------------
# Command_ERROR ():
#-------------------------------------------------
def Command_ERROR ():
#beginFunction
    #os.system('CLS')
    LUSupport.WriteLN ("w/n",  "Команды системы")
    LUSupport.WriteLN ("w/n",  "1. git init")
    LUSupport.WriteLN ("w+/n", "   ...")
    LUSupport.WriteLN ("w/n",  "2. git add .|<FileName>")
    LUSupport.WriteLN ("w+/n", "   ...")
    LUSupport.WriteLN ("w/n",  "3. git status")
    LUSupport.WriteLN ("w+/n", "   ...")
    LUSupport.WriteLN ("w/n",  "4. git commit -a -m <Комментарий>")
    LUSupport.WriteLN ("w+/n", "   ...")
    LUSupport.WriteLN ("w/n",  "5. ")
    LUSupport.WriteLN ("w+/n", "   ...")
    LUSupport.WriteLN ("w/n",  "6. ")
    LUSupport.WriteLN ("w+/n", "   ...")
    LUSupport.WriteLN ("w/n",  "7. ")
    LUSupport.WriteLN ("w+/n", "   ...")
    LUSupport.WriteLN ("w/n",  "8. ")
    LUSupport.WriteLN ("w+/n", "   ...")
    LUSupport.WriteLN ("w/n",  "9. ")
    LUSupport.WriteLN ("w+/n", "   ...")
    LUSupport.WriteLN ("w/n",  "A. ")
    LUSupport.WriteLN ("w+/n", "   ...")
    LUSupport.WriteLN ("w/n",  "Q. Выйти из программы")
    LUSupport.WriteLN ("w+/n", "   ...")
    LUSupport.WriteLN ("w+/n", "Введите команду: ")
#EndFunction

#-------------------------------------------------
# GIT ():
#-------------------------------------------------
def GIT ():
#beginFunction
    Done = False
    while not Done:
        Command_ERROR()
        Command: str = input()
        c = Command.upper()
        match c:
            case "1":
                Command_git_init()
            case "2":
                Command_git_add()
            case "3":
                Command_git_status()
            case "Q":
                Done = True
        #endmatch
    #endwhile
#EndFunction

#------------------------------------------
# main ():
#------------------------------------------
def main ():
#beginfunction
    print (LUConst.Userid)
    print ("Кодировка")
    #print ('PYDir   = '+PYDir)
    print ('Log     = ',LUConst.Log)
    GIT()
#endfunction

#------------------------------------------
#
#------------------------------------------
#beginmodule
if __name__ == "__main__":
    main()
#endif

#endmodule

                    
