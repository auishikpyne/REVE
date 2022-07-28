from flask import Flask, render_template, request
from mutagen.mp3 import MP3
import wave
from werkzeug.wrappers.request import Request
from werkzeug.exceptions import HTTPException, NotFound

from extension import *

app = Flask(__name__)

#app.config['MAX_CONTENT_LENGTH'] = 15 * 1024 * 1024 

@app.route('/upload')

def upload_file():
    return render_template('upload.html')
	
@app.route('/show', methods = ['GET', 'POST'])

def upload_file_1():

    result = mp3_specs()

    return result
		
if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug = True, port= 5000)