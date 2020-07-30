import os, sys
import re
from pydub import AudioSegment
from scipy.fftpack import fft
from pydub.utils import make_chunks
import numpy as np

def audSegFouTrDF(path):
    croak = AudioSegment.from_file(path, format='mp3')
    croak = croak.set_fram_rate(16000)
    output_path = "output/"
    file_name = "recording.mp3"
    complete_path = output_path+file_name
    croak.export(complete_path, format='mp3')
    
    audioarray = []
    for outputs in os.listdir(output_path):
        aud = AudioSegment.from_file(complete_path, format="mp3")
        arr = aud.get_array_of_samples()[:5120]
        abs_four = np.abs(fft(arr))
        audioarray.append(abs_four)

    df_clean = pd.DataFrame({'F.Transform':audioarray})
    return df_clean

def neuralNetworkPred(transDf):
    trained_model = ("0.9034-accuracy-20batch_size-50epochs-loss1.0390")
    print("Loading neural network")
    with open(f'output/{trained_model}.json','r') as f:
        model_json = json.load(f)
        model = model_from_json(model_json)
        model.load(f"output/{trained_model}.h5")
    
    print("Predicting your cute lil frog's familia")
    X_test=np.vstack(transDf['F.Transform'])
    X_test.shape
    pred = model.predict(X_test)
    frog = pred[0].tolist()
    
    print("Evaluating the results")
    frogs = frog.index(max(frog))
    if frogs == 0:
        return("Bufonidae Familia with a likelihood of {}%".format((round(frog[0]*100, 1))))
    elif frogs == 1:
        return("Dendrobatidae Familia with a likelihood of {}%".format((round(frog[1]*100, 1))))
    elif frogs == 2:
        return("Hyperollidae Familia with a likelihood of {}%".format((round(frog[1]*100, 1))))
    elif frogs == 3:
        return("Leptodactylidae Familia with a likelihood of {}%".format((round(frog[1]*100, 1))))
