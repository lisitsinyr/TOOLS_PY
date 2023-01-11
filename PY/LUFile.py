#===============================================================
# LUFile.kxl
#===============================================================
# UnPack   ($FileName)
# BacDirs  ($ASourcePath, $ADestPath, $ACheckSize)
# BacFiles ($ASourcePath, $ADestPath, $AMask, $ACheckSize, optional $ADestPathDelta, optional $Delete, optional $OverwriteNewer)
# BacFile  ($ASourcePath, $ADestPath, $AMask, $ACheckSize, optional $ADestPathDelta, optional $Delete, optional $OverwriteNewer)
# SyncFile ($Array, optional $Delete, optional $OverwriteNewer)
# FileVersion ($File)
# Associate($Extension, $Type, $Description, $OCmd, OPTIONAL $ECmd, OPTIONAL $AddFlag, OPTIONAL $System)
# CreateLink ($CommandLine, $Name, $IconFile, $IconIndex, $WorkDir, $Minimize, $Replace, $RunInOwnSpace)
# CreateLinkLU ($shortcutname,$targetpath,optional $arguments, optional $startdir, optional $iconpath, optional $style,optional $description)
# wshShortCut($shortcutname,$targetpath,optional $arguments, optional $startdir, optional $iconpath, optional $style,optional $description)
# DelDir($Pathname, $Log, $LogFile)
# GetFileName($filespec)
# GetFileNameWithoutExt($filespec)
# GetFileExt($filespec)
# GetFilePath($filespec, optional $seg)
# Function PathSplit($Path)
#---------------------------------------------------------------------------------------------
# shellcmd($commandstring, optional $forcewait)
# UnPackFile($FileName)
# UnPack($FileName)
# function FileAction($file,$action)
# RegServer ($ADestPath, $AServer, optional $ASourcePath)
# Cat($Filename)
# CheckDestFileName ($FileName, $DestPath, $NLimit)
#---------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  BacDirs ($ASourcePath, $ADestPath, $ACheckSize)
#-------------------------------------------------------------------------------
function BacDirs ($ASourcePath, $ADestPath, $ACheckSize)
#begin
   IF $LSourcePath = 0
      if IsDeclared ($ASourcePath)
         $LSourcePath = $ASourcePath
      else
         Exit 1
      #endif
   #endif
   IF $LDestPath = 0
      if IsDeclared ($ADestPath)
         $LDestPath = $ADestPath
      else
         Exit 1
      #endif
   #endif
   $LMask = "*.*"
   if IsDeclared ($ACheckSize)
      $LCheckSize = $ACheckSize
   else
      $LCheckSize = False
   #endif

   $LFile = Dir ($ASourcePath+"\\"+$LMask)
   WHILE @ERROR = 0 AND $LFile
      IF $LFile <> "." AND $LFile <> ".."
         IF GetFileAttr ($ASourcePath + "\\" + $LFile) & 16    # is it a directory ?
            $LSourcePath = $ASourcePath
            $LDestPath = $ADestPath

            $LSourcePath = $ASourcePath + "\\" + $LFile
            $LDestPath = $ADestPath + "\\" + $LFile

            BacDirs($LSourcePath, $LDestPath, $ACheckSize)

            $ASourcePath = $LSaveLSourcePath
            $ADestPath = $LSaveLDestPath
         else
            $LFileNameSource = $ASourcePath + "\\" + $LFile
            $LFileNameDest = $ADestPath + "\\" + $LFile
            IF 0=EXIST($ADestPath)
               MD $ADestPath
            #endif
            $LCopy = False
            $LResult = CompareFileTimes($LFileNameSource, $LFileNameDest)
            if $Result = 1 Or $LResult = -3
               $LCopy = True
            else
               $LFileSizeSource = GetFileSize ($LFileNameSource)
               $LFileSizeDest = GetFileSize ($LFileNameDest)
               if ($LCheckSize=True) and ($LFileSizeSource<>$LFileSizeDest)
                  $LCopy = True
               #endif
            #endif
            if $LCopy = True
               ? $LFileNameSource+" => "+$LFileNameDest+" ..."
               Copy $LFileNameSource $LFileNameDest /r
            #endif
         #endif
      #endif
      if @ERROR = 0
         $LFile = Dir("")
      #endif
   loop
#endfunction

#---------------------------------------------------------------------------------------------
# DelDir($Pathname, optional $Log, optional $LogFile)
#---------------------------------------------------------------------------------------------
#DelDir() - Delete all files and subdirectories 
#  
#---------------------------------------------------------------------------------------------
Function DelDir($PathName, optional $Log, optional $LogFile)
#begin
   $Level = $Level + 1
   $FileName = Dir($PathName + "\\"+"*.*")
   While $FileName <> "" And @ERROR = 0
      If $FileName <> "." And $Filename <> ".."
         If (GetFileAttr($PathName + "\\" + $FileName) & 16)

            DelDir($PathName + "\\" + $FileName, $Log, $LogFile)

            SetFileAttr($PathName + "\\" + $FileName, 128)
         Else
            SetFileAttr($Pathname + "\\" + $Filename, 128)
            if $Debug
               if $Log LogAdd($Log,$LogFile,"I","Delete file ... "+$FileName) #endif
            #endif
            Del ($PathName + "\\" + $FileName)
         #endif
      #endif
      if @ERROR = 0
         $FileName = Dir("")
      #endif
   Loop
   $Level = $Level - 1
   if $Level > 0
      if $Debug
         if $Log LogAdd($Log,$LogFile,"I", "Delete dir  ... "+$PathName) #endif
      #endif
      Rd ($PathName + "\\" + $FileName)
   #endif
#endfunction

#-------------------------------------------------------------------------------
# ScanFile ($ASourcePath, $ADestPath, $AMask, optional $ACheckSize, optional $ADestPathDelta, optional $Delete, optional $ExecFunc, optional $ExecFuncPAR1, optional $OverwriteNewer)
#-------------------------------------------------------------------------------
function ScanFile ($ASourcePath, $ADestPath, $AMask, optional $ACheckSize, optional $ADestPathDelta, optional $Delete, optional $ExecFunc, optional $OverwriteNewer, optional $ExecFuncPAR1)
   Dim $LResult
#begin
   $LFile = Dir ($ASourcePath+"\\"+$AMask)

   IF EXIST($ADestPath)=0
      MD $ADestPath
   #endif

   if $ADestPathDelta
      IF EXIST($ADestPathDelta)=0
         MD $ADestPathDelta
      #endif
   #endif

   WHILE (@ERROR = 0) AND $LFile

      IF $LFile <> "." AND $LFile <> ".."

         $LAttr = GetFileAttr ($ASourcePath + "\\" + $LFile)

         if $Debug
            LogAdd ("3", $LogFile, "F", $ASourcePath+"\\"+$LFile+"_"+$LAttr, "w+/n")
         #endif

         IF ($LAttr & 16)=0
            $LFileNameSource = $ASourcePath + "\\" + $LFile
            $LFileSizeSource = GetFileSize ($LFileNameSource)
            $LFileTimeSource = GetFileTime ($LFileNameSource)
            $LFileNameDest   = $ADestPath + "\\" + $LFile
            if $ADestPathDelta
               $LFileNameDestDelta = $ADestPathDelta + "\\" + $LFile
            #endif

            #--------------------------------------------------------------------
            $LResult = CompareFileTimes($LFileNameSource, $LFileNameDest)
            if $Debug
               LogAdd ("3", $LogFile, "F", "LResult="+$LResult, "w+/n")
            #endif

            #--------------------------------------------------------------------
            # Check Result
            #--------------------------------------------------------------------
            $LCopy = False
            $LDelete = False
            if $Delete 
               if $LResult = -3
                  $LDelete = True
               #endif
            else
               if $LResult = -3
                  $LFileSizeDest = "new"
                  $LFileTimeDest = "new"
                  $LCopy = True
               else
                  $LFileSizeDest = GetFileSize ($LFileNameDest)
                  $LFileTimeDest = GetFileTime ($LFileNameDest)
                  if $LResult = 1 
                     $LCopy = True
                  else
                     if ($LResult = -1) and ($OverwriteNewer=1) 
                        $warnOWN = "More recent dest file " + $LFileNameDest + " is to be overwritten"
                        LogAdd ("3", $LogFile, "F", $warnOWN, "w+/n")
                        $LCopy = True
                     #endif
                     if ($ACheckSize=True) and ($LFileSizeSource<>$LFileSizeDest)
                        $LCopy = True
                     #endif
                  #endif
               #endif
            #endif

            #--------------------------------------------------------------------
            # Copy
            #--------------------------------------------------------------------
            if $LCopy = True
               $s = $LFileNameSource + " ("+$LFileSizeSource+"|"+$LFileTimeSource+")" + " => " +
                    $LFileNameDest   + " ("+$LFileSizeDest+"|"+$LFileTimeDest+")"
               LogAdd ("3", $LogFile, "F", $s, "w+/n")

               Copy $LFileNameSource $LFileNameDest /r /h

               if $ExecFunc

                  if $ExecFuncPAR1
                     $s1 = '$$Res = $ExecFunc ($$LFileNameSource, $$LFileNameDest, $$ExecFuncPAR1)'
                  else
                     $s1 = '$$Res = $ExecFunc ($$LFileNameSource, $$LFileNameDest)'
                  #endif

                  if $Debug
                     LogAdd ($Log, $LogFile, "I", $s1)
                  #endif
                  $ResExe = execute ($s1)
               #endif

               if $ADestPathDelta
                  $s = $s + " => " + $LFileNameDestDelta
                  if $Debug
                     LogAdd ("3", $LogFile, "F", $s)
                  #endif
                  Copy $LFileNameSource $LFileNameDestDelta /r
               #endif
            #endif

            #--------------------------------------------------------------------
            # Delete
            #--------------------------------------------------------------------
            if $LDelete = True
               $s = "Delete file "+$LFileNameSource + " ("+$LFileSizeSource+"|"+$LFileTimeSource+")"+" ..."
               LogAdd ("3", $LogFile, "F", $s, "w+/n")
               Del $LFileNameSource
            #endif

         #endif

      #endif

      if @ERROR = 0

         $LFile = Dir("")

         #if $Debug
         #   LogAdd ("3", $LogFile, "F", @SERROR+"_"+@ERROR+"_"+$LFile+"!", "w+/n")
         ##endif

      #endif

   loop
#endfunction

#-------------------------------------------------------------------------------
#  ScanDir ($ASourcePath, $ADestPath, $AMask, optional $ACheckSize, optional $ADestPathDelta, optional $Delete, optional $ExecFunc)
#-------------------------------------------------------------------------------
function ScanDir ($ASourcePath, $ADestPath, $AMask, optional $ACheckSize, optional $ADestPathDelta, optional $Delete, optional $ExecFunc, optional $OverwriteNewer, optional $ExecFuncPAR1)
#begin
   $LFile = Dir ($ASourcePath+"\*.*")
   WHILE @ERROR = 0 AND $LFile
      IF $LFile <> "." AND $LFile <> ".."
         IF GetFileAttr ($ASourcePath + "\\" + $LFile) & 16    # is it a directory ?

            $LSourcePath = $ASourcePath + "\\" + $LFile
            $LDestPath = $ADestPath + "\\" + $LFile
            if $ADestPathDelta
               $LDestPathDelta = $ADestPathDelta + "\\" + $LFile
               if $Debug
                  LogAdd ("3", $LogFile, "D", $LSourcePath+" => "+$LDestPath+" "+$LDestPathDelta)
               #endif
            else
               $LDestPathDelta = ""
            #endif

            ScanFile($LSourcePath, $LDestPath, $AMask, $ACheckSize, $LDestPathDelta, $Delete, $ExecFunc, $OverwriteNewer, $ExecFuncPAR1)
            ScanDir($LSourcePath, $LDestPath, $AMask, $ACheckSize, $LDestPathDelta, $Delete, $ExecFunc, $OverwriteNewer, $ExecFuncPAR1)
         #endif
      #endif
      if @ERROR = 0
         $LFile = Dir("")
      #endif
   loop
#endfunction

#-------------------------------------------------------------------------------
#  BacFiles ($ASourcePath, $ADestPath, $AMask, optional $ACheckSize, optional $ADestPathDelta, optional $Delete, optional $ExecFunc, optional $OverwriteNewer)
#-------------------------------------------------------------------------------
function BacFiles ($ASourcePath, $ADestPath, $AMask, optional $ACheckSize, optional $ADestPathDelta, optional $Delete, optional $ExecFunc, optional $OverwriteNewer, optional $ExecFuncPAR1)
#begin
   if ($ASourcePath <> "") and ($ADestPath <> "")
      if $Debug
         LogAdd ($Log, $LogFile, "I", "BacFiles: "+$ASourcePath+" => "+$ADestPath+" "+$AMask, "w+/n")
      #endif
      ScanFile($ASourcePath, $ADestPath, $AMask, $ACheckSize, $ADestPathDelta, $Delete, $ExecFunc, $OverwriteNewer, $ExecFuncPAR1)
      ScanDir ($ASourcePath, $ADestPath, $AMask, $ACheckSize, $ADestPathDelta, $Delete, $ExecFunc, $OverwriteNewer, $ExecFuncPAR1)
   #endif
#endfunction

#-------------------------------------------------------------------------------
#  BacFile ($ASourcePath, $ADestPath, $AMask, optional $ACheckSize, optional $ADestPathDelta, optional $Delete, optional $ExecFunc, optional $OverwriteNewer)
#-------------------------------------------------------------------------------
function BacFile ($ASourcePath, $ADestPath, $AMask, optional $ACheckSize, optional $ADestPathDelta, optional $Delete, optional $ExecFunc, optional $OverwriteNewer, optional $ExecFuncPAR1)
#begin
   if ($ASourcePath <> "") and ($ADestPath <> "")
      if $Debug
         LogAdd ($Log, $LogFile, "I", "BacFile: "+$ASourcePath+" => "+$ADestPath+" "+$AMask, "w+/n")
      #endif
      ScanFile($ASourcePath, $ADestPath, $AMask, $ACheckSize, $ADestPathDelta, $Delete, $ExecFunc, $OverwriteNewer, $ExecFuncPAR1)
   #endif
#endfunction

#-------------------------------------------------------------------------------
# SyncFile($Array, optional $Delete, optional $OverwriteNewer)
#-------------------------------------------------------------------------------
function SyncFile($Array, optional $Delete, optional $OverwriteNewer)
#begin
   #LogAdd($Log, $LogFile, "I", "Array="+UBound($Array))
   for Each $Item in $Array
      #LogAdd($Log, $LogFile, "I", "Item="+UBound($Item))
      if UBound($Item) > 0
         if ($Item[0] <> "") and ($Item[1] <> "")
            LogAdd($Log, $LogFile, "I", $Item[0]+"\\"+$Item[2]+" => "+$Item[1])
            #---------------------------------------
            #
            #---------------------------------------
            if UBound($Item) > 3
               if UCase($Item[3]) = "S"
                  #---------------------------------------
                  # with subdir
                  #---------------------------------------
                  if UBound($Item) > 4
                     BacFiles ($Item[0], $Item[1], $Item[2], True, , 0,  $Item[4], $OverwriteNewer, $Item[5])
                  else
                     BacFiles ($Item[0], $Item[1], $Item[2], True, , 0,  $Item[4], $OverwriteNewer,)
                  #endif
               else                                                             
                  if UBound($Item) > 4
                     BacFile  ($Item[0], $Item[1], $Item[2], True, , 0,  $Item[4], $OverwriteNewer, $Item[5])
                  else
                     BacFile  ($Item[0], $Item[1], $Item[2], True, , 0,  $Item[4], $OverwriteNewer,)
                  #endif
               #endif
            else
               if UCase($Item[3]) = "S"
                  #---------------------------------------
                  # with subdir
                  #---------------------------------------
                  BacFiles ($Item[0], $Item[1], $Item[2], True, , 0, , $OverwriteNewer,)
               else
                  BacFile  ($Item[0], $Item[1], $Item[2], True, , 0, , $OverwriteNewer,)
               #endif
            #endif
      
            #---------------------------------------
            #
            #---------------------------------------
            if $Delete
               LogAdd($Log, $LogFile, "I", "Delete ..."+$Item[1]+"\\"+$Item[2]+" "+$Item[0])
               if UCase($Item[3]) = "S"
                  #---------------------------------------
                  # with subdir
                  #---------------------------------------
                  BacFiles ($Item[1], $Item[0], $Item[2], , , 1, , $OverwriteNewer,)
               else
                  BacFile ($Item[1], $Item[0], $Item[2], , , 1, , $OverwriteNewer,)
               #endif
            #endif

         #endif   
      else
         #---------------------------------------------------
         LogAdd($Log, $LogFile, "I", $Item)
         #---------------------------------------------------
      #endif
   next
#endfunction

#-------------------------------------------------------------------------------
#  DelFile ($ASourcePath, $AMask, $Day)
#-------------------------------------------------------------------------------
function DelFile ($ASourcePath, $AMask, $Day)
   Dim $LResult
#begin
   $LFile = Dir ($ASourcePath+"\\"+$AMask)
   $L_Day = EncodeDate(@Year,@MonthNo,@MDayNo)
   WHILE @ERROR = 0 AND $LFile
      IF $LFile <> "." AND $LFile <> ".."
         IF (GetFileAttr ($ASourcePath + "\\" + $LFile) & 16)=0
            $LFileNameSource = $ASourcePath + "\\" + $LFile
            $LFileSizeSource = GetFileSize ($LFileNameSource)
            $LFileTimeSource = GetFileTime ($LFileNameSource)
            $Y = Val(SUBSTR($LFileTimeSource,1,4))
            $M = Val(SUBSTR($LFileTimeSource,6,2))
            $D = Val(SUBSTR($LFileTimeSource,9,2))
            $LFileDaySource = EncodeDate($Y,$M,$D)
            $LDel = 0
            if (($L_Day-$LFileDaySource) => $Day) $LDel = 1 #endif
            if $LDel
               Del $LFileNameSource
               LogAdd ("3", $LogFile, "I", "Delete "+$LFileNameSource+" "+$LFileTimeSource+" Error="+@ERROR+" "+@SError)
            #endif
         #endif
      #endif
      if (@ERROR = 0) or (@ERROR = 5)
         $LFile = Dir("")
      #endif
   loop
#endfunction

#-------------------------------------------------------------------------------
#  ListFile ($ASourcePath, $AMask, optional $OutFile, optional $Option, optional $FuncFile)
#-------------------------------------------------------------------------------
function ListFile ($ASourcePath, $AMask, optional $OutFile, optional $Option, optional $FuncFile)
   Dim $LResult
#begin
   if ($OutFile) and (UCase($OutFile) <> "CONSOLE")
      $HandleFile = FreeFileHandle
      $Res = Open ($HandleFile, $OutFile, 1+4)
   #endif

   $LDay = EncodeDate(@Year,@MonthNo,@MDayNo)
   $LFile = Dir ($ASourcePath+"\\"+$AMask)

   WHILE @ERROR = 0 AND $LFile
      IF $LFile <> "." AND $LFile <> ".."
         IF (GetFileAttr ($ASourcePath + "\\" + $LFile) & 16)=0
            $ListFile = $ListFile + 1
            $LFileNameSource = $ASourcePath + "\\" + $LFile
            $LFileSizeSource = GetFileSize ($LFileNameSource)
            $LFileTimeSource = GetFileTime ($LFileNameSource)

            if $OutFile
               if UCase($OutFile) = "CONSOLE"
                  select
                     case $Option = 1 or $Option = 11
                        ? $LFile
                     case $Option = 2 or $Option = 12
                        ? $LFileNameSource+" "+$LFileTimeSource+" "+$LFileSizeSource
                  endselect
               else
                  select
                     case $Option = 1 or $Option = 11
                        $Res = WriteLine ($HandleFile, $LFile+@CRLF)
                     case $Option = 2 or $Option = 12
                        $Res = WriteLine ($HandleFile, $LFileNameSource+" "+$LFileTimeSource+" "+$LFileSizeSource+" "+$ListFile+@CRLF)
                  endselect
               #endif
            #endif

            if $FuncFile
               $s = '$$Res = $FuncFile ($$ListFile, $$LFileNameSource, $$LFileTimeSource, $$LFileSizeSource)'
               $ResExe = execute ($s)
            #endif

            #--------------------------------------------------------------------------------
            #$Y = Val(SUBSTR($LFileTimeSource,1,4))
            #$M = Val(SUBSTR($LFileTimeSource,6,2))
            #$D = Val(SUBSTR($LFileTimeSource,9,2))
            #$LFileDaySource = EncodeDate($Y,$M,$D)
            #--------------------------------------------------------------------------------

         #endif
      #endif

      if (@ERROR = 0) or (@ERROR = 5)
         $LFile = Dir("")
      #endif
   loop

   if ($OutFile) and (UCase($OutFile) <> "CONSOLE")
      $Res = Close ($HandleFile)
   #endif

#endfunction

#-------------------------------------------------------------------------------
#  ListDir ($ASourcePath, $AMask, optional $OutFile, optional $Option, optional $FuncDir, optional $FuncFile)
#-------------------------------------------------------------------------------
function ListDir ($ASourcePath, $AMask, optional $OutFile, optional $Option, optional $FuncDir, optional $FuncFile)
#begin
   $Level = $Level + 1
   $DirCount = $DirCount + 1

   # $FileCount = ListFile($aSourcePath, $AMask, $OutFile, $Option, $FuncFile)

   if $Option = 10 or $Option = 11 or $Option = 12
      if ($OutFile) and (UCase($OutFile) <> "CONSOLE")
         $HandleDir = FreeFileHandle
         $Res = Open ($HandleDir, $OutFile, 1+4)
      #endif
      if $OutFile
         if UCase($OutFile) = "CONSOLE"
            ? $ASourcePath
         else
            $Res = WriteLine ($HandleDir, $ASourcePath+" "+$DirCount+@CRLF)
         #endif
      #endif
      if ($OutFile) and (UCase($OutFile) <> "CONSOLE")
         $Res = Close ($HandleDir)
      #endif
   #endif

   $LFile = Dir ($ASourcePath+"\*.*")
   WHILE @ERROR = 0 AND $LFile
      IF $LFile <> "." AND $LFile <> ".."
         IF GetFileAttr ($ASourcePath + "\\" + $LFile) & 16    # Это каталог....
            $LSourcePath = $ASourcePath + "\\" + $LFile

            $FileCount = ListFile($LSourcePath, $AMask, $OutFile, $Option, $FuncFile)
            if $FuncDir
               $s = '$$Res = $FuncDir ($$DirCount, $$LSourcePath, $$FileCount)'
               $ResExe = execute ($s)
            #endif

            ListDir ($LSourcePath, $AMask, $OutFile, $Option, $FuncDir, $FuncFile)

            $Level = $Level - 1
         #endif
      #endif
      if (@ERROR = 0) 
         $LFile = Dir("")
      #endif
   loop
#endfunction

#-------------------------------------------------------------------------------
#  DirFile ($ASourcePath, $AMask, optional $OutFile)
#-------------------------------------------------------------------------------
function DirFile ($ASourcePath, $AMask, optional $OutFile)
   Dim $LResult
#begin
   if $OutFile
      del $OutFile
      $Handle = FreeFileHandle
      Open ($Handle, $OutFile, 1+4)
   #endif
   $LDay = EncodeDate(@Year,@MonthNo,@MDayNo)
   $LFile = Dir ($ASourcePath+"\\"+$AMask)
   WHILE @ERROR = 0 AND $LFile
      IF $LFile <> "." AND $LFile <> ".."
         IF (GetFileAttr ($ASourcePath + "\\" + $LFile) & 16)=0
            $LFileNameSource = $ASourcePath + "\\" + $LFile
            $LFileSizeSource = GetFileSize ($LFileNameSource)
            $LFileTimeSource = GetFileTime ($LFileNameSource)
            if $OutFile
               WriteLine ($Handle, $LFile+@CRLF)
            #endif
            # LogAdd ("3", $LogFile, "I", $LFile)
         #endif
      #endif
      if (@ERROR = 0) or (@ERROR = 5)
         $LFile = Dir("")
      #endif
   loop
   if $OutFile
      Close ($Handle)
   #endif
#endfunction


#-------------------------------------------------------------------------------
# FileVersion ($File)
#-------------------------------------------------------------------------------
function FileVersion($File)
   dim $a[12], $b[12], $c
#begin
   $a='Comments','CompanyName','FileDescription','FileVersion','InternalName',
      'Language','LegalCopyright','LegalTrademarks','OriginalFilename','PrivateBuild',
      'ProductName','ProductVersion','SpecialBuild'
   if exist($File)
      for $c=0 to ubound($a)
         $b[$c]=getfileversion($sFile,$a[$c])
      next
   else
      exit 2
   #endif
   $FileVersion=$b
#endfunction

#-------------------------------------------------------------------------------
# Associate($Extension, $Type, $Description, $OCmd, OPTIONAL $ECmd, OPTIONAL $AddFlag, OPTIONAL $System)
#-------------------------------------------------------------------------------
Function Associate($Extension, $Type, $Description, $OCmd, OPTIONAL $ECmd, OPTIONAL $AddFlag, OPTIONAL $System)
#begin
   # make sure the "dot" is specified
   If Left($Extension, 1) <> "."
      $Extension = "." + $Extension
   #endif

   # insure that "$System" has the right format if it's specified
   If $Server <> ""
      If Left($System,2) <> "\\" $System = "\\" + $System #endif
      If Right($System,1) <> "\\" $System = $System + "\\" #endif
   #endif

   # Obtain the Windows System Path value from the target system
   $WSPath = ReadValue($System + "HKEY_Local_Machine\SOFTWARE\Microsoft\Windows NT\CurrentVersion", "SystemRoot")

   # Define the Extension
   $RTN = DelTree($System + "HKEY_CLASSES_ROOT\\" + $Extension)
   $RTN = AddKey($System + "HKEY_CLASSES_ROOT\\" + $Extension)
   $RTN = WriteValue($System + "HKEY_CLASSES_ROOT\\" + $Extension, "", $Type, "REG_SZ")

   # just return if we're adding a new Extension to an existing association
   If $AddFlag = 0
      Exit 0
   #endif

   # Create the definitions for the OPEN command
   $RTN = DelTree($System + "HKEY_CLASSES_ROOT\\" + $Type)
   $RTN = AddKey($System + "HKEY_CLASSES_ROOT\\" + $Type)
   $RTN = AddKey($System + "HKEY_CLASSES_ROOT\\" + $Type + "\DefaultIcon")
   $RTN = AddKey($System + "HKEY_CLASSES_ROOT\\" + $Type + "\Shell")
   $RTN = AddKey($System + "HKEY_CLASSES_ROOT\\" + $Type + "\Shell\Open")
   $RTN = AddKey($System + "HKEY_CLASSES_ROOT\\" + $Type + "\Shell\Open\Command")
   
   $RTN = WriteValue($System + "HKEY_CLASSES_ROOT\\" + $Type, "", $Description, "REG_SZ")
   $RTN = WriteValue($System + "HKEY_CLASSES_ROOT\\" + $Type + "\DefaultIcon", "", $WSPath + "\system32\SHELL32.dll,21", "REG_SZ")
   $RTN = WriteValue($System + "HKEY_CLASSES_ROOT\\" + $Type + "\Shell\Open\Command", "", $OCmd, "REG_EXPAND_SZ")

   # Create the association for the EDIT command, if specified
   If $ECmd <> ""
      $RTN = AddKey($System + "HKEY_CLASSES_ROOT\\" + $Type + "\Shell\Edit")
      $RTN = AddKey($System + "HKEY_CLASSES_ROOT\\" + $Type + "\Shell\Edit\Command")
      $RTN = WriteValue($System + "HKEY_CLASSES_ROOT\\" + $Type + "\Shell\Edit\Command", "", $ECmd, "REG_EXPAND_SZ")
   #endif
#endfunction

#----------------------------------------------------------------------------
# CreateLink ($CommandLine, $Name, $IconFile, $IconIndex, $WorkDir, $Minimize, $Replace, $RunInOwnSpace)
#----------------------------------------------------------------------------
#  $Minimize      = [0,1]   
#  $Replace       = [0,1]   
#  $RunInOwnSpace = [0,1]   
#----------------------------------------------------------------------------
function CreateLink ($CommandLine, $Name, $IconFile, $IconIndex, $WorkDir, $Minimize, $Replace, $RunInOwnSpace)
#begin
   $CreateLink = AddProgramItem ($CommandLine, $Name, $IconFile, $IconIndex, $WorkDir, $Minimize, $Replace, $RunInOwnSpace)
#endfunction

#----------------------------------------------------------------------------
# CreateLinkLU ($Links, $DestPath, $name, $targetpath, optional $arguments, optional $startdir, optional $iconpath, optional $style, optional $description)
#----------------------------------------------------------------------------
function CreateLinkLU($Links, $DestPath, $name, $targetpath, optional $arguments, optional $startdir, optional $iconpath, optional $style, optional $description)
#begin
   $s = '$links -f "$targetpath" -a "$arguments" -w "$startdir" -i "$iconpath" -d "$DestPath" -n "$Name"'
   # ? $s
   Shell $s
   $CreateLinkLU = 0
#endfunction

#---------------------------------------------------------------------------------
# wshShortCut($shortcutname,$targetpath,optional $arguments, optional $startdir, optional $iconpath, optional $style, optional $description)
#---------------------------------------------------------------------------------
function wshShortCut($shortcutname, $CommandFile, optional $arguments, optional $startdir, optional $iconpath, optional $style, optional $description)
   dim $shell, $desktop, $shortcut, $index, $iconinfo, $iconindex, $scdir, $pif
#begin
   $shell = createobject("wscript.shell")
   $wshshortcut=""
   if $shell
      if ucase(right($shortcutname,4))=".URL" or ucase(right($shortcutname,4))=".LNK"
         #do nothing
      else
         if ucase(left($CommandFile,5))="HTTP:" or ucase(left($CommandFile,6))="HTTPS:" or ucase(left($CommandFile,4))="FTP:"
            $shortcutname=$shortcutname + ".url"
         else
            $shortcutname=$shortcutname + ".lnk"
         #endif
      #endif

      if instr($shortcutname,".lnk") and not exist($CommandFile)
         exit 2
      #endif

      if instr($shortcutname,"\\")=0
         $Desktop = $shell.SpecialFolders("Desktop")
         $shortcutname=$desktop + "\\" + $shortcutname
      else
         $scdir=substr($shortcutname,1,instrrev($shortcutname,"\\"))
         if not exist($scdir)
            md $scdir
            if @error
               exit @error
            #endif
         #endif
      #endif

      select
         case (@ProductType = "Windows 98") or (@ProductType = "Windows 95")
            if instr($shortcutname,".lnk")
               $pif=substr($shortcutname,1,instrrev($shortcutname,".lnk")-1)+".pif"
               if Exist ($pif)
                  Del ($pif)
               #endif 
            #endif
         case 1
            if Exist ($shortcutname)
               Del ($shortcutname)
            #endif 
      EndSelect

      $shortcut = $shell.createshortcut($shortcutname)
      if $shortcut
         $shortcut.targetpath = $CommandFile
         if $iconpath
            $shortcut.iconlocation = $iconpath
         #endif
         if $arguments
            $shortcut.arguments = $arguments
         #endif
         if $startdir
            $shortcut.workingdirectory = $startdir
         #endif
         if $style
            $shortcut.windowstyle = $style
         else
            $shortcut.windowstyle = 1
         #endif
         If $description
            $shortcut.description = $description
         else
            $shortcut.description = ""
         #endif
         $shortcut.save
         if @error
            exit @error
         #endif
         if instrrev($shortcutname,".url") and $iconpath
            $index=instrrev($iconpath,",")
            if $index=0
               $iconindex=0
            else
               $iconindex=split($iconpath,",")[1]
               $iconpath=split($iconpath,",")[0]
            #endif
            $=writeprofilestring($shortcutname,"InternetShortcut","IconFile",$iconpath)
            $=writeprofilestring($shortcutname,"InternetShortcut","IconIndex",$iconindex)
         else
         #endif
         #$wshshortcut=$shortcut.FullName
         $wshshortcut = 0
         $shortcut = 0
      else
         exit @error
      #endif 
   else
      exit @error
   #endif 
#endfunction 

#-------------------------------------------------------------------------------
# GetFileName($filespec)
#-------------------------------------------------------------------------------
function GetFileName($filespec)
   dim $bash
   $GetFileName=$filespec
   $bash=instrRev($filespec,"\\")
   if $bash or instrRev($filespec,'.')
      $GetFileName=substr($filespec,$bash+1)
   #endif
#endfunction

#-------------------------------------------------------------------------------
# GetFileNameWithoutExt($filespec)
#-------------------------------------------------------------------------------
function GetFileNameWithoutExt($filespec)
   dim $bash
   $GetFileNameWithoutExt = $filespec
   $bash1 = instrRev($filespec,"\\")
   $bash2 = instrRev($filespec,'.')
   select
      case $bash1 and $bash2
         $GetFileNameWithoutExt = substr($filespec, $bash1+1, $bash2-$bash1-1)
      case $bash1 and (not $bash2)
         $GetFileNameWithoutExt = substr($filespec, $bash1+1)
      case (not $bash1) and $bash2
         $GetFileNameWithoutExt = substr($filespec, $bash1+1, $bash2-$bash1-1)
   endselect
#endfunction

#---------------------------------------------------------------------------------------------
# GetFileExt($filespec)
#---------------------------------------------------------------------------------------------
function GetFileExt($filespec)
   dim $dot
   $GetFileExt=''
   $dot=instrRev($filespec,'.')
   if $dot
      $GetFileExt=substr($filespec,$dot+1)
   #endif
#endfunction

#---------------------------------------------------------------------------------------------
# GetFilePath($filespec, optional $seg)
#---------------------------------------------------------------------------------------------
function GetFilePath($filespec, optional $seg)
#begin
   if instr($filespec,"\\")
      $getfilepath=split($filespec,"\\")
      redim preserve $getfilepath[ubound($getfilepath)-1]
      if not val($seg)
         $getfilepath=join($getfilepath,"\\")
      #endif
   else
      $getfilepath=""
  #endif
#endfunction

#---------------------------------------------------------------------------------------------
# compress($file,$targetfile,optional $mode)
#---------------------------------------------------------------------------------------------
function compress($file,$targetfile,optional $mode)
 dim $,$f,$raw,$pal[0],$_,$s,$mo,$e,$c,$a,$o1,$o2,$i,$lf,$b
 $lf=chr(10) $b=chr(1)
 $f=freefilehandle
 $=open($f,$file)
 if @error exit @error #endif
 do $raw=$raw+$lf+readline($f) until @error
 $=close($f)
 $raw=split($raw,$lf)
  $f=freefilehandle
  $=open($f,$targetfile,5)
  if @error exit @error #endif
 if $mode
  $mo=", $$ .*+-/<>()=&@@?|[]'"+'"#'
  $raw[0]="KXc"
  for $a=1 to ubound($raw)
   $=""
   $i=$raw[$a] $_=len($i) $!=0
   do $!=$!+1
    $c=substr($i,$!,1)
    select
     case $c=""
     case $c="'" $o1=iif($o1 or $o2,0,1) $=$+$c
     case $c='"' $o2=iif($o2 or $o1,0,1) $=$+$c
     case $c="#" if $o1 or $o2 $=$+$c else $!=$_ #endif
     case instr($mo,$c) $=$+$c
     case 1
      $s="" do $s=$s+$c $!=$!+1 $c=substr($i,$!,1) until instr($mo,$c) or $!>$_ $!=$!-1
      $e=ascan($pal,$s)
      if -1=$e
       $e=ubound($pal)+1
       redim preserve $pal[$e]
       $pal[$e]=$s
      #endif
      $=$+$e
    endselect
   until $!=>$_
   $raw[$a]=$
  next
  $=writeline($f,join($raw)+$lf+join($pal))
 else
  if 3<>ubound($raw) exit 13 #endif
  $pal=split($raw[2]) $raw=substr($raw[1],4)
  $mo="0123456789"
  for $=0 to len($raw)
   $!=substr($raw,$,1)
   if instr($mo,$!)
    $s="" do $s=$s+$! $=$+1 $!=substr($raw,$,1) until not instr($mo,$!) or @error
    $_=$_+$pal[$s]
    $=$-1
   else
    $_=$_+$!
   #endif
  next
  $=writeline($f,$_)
 #endif
  $=close($f)
#endfunction

#--------------------------------------------------------------------------------
# DeleteFF($strPath, $strMethod, Optional $blnForce)
#--------------------------------------------------------------------------------
Function DeleteFF($strPath, $strMethod, Optional $blnForce)
    $strFSO                                        = "Scripting.FileSystemObject"
    If KeyExist("HKCR\\" + $strFSO) = 0
        $Tmp = MessageBox("Object " + $strFSO + " is not installed !", "Error", 16)
        Return
    Else
        $objFSO                                    = CreateObject($strFSO)
        If @Error <> 0
            $Tmp = MessageBox("Object " + $strFSO + " can not be created !", "Error", 16)
            Return
        #endif
    #endif
    If Len($strPath) > 0
    And Exist($strPath) = 1
        ? "Deleting " + $strMethod + " " + $strPath
        Select
            Case $strMethod = "File"
                $Tmp                               = $objFSO.DeleteFile($strPath, $blnForce)
                $DeleteFF                          = @Error
            Case $strMethod = "Folder"
                $Tmp                               = $objFSO.DeleteFolder($strPath, $blnForce)
                $DeleteFF                          = @Error
            Case $strMethod = "Content"
                $strContent                        = Dir($strPath)
                While Len($strContent) > 0
                And @Error = 0
                    If $strContent <> "."
                    And $strContent <> ".."
                        If GetFileAttr($strPath + "\\" + $strContent) & 16
                            $Tmp                   = $objFSO.DeleteFolder($strPath + "\\" + $strContent, $blnForce)
                        Else
                            $Tmp                   = $objFSO.DeleteFile($strPath + "\\" + $strContent, $blnForce)
                        #endif
                        $DeleteFF                  = @Error
                    #endif
                    $strContent                    = Dir()
                Loop
            Case 1
                Return
        EndSelect
    Else
        ? $strMethod + " " + $strPath + " doesn't exist."
    #endif
#endfunction

#--------------------------------------------------------------------------------
# DriveEnum(optional $filter)
#--------------------------------------------------------------------------------
function DriveEnum(optional $filter)
   dim $fso, $Drive
#begin
   $fso = CreateObject("Scripting.FileSystemObject")
   if $fso
      for each $Drive in $fso.Drives
         if instr($filter,$Drive.DriveType) or $filter=""
            $DriveEnum = $DriveEnum+$Drive.DriveLetter+" "
         #endif
      next
      $DriveEnum=left($DriveEnum,len($DriveEnum)-1)
      $fso=""
   #endif
#endfunction

#--------------------------------------------------------------------------------
# FileOwner($file)
#--------------------------------------------------------------------------------
function FileOwner($file)
   dim $,$f
#begin
   if not exist($file) exit 2 #endif
   $f=split($file,"\\")
   $file=$f[ubound($f)]
   $f[ubound($f)]=""
   $f=join($f,"\\")
   $=createobject("shell.application")
   if 9<>vartype($) exit 120 #endif
   $FileOwner=$.namespace($f).getdetailsof($.namespace($f).parsename($file),8)
#endfunction

#--------------------------------------------------------------------------------
# fileprops($folder)
#--------------------------------------------------------------------------------
FUNCTION fileprops($folder)
$folderspec = $folder
$fs = CreateObject("Scripting.FileSystemObject")
##$f = $fs.GetFolder(server.mappath($folderspec))
$f = $fs.getfolder($folderspec)
$fc = $f.files
?"File List"
FOR EACH $list IN $fc
?"Name is: " + $list.name
?"File Type: " + $list.type
?"Last Modfied: " + $list.datelastmodified
?"Last Accessed: " + $list.datelastaccessed
$result = GetFileAttr( $list.name ) $attr=""
IF $result & 4096 $attr=$attr+"Offline " 
#endif
IF $result & 2048 $attr=$attr+"compressed " 
#endif
IF $result & 1024 $attr=$attr+"Reparse point " 
#endif
IF $result & 512 $attr=$attr+"Sparse file " 
#endif
IF $result & 256 $attr=$attr+"Temporary " 
#endif
IF $result & 128 $attr=$attr+"Normal " 
#endif
IF $result & 64 $attr=$attr+"Encrypted " 
#endif
IF $result & 32 $attr=$attr+"Archive " 
#endif
IF $result & 16 $attr=$attr+"Directory " 
#endif
IF $result & 4 $attr=$attr+"System " 
#endif
IF $result & 2 $attr=$attr+"Hidden " 
#endif
IF $result & 1 $attr=$attr+"Read only" 
#endif
?"Attributes: $result " + $attr
?
NEXT

$fs = ""
$f = ""
$ = ""
#endfunction

#--------------------------------------------------------------------------------
# fnGetFolderProp($sFldr,$sProp)
#--------------------------------------------------------------------------------
Function fnGetFolderProp($sFldr,$sProp)
   Dim $objFSO, $objFldr, $nul
#begin
   $objFSO = CreateObject("Scripting.FileSystemObject")
   If Not VarType($objFSO)=9 Exit 1 #endif
   $objFldr = $objFSO.GetFolder($sFldr)
   If Not VarType($objFldr)=9 Exit 3 #endif
   $nul=Execute("$$fnGetFolderProp = $$objFldr."+$sProp)
   If VarType($fnGetFolderProp)=0 Exit 87 #endif
#endfunction 

#--------------------------------------------------------------------------------
# fnGetFileProp($sFile,$sProp)
#--------------------------------------------------------------------------------
Function fnGetFileProp($sFile,$sProp)
   Dim $objFSO, $objFile, $nul
#begin
   $objFSO = CreateObject("Scripting.FileSystemObject")
   If Not VarType($objFSO)=9 Exit 1 #endif
   $objFile = $objFSO.GetFile($sFile)
   If Not VarType($objFile)=9 Exit 2 #endif
   $nul=Execute("$$fnGetFileProp = $$objFile."+$sProp)
   If VarType($fnGetFileProp)=0 Exit 87 #endif
#endfunction 

#--------------------------------------------------------------------------------
# fnMapped($sUNC)
#--------------------------------------------------------------------------------
Function fnMapped($sUNC)
Dim $oDrives,$oDrive
$oDrives = CreateObject("Scripting.FileSystemObject").Drives
If Not VarType($oDrives) & 9 Exit 1 #endif
For Each $oDrive in $oDrives
If $oDrive.DriveType = 3 AND $sUNC = $oDrive.ShareName
$fnMapped = $oDrive.DriveLetter + ":"
#endif
Next
#endfunction 

#--------------------------------------------------------------------------------
# fullfile($path1, optional $path2)
#--------------------------------------------------------------------------------
function fullfile($path1, optional $path2)
  Dim $a, $path3

  $a=ubound($path1)
  if $a>0
    $path3=$path1[$a]
    redim preserve $path1[$a-1]
    $path1=fullfile($path1,$path3)
  #endif

  if ubound($path1)=0
    $path1=$path1[0]
  #endif
  if right($path1,1)="\\"
    $path1=left($path1,len($path1)-1)
  #endif

  if $path2
    if left($path2,1)="\\"
      $path2=right($path2,len($path2)-1)
    #endif
    $fullfile=lcase($path1+"\\"+$path2)
  else
    $fullfile=$path1
  #endif

#endfunction

#--------------------------------------------------------------------------------
# ($sSrc, $sDest, OPTIONAL $lFlags, OPTIONAL $bMove)
#--------------------------------------------------------------------------------
Function GUICopy($sSrc, $sDest, OPTIONAL $lFlags, OPTIONAL $bMove)
   Dim $sVer,$objShell,$objFldr
#begin
   If Not Exist($sSrc) Exit 2 #endif
   If Not Exist($sDest) Exit 3 #endif
   If @INWIN=1
      $sVer=GetFileVersion(%WINDIR%+"\System32\Shell32.dll","FileVersion")
   Else
      $sVer=GetFileVersion(%WINDIR%+"\System\Shell32.dll","FileVersion")
   #endif
   If $sVer<"4.71" Exit 10 #endif
   $objShell=CreateObject("Shell.Application")
   $objFldr=$objShell.NameSpace($sDest)
   If @ERROR<0 Exit VAL("&"+Right(DecToHex(@ERROR),4)) #endif
   Select
      Case $bMove=1 $objFldr.MoveHere($sSrc,$lFlags)
      Case $bMove=0 $objFldr.CopyHere($sSrc,$lFlags)
      Case 1 Exit 87
   EndSelect
   If @ERROR<0 Exit VAL("&"+Right(DecToHex(@ERROR),4)) #endif
   Exit @ERROR
#endfunction 

#--------------------------------------------------------------------------------
# GUIDialog($_title, optional $_root, optional $_mode)
#--------------------------------------------------------------------------------
function GUIDialog($_title, optional $_root, optional $_mode)
   dim $LShell
#begin
   $GUIDialog = ""
   $LShell = createobject("shell.application")
   $ObjFolder = $LShell.BrowseForFolder(0, $_title, 0+$_mode, $_root)
   $LPath = $ObjFolder.Self.Path
   $LName = $ObjFolder.Self.Name
   $GUIDialog = $LPath+" "+$LName
   #$GUIDialog = $ObjFolder.Title
   if not len($GUIDialog) exit 1 #endif
#endfunction

#--------------------------------------------------------------------------------
# InPath(Optional $Exe, Optional $Concat)
#--------------------------------------------------------------------------------
Function InPath(Optional $Exe, Optional $Concat)
Dim $Path,$i,$Error
$InPath=''
$Error=3 # Path not found

If ''+$Exe<>''
$Path=Split('%Path%','#')
For $i=0 To UBound($Path)
If $Path[$i]<>'' And Exist($Path[$i]+"\\"+$Exe)=1
If Not $ConCat
$InPath=$Path[$i]
Else
$InPath=$Path[$i]+"\\"+$Exe
#endif

$Error=0
$i=UBound($Path)
#endif
Next
Else
$Error=1
#endif

Exit $Error
#endfunction 

#--------------------------------------------------------------------------------
# insertline($a, $b, optional $c, optional $d)
#--------------------------------------------------------------------------------
Function insertline($a, $b, optional $c, optional $d)
   Dim $e,$f,$h,$x,$y
#begin
   If $b<0 Exit -3 #endif
   If $c="" $d=1 #endif
   $f="%temp%\~kixil00.tmp" # temporary file to use
   Del $f
   If $d<>1 $d=0 #endif
   $e=FreeFileHandle
   $insertline=-2
   If $e=0 Exit -2 #endif
   $insertline=Open($e,$a)
   If $insertline<>0 Exit @Error #endif
   $h=FreeFileHandle
   If $h=0
      $insertline=-2
      $x=Close($e)
      Exit -2 
   #endif
   $insertline=Open($h,$f,5)
   If $insertline<>0
      $x=Close($e)
      Exit @Error
   #endif
   If $b<>0
      For $x=0 To $b-1
         $y=ReadLine($e)
         If @Error<>0
            $x=Close($e)
            $x=Close($h)
            Del $f
            $insertline=-3
            Exit -3
         Else
            $insertline=WriteLine($h,$y+@Crlf)
         #endif
      Next
   #endif
   $insertline=WriteLine($h,$c)
   $y=ReadLine($e)
   If @Error<>0
      $x=Close($e)
      $x=Close($h)
      Del $f
      $insertline=-3
      Exit -3
   #endif
   If $d=0
      $x=WriteLine($h,$y+@Crlf)
   #endif
   $y=ReadLine($e)
   While @Error=0
      $insertline=Writeline($h,$y+@Crlf)
      $y=ReadLine($e)
   Loop
   $x=Close($e)
   $x=Close($h)
   Copy $f $a
   Del $f
   $insertline=0
   Exit 0
#endfunction

#--------------------------------------------------------------------------------
# IsStringInFile($filename,$string)
#--------------------------------------------------------------------------------
function IsStringInFile($filename,$string)

  $isstringinfile=0
  if $string=''
    exit 87
  #endif
  if not exist($filename)
    exit 2
  #endif

  shell '%COMSPEC% /e:1024 /c find /c /i "'+$string+'" "'+$filename+'" > nul'

  if @ERROR=0
    $IsStringInFile=1
  #endif
  exit 0
#endfunction

#--------------------------------------------------------------------------------
# MakeCab($Cab,$Files) 
#--------------------------------------------------------------------------------
function MakeCab($Cab,$Files) 
   dim $[0],$! 
   if exist($Cab) 
      exit 183 
   #endif 
   if 8=vartype($Files) 
      $[0]=$Files 
      $Files=$ 
   #endif 
   $maker=CreateObject("MakeCab.MakeCab.1") 
   if @error exit 120 
   #endif 
   $MakeCab=$Files 
   if instr(@producttype,"Windows XP")  
      $maker.CreateCab($Cab,0,0, not 1) 
   else  
      $maker.CreateCab($Cab,0,0) 
   #endif 
   for $=0 to ubound($Files)  
      if not exist($Files[$])   
         $MakeCab[$]=2  
      else   
         $!=split($Files[$],"\\")   
         $maker.AddFile($Files[$],$![ubound($!)])   
         if @error    
            $MakeCab[$]=156   
         else    
            $MakeCab[$]=0   
         #endif  
      #endif 
   next 
   $maker.closecab 
   if not ubound($MakeCab) 
      $=$MakeCab 
      $MakeCab=$[0] 
   #endif
#endfunction

#--------------------------------------------------------------------------------
# PathSplit($Path)
#--------------------------------------------------------------------------------
Function PathSplit($Path)
   Dim $Server, $Share, $Dir, $File, $Tag
#begin
   $Server='' $Share='' $Dir='' $fFle='' $Tag=0

   # Determine if we received a FilePath or DirectoryPath
   # add a "\\" if we have a DirectoryPath
   If Exist($Path) 
      If GetFileAttr($Path) & 16
         If Right($Path,1) <> "\\"
            $Path = $Path + "\\"
         #endif
      #endif
   #endif

   $arrDir=Split($Path,"\\")
   $UBound = UBound($arrDir)

   # Default - last element is FILE unless overridden
   $File = $arrDir[$UBound]

   Select
      # single element, no ".", assume DIRECTORY
      Case $UBound=0 And Not InStr($Path,'.')
         $Dir = $Path
         $File = ""

      # single element, contains a ":", assume DRIVE
      Case $UBound = 0 And InStr($arrdir[0],":")
         $Share = Left($arrDir[0],2)
         $File = Right($arrDir[0],Len($arrDir[0]) - 2)

      # single element, contains a ".", assume FILE
      Case $UBound = 0 And InStr($Path,'.')
         $File = $Path

      # multiple elements, first element contains ":", DRIVE
      Case Instr($arrDir[0],':')
         $Share = Split($arrDir[0],':')[0] + ':'
         $Dir = Split($arrDir[0],':')[1] + "\\"
         $File=$arrDir[$UBound]
         $Tag = 1

      # multiple elements, first two null, assume \\Server\Share
      Case $arrDir[0]='' And $arrDir[1]=''
         $Server = '\\' + $arrDir[2]
         $Share = "\\" + $arrDir[3]
         $Dir = "\\"
         $File = $arrDir[$ubound]
         $Tag = 4
   EndSelect

   For $Loop = $Tag to $UBound - 1 
      $Dir = $Dir + $arrDir[$loop] + "\\"
   Next

   $PathSplit = $Server, $Share, $Dir, $File

#endfunction

#--------------------------------------------------------------------------------
#Pipe() - Submits a shell command and redirects output to an array 
#--------------------------------------------------------------------------------
function pipe($command) 
   dim $i,$error,$line 
   dim $array[255] 
   dim $redim $redim = ubound($array) 
   dim $tempfile 
#begin
   $tempfile = "%temp%\pipe.tmp" 
   if exist("$tempfile")  del("$tempfile") #endif 
   if @inwin = 2 # win9x  shell '%comspec% /c $command >"$tempfile"' 
   else 
      # winnt  shell '%comspec% /c $command >"$tempfile" 2>nul' 
   #endif 
   $error=@error 
   if open(10,"$tempfile") = 0  $i=0  
   $line = readline(10)  while not @error   
   if $line    $array[$i] = $line    
   if $i = $redim     $redim=$redim*2     
   redim preserve $array[$redim]    
   #endif    $i=$i+1   #endif   
   $line = readline(10)  loop  
   $=close(10)  del "$tempfile"  
   if $i > 0   redim preserve $array[$i-1]   
   $pipe=$array  else   
   $pipe = 0  #endif  exit 
   $error else  $pipe = 0  
   exit @error #endif
#endfunction

#--------------------------------------------------------------------------------
# pipe2($command)
#--------------------------------------------------------------------------------
FUNCTION pipe2($command)
 DIM $error, $tempfile
 DIM $FSO, $oFile
#begin
 $tempfile = "%temp%\pipe.tmp"
 IF Exist($tempfile)  DEL $tempfile  #endif
 IF @inwin = 2 # win9x
   SHELL '%comspec% /c '+$command+' >"'+$tempfile+'"'
 ELSE # winnt
   SHELL '%comspec% /c '+$command+' >"'+$tempfile+'" 2>nul'
 #endif
 $error = @Error
 #
 $pipe = ""
 $FSO = CreateObject("Scripting.FileSystemObject")
 IF @Error <> 0  EXIT @Error  #endif
 $oFile = $FSO.OpenTextFile($tempfile,1,0)
 IF @Error = 0
   $pipe = SPLIT($oFile.ReadAll,@CRLF)
   $oFile = 0
   $FSO = 0
 #endif
 #
 DEL $tempfile
 EXIT $error
#endfunction

#--------------------------------------------------------------------------------
# RemotePath($path,optional $computer)
#--------------------------------------------------------------------------------
Function RemotePath($path,optional $computer)
#begin
   if not $computer   $computer = @wksta   #endif
   if left($computer,1)="\\"
      $computer=substr($computer,instrrev($computer,"\\")+1)
      #endif
   $RemotePath='\\'+$computer+"\\"+join(split($path,':'),chr(36))
#endfunction
 
#--------------------------------------------------------------------------------
# rename($0,$1,$2,optional $3)
#--------------------------------------------------------------------------------
function rename($0,$1,$2,optional $3)
 dim $
#begin
 $rename=0
 if 8<>vartype($0) | 8<>vartype($1) | 8<>vartype($2) $rename=87 exit 87 #endif
 if "\\"<>right($0,1) $0=$0+"\\" #endif
 if exist($0+$2) $rename=80 exit 80 #endif
 if instr($1,"\\") | instr($2,"\\") $rename=87 exit 87 #endif
 if vartype($3) $3=getfileattr($0+$1) $rename=setfileattr($0+$1,128) #endif
 if $rename exit $rename #endif
 $=createobject('shell.application')
 if vartype($)<>9 $rename=196 exit 196 #endif
 $0=$.namespace($0)
 if vartype($0)<>9 $rename=3 exit 3 #endif
 $1=$0.parsename($1)
 if vartype($1)<>9 $rename=2 exit 2 #endif
 $1.name=$2
 if @error $rename=val("&"+Right(DecToHex(@error),4)) exit $rename #endif
 if vartype($3) $rename=setfileattr($1.path,128) if $rename exit $rename #endif #endif
#endfunction

#--------------------------------------------------------------------------------
# shellcmd($commandstring, optional $forcewait)
#--------------------------------------------------------------------------------
function shellcmd($commandstring, optional $forcewait)
   Dim $rc
#begin
   if val($forcewait)
      $forcewait='start /min /wait '
   else
      $forcewait=''
   #endif
   if $commandstring <> ''
      $commandstring='%COMSPEC% /c '+$forcewait+$commandstring
      shell $commandstring
      $shellcmd=@ERROR
   else
      exit 87
   #endif
#endfunction

#--------------------------------------------------------------------------------
# udfPiper(optional $sCommand, optional $sKey)
#--------------------------------------------------------------------------------
Function udfPiper(optional $sCommand, optional $sKey)
   Dim $ret
#begin
   If $sKey="" $sKey="DEFAULT" #endif
   $sFullKey="HKEY_CURRENT_USER\SOFTWARE\KiXtart\Piper\$sKey"
   If $sCommand <> ""
      $ret=AddKey($sFullKey)
      If($ret) Exit $ret #endif
      $ret=WriteValue($sFullKey,"Status",0,"REG_DWORD")
      Run('piper $sKey "$sCommand"')
   Else
      $ret=ReadValue($sFullKey,"Status")
      If @ERROR @ERROR ": " @SERROR Exit @ERROR #endif
      While $ret <> 1
         If $ret=3 # All input drained.
            $ret=DelKey($sFullKey)
            Exit 1
         #endif
         $ret=ReadValue($sFullKey,"Status")
         If @ERROR @ERROR ": " @SERROR Exit @ERROR #endif
      Loop
      $udfPiper=ReadValue($sFullKey,"Input")
      $ret=WriteValue($sFullKey,"Status",2,"REG_DWORD")
   #endif
   Exit 0
#endfunction 

#--------------------------------------------------------------------------------
# udfPiperAbort(optional $sKey)
#--------------------------------------------------------------------------------
Function udfPiperAbort(optional $sKey)
#begin
   If $sKey="" $sKey="DEFAULT" #endif
   $sKey="HKEY_CURRENT_USER\SOFTWARE\KiXtart\Piper\$sKey"
   $ret=WriteValue($sKey,"Status",99,"REG_DWORD")
#endfunction

#--------------------------------------------------------------------------------
# GUICopy2($CMD, $Source, $Destination, OPTIONAL $Flags)
#--------------------------------------------------------------------------------
function GUICopy2($CMD, $Source, $Destination, OPTIONAL $Flags)
#begin
    If not $Flags $Flags=0 #endif
    If not exist($Source) Beep ? "Source does not exist." Exit (1) #endif
    If not exist($Destination) Beep ? "Destination does not exist." Exit (2) #endif
    $objShell=CreateObject("Shell.Application")
    $objFolder=$objShell.NameSpace($Destination)
    If not $objFolder Beep ? "Cannot create namespace. Incorrect Shell32.dll version." Exit (3) #endif
    Select
    Case $CMD="Copy" $objFolder.CopyHere($Source, $Flags)
    Case $CMD="Move" $objFolder.MoveHere($Source, $Flags)
    Case 1 Beep ? "GUICopy Syntax Incorrect. Use COPY or MOVE." $objShell=0 Exit (4)
    EndSelect
    $objShell=0
    Exit @error
#endfunction

#--------------------------------------------------------------------------------
#Function:  Pipe
#--------------------------------------------------------------------------------
function pipe3($command)
    dim $i,$error,$line
    dim $array[255]
    dim $redim $redim = ubound($array)
    dim $tempfile $tempfile = "%temp%\pipe.tmp"
    if exist("$tempfile")
        del("$tempfile")
    #endif
    if @inwin = 2 # win9x
        shell '%comspec% /c $command >"$tempfile"'
    else # winnt
        shell '%comspec% /c $command >"$tempfile" 2>nul'
    #endif
    $error=@error
    if open(10,"$tempfile") = 0
        $i=0
        $line = readline(10)
        while not @error
            if $line
                $array[$i] = $line
                if $i = $redim
                    $redim=$redim*2
                    redim preserve $array[$redim]
                #endif
                $i=$i+1
            #endif
            $line = readline(10)
        loop
        $=close(10)
        del "$tempfile"
        if $i > 0
            redim preserve $array[$i-1]
            $pipe=$array
        else
            $pipe = 0
        #endif
        exit $error
    else
        $pipe = 0
        exit @error
    #endif
#endfunction

#-------------------------------------------------------------------------------
# UnPackFile($FileName)
#-------------------------------------------------------------------------------
function UnPackFile($FileName)
   Dim $s,$f,$e,$a
#begin
   $s = GetFileName($FileName)
   $a = Split($s,".")
   $f = Join($a,".",UBound($a))
   $e = $a[UBound($a)]

   if Exist($f)
      DelDir ($f)
      RD "$f"
   #endif

   MD $f
   Copy "$FileName" "$f" /r
   CD $f
   select
      case UCase($e) = "ZIP"
         $ex = 'unzip "'+$f+'.'+$e+'"'
      case UCase($e) = "ARJ"
         $ex = 'arj x -y -v "'+$f+'.'+$e+'"'
      case UCase($e) = "RAR"
         $ex = 'unrar x -y "'+$f+'.'+$e+'"'
      case 1
         $ex = ""
   EndSelect
   if $ex
      "-----------------------------------------------" ?
      $ex ?
      "-----------------------------------------------" ?
      Shell $ex
      $Error = @error
      "-----------------------------------------------" ?
      "Error = " $Error ?
      if $Error = 0
         $s = $f+'.'+$e
         Del "$s"
      #endif
   else
      Del $FileName
   #endif
   CD ".."
#endfunction

#-------------------------------------------------------------------------------
# UnPack($FileName)
#-------------------------------------------------------------------------------
function UnPack($FileName)
#begin
   $LPath = GetFilePath($FileName)
   if $LPath <> ""
      $LPath = $LPath+"\\"
   #endif

   $LFile = Dir ($FileName)
   WHILE @ERROR = 0 AND $LFile
      IF $LFile <> "." AND $LFile <> ".."
         IF not (GetFileAttr ($LPath+$LFile) & 16)    # is it a directory ?
            if UCase($LFile) <> "UP.LOG"
               "===============================================" ?
               $LPath+$LFile ?
               UnPackFile($LFile)
            #endif
         #endif
      #endif
      if @ERROR = 0
         $LFile = Dir("")
      #endif
   loop
   "===============================================" ?
#endfunction

#-------------------------------------------------------------------------------
# PackDir($DirName)
#-------------------------------------------------------------------------------
function PackDir($DirName,$ARC)
   Dim $s,$f,$e,$a
#begin
   $s = GetFileName($DirName)
   $a = Split($s,".")
   $f = Join($a,"_",UBound($a)+1)

? $s '|' $f '|' $ARC

   if Exist($f)
   #endif

   select
      case UCase($ARC) = "ZIP"
? "Unzip " $f "." $e " ..." ?
         $ex = 'unzip "'+$f+'"'
         ? $ex ?
         Shell $ex
      case UCase($ARC) = "ARJ"
? "arj " $f " ..." ?
         $ex = 'arj a -r -a -hm1 -a1 -i6 -hb "'+$f+'" "'+$s+'"'
         ? $ex ?
         Shell $ex
      case UCase($ARC) = "RAR"
? "Unrar " $f "." $e " ..." ?
         $ex = 'unrar x -y "'+$f+'"'
         ? $ex ?
         Shell $ex
   EndSelect
#endfunction

#-----------------------------------------------------------------------------
#Function:   FileAction()
#-----------------------------------------------------------------------------
function FileAction($file,$action)
   dim $shell,$
#begin
   $fileaction=1
   $shell=createobject("shell.application")
   $file=$Shell.namespace($file).self
   if @error  $fileaction=2 exit 2 #endif
   for each $ in $file.verbs
      if join(split($,"&"),"")=$action
         $file.invokeverb(""+$)
         $fileaction=0
      #endif
   next
   if $fileaction exit 1 #endif
#endfunction

#-------------------------------------------------------------------------------
# RegServer ($ADestPath, $AServer, optional $ASourcePath)
#-------------------------------------------------------------------------------
function RegServer ($ADestPath, $AServer, optional $ASourcePath, optional $Reg)
#begin
   if $ASourcePath
      BacFile ($ASourcePath, $ADestPath, $AServer, True)
   #endif
   if Exist($ADestPath+"\\"+$AServer) and $Reg
      Run "regsvr32 "+$ADestPath+"\\"+$AServer+" /s"
   #endif
#endfunction

#-------------------------------------------------------------------------------
# Cat($Filename, optional $Color)
#-------------------------------------------------------------------------------
function Cat($Filename, optional $Color)
   Dim $Str
#begin
   $Res=RedirectOutput("")
   $SaveColor = @Color
   if $Color COLOR $Color #endif
   $Handle = FreeFileHandle
   if Open ($Handle, $FileName, 2) = 0
      $Str = ReadLine ($Handle)
      while @ERROR = 0
         $Str ?
         $Str = ReadLine ($Handle)
      loop
      $Res = Close ($Handle)
   #endif
   if $Color COLOR $SaveColor #endif
#endfunction

#-------------------------------------------------------------------------------
# SetPath
#-------------------------------------------------------------------------------
function SetPath($Path)
#begin
   $Key = "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
   $LPath = RegReadString ($Key, "Path")
   if ExistWord($LPath, "#", $Path) = 0
      $LPath = $Path+"#"+$LPath
      RegWriteStringExpand ($Key, "Path", $LPath)
   #endif
#endfunction

#-------------------------------------------------
# CheckDestFileName
#-------------------------------------------------
function CheckDestFileName($aFileName, $aDestPath, $aNLimit)
DIM
   $LFileName,$LDirName,$LPathName,$LN
#begin
   $LN = LEN(CSTR($aNLimit))
   $LFileName = GetFileName($aFileName)
   $LDirName  = $aDestPath
   #$LPathName = $LDirName+"\\"+$LFileName
   $LPathName = $LDirName+"\\"+GetFileNameWithoutExt($LFileName)+"."+GetFileExt($LFileName)

   if (EXIST($LPathName))
      $i = 0
      while (EXIST($LPathName)) and ($i < $aNLimit)
         $i = $i + 1
         $LPathName = $LDirName+"\\"+
                      GetFileNameWithoutExt($LFileName)+"~"+AddChar("0",CSTR($i),$LN)+"."+
                      GetFileExt($LFileName)
      loop
   #endif
   $CheckDestFileName = $LPathName
#endfunction

#-------------------------------------------------------------------------------
# DelStrFromFile($Filename, $StrFind)
#-------------------------------------------------------------------------------
function DelStrFromFile($Filename, $StrFind)
   Dim $Str
#begin
   $Res=RedirectOutput("")

   $Handle = FreeFileHandle
   if Open ($Handle, $FileName, 2) = 0

      $OutFile = "list1.m3u"
      Del $OutFile
      $HandleOutFile = FreeFileHandle
      $Res = Open ($HandleOutFile, $OutFile, 1+4)

      $Str = ReadLine ($Handle)
      $Error = @ERROR

      while $ERROR = 0

         $Str ?

         $Begin1 = 1
         $End1   = InStr($Str, $StrFind) - 1 
         $Begin2 = $End1 + Len($StrFind) + 1
         $End2   = Len($Str)
         $StrOut1 = ""
         $StrOut2 = ""
         if $End1 > 0 
            $StrOut1 = Substr($Str, $Begin1, $End1) 
         #endif

         if $End2-Begin2 > 0 
            $StrOut2 = Substr($Str, $Begin2+1, $End2-$Begin2) 
         #endif
         $StrOut = $StrOut1 + $StrOut2

         $StrOut ?

         $Res = WriteLine ($HandleOutFile, $StrOut+@CRLF)

         $Str = ReadLine ($Handle)
         $Error = @ERROR
      loop

      $Res = Close ($Handle)

      if ($OutFile)
         $Res = Close ($HandleOutFile)
      #endif

   #endif
#endfunction

#-------------------------------------------------------------------------------
# CreateTextFile
#-------------------------------------------------------------------------------
function CreateTextFile($Filename, optional $aText)
#begin
   $HandleTextFile = FreeFileHandle
   if $aText
      $Res = Open ($HandleTextFile, $FileName, 5)
      $Res = WriteLine ($HandleTextFile, $aText)
      $Res = Close ($HandleTextFile)
   else
      Del $FileName
      $Res = Open ($HandleTextFile, $FileName, 5)
      $Res = WriteLine ($HandleTextFile, "")
      $Res = Close ($HandleTextFile)
   #endif
#endfunction
