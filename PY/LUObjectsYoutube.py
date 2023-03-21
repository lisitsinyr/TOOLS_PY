"""LUObjectsYouTube.py"""
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
     LUObjectsYouTube.py

 =======================================================
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
import datetime
from pytube import YouTube
from pytube import Playlist

#------------------------------------------
# БИБЛИОТЕКИ LU
#------------------------------------------
from LUObjects import TObjectTypeClass, TObjects

cYUOTUBE = 'WWW.YOUTUBE.COM'
cYUOTUBE_PLAYLISTS = 'PLAYLISTS'
cYUOTUBE_PLAYLIST = 'PLAYLIST'

# where to save
SAVE_PATH = "D:/PROJECTS_LYR/CHECK_LIST/05_DESKTOP/02_Python/PROJECTS_PY/YUOTUBE/TEST_01/STORE"

# link of the video to be downloaded
link1 = "https://www.youtube.com/watch?v=xWOoBJUqlbI"
link2 = "https://www.youtube.com/watch?v=xFKd5q0hqcQ"
link3 = "https://www.youtube.com/watch?v=m6WjhPiUFhw"

playlist1 = "https://www.youtube.com/playlist?list=PLlrxD0HtieHhS8VzuMCfQD4uJ9yne1mE6"
playlist2 = "https://www.youtube.com/playlist?list=PLZcsUsGMRuTc-5-ZHMJVi4mmS2woW1ZKX"

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
        self.__FYoutubeThread = None                    # TYoutubeThreadNew
        self.__FObjectType: TObjectTypeClass = TObjectTypeClass.otYouTubeObject
        self.Clear()
    #endfunction

    #--------------------------------------------------
    # destructor
    #--------------------------------------------------
    def __del__(self):
        """destructor"""
    #beginfunction
        LCclassName = self.__class__.__name__
        #print('{} уничтожен'.format(LCclassName))
        super ().__del__()
    #endfunction

    #--------------------------------------------------
    # @property URL
    #--------------------------------------------------
    # getter
    @property
    def URL(self) -> str:
    #beginfunction
        return self.__FURL
    #endfunction
    # setter
    @URL.setter
    def URL(self, Value: str):
    #beginfunction
        self.__FURL = Value
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
    # @property YoutubeThread
    #--------------------------------------------------
    # getter
    @property
    def YoutubeThread(self):
    #beginfunction
        return self.__FYoutubeThread
    #endfunction
    @YoutubeThread.setter
    def YoutubeThread(self, Value):
    #beginfunction
        self.__FYoutubeThread = Value
    #endfunction

    #public
    def Clear (self):
        """Clear"""
    #beginfunction
        self.URL = ''
        self.ID = 0
        self.StopYouTubeBoolean = False
        self.ProgressMax = 0
        self.RxProgress = None
        self.YoutubeThread = None
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
        pass
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
            FYoutubeThread := nil
        end
        """
        ...
    #endfunction

    def StopYouTubeThread (self):
        """StopYouTubeThread"""
    #beginfunction
        self.__FStopYouTubeBooleanThread = True
        # FRxProgress.Position := 0
        self.__FYoutubeThread = None
    #endfunction

    def StartYouTubeThread (self, ATerminateProc): # TTerminateProc
        """StartYouTubeThread"""
    #beginfunction
        """
        if not Assigned (FYoutubeThread) then
        begin
            FYoutubeThread := TYoutubeThreadNew.Create (UpdateProgressBarThread, True)
            FYoutubeThread.Priority := tpNormal
            FYoutubeThread.FreeOnTerminate := True
            FYoutubeThread.TerminateProc := aTerminateProc
            (*
            Происходит после возврата метода Execute
            потока и перед уничтожением потока.
            *)
            FYoutubeThread.OnTerminate := aTerminateProc
            FYoutubeThread.FObjectIDStr := GenerateObjectIDStr (ID)
            FYoutubeThread.FStopYouTubeBooleanThread := False
            FYoutubeThread.Start ()
        end
        """
        pass
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
        #print('{} уничтожен'.format(LClassName))
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
# TYoutubeObjectsCollection
# --------------------------------------------
class TYoutubeObjectsCollection (list):
    """TObjectsCollection"""
    luClassName = "TYoutubeObjectsCollection"

    #--------------------------------------------------
    # constructor
    #--------------------------------------------------
    def __init__ (self):
        """Constructor"""
        super ().__init__ ()
    #endfunction

    #--------------------------------------------------
    # destructor
    #--------------------------------------------------
    def __del__ (self):
    #beginfunction
        """destructor"""
        LClassName = self.__class__.__name__
        #print('{} уничтожен'.format(LClassName))
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
        for YouTubeObjectsItem in self:
            LURL: str = YouTubeObjectsItem.URL
            if LURL == AURL:
                LResult = YouTubeObjectsItem
                return LResult
            #endif
        #endfor
    #endfunction
#endclass

def LoadYouTubeVideo0 (AURL:str, aSAVE_PATH:str):
    """LoadYouTubeVideo0"""
#beginfunction
    try:
        # object creation using YouTube
        # which was imported in the beginning
        Lyt: YouTube = YouTube(AURL)
        print (Lyt.author)
        #LStream = yt.streams.first()
        for LVideoStream in Lyt.streams:
            print (LVideoStream)
            LVideoStream.download (aSAVE_PATH)
            print ("Видео успешно загружено")
    except:
        print("Connection Error") #to handle exception

    # filters out all the files with "mp4" extension
    #mp4files = Lyt.filter('mp4')

    # to set the name of the file
    #Lyt.set_filename('GeeksforGeeks Video')

    # get the video with the extension and
    # resolution passed in the get() function
    #Lvideo = Lyt.get(mp4files[-1].extension,mp4files[-1].resolution)

    #try:
    #   # downloading the video
    #   Lvideo.download(SAVE_PATH)
    #except:
    #   print("Some Error!")
#endfunction

def LoadYouTubeVideo1 (AURL:str, aSAVE_PATH:str):
    """LoadYouTubeVideo1"""
#beginfunction
    try:
        # object creation using YouTube
        # which was imported in the beginning
        Lyt: YouTube = YouTube(AURL)

        #-------------------------------------------------------------------
        #register_on_complete_callback(func: Callable[[Any, Optional[str]], None])[source]
        #Register a download complete callback function post initialization.
        #Parameters: func (callable) - A callback function that takes stream and file_path.
        #Return type:    None
        #-------------------------------------------------------------------
        #register_on_progress_callback(func: Callable[[Any, bytes, int], None])[source]
        #Register a download progress callback function post initialization.
        #Parameters: func (callable) - A callback function that takes stream, chunk, and bytes_remaining as parameters.
        #Return type:    None
        #-------------------------------------------------------------------

        #Get the video author.
        print (Lyt.author)
        #Get a list of Caption.
        print (Lyt.caption_tracks)
        #Interface to query caption tracks.
        print (Lyt.captions)
        #Get the video poster’s channel id.
        print (Lyt.channel_id)
        #Construct the channel url for the video’s poster from the channel id.
        print (Lyt.channel_url)
        #Get the video description.
        print (Lyt.description)
        #Returns a list of streams if they have been initialized.
        print (Lyt.fmt_streams)
        #Get the video keywords.
        print (Lyt.keywords)
        #Get the video length in seconds.
        print (Lyt.length)
        #Get the metadata for the video.
        print (Lyt.metadata)
        #Get the publish date.
        print (Lyt.publish_date)
        #Get the video average rating.
        print (Lyt.rating)
        #Return streamingData from video info.
        print (Lyt.streaming_data)
        #Interface to query both adaptive (DASH) and progressive streams.
        print (Lyt.streams)
        #Get the thumbnail url image.
        print (Lyt.thumbnail_url)
        #Get the video title.
        print (Lyt.title)
        #Parse the raw vid info and return the parsed result.
        print (Lyt.vid_info)
        #Get the number of the times the video has been viewed.
        print (Lyt.views)

        #LStream = yt.streams.first()

        for LVideoStream in Lyt.streams:
            print (LVideoStream)
            print (LVideoStream.itag)
            print (LVideoStream.mime_type)
            print (LVideoStream.type)
            #print (VideoStream.progressive)

            # video
            #print (LVideoStream.res)
            #print (LVideoStream.vcodec)
            #print (LVideoStream.fps)
            # audio
            #print (LVideoStream.abr)
            #print (LVideoStream.acodec)

            #Generate filename based on the video title.
            print (LVideoStream.default_filename)
            #File size of the media stream in bytes.
            print (LVideoStream.filesize)
            #Get approximate filesize of the video
            print (LVideoStream.filesize_approx)
            #File size of the media stream in gigabytes.
            print (LVideoStream.filesize_gb)
            #File size of the media stream in kilobytes.
            print (LVideoStream.filesize_kb)
            #File size of the media stream in megabytes.
            print (LVideoStream.filesize_mb)
            #Whether the stream only contains audio.
            print (LVideoStream.includes_audio_track)
            #Whether the stream only contains video.
            print (LVideoStream.includes_video_track)
            #Whether the stream is DASH.
            print (LVideoStream.is_adaptive)
            #Whether the stream is progressive.
            print (LVideoStream.is_progressive)
            #On download complete handler function.
            #on_complete (file_path: Optional [str])[source]
            #On progress callback function.
            #on_progress (chunk: bytes, file_handler: BinaryIO, bytes_remaining: int)[source]
            #Get the video/audio codecs from list of codecs.
            print (LVideoStream.parse_codecs ())
            #Write the media stream to buffer
            #stream_to_buffer (buffer: BinaryIO) - None [source]
            #Get title of video
            print (LVideoStream.title)
            #if LVideoStream.type.split ('/')[0] == 'video':
            if LVideoStream.type == 'video':
                print ("Это Видео !!!!!!!!!!!!!")
                #download (output_path: Optional[str] = None, filename: Optional[str] = None,
                # filename_prefix: Optional[str] = None, skip_existing: bool = True,
                # timeout: Optional[int] = None, max_retries: Optional[int] = 0) → str
                LVideoStream.download (aSAVE_PATH)
                print ("Видео успешно загружено")
            else:
                print ("Это не Видео")

    except:
        print("Connection Error") #to handle exception
#endfunction

def LoadPlaylist (APlayListURL):
    """LoadPlaylist"""
#beginfunction
    Lplaylist = Playlist (APlayListURL)
    print (f"Загрузка плейлиста: {Lplaylist.title}")
    for Lvideo in Lplaylist.videos:
        Lvideo.streams.first ().download ()
        print (f"Видео {Lvideo.title} загружено")
#endfunction

def PrintPlaylistVideoURL (APlayListURL):
    """PrintPlaylistVideoURL"""
#beginfunction
    Lplaylist = Playlist (APlayListURL)
    for Lurl in Lplaylist.video_urls:
        print (Lurl)
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
