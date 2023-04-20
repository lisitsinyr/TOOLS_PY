"""LUObjectsYT.py"""
# -*- coding: UTF-8 -*-
__annotations__ ="""
 =======================================================
 Copyright (c) 2023
 Author:
     Lisitsin Y.R.
 Project:
     LU_PY
     Python (LU)
 Module:
     LUObjectsYT.py

 =======================================================
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import os
import datetime
import logging

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
from typing import BinaryIO

from pytube import YouTube
from pytube import Playlist
from urllib.parse import urlparse

#------------------------------------------
# БИБЛИОТЕКИ LU
#------------------------------------------
from LULog import LULogger
import LULog
# import LUConst
from LUObjects import TObjectTypeClass, TObjects
import LUFile
import LUStrUtils
import LUThread

CYOUTUBE_COM = 'WWW.YOUTUBE.COM'
CYOUTUBE_BE = 'YOUTU.BE'
CYOUTU = 'YOUTU'
CYOUTUBE_PLAYLISTS = 'PLAYLISTS'
CYOUTUBE_PLAYLIST = 'PLAYLIST'
cMaxRes1080p = ('1080p','720p','480p','360p','240p','144p')
cMaxRes720p = ('720p','480p','360p','240p','144p')
cMaxRes480p = ('480p','360p','240p','144p')
cMaxRes360p = ('360p','240p','144p')
cMaxRes240p = ('240p','144p')
cMaxRes144p = ('144p')

def ONfunction():
#beginfunction
    ...
#endfunction
TONfunction = ONfunction

class TYouTubeObject (TObjects):
    """TYouTubeObject"""
    luClassName = "TYouTubeObject"
    
    #--------------------------------------------------
    # constructor
    #--------------------------------------------------
    def __init__ (self):
        """Constructor"""
    #beginfunction
        super ().__init__ ()
        self.__FURL: str = ''
        self.__FID: datetime = 0
        self.__FProgressMax: int = 0
        self.__FStopYouTubeBoolean: bool = False
        self.__FStopYouTubeBooleanThread: bool = False
        self.__FRxProgress = None                       # TRxProgress
        self.FYouTubeThread: LUThread.TThread = None
        self.__FObjectType: TObjectTypeClass = TObjectTypeClass.otYouTubeObject
        self.__FURLYouTube: YouTube = None
        self.__FPlayList: str = ''
        self.__FNumber: int = 0
        self.__FCount: int = 0
        self.__FURLInfo = {}
        self.__FStreamInfo = {}
        self.FONprogress: TONfunction = self.ONprogress
        self.FONcomplete: TONfunction = self.ONcomplete
        self.Clear()
    #endfunction

    #--------------------------------------------------
    # destructor
    #--------------------------------------------------
    def __del__(self):
        """destructor"""
    #beginfunction
        super ().__del__()
        LClassName = self.__class__.__name__
        s = '{} уничтожен'.format (LClassName)
        LULogger.log (LULog.DEBUGTEXT, s)
    #endfunction

    #--------------------------------------------------
    # ONprogress
    #--------------------------------------------------
    # def show_progress_bar (stream, chunk, bytes_remaining):
    #     prog.update (task, completed = stream.filesize - bytes_remaining)
    #     #this show the bytes_remaining, use rich to display a progress bar
    def ONprogress(self, stream, chunk: bytes, bytes_remaining: int):

    #beginfunction
        s = 'ONprogress...'
        LULogger.info (s)
        # print (stream.filesize)
        # print (len (chunk))
        # print (bytes_remaining)
    #endfunction

    #--------------------------------------------------
    # ONcomplete
    #--------------------------------------------------
    # def on_complete (stream, file_path):
    #     prog.remove_task (task)
    #     prog.stop ()
    #     print ('[green] Downloaded ', file_path.split ('/') [-1], '\n')
    def ONcomplete(self, stream, file_path):
    #beginfunction
        s = 'ONcomplete...'
        LULogger.info (s)
        # print (s)
        # print (stream)
        # print (file_path)
    #endfunction

    #--------------------------------------------------
    # @property URL
    #--------------------------------------------------
    def SetURL(self, Value: str, APlayList: str, ANumber: int, ACount: int):
    #beginfunction
        self.__FURL = Value
        self.__FURLYouTube: YouTube = YouTube(Value)
                            # on_progress_callback = None,
                            # on_complete_callback = None)
                            # on_progress_callback = self.ONprogress,
                            # on_complete_callback = self.ONcomplete)

        # self.SetURLInfo()
        self.PlayList = APlayList
        self.Number = ANumber
        self.Count = ACount
    #endfunction

    # getter
    @property
    def URL(self) -> str:
    #beginfunction
        return self.__FURL
    #endfunction

    #--------------------------------------------------
    # @property ID
    #--------------------------------------------------
    # getter
    @property
    def ID(self) -> datetime:
    #beginfunction
        return self.__FID
    #endfunction
    @ID.setter
    def ID(self, Value: datetime):
    #beginfunction
        self.__FID = Value
    #endfunction

    #--------------------------------------------------
    # @property URLInfo
    #--------------------------------------------------
    # getter
    @property
    def URLInfo(self) -> {}:
    #beginfunction
        return self.__FURLInfo
    #endfunction

    #--------------------------------------------------
    # @property URLYouTube
    #--------------------------------------------------
    # getter
    @property
    def URLYouTube(self) -> YouTube:
    #beginfunction
        return self.__FURLYouTube
    #endfunction

    #--------------------------------------------------
    # @property PlayList
    #--------------------------------------------------
    # getter
    @property
    def PlayList(self) -> str:
    #beginfunction
        return self.__FPlayList
    #endfunction
    @PlayList.setter
    def PlayList(self, Value: str):
    #beginfunction
        self.__FPlayList = Value
    #endfunction

    #--------------------------------------------------
    # @property Number
    #--------------------------------------------------
    # getter
    @property
    def Number(self) -> int:
    #beginfunction
        return self.__FNumber
    #endfunction
    @Number.setter
    def Number(self, Value: int):
    #beginfunction
        self.__FNumber = Value
    #endfunction

    #--------------------------------------------------
    # @property Count
    #--------------------------------------------------
    # getter
    @property
    def Count(self) -> int:
    #beginfunction
        return self.__FCount
    #endfunction
    @Count.setter
    def Count(self, Value: int):
    #beginfunction
        self.__FCount = Value
    #endfunction

    #--------------------------------------------------
    # @property ProgressMax
    #--------------------------------------------------
    # getter
    @property
    def ProgressMax(self) -> int:
    #beginfunction
        return self.__FProgressMax
    #endfunction
    @ProgressMax.setter
    def ProgressMax(self, Value: int):
    #beginfunction
        self.__FProgressMax = Value
    #endfunction

    #--------------------------------------------------
    # @property StopYouTubeBoolean
    #--------------------------------------------------
    # getter
    @property
    def StopYouTubeBoolean(self) -> bool:
    #beginfunction
        return self.__FStopYouTubeBoolean
    #endfunction
    @StopYouTubeBoolean.setter
    def StopYouTubeBoolean(self, Value: bool):
    #beginfunction
        self.__FStopYouTubeBoolean = Value
    #endfunction

    #--------------------------------------------------
    # @property RxProgress
    #--------------------------------------------------
    # getter
    @property
    def RxProgress(self):
    #beginfunction
        return self.__FRxProgress
    #endfunction
    @RxProgress.setter
    def RxProgress(self, Value):
    #beginfunction
        self.__FRxProgress = Value
    #endfunction

    #--------------------------------------------------
    # @property YouTubeThread
    #--------------------------------------------------
    # getter
    @property
    def YouTubeThread(self):
    #beginfunction
        return self.__FYouTubeThread
    #endfunction
    @YouTubeThread.setter
    def YouTubeThread(self, Value):
    #beginfunction
        self.__FYouTubeThread = Value
    #endfunction

    #public
    def Clear (self):
        """Clear"""
    #beginfunction
        self.__FURL = ''
        self.ID = 0
        self.StopYouTubeBoolean = False
        self.ProgressMax = 0
        self.RxProgress = None
        self.YouTubeThread = None
        self.PlayList = ''
        self.Number = 0
    #endfunction

    def SetURLInfo (self):
        """Print_URL"""
    #beginfunction
        #Get the video author.
        self.URLInfo['author'] = self.URLYouTube.author
        #Get a list of Caption.
        self.URLInfo['caption_tracks'] = self.URLYouTube.caption_tracks
        #Interface to query caption tracks.
        self.URLInfo['captions'] = self.URLYouTube.captions
        #Get the video poster’s channel id.
        self.URLInfo['channel_id'] = self.URLYouTube.channel_id
        #Construct the channel url for the video’s poster from the channel id.
        self.URLInfo['channel_url'] = self.URLYouTube.channel_url
        #Get the video description.
        self.URLInfo['description'] = self.URLYouTube.description
        #Returns a list of streams if they have been initialized.
        self.URLInfo['fmt_streams'] = self.URLYouTube.fmt_streams
        #Get the video keywords.
        self.URLInfo['keywords'] = self.URLYouTube.keywords
        # родолжительность видео [Get the video length in seconds]
        self.URLInfo['length'] = self.URLYouTube.length
        #Get the metadata for the video.
        self.URLInfo['metadata'] = self.URLYouTube.metadata
        #Get the publish date.
        self.URLInfo['publish_date'] = self.URLYouTube.publish_date
        #Get the video average rating.
        self.URLInfo['rating'] = self.URLYouTube.rating
        #Return streamingData from video info.
        self.URLInfo['streaming_data'] = self.URLYouTube.streaming_data
        #Interface to query both adaptive (DASH) and progressive streams.
        self.URLInfo['streams'] = self.URLYouTube.streams
        #Get the thumbnail url image.
        self.URLInfo['thumbnail_url'] = self.URLYouTube.thumbnail_url
        # Заголовок [Get the video title]
        self.URLInfo['title'] = self.URLYouTube.title
        #Parse the raw vid info and return the parsed result.
        self.URLInfo['vid_info'] = self.URLYouTube.vid_info
        # Количество просмотров [Get the number of the times the video has been viewed]
        self.URLInfo['views'] = self.URLYouTube.views
    #endfunction

    def GetStreamInfo (self, AStream) -> {}:
        """GetStreamInfo"""
    #beginfunction
        self.__FStreamInfo['itag'] = AStream.itag
        # video/mp4
        self.__FStreamInfo['mime_type'] = AStream.mime_type
        # 'video' 'audio'
        self.__FStreamInfo['type'] = AStream.type
        # FileName - Generate filename based on the video title.
        self.__FStreamInfo['default_filename'] = AStream.default_filename
        # Bytes - File size of the media stream in bytes.
        self.__FStreamInfo['filesize'] = AStream.filesize
        #Get approximate filesize of the video
        self.__FStreamInfo['filesize_approx'] = AStream.filesize_approx
        #File size of the media stream in gigabytes.
        self.__FStreamInfo['filesize_gb'] = AStream.filesize_gb
        #File size of the media stream in kilobytes.
        self.__FStreamInfo['filesize_kb'] = AStream.filesize_kb
        #File size of the media stream in megabytes.
        self.__FStreamInfo['filesize_mb'] = AStream.filesize_mb
        # True/False - Whether the stream only contains audio.
        self.__FStreamInfo['includes_audio_track'] = AStream.includes_audio_track
        # True/False - Whether the stream only contains video.
        self.__FStreamInfo['includes_video_track'] = AStream.includes_video_track
        #Whether the stream is DASH.
        self.__FStreamInfo['is_adaptive'] = AStream.is_adaptive
        #Whether the stream is progressive.
        self.__FStreamInfo['is_progressive'] = AStream.is_progressive
        #Get title of video
        self.__FStreamInfo['title'] = AStream.title
        #Get the video/audio codecs from list of codecs.
        self.__FStreamInfo['parse_codecs'] = AStream.parse_codecs ()
        return self.__FStreamInfo
    #endfunction

    def DownloadURL (self, APATH: str, AMaxRes: (), type='video', file_extension='mp4',
                     skip_existing=False, filename_prefix=''):
        """DownloadURL"""
    #beginfunction

        self.__FURLYouTube.register_on_progress_callback(self.FONprogress)
        self.__FURLYouTube.register_on_complete_callback(self.FONcomplete)

        if len(self.PlayList) > 0:
            LPATH = os.path.join (APATH, self.PlayList)
            if not LUFile.DirectoryExists (LPATH):
                LUFile.ForceDirectories (LPATH)
            Lfilename_prefix = LUStrUtils.AddChar('0', str (self.Number), 3)+'. '
        else:
            LPATH = APATH
            Lfilename_prefix = filename_prefix
        #endif

        for res in AMaxRes:
            LStreams = ()
            try:
                LStreams = self.URLYouTube.streams.filter (type=type, file_extension=file_extension, res=res)
            except BaseException as ERROR:
                s = f'filter={ERROR}'
                LULogger.error(s)
            #endtry
            if len (LStreams) > 0:
                for LStream in LStreams:
                    try:
                        # print (LStream.default_filename)
                        LFileName = LStream.download (LPATH, skip_existing=skip_existing, filename_prefix=Lfilename_prefix)
                    except BaseException as ERROR:
                        s = f'DownloadURL={ERROR}'
                        LULogger.error (s)
                    #endtry
                    break
                #endfor
                break
            #endif
        #endfor
        ...
    #endfunction

    def StartYouTubeThread (self, *args, **kwargs): # TTerminateProc
        """StartYouTubeThread"""
    #beginfunction
        """
        if not Assigned (FYouTubeThread) then
        begin
            FYouTubeThread := TYouTubeThreadNew.Create (UpdateProgressBarThread, True)
            FYouTubeThread.Priority := tpNormal
            FYouTubeThread.FreeOnTerminate := True
            FYouTubeThread.TerminateProc := aTerminateProc
            (*
            Происходит после возврата метода Execute
            потока и перед уничтожением потока.
            *)
            FYouTubeThread.OnTerminate := aTerminateProc
            FYouTubeThread.FObjectIDStr := GenerateObjectIDStr (ID)
            FYouTubeThread.FStopYouTubeBooleanThread := False
            FYouTubeThread.Start ()
        end
        """
        # class threading.Thread(group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None)
        self.FYouTubeThread = LUThread.TThread(target=self.DownloadURL, args=args, kwargs=kwargs)
        # print (self.FYouTubeThread.name)
        self.FYouTubeThread.start ()
        # self.FYouTubeThread.join ()
        ...
    #endfunction

    def StartYouTube (self):
        """StartYouTube"""
    #beginfunction
        """
        FStopYouTubeBoolean := False
        # LRxProgress 
        FRxProgress.Min := 0
        FRxProgress.Max := ProgressMax
        FRxProgress.Position := 0
        for i := 0 to FRxProgress.Max do
        begin
            if FStopYouTubeBoolean then
            begin
                Break
            end
            FRxProgress.Position := i
            FRxProgress.Update // Make sure to repaint the progressbar
            Sleep (cSleep)
            Application.ProcessMessages
        end
        FRxProgress.Position := 0
        """
        ...
    #endfunction

    def StopYouTube (self):
        """StopYouTube"""
    #beginfunction
        self.StopYouTubeBoolean = True
        """
        FRxProgress.Position := 0
        """
    #endfunction

    def UpdateProgressBarThread (self, AProgress: int):
        """UpdateProgressBarThread"""
    #beginfunction
        """
        FRxProgress.Position := aProgress
        FRxProgress.Update // Make sure to repaint the progressbar
        if aProgress >= cProgressBarMax then
        begin
            FRxProgress.Position := 0
            FYouTubeThread := nil
        end
        """
        ...
    #endfunction

    def StopYouTubeThread (self):
        """StopYouTubeThread"""
    #beginfunction
        self.__FStopYouTubeBooleanThread = True
        # FRxProgress.Position := 0
        self.__FYouTubeThread = None
    #endfunction
#endclass

# --------------------------------------------
# TYouTubeObjectsItem
# --------------------------------------------
class TYouTubeObjectsItem (object):
    """TYouTubeObjectsItem"""
    luClassName = "TYouTubeObjectsItem"

    #--------------------------------------------------
    # constructor
    #--------------------------------------------------
    def __init__(self):
        """Constructor"""
        super().__init__()
        self.__FYouTubeObject: TYouTubeObject = TYouTubeObject()
    #endfunction

    #--------------------------------------------------
    # destructor
    #--------------------------------------------------
    def __del__(self):
        """destructor"""
        # удалить объект
        del self.__FYouTubeObject
        LClassName = self.__class__.__name__
        s = '{} уничтожен'.format (LClassName)
        LULogger.log (LULog.DEBUGTEXT, s)
    #endfunction

    #--------------------------------------------------
    # @property YouTubeObject
    #--------------------------------------------------
    # getter
    @property
    def YouTubeObject(self):
    #beginfunction
        return self.__FYouTubeObject
    #endfunction
    @YouTubeObject.setter
    def YouTubeObject(self, Value: TYouTubeObject):
    #beginfunction
        self.__FYouTubeObject = Value
    #endfunction
#endclass

# --------------------------------------------
# TYouTubeObjectsCollection
# --------------------------------------------
class TYouTubeObjectsCollection (list):
    """TObjectsCollection"""
    luClassName = "TYouTubeObjectsCollection"

    #--------------------------------------------------
    # constructor
    #--------------------------------------------------
    def __init__ (self):
        """Constructor"""
    #beginfunction
        super ().__init__ ()
    #endfunction

    #--------------------------------------------------
    # destructor
    #--------------------------------------------------
    def __del__ (self):
        """destructor"""
    #beginfunction
        self.clear()            # удалить все items
        LClassName = self.__class__.__name__
        s = '{} уничтожен'.format (LClassName)
        LULogger.log (LULog.DEBUGTEXT, s)
    #endfunction

    def AddItem (self) -> TYouTubeObjectsItem:
        """AddItem"""
    #beginfunction
        LYouTubeObjectsItem: TYouTubeObjectsItem = TYouTubeObjectsItem ()
        self.append (LYouTubeObjectsItem)
        return self [self.__len__()-1]
    #endfunction

    def GetItem (self, Index: int) -> TYouTubeObjectsItem:
        """GetItem"""
    #beginfunction
        LResult: TYouTubeObjectsItem = self [Index]
        return LResult
    #endfunction

    def SetItem (self, Index: int, Value: TYouTubeObjectsItem):
        """SetItem"""
    #beginfunction
        self [Index] = Value
    #endfunction

    def FindYouTubeObjectsItemURL (self, AURL: str) -> TYouTubeObjectsItem:
        """Поиск YouTubeObjectsItem по AURL"""
    #beginfunction
        for item in self:
            LYouTubeObjectsItem:TYouTubeObjectsItem = item
            # print(LYouTubeObjectsItem)
            LURL = LYouTubeObjectsItem.YouTubeObject.URL
            if LURL == AURL:
                return LYouTubeObjectsItem
            #endif
        #endfor
        return None
    #endfunction
#endclass

# def PrintPlaylist_video_urls (AURL):
#     """PrintPlaylist_video_urls"""
# #beginfunction
#     LURI = urlparse (AURL)
#     if LURI.hostname.upper () == cYOUTUBE:
#         if cYOUTUBE_PLAYLISTS in LURI.path.upper ():
#             ...
#         else:
#             if cYOUTUBE_PLAYLIST in LURI.path.upper ():
#                 Lplaylist = Playlist (AURL)
#                 for Lurl in Lplaylist.video_urls:
#                     print (Lurl)
#                 #endfor
#             #endif
#         #endif
#     #endif
# #endfunction
#
# def DownloadPlaylist_videos (AURL):
#     """DownloadPlaylist_videos"""
# #beginfunction
#     LURI = urlparse (AURL)
#     if LURI.hostname.upper () == cYOUTUBE:
#         if cYOUTUBE_PLAYLISTS in LURI.path.upper ():
#             ...
#         else:
#             if cYOUTUBE_PLAYLIST in LURI.path.upper ():
#                 Lplaylist = Playlist (AURL)
#                 print (f"Загрузка плейлиста: {Lplaylist.title}")
#                 for Lvideo in Lplaylist.videos:
#                     Lvideo.streams.first ().download ()
#                     print (f"Видео {Lvideo.title} загружено")
#                 #endfor
#             #endif
#         #endif
#     #endif
# #endfunction

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
