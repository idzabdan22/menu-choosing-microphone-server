import time
import numpy as np
import librosa
import tensorflow as tf


RATE = 44100
MODEL_PATH = "model/mfcc_13_with_oke_cnn_200.h5"
# TEMPORARY_FILE_PATH = "/home/abdan2345/Dataset_Skripsi/clean_dataset/with_oke/Tidak/KHOIR_Tidak_2.wav"
TEMPORARY_FILE_PATH = "audio/temp.wav"

# Mapping
# Label
# MFCC

# for classification methods, there is 2 option for the best result: CNN or GRU

class _Speech_Recognition: 
    def __init__(self):
        model = tf.keras.models.load_model(MODEL_PATH)
        _mapping = [
            "Info",
            "Tiga",
            "Mati",
            "Enam",
            "Satu",
            "Empat",
            "Next",
            "Keluar",
            "Nyala",
            "Dua",
            "Oke",
            "Tidak",
            "Back",
            "Lima"
        ]
        self.model = model
        self._mapping = _mapping
        self.RATE = RATE
    
    def predict(self):
        MFCCs = self.preprocess(TEMPORARY_FILE_PATH, num_mfcc=13)
        ct = time.time()
        predicted_index = np.argmax(self.model.predict(MFCCs[np.newaxis, ..., np.newaxis]))
        # predicted_index_class = self.model.predict(MFCCs[np.newaxis, ..., np.newaxis])
        # print(predicted_index_class)
        execution_time = time.time() - ct
        print(f"done in {round(execution_time, 2)} seconds")
        print(f"predicted: {self._mapping[predicted_index]}")
        return predicted_index

    def preprocess(self, file_path, num_mfcc=13, n_fft=2048, hop_length=512):
        signal, sample_rate = librosa.load(file_path)
        resample = librosa.resample(signal, orig_sr=sample_rate, target_sr=self.RATE)
        if len(resample) >= self.RATE:
            resample = resample[:self.RATE]
            MFCCs = librosa.feature.mfcc(y=resample, sr=self.RATE, n_mfcc=num_mfcc, n_fft=n_fft, hop_length=hop_length)
        return MFCCs.T
