import streamlit as st
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

def plot_spectrogram(y, sr, title):
    """Hàm phụ trợ xuất phổ đồ."""
    fig, ax = plt.subplots(figsize=(10, 1.5)) 
    
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    img = librosa.display.specshow(D, y_axis='linear', x_axis='time', sr=sr, ax=ax)

    ax.set_title(title, fontsize=10, pad=5)
    ax.tick_params(axis='both', which='major', labelsize=8)
    ax.set_xlabel("Time", fontsize=8)
    ax.set_ylabel("Hz", fontsize=8)
    
    cbar = fig.colorbar(img, ax=ax, format="%+2.0f dB")
    cbar.ax.tick_params(labelsize=8)
    
    plt.tight_layout()
    return fig

def render_results(audio_raw, audio_low, audio_recon, fs, cutoff_freq):
    """Hiển thị trình phát âm thanh và biểu đồ đối chiếu theo 3 hàng dọc."""
    st.header("3. Results & Evaluation")
    st.write("So sánh phổ âm từ trên xuống dưới giúp bạn dóng hàng và nhận diện dải tần bị mất/được khôi phục dễ dàng hơn.")
    
    # Hàng 1: Original Audio (Raw)
    st.subheader("1. Original (Raw) Audio")
    st.audio(audio_raw, sample_rate=fs)
    fig_raw = plot_spectrogram(audio_raw, fs, "Original Audio")
    st.pyplot(fig_raw)
    
    st.markdown("---")
    
    # Hàng 2: Filtered Audio (Low)
    st.subheader("2. Low-Bitrate (Filtered) Audio")
    st.audio(audio_low, sample_rate=fs)
    fig_low = plot_spectrogram(audio_low, fs, f"Low-pass Filtered (Cutoff: {cutoff_freq}Hz)")
    st.pyplot(fig_low)
    
    st.markdown("---")
    
    # Hàng 3: Reconstructed Audio
    st.subheader("3. Reconstructed Audio")
    st.audio(audio_recon, sample_rate=fs)
    fig_recon = plot_spectrogram(audio_recon, fs, "High-Frequency Reconstructed")
    st.pyplot(fig_recon)