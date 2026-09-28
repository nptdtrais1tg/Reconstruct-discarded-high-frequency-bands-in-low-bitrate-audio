import sys
import os
import streamlit as st

# Phân giải không gian tên để tích hợp module xử lý lõi
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

# Nhập thuật toán xử lý tín hiệu
from src.filters import low_pass_filter
from src.reconstruction import spectral_translation

# Nhập các thành phần giao diện độc lập
from components.uploader import render_uploader
from components.parameters import render_parameters
from components.visualizer import render_results

def main():
    # Cấu hình siêu dữ liệu trang
    st.set_page_config(page_title="HF Reconstruction Demo", layout="wide")
    st.title("Reconstructing High Frequencies in Low-Bitrate Audio")
    st.markdown("---")

    # Kích hoạt Component 1: Thu thập đầu vào
    audio_data, fs = render_uploader()

    if audio_data is not None:
        st.markdown("---")
        
        # Kích hoạt Component 2: Thu thập tham số
        cutoff_freq = render_parameters()

        # Nút kích hoạt tiến trình
        if st.button("Run Reconstruction Pipeline"):
            st.markdown("---")
            
            with st.spinner("Applying digital signal processing algorithms..."):
                # Thực thi thuật toán lõi
                audio_low = low_pass_filter(audio_data, cutoff=cutoff_freq, fs=fs, order=8)
                audio_recon = spectral_translation(audio_low, fs=fs, cutoff=cutoff_freq)
                
            # Kích hoạt Component 3: Xuất kết quả
            render_results(audio_data, audio_low, audio_recon, fs, cutoff_freq)

if __name__ == "__main__":
    main()