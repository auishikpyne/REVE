import os 
# from IPython import display as disp
import torch
import torchaudio
from denoiser import pretrained
from denoiser.dsp import convert_audio
import soundfile as sf
import librosa as lr


# input_path = '/home/auishik/denoiser/audio_files/Meeting_Recording_1.wav'
output_dir = '/home/auishik/denoiser_webrtcvad_api/saved_files/'
# wav, sr = torchaudio.load(path)

def filename_extension(path):
    filename = path.split(os.sep)[-1].split('.')[0]
    extension = '.' + (path.split(os.sep)[-1].split('.')[-1])
    return filename, extension



def deepfilternet(path):
    os.system(f'deepFilter "{path}" --output-dir {output_dir}')
    filename, extension = filename_extension(path)
    output_path = output_dir + filename  + '_DeepFilterNet2' + extension
    return output_path

# def facebook_denoiser(path):
#     model = pretrained.dns64()
#     wav, sr = torchaudio.load(path)
#     print(sr, model.sample_rate)
#     wav = convert_audio(wav, sr, model.sample_rate, model.chin)
    
#     filename, extension = filename_extension(path)
#     output_path = f"{output_dir}{filename}_facebook_denoised{extension}"
#     with torch.no_grad():
#         denoised = model(wav)[0]
#         np_arr = denoised.cpu().detach().numpy()
#         # print(np_arr, type(np_arr))
#         sf.write(output_path, np_arr.T, sr)
#     return output_path
    



# def combined_denoiser(path):
#     deepfilter_output = deepfilternet(path)
#     print("deep filter output: ", (deepfilter_output))

#     combined_output = facebook_denoiser(deepfilter_output)
#     print("facebook output :", combined_output)
    
#     filename, extension = filename_extension(path)
#     output_path = f"{output_dir}{filename}_combined_denoised{extension}"

#     y, sample_rate = lr.load(combined_output, sr=None)
#     print(sample_rate)
#     sf.write(output_path, y, sample_rate)
#     print("combined output :", output_path)
#     os.remove(deepfilter_output)
#     os.remove(combined_output)
    
#     return output_path    

# combined_denoiser(input_path)
# facebook_denoiser(input_path)
# deepfilternet(input_path)

