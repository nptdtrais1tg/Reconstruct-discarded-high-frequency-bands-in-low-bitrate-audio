import streamlit as st
import librosa

def render_uploader():
    """Hiển thị giao diện tải tệp và tiền xử lý âm thanh."""
    st.header("1. Upload Audio File")
    uploaded_file = st.file_uploader("Select a .wav file to process", type=["wav"])
    
    if uploaded_file is not None:
        audio_data, fs = librosa.load(uploaded_file, sr=48000)
        st.audio(uploaded_file, format='audio/wav')
        st.write(f"**Sample Rate:** {fs} Hz | **Duration:** {len(audio_data)/fs:.2f} seconds")
        return audio_data, fs
    
    return None, None