from app import *
import wave
from crypt import methods
from flask import Flask, request, render_template

def audio_check():
    if request.method == 'POST':
        file = request.files['file']
    try:
        wave.open(file, mode = 'rb')
        return "This is a valid audio file"
    except:
        return "This is an invalid WAV file. Please upload a valid .WAV file."

