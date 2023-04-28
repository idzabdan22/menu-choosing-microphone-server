import asyncio
import websockets
import Audio as audio

PORT=3000
ADDRESS="127.0.0.1"

async def sendSpeech(websocket):
    try:
        myAudio = audio.Audio()
        await myAudio.process_audio(websocket)
    except Exception as e:
        print(e)
    
async def main():
    async with websockets.serve(sendSpeech, ADDRESS, PORT):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
