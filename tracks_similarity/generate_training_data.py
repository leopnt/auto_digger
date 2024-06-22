"""
Script to generate a training data.

Usefull to import filtered training data to Google Collab or whatever instead of copying Gigabytes of raw audio tracks
"""

import numpy as np
import pandas as pd
import librosa
import joblib
from tqdm import tqdm

from triplet_dataset import TripletDataset

class Track:
    def __init__(self, filepath: str, sr: int = 22050) -> None:
        self.filepath = filepath
        self.sr = sr
    
    def _normalize_mel_spectrogram(mel_spec: np.ndarray) -> np.ndarray:
        max_val = np.max(mel_spec)
        min_val = np.min(mel_spec)
        normalized_spectrogram = (mel_spec - min_val) / (max_val - min_val)

        return normalized_spectrogram
    
    def audio_extract(self, from_sec: int, to_sec: int) -> np.ndarray:
        audio, _ = librosa.load(
            self.filepath,
            mono=True,
            sr=self.sr,
            offset=from_sec,
            duration=to_sec - from_sec
        )

        if audio is None:
            raise Exception("Something went wrong went reading extract")

        return audio
    
    def spectrogram(self, from_sec: int = 40, to_sec: int = 43) -> np.ndarray:
        extract = self.audio_extract(from_sec, to_sec)

        spec = librosa.feature.melspectrogram(y=extract, sr=self.sr, n_fft=512, hop_length=128)
        spec_db = librosa.power_to_db(S=spec, ref=np.max)
        spec_db_norm = Track._normalize_mel_spectrogram(spec_db)

        return spec_db_norm

class TrackPair:
    def __init__(self, filepath_left: str, filepath_right: str, similar: bool) -> None:
        self.left = Track(filepath_left)
        self.right = Track(filepath_right)
        self.similar = similar

class Dataset:
    def __init__(self, triplets: TripletDataset) -> None:
        self.trackpairs: list[TrackPair] = []

        for _, row in triplets.df.iterrows():
            file_pair = (row["anchor"], row["positive"])
            track_pair = TrackPair(file_pair[0], file_pair[1], 1)
            self.trackpairs.append(track_pair)

            file_pair = (row["anchor"], row["negative"])
            track_pair = TrackPair(file_pair[0], file_pair[1], 0)
            self.trackpairs.append(track_pair)
    
    def as_dataframe(self) -> pd.DataFrame:
        data = {"left": [], "right": [], "similar": []}

        for track_pair in self.trackpairs:
            data["left"].append(track_pair.left.filepath)
            data["right"].append(track_pair.right.filepath)
            data["similar"].append(int(track_pair.similar))
        
        return pd.DataFrame(data)
    
    def as_training_data(self) -> tuple[np.ndarray, np.ndarray]:
        pairs = []
        labels = []

        for track_pair in tqdm(self.trackpairs):
            pairs.append([track_pair.left.spectrogram(), track_pair.right.spectrogram()])
            labels.append(track_pair.similar)
        
        return np.array(pairs).astype(float), np.float32(np.array(labels))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "tracks_folder",
        help="path to folder of tracks with comment ID3 tags like '2;e;d'"
    )
    parser.add_argument(
        "output",
        help="output file"
    )
    parser.add_argument(
        "num_triplets",
        help="number of similar anchor per triplets"
    )
    args = parser.parse_args()

    triplets = TripletDataset(args.tracks_folder, n=int(args.num_triplets))
    dataset = Dataset(triplets)

    X, y = dataset.as_training_data()

    print(f"X.shape: {X.shape}")
    print(f"y.shape: {y.shape}")
    compression = 3
    print(f"Exporting (X, y) to joblib with compression: {compression}...")
    joblib.dump((X, y), args.output, compress=compression)
