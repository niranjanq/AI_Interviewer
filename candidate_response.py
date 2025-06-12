import streamlit as st

def record_response(key="default"):
    audio_value = st.audio_input("🎙️ Record your answer", key=f"audio_input_{key}")
    if audio_value is not None:
        st.session_state["audio_response"] = audio_value
        st.success("🎧 Audio recorded successfully!")

    if "audio_response" in st.session_state:
        st.markdown("### ▶️ Your Recorded Response:")
        st.audio(st.session_state["audio_response"])
        
    return st.session_state.get("audio_response", None)
