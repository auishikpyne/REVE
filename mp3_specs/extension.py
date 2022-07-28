from app import *
import wave
from mutagen.mp3 import MP3
from crypt import methods
from flask import Flask, request, render_template



def mp3_specs():
    if request.method == 'POST':
        file = request.files['file']

    audio = MP3(file)
    
    d = dict()
    d['length'] = audio.info.length
    d['bit rate'] = audio.info.bitrate
    d['sample rate'] = audio.info.sample_rate
    d['encoder_info'] = audio.info.encoder_info
    d['Version'] = audio.info.version
    d['layer'] = audio.info.layer
    d['mode'] = audio.info.mode
    d['track gain'] = audio.info.track_gain
    d['track peak'] = audio.info.track_peak
    d['overall info'] = audio.info.pprint()

    return d


