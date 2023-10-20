import numpy as np
import librosa

def describe(freqs, key_prefix=None) -> dict[str, float]:
    mean = np.mean(freqs)
    std = np.std(freqs) 
    maxv = np.amax(freqs) 
    minv = np.amin(freqs) 
    median = np.median(freqs)
    q1 = np.quantile(freqs, 0.25)
    q3 = np.quantile(freqs, 0.75)
    
    return {
        key_prefix + 'mean': mean,
        key_prefix + 'std': std,
        key_prefix + 'maxv': maxv,
        key_prefix + 'minv': minv,
        key_prefix + 'median': median,
        key_prefix + 'q1': q1,
        key_prefix + 'q3': q3}

def build_feature_vector(audio_path: str) -> dict:
    x , sr = librosa.load(audio_path, sr=44100)

    out_vector: dict[str, float] = dict()

    tempo = librosa.feature.tempo(y=x, sr=sr)[0]
    out_vector["tempo"] = tempo

    rmse = np.sqrt(np.mean(x**2))
    out_vector["rmse"] = rmse

    freqs = describe(np.fft.fftfreq(x.size), key_prefix="freqs_")
    for key, stat in freqs.items():
        out_vector[key] = stat

    zero_crossing_rate = describe(librosa.feature.zero_crossing_rate(x)[0], key_prefix="zero_crossing_rate_")
    for key, stat in zero_crossing_rate.items():
        out_vector[key] = stat

    spectral_centroids = describe(librosa.feature.spectral_centroid(y=x, sr=sr)[0], key_prefix="spectral_centroids_")
    for key, stat in spectral_centroids.items():
        out_vector[key] = stat

    spectral_bandwidth = describe(librosa.feature.spectral_bandwidth(y=x, sr=sr)[0], key_prefix="spectral_bandwidth_")
    for key, stat in spectral_bandwidth.items():
        out_vector[key] = stat

    spectral_contrast = describe(librosa.feature.spectral_contrast(y=x, sr=sr)[0], key_prefix="spectral_contrast_")
    for key, stat in spectral_contrast.items():
        out_vector[key] = stat

    spectral_rolloff = describe(librosa.feature.spectral_rolloff(y=x, sr=sr)[0], key_prefix="spectral_rolloff_")
    for key, stat in spectral_rolloff.items():
        out_vector[key] = stat

    spectral_flatness = describe(librosa.feature.spectral_flatness(y=x)[0], key_prefix="spectral_flatness_")
    for key, stat in spectral_flatness.items():
        out_vector[key] = stat

    mfcc = describe(librosa.feature.mfcc(y=x, sr=sr), key_prefix="mfcc_")
    for key, stat in mfcc.items():
        out_vector[key] = stat

    return out_vector

if __name__ == "__main__":
    import argparse
    import pprint

    parser = argparse.ArgumentParser(description='Extract features of a raw audio file.')
    parser.add_argument('audio_file', help='Path to the audio file')
    args = parser.parse_args()

    print(f"Calculating features of '{args.audio_file}'...")
    pprint.pprint(build_feature_vector(args.audio_file))
