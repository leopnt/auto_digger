import os
import random
from track_feature_extraction import build_feature_vector
import pandas as pd


def build_class_vector(file_name: str) -> dict[str, bool]:
    """
    Builds a dictionary representing the presence of each class in the given file name.

    Args:
        file_name (str): The name of the file to build the class vector for.

    Returns:
        dict[str, bool]: A dictionary where the keys are the class names and the values are True if the class is present in the file name, False otherwise.
    """
    classes = ["h", "o", "d", "a", "t", "g", "e", "b", "f", "i", "r"]

    out_vector: dict[str, bool] = dict()

    file_classes = [char for char in file_name.split(" ")[0][1:]]

    for c in classes:
        out_vector[c] = c in file_classes

    return out_vector


def build_dataset(tracks: list[str], verbose=False) -> pd.DataFrame:
    """
    Builds a dataset from a list of audio tracks.

    Args:
        tracks (list[str]): A list of file paths to audio tracks.
        verbose (bool, optional): Whether to print progress messages. Defaults to False.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the features vectors of the audio tracks.

    Example:
        >>> tracks = ['/path/to/track1.wav', '/path/to/track2.wav']
        >>> dataset = build_dataset(tracks, verbose=True)
        Building features vector of '/path/to/track1.wav'...
        Building features vector of '/path/to/track2.wav'...
        >>> print(dataset)
                                        audio  class  feature1  feature2  ...
        0                        /path/to/track1.wav      1      0.23      0.45  ...
        1                        /path/to/track2.wav      2      0.12      0.67  ...
        ...
    """
    dataset = []

    for file_path in tracks:
        if verbose:
            print(f"Building features vector of '{file_path}'...")

        out_vector = {"audio": file_path}
        out_vector |= build_class_vector(file_path)
        out_vector |= build_feature_vector(os.path.join(directory_path, file_path))

        dataset.append(out_vector)

    return pd.DataFrame(dataset)


if __name__ == "__main__":
    directory_path = "/Users/leopnt/Downloads/music_lib/h"

    tracks = os.listdir(directory_path)

    random.seed(42)
    tracks = random.sample(tracks, 200)

    df = build_dataset(tracks, verbose=True)
    df.to_csv("track_features.csv", index=False)
