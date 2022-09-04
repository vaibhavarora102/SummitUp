from django.core.files.storage import FileSystemStorage
from django.http import *
from django.shortcuts import *
import sqlite3
import random
from django.views.decorators.csrf import *

import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub import AudioSegment
import moviepy.editor
from transformers import pipeline
from transformers import BartTokenizer, BartForConditionalGeneration

from templates import *

def index(request):
    return render(request, "index.html")

# create a speech recognition object
r = sr.Recognizer()
def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text
    # return the text for all chunks detected
    return whole_text


def summarizeTheText(inpt):
    model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
    tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")

    ARTICLE_TO_SUMMARIZE=inpt

    inputs = tokenizer([ARTICLE_TO_SUMMARIZE], max_length=1024, return_tensors="pt")

    summary_ids = model.generate(inputs["input_ids"], num_beams=2, min_length=0, max_length=20)
    temp = tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
    return temp

def audioToText(request):
    #video path
    files=os.listdir("static\\media")[:1]
    for i in files:
        path=r"static\\media\\"+i
        video = moviepy.editor.VideoFileClip(path)
        audio = video.audio
        audio.write_audiofile(r"my_result.wav")
        res=get_large_audio_transcription(r"my_result.wav")
        print(summarizeTheText(res))

    return HttpResponse("Done")

@csrf_exempt
def uploadVideo(request):
    # Step1 upload Photo
    path=""
    if request.method == "POST":
    # if the post request has a file under the input name 'document', then save the file.
        request_file = request.FILES['vdo']
        if request_file:
            # create a new instance of FileSystemStorage
            fs = FileSystemStorage()
            file = fs.save(request_file.name, request_file)
            # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.                        
            video = moviepy.editor.VideoFileClip(file)
            audio = video.audio
            audio.write_audiofile(r"my_result.wav")
            res=summarizeTheText(get_large_audio_transcription(r"my_result.wav"))  
    return render(request, "summary.html", {"smry": summarizeTheText(res).split(' ')})
