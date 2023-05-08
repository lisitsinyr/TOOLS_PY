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
import pytube
import pytube.exceptions
import string

#------------------------------------------
# БИБЛИОТЕКИ LU
#------------------------------------------
import LULog
# import LUConst
from LUObjects import TObjectTypeClass, TObjects
import LUFile
import LUStrUtils
import LUThread
import LUDateTime

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
cMaxRes144p = ('144p','')

def ONfunction(*args):
#beginfunction
    print('def ONfunction():')
    ...
#endfunction
TONfunction = ONfunction

def progress_func (AStream, AChunk: bytes, bytes_remaining: int):
    #beginfunction
    s = 'progress_func...'
    # LULog.LoggerTOOLS.info (s)
    # LULog.LoggerTOOLS.info (bytes_remaining)
    if not AStream is None:
        # print (stream.filesize)
        ...
    #endif
    if not AChunk is None:
        # print (len(AChunk))
        ...
    #endif
#endfunction

def complete_func (stream, AFilePath: str):
#beginfunction
    s = 'complete_func...'
    # LULog.LoggerTOOLS.info (s)
    #print (AFilePath)
    ...
#endfunction

#--------------------------------------------------
# ONprogress
#--------------------------------------------------
# def show_progress_bar (stream, chunk, bytes_remaining):
#     prog.update (task, completed = stream.filesize - bytes_remaining)
#     #this show the bytes_remaining, use rich to display a progress bar
def ONprogress (AStream, AChunk: bytes, bytes_remaining: int):
#beginfunction
    s = 'ONprogress...'
    # LULog.LoggerTOOLS.info (s)
    # LULog.LoggerTOOLS.info (bytes_remaining)
    if not AStream is None:
        # print (stream.filesize)
        ...
    #endif
    if not AChunk is None:
        # print (len(AChunk))
        ...
    #endif
#endfunction

#--------------------------------------------------
# ONcomplete
#--------------------------------------------------
# def on_complete (stream, file_path):
#     prog.remove_task (task)
#     prog.stop ()
#     print ('[green] Downloaded ', file_path.split ('/') [-1], '\n')
def ONcomplete(AStream, AFilePath):
#beginfunction
    s = 'ONcomplete...'
    # LULog.LoggerTOOLS.info (s)
    #print (AFilePath)
#endfunction

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
        self.__FYouTube: YouTube = None

        self.__FURL: str = ''
        self.__FID: datetime = 0
        self.__FURLInfo = dict ()
        self.__FStreamInfo = dict ()
        self.__FPlayList: str = ''
        self.__FNumber: int = 0
        self.__FCount: int = 0

        self.FONprogress = progress_func
        self.FONcomplete = complete_func
        self.FONprogress = ONfunction
        self.FONcomplete = ONfunction

        self.__FRxProgress = None                       # TRxProgress
        self.__FProgressMax: int = 0
        self.__FStopYouTubeBoolean: bool = False
        self.__FStopYouTubeBooleanThread: bool = False
        self.FYouTubeThread: LUThread.TThread = None
        self.__FObjectType: TObjectTypeClass = TObjectTypeClass.otYouTubeObject
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
        # LULog.LoggerTOOLS.log (LULog.DEBUGTEXT, s)
        #print (s)
    #endfunction

    @staticmethod
    def _GetURLInfo (AYouTube: YouTube) -> {}:
        """__GetURLInfo"""
    #beginfunction
        LURLInfo = dict ()
        #Get the video author.
        LURLInfo['author'] = AYouTube.author
        #Get the video description.
        LURLInfo['description'] = AYouTube.description
        #Get the thumbnail url image.
        LURLInfo['thumbnail_url'] = AYouTube.thumbnail_url
        # Заголовок [Get the video title]
        LURLInfo['title'] = AYouTube.title

        # #Get a list of Caption.
        # LURLInfo['caption_tracks'] = AYouTube.caption_tracks
        # #Interface to query caption tracks.
        # LURLInfo['captions'] = AYouTube.captions
        # #Get the video poster’s channel id.
        # LURLInfo['channel_id'] = AYouTube.channel_id
        # #Construct the channel url for the video’s poster from the channel id.
        # LURLInfo['channel_url'] = AYouTube.channel_url
        # #Returns a list of streams if they have been initialized.
        # LURLInfo['fmt_streams'] = AYouTube.fmt_streams
        # #Get the video keywords.
        # LURLInfo['keywords'] = AYouTube.keywords
        # # продолжительность видео [Get the video length in seconds]
        # LURLInfo['length'] = AYouTube.length
        # #Get the metadata for the video.
        # LURLInfo['metadata'] = AYouTube.metadata
        # #Get the publish date.
        # LURLInfo['publish_date'] = AYouTube.publish_date
        # #Get the video average rating.
        # LURLInfo['rating'] = AYouTube.rating
        # #Return streamingData from video info.
        # LURLInfo['streaming_data'] = AYouTube.streaming_data
        # #Interface to query both adaptive (DASH) and progressive streams.
        # LURLInfo['streams'] = AYouTube.streams
        # #Parse the raw vid info and return the parsed result.
        # LURLInfo['vid_info'] = AYouTube.vid_info
        # # Количество просмотров [Get the number of the times the video has been viewed]
        # LURLInfo['views'] = AYouTube.views
        return LURLInfo
    #endfunction

    def __SetURLInfo (self):
        """__SetURLInfo"""
    #beginfunction
        self.__FURLInfo = self._GetURLInfo (self.__FYouTube)
    #endfunction

    @staticmethod
    def _GetStreamInfo (AStream) -> {}:
        """GetStreamInfo"""
    #beginfunction
        LStreamInfo = dict ()
        # FileName - Generate filename based on the video title.
        LStreamInfo['default_filename'] = AStream.default_filename
        #Get title of video
        LStreamInfo['title'] = AStream.title
        #Get the video/audio codecs from list of codecs.
        LStreamInfo['parse_codecs'] = AStream.parse_codecs ()
        # Bytes - File size of the media stream in bytes.
        LStreamInfo['filesize'] = AStream.filesize
        #Get approximate filesize of the video
        LStreamInfo['filesize_approx'] = AStream.filesize_approx
        #File size of the media stream in gigabytes.
        LStreamInfo['filesize_gb'] = AStream.filesize_gb
        #File size of the media stream in kilobytes.
        LStreamInfo['filesize_kb'] = AStream.filesize_kb
        #File size of the media stream in megabytes.
        LStreamInfo['filesize_mb'] = AStream.filesize_mb

        # LStreamInfo['itag'] = AStream.itag
        # # video/mp4
        # LStreamInfo['mime_type'] = AStream.mime_type
        # # 'video' 'audio'
        # LStreamInfo['type'] = AStream.type
        # # True/False - Whether the stream only contains audio.
        # LStreamInfo['includes_audio_track'] = AStream.includes_audio_track
        # # True/False - Whether the stream only contains video.
        # LStreamInfo['includes_video_track'] = AStream.includes_video_track
        # #Whether the stream is DASH.
        # LStreamInfo['is_adaptive'] = AStream.is_adaptive
        # #Whether the stream is progressive.
        # LStreamInfo['is_progressive'] = AStream.is_progressive
        return LStreamInfo
    #endfunction

    def __SetStreamInfo (self, AStream):
        """SetStreamInfo"""
    #beginfunction
        self.__FStreamInfo = self._GetStreamInfo(AStream)
    #endfunction

    #--------------------------------------------------
    #
    #--------------------------------------------------
    def __SetStream(self, AMaxRes: ()):
    #beginfunction
        for res in AMaxRes:
            LStreams = list ()
            try:
                LStreams = self.__FYouTube.streams.filter (res=res, type='video', file_extension='mp4')
            except BaseException as ERROR:
                s = f'filter={ERROR}'
                LULog.LoggerTOOLS.error(s)
            #endtry
            if len (LStreams) > 0:
                for LStream in LStreams:
                    self.__FStream = LStream
                    self.__SetStreamInfo (self.__FStream)
                    break
                #endfor
                break
            #endif
        #endfor
    #endfunction

    #--------------------------------------------------
    # @property URL
    #--------------------------------------------------
    def SetURL(self, AURL: str, AMaxRes: (), APlayList: str, ANumber: int, ACount: int):
    #beginfunction
        self.__FURL = AURL
        self.__FYouTube: YouTube = YouTube(AURL)
                            # on_progress_callback = None,
                            # on_complete_callback = None)
                            # on_progress_callback = self.ONprogress,
                            # on_complete_callback = self.ONcomplete)

        self.__SetStream(AMaxRes)
        self.__SetURLInfo()
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
    def URLInfo(self) -> dict:
    #beginfunction
        return self.__FURLInfo
    #endfunction

    #--------------------------------------------------
    # @property StreamInfo
    #--------------------------------------------------
    # getter
    @property
    def StreamInfo(self) -> dict:
    #beginfunction
        return self.__FStreamInfo
    #endfunction

    # #--------------------------------------------------
    # # @property URLYouTube
    # #--------------------------------------------------
    # # getter
    # @property
    # def URLYouTube(self) -> YouTube:
    # #beginfunction
    #     return self.__FYouTube
    # #endfunction

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

    def DownloadURL (self, APATH: str, ADownload=False, filename_prefix=''):
        """DownloadURL"""
    #beginfunction
        # LULog.LoggerTOOLS.info (APATH)
        # LULog.LoggerTOOLS.info (filename_prefix)
        s = self.URLInfo ['thumbnail_url']
        # LULog.LoggerTOOLS.info (s)
        s = self.URLInfo ['author']
        # LULog.LoggerTOOLS.info (s)
        s = self.URLInfo ['title']
        s = LUStrUtils.PrintableStr(s)
        # LULog.LoggerTOOLS.info (s)
        s = self.__FStreamInfo ['default_filename']
        s = LUStrUtils.PrintableStr(s)
        # LULog.LoggerTOOLS.info (s)

        # s = self.__FStreamInfo ['filesize']
        # LULog.LoggerTOOLS.info (s)
        # s = self.__FStreamInfo ['filesize_kb']
        # LULog.LoggerTOOLS.info (s)
        # s = self.__FStreamInfo ['filesize_mb']
        # LULog.LoggerTOOLS.info (s)

        self.__FYouTube.register_on_progress_callback(self.FONprogress)
        # print (self.FONprogress)
        self.__FYouTube.register_on_complete_callback(self.FONcomplete)
        # print (self.FONcomplete)

        if len(self.PlayList) > 0:
            LPATH = os.path.join (APATH, self.PlayList)
            if not LUFile.DirectoryExists (LPATH):
                LUFile.ForceDirectories (LPATH)
            Lfilename_prefix = LUStrUtils.AddChar('0', str (self.Number), 3)+'. '
        else:
            LPATH = APATH
            Lfilename_prefix = filename_prefix
        #endif

        if ADownload:
            try:
                LFileName = self.__FStream.download (LPATH,
                                                     type='video', file_extension='mp4',
                                                     skip_existing=False,
                                                     filename_prefix=Lfilename_prefix)
            except BaseException as ERROR:
                s = f'DownloadURL={ERROR}'
                LULog.LoggerTOOLS.error (s)
            #endtry
        else:
            mb = int (self.__FStreamInfo ['filesize_mb'])
            # LULog.LoggerTOOLS.info (str(mb))
            i = 0
            while i < mb:
                self.FONprogress(self.__FStream, None, i)
                i = i + 1
            #endwhile
        #endif
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
        # self.FYouTubeThread = LUThread.TThread(target=self.DownloadURL, args=args, kwargs=kwargs)
        self.FYouTubeThread = LUThread.TThread(target = self.DownloadURL, args=args, kwargs=kwargs)
        self.FYouTubeThread.start ()
        # self.FYouTubeThread.join ()
        ...
    #endfunction

    # def StartYouTubeQThread (self, *args, **kwargs): # TTerminateProc
    #     """StartYouTubeThread"""
    # #beginfunction
    #     self.FYouTubeQThread = LUThreadQ.TQThread(self.DownloadURL)
    #     self.FYouTubeQThread.start ()
    #     ...
    # #endfunction

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


def CreateURLs (AURL: str, AMaxRes: ()) -> list:

    def _CreateYOUTUBEObject (AURL: str, APlayList: str, ANumber: int, ACount: int) -> TYouTubeObject:
    #beginfunction
        s = 'CreateObject...'
        LULog.LoggerTOOLS.log(LULog.PROCESS, s)
        s = AURL
        LULog.LoggerTOOLS.log(LULog.PROCESS, s)
        LObjectID: datetime = LUDateTime.Now()
        s = LUDateTime.GenerateObjectIDStr (LObjectID)
        LULog.LoggerTOOLS.log(LULog.PROCESS, s)
        # LYouTubeObjectItem
        LYouTubeObject = TYouTubeObject()
        LYouTubeObject.ID = LObjectID
    
        LYouTubeObject.SetURL(AURL, AMaxRes, APlayList, ANumber, ACount)

        # LYouTubeObject.FONcomplete = ONcomplete
        # LYouTubeObject.FONprogress = ONprogress

        # LYouTubeObject.FONcomplete = complete_func
        # LYouTubeObject.FONprogress = progress_func

        return LYouTubeObject
    #endfunction
    def _CheckPlaylists (AURL: str, ADownload=False) -> list:
    #beginfunction
        LURLs = list()
        """
        # ЦИКЛ ОТ i=0 ДО AURLPlaylists.count-1
        """
        return LURLs
    #endfunction
    def _CheckYOUTUBEPlaylist (AURL: str, ADownload=False) -> list:
    #beginfunction
        LURLs = list()
        LPlaylist = Playlist (AURL)
        Lvideo_urls = LPlaylist.video_urls
        j = len(LPlaylist.video_urls)
        i = 0
        for url in Lvideo_urls:
            i = i + 1
            LURLs.append(_CreateYOUTUBEObject (url, LPlaylist.title, i, j))
        #endfor
        return LURLs
    #endfunction

#beginfunction
    LURI = urlparse (AURL)
    if LURI.hostname.upper() == CYOUTUBE_COM or LURI.hostname.upper() == CYOUTUBE_BE:
        if CYOUTUBE_PLAYLISTS in LURI.path.upper():
            LURLs = _CheckPlaylists (AURL)
            return LURLs
        else:
            if CYOUTUBE_PLAYLIST in LURI.path.upper():
                LURLs = _CheckYOUTUBEPlaylist (AURL)
                return LURLs
            else:
                LURLs = list ()
                LURLs.append (_CreateYOUTUBEObject (AURL, '', 0, 0))
                return LURLs
            #endif
        #endif
    #endif
#endfunction

#------------------------------------------
#
#------------------------------------------
def DownloadURL (AURL: str, APATH: str, AMaxRes: (), ADownload=False,
                 type='video', file_extension = 'mp4',
                 skip_existing = False, filename_prefix=''):
    """DownloadURL"""
#beginfunction
    LYouTube: YouTube = YouTube (AURL,
                                    on_progress_callback=progress_func,
                                    on_complete_callback=complete_func)
    LURLInfo = TYouTubeObject._GetURLInfo(LYouTube)
    for res in AMaxRes:
        try:
            LStreams = LYouTube.streams.filter (type=type, file_extension=file_extension, res=res)
        except BaseException as ERROR:
            LStreams = None
            s = f'filter={ERROR}'
            LULog.LoggerTOOLS.error (s)
        #endtry

        if not LStreams is None:
            i = 0
            for LStream in LStreams:
                LStreamInfo = TYouTubeObject._GetStreamInfo (LStream)
                i = i + 1
                Lfilename_prefix = filename_prefix+str (i) + '. '
                try:
                    if ADownload:
                        LFileName  = LStream.download (APATH, skip_existing=skip_existing, filename_prefix=Lfilename_prefix)
                        s = f'Видео успешно загружено: {LFileName}'
                    else:
                        s = LStreamInfo ['default_filename']
                        LFileName = LUStrUtils.PrintableStr (s)
                        s = f'Видео не загружалось: {LFileName}'
                    #endif
                    LULog.LoggerTOOLS.info(s)
                except BaseException as ERROR:
                    s = f'DownloadURL={ERROR}'
                    LULog.LoggerTOOLS.error(s)
                #endtry
            #endfor
            # если по фильтру есть хотя бы один поток
            break
        #endif
    #endfor

#endfunction

#------------------------------------------
#
#------------------------------------------
def DownloadURLVideo (AURL:str, APATH:str, ADownload=False):
    """DownloadURLVideo"""
#beginfunction
    LYouTube: YouTube = YouTube (AURL,
                                    # use_oauth = True, allow_oauth_cache = True,
                                    on_progress_callback = progress_func,
                                    on_complete_callback = complete_func)
    LURLInfo = TYouTubeObject._GetURLInfo(LYouTube)
    try:
        # все потоки
        LStreams = LYouTube.streams
        # все потоки progressive
        LStreams = LYouTube.streams.filter (progressive = True)
        # все потоки video, mp4, 480p
        LStreams = LYouTube.streams.filter (type='video', file_extension = 'mp4', res = '480p')
        for LStream in LStreams:
            LStreamInfo = TYouTubeObject._GetStreamInfo (LStream)
            if ADownload:
                LFileName  = LStream.download (APATH, skip_existing = False, filename_prefix=LStream.itag)
                s = f'Видео успешно загружено: {LFileName}'
            else:
                s = LStreamInfo ['default_filename']
                LFileName = LUStrUtils.PrintableStr (s)
                s = f'Видео не загружалось: {LFileName}'
            #endif
            LULog.LoggerTOOLS.info (s)
        #endfor
    # except BaseException as ERROR:
    except pytube.exceptions.PytubeError:
        print (pytube.exceptions.PytubeError)
        # s = f'DownloadURLVideo={ERROR}'
        # LULog.LoggerTOOLS.error (s)
    #endtry
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
