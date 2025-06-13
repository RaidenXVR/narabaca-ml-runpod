## Overview
Repositori ini berisi backend model Audio Classification Machine Learning untuk NaraBaca menggunakan teknologi Runpod Serverless.

## Instalasi
- Pastikan anda sudah punya python dengan versi diantara 3.8 sampai 3.12.
- Buat virtual environment dengan perintah:
```bash
python -m venv .venv
```
- Aktifkan virtual environment dengan perintah:
```bash
./.venv/scripts/activate
```
- install dependecies dengan perintah:
```bash
pip install -r requirements.txt
```

## Menjalankan secara lokal
- Pastikan anda sudah melakukan proses instalasi.
- Copy audio untuk test ke dalam working directory.
- Buka file `local_main.py` dan ubah variabel `AUDIO_PATH` dan `AUDIO_FILENAME` sesuai dengan path dan nama file audio.
- Jalankan file local_main.py
- Pastikan file `test_input.json` telah berubah.
- Jalankan file `rp_handler.py` dan tunggu sampai selesai.
- Hasil inferensi ada pada terminal dengan format pada `Job result`:
```python
{'output':{'predicted_keywords': [KATA_KATA_PREDIKSI, '']}}
```