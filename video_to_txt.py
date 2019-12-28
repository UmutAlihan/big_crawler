import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks
from pytube import YouTube
from moviepy.editor import *
import os
import glob

class VideoToText:
    def __init__(self):
       pass


    def yt_download_video_convert_to_mp3(self,videourl):
        yt = YouTube(videourl)
        video_ext = yt.embed_url.split("/embed/")[1]

        yt = yt.streams.filter(progressive=True, file_extension='mp4')\
            .order_by('resolution')\
            .desc()\
            .first()

        if not os.path.exists("static"):
            os.makedirs("static")

        if not os.path.exists("static/"+video_ext):
            os.makedirs("static/"+video_ext)

        yt.download("static/"+video_ext,filename=video_ext)

        video = VideoFileClip(os.path.join("static/"+video_ext+"/"+video_ext+".mp4"))
        video.audio.write_audiofile(os.path.join("static/"+video_ext+"/"+video_ext+".mp3"))
        sound = AudioSegment.from_mp3("static/"+video_ext+"/"+video_ext+".mp3")
        sound.export("static/"+video_ext+"/"+video_ext+ ".wav", format="wav")

        myaudio = AudioSegment.from_file("static/"+video_ext+"/"+video_ext+ ".wav", "wav")
        chunk_length_ms = 3000  #
        chunks = make_chunks(myaudio, chunk_length_ms)

        for i, chunk in enumerate(chunks):
            chunk_name = "{}{}.wav".format(video_ext, i)
            print("exporting", chunk_name)
            if not os.path.exists("static/" + video_ext+"_chunk"):
                os.makedirs("static/" + video_ext+"_chunk")

            chunk.export("static/"+ video_ext+"_chunk/"+chunk_name, format="wav")


    def run(self,video_ext):
        tifCounter = len(glob.glob1("static/"+ video_ext+"_chunk/", "*.wav"))
        for i in range(tifCounter):
            file = "{}{}.wav".format("static/"+ video_ext+"_chunk/{}".format(video_ext),i)

            r = sr.Recognizer()

            with sr.AudioFile(file) as source:
                audio = r.record(source)
                try:
                    print(r.recognize_google(audio, language="tr"))

                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")


videourl = "https://www.youtube.com/watch?v=vfZQK1G2O90"
VideoToText().run("vfZQK1G2O90")