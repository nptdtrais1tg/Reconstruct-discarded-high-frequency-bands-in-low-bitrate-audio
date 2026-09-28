# Reconstructing High Frequencies in Low-Bitrate Audio

## Overview
* Modern digital communication and multimedia streaming demand audio compression to facilitate smooth transmission over constrained bandwidths[cite: 3]. 
* Compression algorithms often utilize a low-pass filter to aggressively discard high-frequency components (typically above 8-10 kHz), which results in muffled and dull audio[cite: 3].
* This project provides a post-processing system at the receiver's end capable of artificially reconstructing the discarded high-frequency bands[cite: 3].
* By applying Spectral Translation, the system patches the lost frequency range to enhance perceptual quality without requiring additional transmission bandwidth[cite: 3].

## System Architecture & Methodology
### Degradation & Reconstruction
* **Degradation Model:** The system simulates a low-bandwidth environment using a 4th-order Butterworth Low-Pass Filter (LPF) with a cutoff frequency of 8 kHz[cite: 3].
* **Numerical Stability:** The filter is implemented using Second-Order Sections (SOS) to prevent numerical instability[cite: 3].
* **Reconstruction Algorithm:** The project uses Spectral Translation to copy magnitude data from the baseband (e.g., 4-8 kHz) and shift it to the target high-frequency region (e.g., 8-12 kHz)[cite: 3].
* **Normalization:** A Peak Normalization step is applied to scale the final waveform to a maximum peak of 0.8, preventing digital clipping and distortion[cite: 3].

### System Modules
* **Controller Layer:** Manages file paths and utilizes multi-threading (`ThreadPoolExecutor`) to process multiple audio files simultaneously[cite: 3].
* **DSP Core:** Contains the LPF Simulator, High-Frequency Reconstruction (HFR) module, and Metric Calculator (SNR and LSD)[cite: 3].
* **Web-based Interactive System:** Built with Streamlit, the interface includes an audio file uploader, a parameter tuning section (cutoff frequency slider), and a visualizer for side-by-side spectrogram comparisons[cite: 3].

## Setup Instructions
* **Clone the repository:** `git clone <your-repo-link>`[cite: 4].
* **Create a virtual environment:** `python3 -m venv venv`[cite: 3, 4].
* **Activate the environment (Windows):** `venv\Scripts\activate`[cite: 3, 4].
* **Activate the environment (Linux/macOS):** `source venv/bin/activate`[cite: 3, 4].
* **Install dependencies:** `pip install -r requirements.txt`[cite: 3, 4].

## How to Run
* Execute the main batch processing pipeline using: `python src/main.py --input data/raw/sample.wav`[cite: 3, 4].
* To run the Live Demo System with the web interface: `streamlit run ui/app.py`[cite: 3, 4].

## Credits
* **Institution:** School of Electrical and Electronic Engineering, Hanoi University of Science and Technology[cite: 3].
* **Course:** [ET4262E] Multimedia Data Compression and Coding[cite: 3].
* **Students:** Nguyen Phuong Trang (202414668) & Nguyen Phuong Anh (202414605)[cite: 3].
* **Instructor:** Pham Van Tien[cite: 3].
