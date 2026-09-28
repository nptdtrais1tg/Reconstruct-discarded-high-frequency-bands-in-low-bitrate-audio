import concurrent.futures
import os
import soundfile as sf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import librosa.display
import numpy as np
from processor import apply_lpf, spectral_translation, compute_metrics


def save_comparison_plot(y_orig, y_low, y_recon, sr, file_name, output_path):
    fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
    
    signals = [y_orig, y_low, y_recon]
    titles = [f"Original: {file_name}", "Low-Pass Filtered (8000Hz)", "Reconstructed (Spectral Translation)"]
    
    for i, (y, title) in enumerate(zip(signals, titles)):
        D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
        img = librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='hz', ax=axes[i])
        axes[i].set_title(title, fontsize=12, fontweight='bold')
        axes[i].set_ylabel('Hz', fontsize=10)
        if i < 2:
            axes[i].set_xlabel('')

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def load_audio(input_path):
    """Load a WAV file using soundfile and convert stereo to mono."""
    audio, sr = sf.read(input_path, dtype='float32')
    if audio.ndim > 1:
        audio = np.mean(audio, axis=1)
    return audio, sr


def run_pipeline(input_path, output_base_dir, cutoff=8000):
    """
    Core pipeline to process a single audio file.
    Outputs are saved in a sub-folder named after the input file.
    """
    file_name = os.path.splitext(os.path.basename(input_path))[0]
    file_output_dir = os.path.join(output_base_dir, file_name)
    
    if not os.path.exists(file_output_dir):
        os.makedirs(file_output_dir)
        
    # STEP 1: LOAD AUDIO
    y, fs = load_audio(input_path)
    print(f"\n>>> Processing: {file_name}.wav")
    print(f"DEBUG: Max amplitude of {file_name} is {np.max(np.abs(y))}")
    
    # STEP 2: LPF SIMULATION
    y_low = apply_lpf(y, cutoff, fs)
    
    # STEP 3: RECONSTRUCTION 
    y_recon = spectral_translation(y_low, fs, cutoff)

    # STEP 3.1: ADJUST RECONSTRUCTION LEVEL 
    peak_orig = np.max(np.abs(y))
    peak_recon = np.max(np.abs(y_recon))
    target_peak = min(peak_orig, 0.8)
    if target_peak > 0 and peak_recon > 0:
        y_recon = y_recon * (target_peak / peak_recon)
    
    # STEP 4: EVALUATION 
    snr_low, lsd_low = compute_metrics(y, y_low)
    snr_recon, lsd_recon = compute_metrics(y, y_recon)
    
    print(f"  [LPF]   SNR: {snr_low:.2f}dB | LSD: {lsd_low:.2f}")
    print(f"  [Recon] SNR: {snr_recon:.2f}dB | LSD: {lsd_recon:.2f}")
    
    # STEP 5: EXPORT 
    sf.write(os.path.join(file_output_dir, "original.wav"), y, fs, subtype='PCM_16')
    sf.write(os.path.join(file_output_dir, "lpf_version.wav"), y_low, fs, subtype='PCM_16')
    sf.write(os.path.join(file_output_dir, "reconstructed.wav"), y_recon, fs, subtype='PCM_16')
    save_comparison_plot(y, y_low, y_recon, fs, file_name, 
                          os.path.join(file_output_dir, "comparison_spectrogram.png"))
    
    print(f"  Saved outputs and comparison plot to: {file_output_dir}")

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(base_dir, "data", "raw")
    output_dir = os.path.join(base_dir, "data", "processed")
    os.makedirs(output_dir, exist_ok=True)
    
    files_to_process = [
        "sample_talking.wav",
        "sample_fullsong.wav",
        "sample_piano.wav"
    ]

    print("Starting Batch Audio Processing...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = {}
        for file_name in files_to_process:
            input_path = os.path.join(raw_dir, file_name)
            if os.path.exists(input_path):
                futures[executor.submit(run_pipeline, input_path, output_dir)] = file_name
            else:
                print(f"Warning: File not found -> {input_path}")

        for future in concurrent.futures.as_completed(futures):
            file_name = futures[future]
            try:
                future.result()
            except Exception as exc:
                print(f"Error processing {file_name}: {exc}")

    print("\nAll tasks completed successfully!")

if __name__ == "__main__":
    main()