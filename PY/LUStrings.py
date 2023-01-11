#--------------------------------------------------------------------
#LUStrings.py
#--------------------------------------------------------------------
#AddChar (Pad, Input, Length):
#AddCharR (Pad, Input, Length):
#ExtractWord (i, String, Delimiter):
#WordCount (String, Delimiter):
#ExistWord (String, Delimiter, Word):
#--------------------------------------------------------------------
#BaseConverter(v,f,t)
#CnvtBase2(vNum,iOB,iNB,OPTIONAL bNoHex, OPTIONAL bforceSep)
#FMT(sText, sMinMax, OPTIONAL iCtrl, OPTIONAL sPad)
#PadStr(Input, Pad, Length, optional PadSide)
#Like(string1, string2, optional wc, optional sc) 
#Search(searchIn, searchfor, searchHow)
#--------------------------------------------------------------------

#--------------------------------------------------------------------
#AddChar (Pad, Input, Length):
#--------------------------------------------------------------------
def AddChar (APad, AInput, ALength):
#beginfunction
    x = len (AInput)
    for i in range (x, ALength, len (APad)):
        AInput = APad + AInput
    #endfor
    LAddChar = AInput
    return LAddChar
#endfunction

#--------------------------------------------------------------------
#AddCharR (Pad, Input, Length):
#--------------------------------------------------------------------
def AddCharR (APad, AInput, ALength):
#beginfunction
    x = len (AInput)
    for i in range (x, ALength, len (APad)):
        AInput = AInput + APad
    #endfor
    LAddCharR = AInput
    return LAddCharR
#endfunction

#--------------------------------------------------------------------
#ExtractWord (i, String, Delimiter):
#--------------------------------------------------------------------
def ExtractWord (i, AString, ADelimiter):
#beginfunction
   LArray = AString.split (ADelimiter)
   if (i > 0) and (i <= len (LArray) + 1):
      LExtractWord = LArray [i-1]
   else:
      LExtractWord = ""
   #endif
   return LExtractWord
#endfunction

#--------------------------------------------------------------------
#WordCount (String, Delimiter):
#--------------------------------------------------------------------
def WordCount (AString, ADelimiter):
#beginfunction
   LArray = AString.split (ADelimiter)
   LWordCount = len (LArray)
   return LWordCount
#endfunction

#--------------------------------------------------------------------
#ExistWord (String, Delimiter, Word):
#--------------------------------------------------------------------
def ExistWord (AString, ADelimiter, AWord):
#beginfunction
    LExistWord = 0
    n = WordCount (AString, ADelimiter)
    for i in range (1, n+1, 1):
        w = ExtractWord (i, AString, ADelimiter)
        if AWord.upper() == w.upper ():
            LExistWord = 1
            break
        #endif
    #endfor
    return LExistWord
#endfunction

#--------------------------------------------------------------------
#BaseConverter(v,f,t)
#--------------------------------------------------------------------
#def BaseConverter(v,f,t)
#beginfunction
#  =0
#  t=+t
#  f=+f
#  e=(f>36)|(t>36)|(f<2)|(t<2)   
#  y=1.
#  for n=len(v) to 1 step -1
#     x=ASC(UCASE(substr(v,n,1)))
#     z=(x-48-(x>64)*7)
#     if (z<0)|((x>57)&(x<65))|e|(z>(f-1))
#      EXIT 1
#     #endif
#     =y*z+
#     y=y*f
#  next
#  n=""
#  While 
#     x=INT(-(INT(/t)*t))
#     =(-x)/t
#     n=CHR(x+48+(x>9)*7)+n
#  Loop
#  BaseConverter=n
#endfunction

#--------------------------------------------------------------------------------
#CnvtBase2(vNum,iOB,iNB,OPTIONAL bNoHex, OPTIONAL bforceSep)
#--------------------------------------------------------------------------------
#def CnvtBase2(vNum,iOB,iNB,OPTIONAL bNoHex, OPTIONAL bforceSep)
#beginfunction
#  iOB=0+iOB iNB=0+iNB
#  if iOB < 2 OR iNB < 2 EXIT -1 #endif
#  #Make vNum an array if necessary
#  if VarType(vNum) < 8192
#     if InStr(vNum,':') > 0
#        vNum = Split(vNum,':')
#     else:
#        sTmp = '' + vNum
#        iLen = Len(sTmp)
#        REDIM PRESERVE vNum[iLen-1]
#        for i = 1 TO iLen
#           vNum[i - 1] = SubStr(sTmp,i,1)
#        NEXT
#     #endif
#  #endif
#  if iNB > 16 OR (iNB > 10 AND bNoHex) OR bforceSep
#     sSep = ':' 
#  else: 
#     sSep = ''
#  #endif
#  iPos=0 iDigVal=0 iB10=0 i=0
#  vRemain='' sBx='' sSign='' sDigit=''
#  sDigits='0123456789ABCDEF'
#  iLen=UBound(vNum)
#  #Preserve the sign, if supplied
#  if vNum[0] = '-' OR vNum[0] = '+'
#     sSign = vNum[0]
#     for i = 1 TO iLen
#        vNum[i-1] = vNum[i]
#     NEXT
#     REDIM PRESERVE vNum[iLen - 1]
#     iLen=UBound(vNum)
#  #endif
#  iPlcNum  = 1
#  iPos     = 0
#  WHILE iPos <= iLen
#   #Convert to base 10
#     sDigit = '' + vNum[iLen-iPos]
#     if Len(sDigit) = 1
#        iDigVal = InStr(sDigits,sDigit) - 1
#     else:
#        iDigVal = 0 + sDigit
#     #endif
#     if iDigVal > (iOB - 1) EXIT -1 #endif
#     iB10    = 0 + iB10 + (iDigVal * iPlcNum)
#     iPlcNum = iPlcNum * iOB
#     iPos    = iPos + 1
#  LOOP
#  iPos=0
#  WHILE iB10 > 0 #Convert to new base
#     vRemain = iB10 - ((iB10 / iNB) * iNB)
#     if bNoHex OR vRemain > 15
#        sBx = sSep + vRemain + sBx
#     else:
#        sBx = sSep + SubStr(sDigits,vRemain+1,1) + sBx
#     #endif
#     iPos = iPos + 1
#     iB10 = iB10 / iNB
#  LOOP
#  if Len(sBx) > 1 and sSep = ':'
#      sBx = SubStr(sBx,2)
#      #endif
#  if sSign <> ''
#     #Add the sign back in
#     sBx = sSign + sBx
#  #endif
#  if sBx = ''
#  sBx='0' 
#  #endif
#  CnvtBase2 = sBx
#  EXIT 0
#endfunction

#-----------------------------------------------------------------------
#FMT(sText, sMinMax, OPTIONAL iCtrl, OPTIONAL sPad)
#-----------------------------------------------------------------------
#def Fmt(sText, sMinMax, OPTIONAL iCtrl, OPTIONAL sPad)
#beginfunction
#   if VarType(sText) < 2 OR VarType(sText) > 8 
#       RETURN
#   #endif
#   iTabSpc=0 ifmtLen=0 iPadLen =0 iTabWid=8 iCharWid=1
#   sText    = '' + sText
#   sMinMax  = '' + sMinMax
#   iCtrl    = 0 + iCtrl
#   sPad     = '' + sPad
#   if sPad = '' sPad = Chr(32) #endif
#   if iCtrl & 4 sPad = Chr(9) #endif #Horizontal Tab
#   #Calculate the width of the pad string
#   for i = 1 TO Len(sPad)
#       if Asc(SubStr(sPad,i,1)) = 9
#           iPadLen = iPadLen + (iTabWid * (1 + (iCtrl & 2)/2))
#       else:
#          iPadLen = iPadLen + (iCharWid * (1 + (iCtrl & 2)/2))
#       #endif
#   #endfor
#   #Parse MinMax
#   if InStr(sMinMax,".") > 0
#       iMin = Val(SubStr(sMinMax,1,InStr(sMinMax,".") - 1))
#      iMax = Val(SubStr(sMinMax,InStr(sMinMax,".") + 1))
#   else:
#       iMin = Val(sMinMax)
#       if iMin = 0 
#       iMin = Len(sText) 
#       #endif
#       iMax = 32000
#   #endif
#  
#  #UDF dependencies.
#  if iCtrl & 0256
#     sText = Flip_NumSep(sText) 
#     #endif
#  if iCtrl & 0512
#     sText = Flip_Dec(sText) 
#     #endif
#  if iCtrl & 1024
#     sText = Flip_Currency(sText) 
#     #endif
#
#  #After pre-processing, truncate string to iMax length
#  if iMax < Len(sText) sText = SubStr(sText,1,iMax) #endif
#  
#  #Calculate the width of the supplied string including TABS
#  for i = 1 TO Len(sText)
#      if Asc(SubStr(sText,i,1)) = 9
#          ifmtLen = ifmtLen + iTabWid
#      else:
#          ifmtLen = ifmtLen + 1
#      #endif
#  NEXT
#  if ifmtLen < iMin
#      j = iMin - (ifmtLen + iPadLen)
#      k = 0
#      for i = 0 TO j STEP iPadLen #Number of sPad strings needed
#          sPadding = sPadding + sPad
#          k = k + iPadLen
#      NEXT
#      ifmtLen = ifmtLen + k
#      sLPad=sPadding sRPad=sPadding
#      for i = 1 TO (iMin - ifmtLen) #Fill remainder with even number of spaces
#          if iCtrl & 2
#              if i & 1 
#                  sRPad = sRPad + ' '
#              else: 
#                  sLPad = ' ' + sLPad 
#              #endif
#          else:
#              sPadding = sPadding + ' '
#          #endif
#      NEXT
#  #endif
#  if iCtrl & 1 #LJust
#      Fmt = sText + sPadding
#  else:  #RJust
#      Fmt = sPadding + sText
#  #endif
#  if iCtrl & 2 #Center
#      Fmt = sLPad + sText + sRPad
#  #endif
#  #Recalculate the total length of the string.
#  ifmtLen = 0
#  for i = 1 TO Len(Fmt)
#      if Asc(SubStr(Fmt,i,1)) = 9
#          ifmtLen = ifmtLen + iTabWid
#      else:
#          ifmtLen = ifmtLen + 1
#      #endif
#  NEXT
#  for i = 1 TO (iMin - ifmtLen) #Fill remainder with spaces
#      Fmt = Fmt + ' '
#  NEXT
#  Fmt = SubStr(Fmt,1,iMax)
#endfunction #Fmt()

#--------------------------------------------------------------------
#PadStr(Input, Pad, Length, optional PadSide)
#--------------------------------------------------------------------
#def PadStr(Input, Pad, Length, optional PadSide):
#beginfunction
#   PadStr = ""
#   Input = "" + Input
#   Pad = "" + Pad
#   if PadSide = "" or len (PadSide) > 1 or Instr("LR",PadSide) = 0
#       PadSide = "L"
#   #endif
#   x = Len(Input)
#   for i=x to Length - 1 Step Len(Pad)
#       if PadSide = "L"
#           Input = Pad + Input
#       else:
#           Input = Input + Pad
#       #endif
#   #endfor
#   if PadSide = "L"
#       Input = Right(Input, Length)
#   else:
#       Input = Left(Input, Length)
#   #endif
#   return PadStr = Input
#endfunction

#--------------------------------------------------------------------
# Like(string1, string2, optional wc, optional sc) 
#--------------------------------------------------------------------
#def Like(string1, string2, optional wc, optional sc) 
#beginfunction  
#  if(NOT wc)
#     wc = "*"
#  #endif
#
#  if(NOT sc)
#     sc = "?"
#  #endif
#  
#  #base case
#  if string2 = "" or string2 = wc or (string2 = sc and len(string1) = 1)
#    Like = 1
#    return
#  #endif
#  if(string2 = sc and len(string1) <> 1)
#     Like = 0
#     return
#  #endif
#
#  #different places we may want to look for the substring.  Default to exact
#  anyWhere = 0
#  exact = 1
#  front = 2
#  back = 3
#  
#  case = exact
#
#  j = 1
#  subString = ""
#  
#  if(substr(string2, 1, 1) = sc)
#     string2 = substr(string2, 2, len(string2) -1)
#     string1 = substr(string1, 2, len(string1) -1)
#     Like = Like(string1, string2, wc, sc)
#     return
#  #endif
#
#  if(substr(string2, 1, 1) = wc and substr(string2, 2, 1) = sc) 
#     if(len(string2) = 2 and string1 = "")
#        Like = 0
#        return
#     #endif
#     string2 = wc + substr(string2, 3, len(string2) - 2)
#     string1 = substr(string1, 2, len(string1) -1)
#     Like = Like(string1, string2, wc, sc)
#     return
#  #endif
#  if(substr(string2, 1, 1) = wc)
#     j = 2                        
#     case = back                 
#  #endif
#  
#  #Build the search string
#  curChar = substr(string2, j, 1)
#  while(curChar <> "" And curChar <> wc And curChar <> sc)   #build the substring until we hit a wildcard
#     subString = subString + curChar                           #or until we get to the end of string2
#     j = j + 1
#     curChar = substr(string2, j, 1)                       #building the substring
#  loop
#  
#  if(curChar = wc or curChar = sc)  #there was a wildcard found in string2
#     if(case = back)
#       case = anyWhere  #one percent in front and one in back, ex: *string2*
#     #endif
#     if(case = exact)  #one percent in back, ex: string2*
#       case = front    
#     #endif
#  #endif
#
#  inThere = search(string1, subString, case) #search for substring given where to look for it
#  
#  if(NOT inThere)
#    Like = 0
#    return
#  #endif
#  string1 = substr(string1, inThere + len(subSTring))            
#  string2 = substr(string2, j)                                     
#  Like = Like(string1, string2, wc, sc)
#  
#endfunction   

#--------------------------------------------------------------------
#Search(searchIn, searchfor, searchHow)
#--------------------------------------------------------------------
#def Search(searchIn, searchfor, searchHow)
#beginfunction
#  posInString = instr(searchIn, searchfor)
#  if (searchHow = 0)                         #look anywhere for searchfor in searchIn
#     search = posInString
#  #endif
#
#  if (searchHow = 1)                         #must be an exact match (no wildcards)
#     if (searchIn = searchfor) #posInString <> 0 and len(searchIn) = len(searchfor))
#        search = posInString
#     else:
#        search = 0
#     #endif
#  #endif
#
#  if (searchHow = 2)                         #searchIn must start with searchfor
#     if(posInString = 1)
#        search = posInstring
#     else:
#        search = 0
#     #endif
#  #endif
#
#  if (searchHow = 3)                         #searchIn must end with searchfor
#     if(substr(searchIn, len(searchIn) - len(searchfor) + 1) = searchfor) 
#        search = len(searchIn) - len(searchfor) + 1
#     else:
#        search = 0
#     #endif
#  #endif
#endfunction

#--------------------------------------------------------------------------------
#def RegASCIItoHEX
#--------------------------------------------------------------------------------
#def RegASCIItoHEX(data)
#  return = ""
#
#  for i = 1 to len(data)
#     return = return + dectohex(asc(substr(data,i,1)))+ "00"
#  next
#  return = lcase(return) + "0000"
#  regASCIItoHex = return
#endfunction

#--------------------------------------------------------------------------------
#def RegHEXtoASCII
#--------------------------------------------------------------------------------
#def RegHextoAscii(data)
#  for i = 1 to len(data) step 2
#     hex = "&" + substr(data,i,2)
#     return = return + chr(val(hex))
#  next
#  reghextoascii = return
#endfunction

#--------------------------------------------------------------------------------
#def Replace()
#--------------------------------------------------------------------------------
#def Replace(SourceString, SearchString, ReplaceString, Optional First, Optional CaseSensitive)
#  Finished = 0
#  Counter = 0
#  String1 = SourceString
#  if CaseSensitive
#     PreviousState = SetOption("CaseSensitivity", "On")
#  #endif
#  While Not Finished
#     String2 = String1
#     Location = InStr(String1, SearchString)
#     if Location > 0
#        String1 = Substr(String1, 1, Location - 1) + ReplaceString + Substr(String1, Location + Len(SearchString), Len(SourceString) - Location + Len(SearchString) + 1)
#     else:
#        Finished = 1
#     #endif
#     if First
#        Finished = 1
#     #endif
#     if String1 = String2
#        Finished = 1
#     #endif
#  Loop
#  Replace = String1
#  Nul = SetOption("CaseSensitivity", PreviousState)
#endfunction

#--------------------------------------------------------------------------------
#Squeeze() - Remove all occurrences of a string from within a string 
#--------------------------------------------------------------------------------
#def squeeze(string1,string2)
#  while instr(string1,string2)
#     string1=substr(string1,1,instr(string1,string2)-1)+substr(string1,instr(string1,string2)+len(string2))
#  loop
#  squeeze = string1
#endfunction

#--------------------------------------------------------------------------------
#StringCount()
#--------------------------------------------------------------------------------
#def StringCount(searchstring, findstring, optional word)
# stringcount=split(searchstring,findstring)
# stringcount=ubound(stringcount)
#endfunction

#--------------------------------------------------------------------------------
#Strip() - strip leading or trailing character from string 
#--------------------------------------------------------------------------------
#def Strip(String,Optional Char, Optional Mode)
#  #Check parameters..
#  if Not VarType(String) Exit(1)    #endif
#  if Not VarType(Char)   Char=' '  #endif
#  if Not VarType(Mode)   Mode='lt' #endif
#
#  Strip=''
#  Select
#    Case Mode='lt'
#       #only leading and trailing chars..
#       for Cnt=1 to Len(String)
#        if SubStr(String,Cnt,1)<>Char Start=Cnt Cnt=Len(String)+1 #endif
#     Next
#       for Cnt=Len(String) to 1 Step -1
#        if SubStr(String,Cnt,1)<>Char End=Cnt+1 Cnt=0 #endif
#     Next
#     Strip=SubStr(String,Start,End-Start)
#
#    Case Mode='all'
#       #all chars..
#       for Cnt=1 to Len(String)
#        if SubStr(String,Cnt,1)<>Char Strip=Strip+SubStr(String,Cnt,1) #endif
#     Next
#    Case 1
#     Strip=String
#  EndSelect
#endfunction

#--------------------------------------------------------------------------------
#StripCopies() - Strips multipile instances of a string and integer from an array 
#--------------------------------------------------------------------------------
#def StripCopies(striArray)
#   on = 1 
#   searArr = ""
#for Each add in StriArray 
#  if Ubound(SearArr) = -1
#  ReDim searArr[0] SearArr[0] = add
#  #endif
#  counter = 0 
#  While Ubound(SearArr)+1 <> counter 
#  if add = searArr[counter]
#  on = 1 
#  #endif
#  counter = counter + 1 
#  Loop
#  counter = 0 
#  if on = 0 ReDim preserve SearArr[Ubound(SearArr)+1] SearArr[Ubound(SearArr)] = add #endif
#  on = 0
#Next 
#StripCopies = SearArr 
#endfunction

#--------------------------------------------------------------------------------
#udfSqueeze() - Reduce repeated characters in a string. 
#--------------------------------------------------------------------------------
#def udfSqueeze(sSource,Optional sDelimiters, Optional bTrim)
##beginfunction   
#  udfSqueeze = ""
#  
#  #--------------------------
#  #Defaults and sanity checks
#  #--------------------------
#  if sDelimiters  = "" sDelimiters = " " #endif
#  if bTrim bTrim = 1  else: bTrim = 0 #endif
#  
#  #----------------------------------------
#  #High speed squeeze for single characters
#  #----------------------------------------
#  if Len(sDelimiters)=1
#     sDelimiters=""+sDelimiters+sDelimiters
#     iIndex=InStr(sSource,sDelimiters)
#     While iIndex
#        sSource=""+SubStr(sSource,1,iIndex)+SubStr(sSource,iIndex+2,Len(sSource))
#        iIndex=InStr(sSource,sDelimiters)
#     Loop
#     if bTrim
#        sDelimiters=SubStr(sDelimiters,1,1)
#        #-------------
#        #Trim leading.
#        #-------------
#        While SubStr(sSource,1,1)=sDelimiters
#           sSource=SubStr(sSource,2,Len(sSource))
#        Loop
#        #--------------
#        #Trim Trailing.
#        #--------------
#        iIndex=Len(sSource)
#        While SubStr(sSource,iIndex,1)=sDelimiters
#           sSource=SubStr(sSource,1,iIndex-1)
#           iIndex=Len(sSource)
#        Loop
#     #endif
#     udfSqueeze=sSource
#  else:
#     #--------------------------------------
#     #Slower squeeze for multiple characters
#     #--------------------------------------
#     iSourceLength=Len(sSource)
#     for iIndex = 1 To iSourceLength
#        cChar=SubStr(sSource,iIndex,1)
#        if InStr(sDelimiters,cChar)
#           if bFound=0 AND ( iLastGood OR bTrim=0 )
#              udfSqueeze=""+udfSqueeze+SubStr(sDelimiters,1,1)
#           #endif
#           bFound=1
#        else:
#           bFound=0
#           udfSqueeze=""+udfSqueeze+cChar
#           if bTrim iLastGood=Len(udfSqueeze) #endif
#        #endif
#     Next
#     if iLastGood udfSqueeze=SubStr(udfSqueeze,1,iLastGood)
#     #endif
#  #endif
#endfunction
