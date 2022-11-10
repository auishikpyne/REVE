from fastapi import FastAPI, File, UploadFile, Request
import json
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import wave
import logging
from pydub import AudioSegment
from df_fb_denoiser import deepfilternet
from example import get_chunks

logging.basicConfig(filename='file.log',
                    filemode='a',
                    format='%(asctime)s %(levelname)s-%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

logger.info("Just an information")
logger.warning("Its a Warning")
logger.error("Did you try to divide by zero")
logger.critical("Internet is down")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Body(BaseModel):
    path:str
    
    
@app.get('/')
async def home():
    return "Fast server is working!"

@app.post('/get_denoised_segments_from_path/')
async def denoised_webrtcvad(body:Body):
    
    path = body.dict()['path']
    logger.debug("Harmless debug Message")
    out_path = deepfilternet(path)
    return get_chunks(out_path)

@app.post('/get_denoised_segments/')
async def webrtcvad(file: UploadFile = File(...)):
    file_location = f"/home/auishik/denoiser_webrtcvad_api/audio_files/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
        
    out_path = deepfilternet(file_location)
    return get_chunks(out_path)
        
        
        
    
if __name__=="__main__":
    uvicorn.run("main:app", host='0.0.0.0', port = 7777, reload = True)