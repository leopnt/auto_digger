import os
import random
from track_feature_extraction import build_feature_vector
import pandas as pd

def build_class_vector(file_name: str) -> dict[str, bool]:
    classes = ['h', 'o', 'd', 'a', 't', 'g', 'e', 'b', 'f', 'i', 'r']

    out_vector: dict[str, bool] = dict()

    file_classes = [char for char in file_name.split(' ')[0][1:]]

    for c in classes:
        out_vector[c] = c in file_classes
    
    return out_vector

def build_dataset(tracks: list[str], verbose=False) -> pd.DataFrame:
    dataset = []

    for file_path in tracks:
        if verbose:
            print(f"Building features vector of '{file_path}'...")

        out_vector = {'audio': file_path}
        out_vector |= build_class_vector(file_path)
        out_vector |= build_feature_vector(os.path.join(directory_path, file_path))

        dataset.append(out_vector)

    return pd.DataFrame(dataset)

if __name__ == "__main__":
    directory_path = '/Users/leopnt/Downloads/music_lib/h'

    tracks = os.listdir(directory_path)

    random.seed(42)
    tracks = random.sample(tracks, 200)

    df = build_dataset(tracks, verbose=True)
    df.to_csv("track_features.csv", index=False)