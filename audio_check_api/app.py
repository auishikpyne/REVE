from flask import Flask, render_template, request

import wave

from extension import *

app = Flask(__name__)

#app.config['MAX_CONTENT_LENGTH'] = 15 * 1024 * 1024 

@app.route('/upload')

def upload_file():
    return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])

def upload_file_1():

    result = audio_check()

    return result
		
if __name__ == '__main__':
    app.run(debug = True)