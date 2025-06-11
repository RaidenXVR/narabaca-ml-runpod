import numpy as np
import tensorflow as tf
import torch
import torchaudio
from pydub import AudioSegment
from transformers import Wav2Vec2Model, Wav2Vec2Processor

SAMPLE_RATE = 16000  # sesuai model
with open("words.txt", "r") as r:
    words = r.readlines()
ALLOWED_WORDS = [x.split("\n") for x in words]

# Load processor dan model Wav2Vec2
MODEL_DIR = "./models/wav2vec2-indonesian"

# Load from local path
processor_wav2vec2 = Wav2Vec2Processor.from_pretrained(MODEL_DIR)
model_wav2vec2 = Wav2Vec2Model.from_pretrained(MODEL_DIR)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_wav2vec2 = model_wav2vec2.to(device)

# Load model klasifikasi
model_classifier = tf.keras.models.load_model("voice_classifier_finetuned_v1.keras")


def convert_mp3_to_wav(mp3_path: str, output_path: str) -> str:
    audio = AudioSegment.from_file(mp3_path, format="mp3")
    audio.export(output_path, format="wav")
    return output_path


def infer_single_file(file_path):
    waveform, sr = torchaudio.load(file_path)

    if waveform.shape[0] > 1:
        waveform = waveform.mean(dim=0, keepdim=True)

    if sr != SAMPLE_RATE:
        resampler = torchaudio.transforms.Resample(sr, SAMPLE_RATE)
        waveform = resampler(waveform)

    inputs = processor_wav2vec2(
        waveform.squeeze().numpy(), sampling_rate=SAMPLE_RATE, return_tensors="pt"
    )
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model_wav2vec2(**inputs).last_hidden_state
        mean = outputs.mean(dim=1)
        std = outputs.std(dim=1)
        pooled = torch.cat([mean, std], dim=1)

    return pooled.squeeze(0).cpu().numpy()


def predict_keywords(audio_path):
    try:
        feature_vector = infer_single_file(audio_path)
        feature_vector = feature_vector.reshape(1, -1)
        preds = model_classifier.predict(feature_vector)[0]

        predicted_indices = [i for i, p in enumerate(preds) if p >= 0.2]
        predicted_words = [ALLOWED_WORDS[i] for i in predicted_indices][0]
        return predicted_words
    except Exception as e:
        print(e)
        return []
