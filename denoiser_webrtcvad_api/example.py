import collections
import contextlib
import sys
import wave
from pydub import AudioSegment
from torch import chunk
import webrtcvad
import os
import shutil
import json
import requests
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
disable_warnings(InsecureRequestWarning)

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# #directory creation
# if not os.path.exists('saved_chunks'):
#     os.mkdir('saved_chunks')

chunk_dict = {}
start_end_list = []



def read_wave(path):
    """Reads a .wav file.
    Takes the path, and returns (PCM audio data, sample rate).
    """
   
    pcm_data = AudioSegment.from_file(path).set_channels(1).set_sample_width(2).raw_data
    frame_rate = AudioSegment.from_file(path).frame_rate
    print(frame_rate)
    
    if frame_rate not in [8000, 16000, 32000, 48000]:
        print("changing sample rate . . . . . to 16000")
        pcm_data = AudioSegment.from_file(path).set_channels(1).set_sample_width(2).set_frame_rate(16000).raw_data
        frame_rate = 16000
    
    return pcm_data, frame_rate 


def write_wave(path, audio, sample_rate):
    """Writes a .wav file.
    Takes path, PCM audio data, and sample rate.
    """
    with contextlib.closing(wave.open(path, 'wb')) as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio)

    

class Frame(object):
    """Represents a "frame" of audio data."""
    def __init__(self, bytes, timestamp, duration):
        self.bytes = bytes
        self.timestamp = timestamp
        self.duration = duration


def frame_generator(frame_duration_ms, audio, sample_rate):
    """Generates audio frames from PCM audio data.
    Takes the desired frame duration in milliseconds, the PCM data, and
    the sample rate.
    Yields Frames of the requested duration.
    """
    n = int(sample_rate * (frame_duration_ms / 1000.0) * 2)
    offset = 0
    timestamp = 0.0
    duration = (float(n) / sample_rate) / 2.0
    while offset + n < len(audio):
        yield Frame(audio[offset:offset + n], timestamp, duration)
        timestamp += duration
        offset += n


def vad_collector(sample_rate, frame_duration_ms, padding_duration_ms, vad, frames):
    """Filters out non-voiced audio frames.
    Given a webrtcvad.Vad and a source of audio frames, yields only
    the voiced audio.
    Uses a padded, sliding window algorithm over the audio frames.
    When more than 90% of the frames in the window are voiced (as
    reported by the VAD), the collector triggers and begins yielding
    audio frames. Then the collector waits until 90% of the frames in
    the window are unvoiced to detrigger.
    The window is padded at the front and back to provide a small
    amount of silence or the beginnings/endings of speech around the
    voiced frames.
    Arguments:
    sample_rate - The audio sample rate, in Hz.
    frame_duration_ms - The frame duration in milliseconds.
    padding_duration_ms - The amount to pad the window, in milliseconds.
    vad - An instance of webrtcvad.Vad.
    frames - a source of audio frames (sequence or generator).
    Returns: A generator that yields PCM audio data.
    """
    num_padding_frames = int(padding_duration_ms / frame_duration_ms)
    # We use a deque for our sliding window/ring buffer.
    ring_buffer = collections.deque(maxlen=num_padding_frames)
    # We have two states: TRIGGERED and NOTTRIGGERED. We start in the
    # NOTTRIGGERED state.
    triggered = False
    
    voiced_frames = []
    for frame in frames:
        is_speech = vad.is_speech(frame.bytes, sample_rate)

        sys.stdout.write('1' if is_speech else '0')

        if not triggered:
            ring_buffer.append((frame, is_speech))
            num_voiced = len([f for f, speech in ring_buffer if speech])
            # If we're NOTTRIGGERED and more than 90% of the frames in
            # the ring buffer are voiced frames, then enter the
            # TRIGGERED state.
            if num_voiced > 0.9 * ring_buffer.maxlen:
                triggered = True
                sys.stdout.write('+(%s)' % (ring_buffer[0][0].timestamp))
                start_end_list.append(ring_buffer[0][0].timestamp)
                # dic['chunk']
                # We want to yield all the audio we see from now until
                # we are NOTTRIGGERED, but we have to start with the
                # audio that's already in the ring buffer.
                for f, s in ring_buffer:
                    voiced_frames.append(f)
                ring_buffer.clear()
        else:
            # We're in the TRIGGERED state, so collect the audio data
            # and add it to the ring buffer.
            voiced_frames.append(frame)
            ring_buffer.append((frame, is_speech))
            num_unvoiced = len([f for f, speech in ring_buffer if not speech])
            # If more than 90% of the frames in the ring buffer are
            # unvoiced, then enter NOTTRIGGERED and yield whatever
            # audio we've collected.
            if num_unvoiced > 0.9 * ring_buffer.maxlen:
                sys.stdout.write('-(%s)' % (frame.timestamp + frame.duration))
                start_end_list.append(frame.timestamp + frame.duration)
                triggered = False
                yield b''.join([f.bytes for f in voiced_frames])
                ring_buffer.clear()
                voiced_frames = []
    
    
    if triggered:
        sys.stdout.write('-(%s)' % (frame.timestamp + frame.duration))
        start_end_list.append(frame.timestamp + frame.duration)
    sys.stdout.write('\n')
    # If we have any leftover voiced audio when we run out of input,
    # yield it.
    if voiced_frames:
        yield b''.join([f.bytes for f in voiced_frames])


def get_chunks(path):
    if os.path.exists('/home/auishik/denoiser_webrtcvad_api/saved_chunks'):
        shutil.rmtree('/home/auishik/denoiser_webrtcvad_api/saved_chunks')
    os.makedirs('/home/auishik/denoiser_webrtcvad_api/saved_chunks')
    audio, sample_rate = read_wave(path)
    vad = webrtcvad.Vad(3) # agressiveness
    frames = frame_generator(30, audio, sample_rate)
    frames = list(frames)
    

    segments = vad_collector(sample_rate, 30, 300, vad, frames)
    
    
    dir = '/home/auishik/denoiser_webrtcvad_api/saved_chunks'
    stt_url = "https://dev.revesoft.com:9395/file"
    phonemizer_url =  'https://dev.revesoft.com:6790/phonemizer_non_contextual'

    
    payload = {}
    
    headers = {}
    
    for i, segment in enumerate(segments):
        path = f"{dir}/chunk-{i}.wav"
        print(' Writing %s' % (path,))
        write_wave(path, segment, sample_rate)
        
    print("start end list . . . . . . .:", (start_end_list))
    
    i = 0
    while len(start_end_list) > 0:
        chunk_dict[f"chunk-{i}"] = {}
        chunk_dict[f"chunk-{i}"]["id"] = f"SB_{i+1}"
        # chunk_dict[f"chunk-{i}"]["tierId"] = 1
        # chunk_dict[f"chunk-{i}"]["tierName"] = "sentence"
        chunk_dict[f"chunk-{i}"]["start"] = round(start_end_list.pop(0), 5)
        
        
        chunk_dict[f"chunk-{i}"]["end"] = round(start_end_list.pop(0), 5)
        
            
        files = [('file', (f'chunk-{i}.wav', open(f'/home/auishik/denoiser_webrtcvad_api/saved_chunks/chunk-{i}.wav', 'rb'),'audio/wav')
        )]
        chunk_dict[f"chunk-{i}"]["text"] = requests.post(stt_url, headers = headers, files=files, data = payload, verify=False).json()["output"]
        # script = chunk_dict[f"chunk-{i}"]["text"]
        # body = {
        #     "text" : script
        # }
        # chunk_dict[f"chunk-{i}"]["phoneme"] = requests.post(phonemizer_url, headers=headers, json=body, verify=False).json()["output"]
        
        print(chunk_dict[f"chunk-{i}"])
        i += 1
    
    
    print(chunk_dict)
    # with open('response.json', 'w', encoding='utf-8') as response_json:
    #     json.dump(chunk_dict, response_json, indent= 4)
        
    response_array = []
    
    for key, value in chunk_dict.items():
        response_array.append(chunk_dict[key])
        
    start_end_list.clear()
    chunk_dict.clear()
    
    return response_array

    