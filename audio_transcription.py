import streamlit as st
import tempfile
import torchaudio
import torch
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq  # ✅ Import added

@st.cache_resource
def load_whisper_model():
    model_name = "openai/whisper-small"  # Can be changed to another Whisper variant
    processor = AutoProcessor.from_pretrained(model_name)
    model = AutoModelForSpeechSeq2Seq.from_pretrained(model_name)
    return processor, model

processor, model = load_whisper_model()

def transcribe_audio(audio_file):
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
            temp_audio.write(audio_file.read())
            temp_audio.flush()
            temp_audio_path = temp_audio.name

        waveform, sample_rate = torchaudio.load(temp_audio_path)

        if sample_rate != 16000:
            resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
            waveform = resampler(waveform)
            sample_rate = 16000

        input_values = processor(waveform.squeeze().numpy(), sampling_rate=sample_rate, return_tensors="pt").input_features
        predicted_ids = model.generate(input_values)
        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
        return transcription

    except Exception as e:
        import traceback
        st.error(f"❌ Error during transcription: {e}")
        st.text(traceback.format_exc())
        return ""
