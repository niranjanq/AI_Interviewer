import os
import urllib.request
import tarfile
from pydub import AudioSegment
from pydub.utils import which
import tempfile
import librosa
import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import streamlit as st

# Ensure ffmpeg is available (works on Streamlit Cloud & Render)
ffmpeg_path = "/tmp/ffmpeg"
if not os.path.exists(ffmpeg_path):
    # Download static build of ffmpeg (safe public link)
    ffmpeg_url = "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-i686-static.tar.xz"
    ffmpeg_archive = "/tmp/ffmpeg.tar.xz"
    urllib.request.urlretrieve(ffmpeg_url, ffmpeg_archive)

    with tarfile.open(ffmpeg_archive) as tar:
        for member in tar.getmembers():
            if "ffmpeg" in member.name and member.isfile():
                tar.extract(member, path="/tmp/")
                os.rename(f"/tmp/{member.name}", ffmpeg_path)
                break

os.environ["PATH"] = f"/tmp:{os.environ['PATH']}"
AudioSegment.converter = which("ffmpeg")  # Set ffmpeg for pydub

# Load Whisper model
@st.cache_resource
def load_whisper_model():
    model_name = "openai/whisper-large-v3-turbo"
    processor = WhisperProcessor.from_pretrained(model_name)
    model = WhisperForConditionalGeneration.from_pretrained(model_name)
    return processor, model

processor, model = load_whisper_model()

def transcribe_audio(audio_file):
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
            temp_audio.write(audio_file.read())  # Convert UploadedFile to bytes
            temp_audio.flush()
            temp_audio_path = temp_audio.name

        input_audio, _ = librosa.load(temp_audio_path, sr=16000)
        input_features = processor(input_audio, sampling_rate=16000, return_tensors="pt").input_features
        predicted_ids = model.generate(input_features)
        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
        return transcription

    except Exception as e:
        import traceback
        st.error(f"❌ Error during transcription: {e}")
        st.text(traceback.format_exc())
        return ""
