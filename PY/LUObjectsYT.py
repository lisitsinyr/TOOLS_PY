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
import io
import datetime
import logging
import string
from typing import BinaryIO

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
from urllib.parse import urlparse

from pytube import YouTube, request
from pytube import Playlist
import pytube
import pytube.exceptions

#------------------------------------------
# БИБЛИОТЕКИ LU
#------------------------------------------
import LULog
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

def progress_func (AStream, AChunk: bytes, Abytes_remaining: int):
#beginfunction
    s = 'progress_func...'
    LULog.LoggerTOOLS.info (s)
    # if not AStream is None:
    #     LProgressMax = AStream.filesize
    #     LProgressLeft = Abytes_remaining
    #     LProgressValue = LProgressMax - LProgressLeft
    #     if not AChunk is None:
    #         ...
    #     #endif
    #     ...
    # #endif
#endfunction

def complete_func (AStream, AFilePath: str):
#beginfunction
    s = 'complete_func...'
    LULog.LoggerTOOLS.info (s)
    if not AStream is None:
        LProgressMax = AStream.filesize
        LProgressLeft = 0
        LProgressValue = LProgressMax - LProgressLeft
        # LULog.LoggerTOOLS.info (f'{LProgressMax}-{LProgressLeft}-{LProgressValue}')

        if not AFilePath is None:
            LFileName = LUStrUtils.PrintableStr (AFilePath)
            LULog.LoggerTOOLS.info ('Файл ' + LFileName + ' загружен')
        #endif
    #endif
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
        self.__FObjectType: TObjectTypeClass = TObjectTypeClass.otYouTubeObject

        self.__FYouTube: YouTube = None
        self.__FStream: pytube.Stream = None
        self.__FURL: str = ''
        self.__FID: datetime = 0
        self.__FURLInfo = dict ()
        self.__FStreamInfo = dict ()
        self.__FPlayList: str = ''
        self.__FNumber: int = 0
        self.__FCount: int = 0

        # self.__FONprogress = ONfunction
        # self.__FONcomplete = ONfunction
        # self.__FONprogress = progress_func
        # self.__FONcomplete = complete_func
        self.__FONprogress = self.ONprogress
        self.__FONcomplete = self.ONcomplete

        self.__FProgressMax: int = 0
        self.__FProgressMin: int = 0
        self.__FProgressValue: int = 0
        self.__FProgressLeft: int = 0

        self.__FYouTubeThread: LUThread.TThread = None
        self.__FStopYouTubeBoolean: bool = False
        self.__FStopYouTubeBooleanThread: bool = False

        self.__Fis_paused = False
        self.__Fis_cancelled = False
        self.__Filechunk: io.BufferedWriter = None
        self.__FileNamechunk = ''
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

    #--------------------------------------------------
    # ONprogress
    #--------------------------------------------------
    # def show_progress_bar (stream, chunk, bytes_remaining):
    #     prog.update (task, completed = stream.filesize - bytes_remaining)
    #     #this show the bytes_remaining, use rich to display a progress bar
    #--------------------------------------------------
    def ONprogress (self, AStream: pytube.Stream, AChunk: bytes, Abytes_remaining: int):
    #beginfunction
        s = 'TYouTubeObject.ONprogress...'
        LULog.LoggerTOOLS.info (s)
        if not AStream is None:
            self.__FProgressMax = AStream.filesize
            self.__FProgressLeft = Abytes_remaining
            self.__FProgressValue = self.__FProgressMax - self.__FProgressLeft
            # LULog.LoggerTOOLS.info (f'{self.__FProgressMax}-{self.__FProgressLeft}-{self.__FProgressValue}')

            if not AChunk is None:
                if not self.__Filechunk is None:
                    self.__Filechunk.write (AChunk)
                #endif
            #endif
        #endif
    #endfunction

    #--------------------------------------------------
    # ONcomplete
    #--------------------------------------------------
    # def on_complete (stream, file_path):
    #     prog.remove_task (task)
    #     prog.stop ()
    #     print ('[green] Downloaded ', file_path.split ('/') [-1], '\n')
    #--------------------------------------------------
    def ONcomplete (self, AStream: pytube.Stream, AFilePath: str):
    #beginfunction
        s = 'TYouTubeObject.ONcomplete...'
        LULog.LoggerTOOLS.info (s)
        if not AStream is None:
            self.__FProgressMax = AStream.filesize
            self.__FProgressLeft = 0
            self.__FProgressValue = self.__FProgressMax - self.__FProgressLeft

            if not AFilePath is None:
                LFileName = LUStrUtils.PrintableStr (AFilePath)
                LULog.LoggerTOOLS.info ('Файл ' + LFileName + ' загружен')
            #endif

            if not self.__FYouTubeThread is None:
                self.__FYouTubeThread.StopThread()
                # self.__FYouTubeThread.FStopThread = True
            #endif
        #endif
    #endfunction

    @staticmethod
    def GetURLInfo (AYouTube: YouTube) -> {}:
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
        s = AYouTube.title
        LURLInfo['title'] = LUStrUtils.PrintableStr(s)
        # продолжительность видео [Get the video length in seconds]
        LURLInfo['length'] = AYouTube.length

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
        self.__FURLInfo = self.GetURLInfo (self.__FYouTube)
    #endfunction

    @staticmethod
    def GetStreamInfo (AStream: pytube.Stream) -> {}:
        """GetStreamInfo"""
    #beginfunction
        LStreamInfo = dict ()
        s = AStream.default_filename
        LStreamInfo['default_filename'] = LUStrUtils.PrintableStr(s)
        # LStreamInfo['title'] = AStream.title
        i = AStream.filesize
        LStreamInfo['filesize'] = i
        # ('1080p', '720p', '480p', '360p', '240p', '144p')
        # LStreamInfo['resolution'] = AStream.resolution
        # 'video'|'audio'
        # LStreamInfo['type'] = AStream.type
        # video/mp4
        # LStreamInfo['mime_type'] = AStream.mime_type
        # itag
        # LStreamInfo['itag'] = AStream.itag
        LStreamInfo['itag'] = 'itag'
        # subtype
        # LStreamInfo['subtype'] = AStream.subtype

        # размер приблизительно
        # LStreamInfo['filesize_approx'] = AStream.filesize_approx
        # размер в Гб
        # LStreamInfo['filesize_gb'] = AStream.filesize_gb
        # размер в Кб
        # LStreamInfo['filesize_kb'] = AStream.filesize_kb
        # размер в Мб
        # LStreamInfo['filesize_mb'] = AStream.filesize_mb
        # url видео плейера
        # LStreamInfo['url'] = AStream.url
        # Get the video/audio codecs from list of codecs.
        # LStreamInfo['parse_codecs'] = AStream.parse_codecs ()
        # True/False - Whether the stream only contains audio.
        # LStreamInfo['includes_audio_track'] = AStream.includes_audio_track
        # True/False - Whether the stream only contains video.
        # LStreamInfo['includes_video_track'] = AStream.includes_video_track
        # #Whether the stream is DASH.
        # LStreamInfo['is_adaptive'] = AStream.is_adaptive
        # #Whether the stream is progressive.
        # LStreamInfo['is_progressive'] = AStream.is_progressive
        # AStream.exists_at_path()
        return LStreamInfo
    #endfunction

    def __SetStreamInfo (self, AStream: pytube.Stream):
        """SetStreamInfo"""
    #beginfunction
        self.__FStreamInfo = self.GetStreamInfo(AStream)
    #endfunction

    #--------------------------------------------------
    #
    #--------------------------------------------------
    def SetStream(self, AMaxRes: ()):
    #beginfunction
        self.__FStream = None
        for res in AMaxRes:
            LStreams = list ()
            try:
                LStreams = self.__FYouTube.streams.filter (res=res, type='video', file_extension='mp4')
            except BaseException as ERROR:
                s = f'__FYouTube.streams.filter={ERROR} res={res} URL={self.URL}'
                LULog.LoggerTOOLS.error(s)
            #endtry
            if len (LStreams) > 0:
                for LStream in LStreams:
                    try:
                        self.__SetStreamInfo (LStream)
                        self.__FStream = LStream
                        break
                    except BaseException as ERROR:
                        s = f'__SetStreamInfo={ERROR} res={res} URL={self.URL}'
                        LULog.LoggerTOOLS.error (s)
                    #endtry
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
        # self.SetStream(AMaxRes)
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

    #--------------------------------------------------
    # @property YOUTUBE
    #--------------------------------------------------
    # getter
    @property
    def YOUTUBE(self) -> YouTube:
    #beginfunction
        return self.__FYouTube
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

    def Clear (self):
        """Clear"""
    #beginfunction
        self.__FURL = ''
        self.ID = 0
        self.StopYouTubeBoolean = False
        self.ProgressMax = 0
        self.YouTubeThread = None
        self.PlayList = ''
        self.Number = 0
    #endfunction

    def DownloadURL_chunk (self, APATH: str, Afilename_prefix: str):
        """DownloadURL_chunk"""
    #beginfunction
        try:
            s = self.__FStreamInfo ['default_filename']
            self.__FileNamechunk = os.path.join (APATH, Afilename_prefix+s)
            s = self.__FStreamInfo ['filesize']
            LFileSize = int(s)
            if not self.__FStream.exists_at_path (self.__FileNamechunk):
                with open(self.__FileNamechunk, 'wb') as self.__Filechunk:
                    stream = request.stream(self.__FStream.url) # get an iterable stream
                    Ldownloaded = 0
                    while True:
                        if self.__Fis_cancelled:
                            break
                        #endif
                        if self.__Fis_paused:
                            continue
                        #endif
                        Lchunk = next(stream, None) # get next chunk of video
                        if Lchunk:
                            self.__FONprogress (self.__FStream, Lchunk, LFileSize-Ldownloaded)
                            # self.__Filechunk.write(Lchunk)
                            Ldownloaded += len(Lchunk)
                        else:
                            # no more data
                            self.__FONcomplete (self.__FStream, self.__FileNamechunk)
                            break
                        #endif
                    #endwhile
                #endwith
            else:
                self.__FONcomplete (self.__FStream, self.__FileNamechunk)
                # LULog.LoggerTOOLS.info ('Файл ' + self.__FileNamechunk + ' существует...')
            #endif
        except Exception as ERROR:
            LULog.LoggerTOOLS.error(ERROR)
    #endfunction

    def DownloadURL (self, APATH: str, ADownload=False, Achunk=False,
                     filename_prefix='', skip_existing=False):
        """DownloadURL"""
    #beginfunction
        s = self.URLInfo ['thumbnail_url']
        s = self.URLInfo ['author']
        s = self.URLInfo ['title']
        if not self.__FONprogress is None:
            self.__FYouTube.register_on_progress_callback(self.__FONprogress)
        if not self.__FONcomplete is None:
            self.__FYouTube.register_on_complete_callback(self.__FONcomplete)

        if len(self.PlayList) > 0:
            LPATH = os.path.join (APATH, self.PlayList)
            if not LUFile.DirectoryExists (LPATH):
                LUFile.ForceDirectories (LPATH)
            Lfilename_prefix = LUStrUtils.AddChar('0', str (self.Number), 3)+'. '
        else:
            LPATH = APATH
            Lfilename_prefix = filename_prefix
        #endif

        #ПРОВЕРИТЬ
        try:
            LFilesize = self.__FStreamInfo ['filesize']
        except:
            LFilesize = 0
        #endtry
        #ПРОВЕРИТЬ
        try:
            LFileName = os.path.join (LPATH, Lfilename_prefix+self.__FStreamInfo ['default_filename'])
        except:
            LFileName = ''
        #endtry

        if ADownload and len (LFileName) > 0:
            LPATH = os.path.join (APATH, self.PlayList)
            # if not self.__FStream.exists_at_path (LFileName):
            if True:
                if not Achunk:
                    try:
                        LFileName = self.__FStream.download (LPATH,
                                                             skip_existing=skip_existing,
                                                             filename_prefix=Lfilename_prefix)
                    # except BaseException as ERROR:
                    except Exception as ERROR:
                        s = f'DownloadURL={ERROR}'
                        LULog.LoggerTOOLS.error (s)
                    #endtry
                else:
                    self.DownloadURL_chunk (LPATH, Lfilename_prefix)
                #endif
            else:
                LULog.LoggerTOOLS.info ('Файл ' + LFileName + ' существует...')
                self.FONcomplete (self.__FStream, None)
            #endif
        else:
            N = LFilesize // 4
            i = N
            while i < LFilesize:
                self.__FONprogress(self.__FStream, None, N-i)
                i = i + N
            #endwhile
            self.__FONcomplete (self.__FStream, None)
        #endif
    #endfunction

    def StartYouTubeThread (self, *args, **kwargs):
        """StartYouTubeThread"""
    #beginfunction
        self.__FYouTubeThread = LUThread.TThread(target = self.DownloadURL, args=args, kwargs=kwargs)

        self.__FYouTubeThread.StartThread()
        # self.FYouTubeThread.start ()

    #endfunction
#endclass

def CheckURLs (AURL: str, AURLs: dict):

    def _CheckPlaylists ():
    #beginfunction
        """
        # ЦИКЛ ОТ i=0 ДО AURLPlaylists.count-1
        """
        ...
    #endfunction

    def _CheckYOUTUBEPlaylist ():
    #beginfunction
        LPlaylist = Playlist (AURL)
        Lvideo_urls = LPlaylist.video_urls
        j = len(LPlaylist.video_urls)
        i = 0
        for url in Lvideo_urls:
            i = i + 1
            LPlaylistTitle = LUStrUtils.DelChars(LPlaylist.title, '/')
            AURLs[url] = {'PlayListName': LPlaylistTitle, 'N': j, 'NN': i}
        #endfor
    #endfunction

#beginfunction
    LURI = urlparse (AURL)
    if LURI.hostname.upper() == CYOUTUBE_COM or LURI.hostname.upper() == CYOUTUBE_BE:
        if CYOUTUBE_PLAYLISTS in LURI.path.upper():
            _CheckPlaylists ()
        else:
            if CYOUTUBE_PLAYLIST in LURI.path.upper():
                _CheckYOUTUBEPlaylist ()
            else:
                AURLs [AURL] = {'PlayListName': '', 'N': 1, 'NN': 1}
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
    LURLInfo = TYouTubeObject.GetURLInfo(LYouTube)

    LPATH = APATH

    # все потоки
    LStreams = LYouTube.streams
    # все потоки progressive
    LStreams = LYouTube.streams.filter (progressive = True)
    # все потоки video, mp4, LMaxRes
    LMaxRes = cMaxRes480p
    LMaxRes = cMaxRes1080p
    LMaxRes = AMaxRes

    for res in LMaxRes:
        try:
            LStreams = LYouTube.streams.filter (type=type, file_extension=file_extension, res=res)
        except BaseException as ERROR:
            LStreams = None
            s = f'filter={ERROR}'
            LULog.LoggerTOOLS.error (s)
        #endtry

        if not LStreams is None:
            for LStream in LStreams:
                LStreamInfo = TYouTubeObject.GetStreamInfo (LStream)
                LTag = LStreamInfo ['itag']
                Lresolution = LStreamInfo ['resolution']
                # LULog.LoggerTOOLS.info (Lresolution)

                Lfilename_prefix = filename_prefix
                LFileName = os.path.join (LPATH, Lfilename_prefix + LStreamInfo ['default_filename'])

                try:
                    if ADownload:
                        if not LStream.exists_at_path (LFileName):
                            s  = LStream.download (APATH, skip_existing=skip_existing, filename_prefix=filename_prefix)
                        else:
                            LULog.LoggerTOOLS.info ('Файл ' + LFileName + ' существует...')
                            complete_func (LStream, None)
                        #endif
                    else:
                        LFileName = LStreamInfo ['default_filename']
                        AFileSize = int (LStreamInfo ['filesize'])
                        N = AFileSize // 4
                        i = N
                        while i < AFileSize:
                            progress_func (LStream, None, i)
                            i = i + N
                        #endwhile
                        s = f'Видео не загружалось: {res}/{LTag}={LFileName}'
                        LULog.LoggerTOOLS.info (s)
                        complete_func (LStream, None)
                    #endif
                except BaseException as ERROR:
                    s = f'DownloadURL={ERROR}'
                    LULog.LoggerTOOLS.error (s)
                    LULog.LoggerTOOLS.error (LFileName)
                #endtry
            #endfor
            # если по фильтру есть хотя бы один поток
            break
        #endif
    #endfor
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
