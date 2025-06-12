import streamlit as st
import tempfile
import torchaudio
import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration

@st.cache_resource
def load_whisper_model():
    model_name = "openai/whisper-large-v3-turbo"
    processor = WhisperProcessor.from_pretrained(model_name)
    model = WhisperForConditionalGeneration.from_pretrained(model_name)
    return processor, model

processor, model = load_whisper_model()

def transcribe_audio(audio_file):
    try:
        # Save audio file temporarily
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
            temp_audio.write(audio_file.read())
            temp_audio.flush()
            temp_audio_path = temp_audio.name

        # Load with torchaudio (no ffmpeg dependency)
        waveform, sample_rate = torchaudio.load(temp_audio_path)

        # Resample if needed
        if sample_rate != 16000:
            resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
            waveform = resampler(waveform)
            sample_rate = 16000

        # Whisper expects a 1D float32 tensor
        input_values = processor(waveform.squeeze().numpy(), sampling_rate=sample_rate, return_tensors="pt").input_features

        predicted_ids = model.generate(input_values)
        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
        return transcription

    except Exception as e:
        import traceback
        st.error(f"❌ Error during transcription: {e}")
        st.text(traceback.format_exc())
        return ""
