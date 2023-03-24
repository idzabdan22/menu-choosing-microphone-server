import math
import struct
import wave
import pyaudio
import warnings
import websockets

warnings.filterwarnings("ignore")

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
SHORT_NORMALIZE = (1.0/32768.0)
TIMEOUTSIGNAL = ((RATE / CHUNK * 1)+2)
TEMPORARY_WAVE_FILENAME = "audio/temp.wav"
SWIDTH = 2
Threshold = 100

class Audio:
    def __init__(self,):
        try:
            audio = pyaudio.PyAudio()
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
            self.var = False
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
            # return recognize()

        except Exception as ex:
            print(ex)

    async def process_audio(self, websocket):
        try:
            while True:
                while self.silence:
                        input = self.stream.read(CHUNK)
                        rms_val = self.rms(input)
                        if rms_val > Threshold:
                            self.var = not self.var
                            self.silence = False
                            LastBlock = input
                            self.recording(LastBlock, self.stream)
                            if self.var:
                                await websocket.send("Next")
                            else:
                                await websocket.send("Info")
        except websockets.exceptions.ConnectionClosedError:
            self.onClose()

    def onClose(self,):
        try:
            print("Closing Stream and release port Audio")
            self.stream.close()
            self.audio.terminate()
        except Exception as ex:
            print(ex)


