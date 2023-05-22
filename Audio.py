import math
import struct
import wave
import pyaudio
import warnings
import websockets
# import threading
import _Speech_Recognition as SR

warnings.filterwarnings("ignore")

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
SHORT_NORMALIZE = (1.0/32768.0)
TIMEOUTSIGNAL = ((RATE / CHUNK * 1)+2)
TEMPORARY_WAVE_FILENAME = "audio/temp.wav"
SWIDTH = 2
Threshold = 120

class Audio:
    def __init__(self,):
        try:
            audio = pyaudio.PyAudio()
            speechRecognition = SR._Speech_Recognition()
            self.audio = audio
            stream = audio.open(
                format=FORMAT, 
                channels=CHANNELS,
                rate=RATE, 
                input=True,
                frames_per_buffer=CHUNK,
            )
            self.stream = stream
            self.silence = True
            self.speech_recognition = speechRecognition
            self.output = {
                0 : "info",
                1 : "3",
                2 : "mati",
                3 : "6",
                4 : "1",
                5 : "4",
                6 : "next",
                7 : "keluar",
                8 : "nyala",
                9 : "2",
                10 : "oke",
                11 : "tidak",
                12 : "back",
                13 : "5"
            }
        except Exception as ex:
            self.audio.terminate()

    def rms(self, frame):
        count = len(frame)/SWIDTH
        format = "%dh"%(count)
        # short is 16 bit int
        shorts = struct.unpack(format, frame)
        sum_squares = 0.0
        for sample in shorts:
            n = sample * SHORT_NORMALIZE
            sum_squares += n*n
        # compute the rms
        rms = math.pow(sum_squares/count,0.5)
        return rms * 1000

    def recording(self, lastblock, stream):
        try:
            arr = []
            arr.append(lastblock)
            
            print ("recording...")

            for i in range(0, int(TIMEOUTSIGNAL)):
                data = stream.read(CHUNK)
                arr.append(data)

            print ("Finish recording...")

            waveFile = wave.open(TEMPORARY_WAVE_FILENAME, 'wb')
            waveFile.setnchannels(CHANNELS)
            waveFile.setsampwidth(self.audio.get_sample_size(FORMAT))
            waveFile.setframerate(RATE)
            waveFile.writeframes(b''.join(arr))
            waveFile.close()
            del stream
            self.silence = True
            return self.output[self.speech_recognition.predict()]
        except Exception as ex:
            print(ex)

    async def process_audio(self, websocket):
        try:
            while True:
                while self.silence:
                        input = self.stream.read(CHUNK)
                        rms_val = self.rms(input)
                        print("RMS:", rms_val)
                        if rms_val > Threshold:
                            self.silence = False
                            LastBlock = input
                            output = self.recording(LastBlock, self.stream)
                            await websocket.send(output)
                            
        except websockets.exceptions.ConnectionClosedError:
            self.onClose()
        # except Exception as ex:
        #     print(ex)

    def onClose(self,):
        try:
            print("Closing Stream and release port Audio")
            self.stream.close()
            self.audio.terminate()
        except Exception as ex:
            print(ex)

# if __name__ == "__main__":
#     audio = Audio()
#     x = threading.Thread(target=audio.process_audio, args=("none",))
#     x.start()
#     # audio.process_audio("none")


