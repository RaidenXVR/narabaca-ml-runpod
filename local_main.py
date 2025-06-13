import base64
import json

AUDIO_PATH = "./test/kamu1.wav"
AUDIO_FILENAME = "kamu1.wav"

with open(AUDIO_PATH, "rb") as f:
    byte_data = f.read()

base64_str = base64.b64encode(byte_data).decode("utf-8")

payload = {"input": {"file_base64": base64_str, "filename": AUDIO_FILENAME}}

with open("test_input.json", "w") as f:
    json.dump(payload, f, indent=4)

print("Test input JSON created: test_input.json")


