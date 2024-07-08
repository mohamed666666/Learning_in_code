import json
from channels.generic.websocket import AsyncWebsocketConsumer
from vosk import Model, KaldiRecognizer
import base64
from pydub import AudioSegment
from io import BytesIO
import whisper
import os

class TranscriptionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("WebSocket Connected!")
        self.recognizer = None
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')

        model = whisper.load_model("tiny")
        #self.recognizer = KaldiRecognizer(model, 16000)
        print("ali")
        if message_type == 'start':
            print("Ahmed")
            #model = Model(model_name="vosk-model-small-en-us-0.15")
            #self.recognizer = KaldiRecognizer(model, 16000)
        elif message_type == 'audio':
            print("mohamed")
            audio_base64_str = data.get('audio').split(",")[1]  # Get only the base64 content, removing the MIME type prefix.
            audio_bytes = base64.b64decode(audio_base64_str)  # Decode the base64 string to bytes

            # Save the audio bytes as a .wav file
            audio_file_path = 'aod.wav'
            with open(audio_file_path, 'wb') as f:
                f.write(audio_bytes)

            result = model.transcribe(audio_file_path)
            print("Transcription:", result["text"])

            os.remove(audio_file_path)

            await self.send(text_data=json.dumps({
                        'transcription': result.get('text')
                    }))

            # Convert the audio bytes to the desired format using pydub
            # audio_file = BytesIO(audio_bytes)
            # audio = AudioSegment.from_file(audio_file).set_channels(1).set_frame_rate(16000)
            # converted_audio_bytes = audio.export(format="wav").read()[44:]
            # print("converted_audio_bytes", converted_audio_bytes)

            # if self.recognizer:
            #     print('hassan')
            #     if self.recognizer.AcceptWaveform(converted_audio_bytes):
            #         result = json.loads(self.recognizer.Result())
            #         print("Ali Ahmed")
            #         print(result.get('text'))
            #         print("Emam Ismail")
                    
