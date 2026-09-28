import streamlit as st

def render_parameters():
    """Hiển thị và thu thập giá trị cấu hình từ người dùng."""
    st.header("2. Process Parameters")
    cutoff_freq = st.slider(
        "Low-pass Filter Cutoff Frequency (Hz)", 
        min_value=2000.0, 
        max_value=16000.0, 
        value=8000.0, 
        step=500.0,
        help="Xác định ngưỡng tần số giới hạn để mô phỏng sự suy hao dữ liệu."
    )
    return cutoff_freq