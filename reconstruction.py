import librosa
import numpy as np

def spectral_translation(audio_low, fs, cutoff):
    """Basic Spectral Translation Algorithm."""
    
    # Convert to frequency domain
    S_low = librosa.stft(audio_low)
    mag, phase = librosa.magphase(S_low)
    
    # Determine cutoff position on spectrum
    n_fft = 2048
    bin_cutoff = int(cutoff * n_fft / fs)
    
    # Perform translation
    mag_reconstructed = np.copy(mag)
    source_width = bin_cutoff // 2
    
    # Check boundaries to prevent IndexError
    max_bins = mag.shape[0]
    end_bin = min(bin_cutoff + source_width, max_bins)
    actual_width = end_bin - bin_cutoff
    
    # Take the segment from below cutoff and overlay it on top of cutoff
    if actual_width > 0:
        mag_reconstructed[bin_cutoff:end_bin, :] = mag[bin_cutoff - actual_width : bin_cutoff, :]
    
    # Return to audio domain
    S_recon = mag_reconstructed * phase
    audio_recon = librosa.istft(S_recon)
    
    return audio_recon