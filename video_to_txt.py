import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks
from pytube import YouTube
from moviepy.editor import *
import os
import glob

class VideoToText:
    def __init__(self,yt_url,file_name):
        self.file_name =file_name
        YouTube(yt_url).streams.first().download()
        self.yt = YouTube(yt_url)
        self.yt_download_video_convert_to_mp3()
        self.mp3_to_wav_mem()
        self.wav_chunks()

    def yt_download_video_convert_to_mp3(self):
        print("yt",self.file_name)
        self.yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(filename=self.file_name)

        video = VideoFileClip(os.path.join(self.file_name+".mp4"))
        video.audio.write_audiofile(os.path.join(self.file_name+".mp3"))

    def mp3_to_wav_mem(self):
        sound = AudioSegment.from_mp3(self.file_name+".mp3")
        sound.export(self.file_name+".wav", format="wav")

    def wav_chunks(self):
        myaudio = AudioSegment.from_file(self.file_name+".wav", "wav")
        chunk_length_ms = 3000  # pydub calculates in millisec
        chunks = make_chunks(myaudio, chunk_length_ms)  # Make chunks of one sec

        for i, chunk in enumerate(chunks):
            chunk_name = "{}{}.wav".format(self.file_name,i)
            print("exporting", chunk_name)
            chunk.export("static/"+chunk_name, format="wav")


    def run(self):
        tifCounter = len(glob.glob1("static", "*.wav"))
        for i in range(tifCounter):
            file = "{}{}.wav".format("static/{}".format(self.file_name),i)
            r = sr.Recognizer()

            with sr.AudioFile(file) as source:
                audio = r.record(source)
                try:
                    print(r.recognize_google(audio, language="tr"))

                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")


VideoToText(yt_url="https://www.youtube.com/watch?v=vfZQK1G2O90",file_name="paramore").run()