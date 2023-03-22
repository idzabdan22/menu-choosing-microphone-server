#!/usr/bin/env python

import asyncio
import websockets
import audio as audio

async def sendSpeech(websocket):
    print("Client Connected!")
    myAudio = audio.Audio()
    await myAudio.process_audio(websocket)
    
async def main():
    async with websockets.serve(sendSpeech, "127.0.0.1", 3000):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
