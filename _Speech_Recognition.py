import time
import numpy as np
import librosa
import tensorflow as tf

RATE = 44100
SAVED_MODEL_PATH = "model/gru.h5"
TEMPORARY_FILE_PATH = "temp.wav"

# Pemetaan
# Label
# MFCC


# for classification methods, there is 2 option for the best result: CNN or GRU

class _Speech_Recognition: #keyword spotting service
    def __init__(self):
        model = tf.keras.models.load_model(SAVED_MODEL_PATH)
        _mapping = [
            "Five",
            "Four",
            "No",
            "Off",
            "On",
            "One",
            "Six",
            "Three",
            "Two",
            "Yes"
        ]
        self.model = model
        self._mapping = _mapping
    

    def predict(self):
        MFCCs = self.preprocess(TEMPORARY_FILE_PATH)

        # Penamahan 1 layer di awal dan 1 layer di akhir yang membuat bantuk array menjadi [sample, timesample, banyaknya MFCC, channel]
        MFCCs = MFCCs[np.newaxis, ..., np.newaxis]

        # Prediksi menggunkan model
        predictions = self.model.predict(MFCCs)
        predicted_index = np.argmax(predictions)
        predicted_keyword = self._mapping[predicted_index]  

        return predicted_keyword

    def preprocess(self, file_path, num_mfcc=39, n_fft=2048, hop_length=256):
        # load file audio
        signal, sample_rate = librosa.load(file_path, sr=44100)

        # Melihat panjang sinyal, dan merubah panjangan sinyal menjadi 22050 (di potong atau di padding)
        signal = librosa.util.fix_length(data=signal, sr=44100)

        # extract MFCCs
        MFCCs = librosa.feature.mfcc(signal, sample_rate, n_mfcc=num_mfcc, n_fft=n_fft, hop_length=hop_length)

        return MFCCs.T
