import os
import uuid
import shutil
import base64
from model_utils import predict_keywords

from runpod.serverless import start
from model_utils import convert_mp3_to_wav, predict_keywords

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def handler(event):
    try:
        # Get base64 encoded file and filename from the request
        encoded_data = event["input"].get("file_base64")
        original_filename = event["input"].get("filename", f"{uuid.uuid4()}.wav")

        if not encoded_data:
            return {"error": "Missing 'file_base64' input"}

        ext = original_filename.split(".")[-1]
        temp_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}.{ext}")

        # Decode and write the file
        with open(temp_path, "wb") as f:
            f.write(base64.b64decode(encoded_data))

        # Convert MP3 to WAV if needed
        if ext.lower() == "mp3":
            wav_path = temp_path.replace(".mp3", ".wav")
            convert_mp3_to_wav(temp_path, wav_path)
            os.remove(temp_path)
            temp_path = wav_path

        # Predict keywords
        keywords = predict_keywords(temp_path)

        return {"predicted_keywords": keywords}

    except Exception as e:
        return {"error": str(e)}


start({"handler": handler})
