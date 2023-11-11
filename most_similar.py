import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

from track_feature_extraction import build_feature_vector


def most_similar(df, df_index=0, audio_path: str = "", verbose=False) -> list[str]:
    """
    Calculates the most similar individuals to the given individual using the Euclidean distance between their feature vectors.

    Parameters:
    df (pandas.DataFrame): The dataframe containing the individuals.
    df_index (int): The index of the individual to compare to. Default is 0.
    audio_path (str): The path to an audio file to compare to. Default is an empty string.
    verbose (bool): Whether to print the closest candidates. Default is False.

    Returns:
    list[str]: A list of the names of the most similar individuals.
    """
    X = df.iloc[:, 12:].values

    if audio_path:
        name = audio_path
        given_individual = np.fromiter(
            build_feature_vector(audio_path, verbose=verbose).values(), dtype=float
        )

    else:
        name = df.iloc[df_index, 0]
        given_individual = np.array(df.iloc[df_index, 12:], dtype=float)

    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(X)

    scaled_given_individual = scaler.transform(given_individual.reshape(1, -1))

    distances = np.linalg.norm(scaled_data - scaled_given_individual, axis=1)

    top_n = 5  # Number of most similar individuals to select
    most_similar_indices = np.argsort(distances)[: (top_n + 1)][1:]

    most_similar_individuals = df.iloc[most_similar_indices, 0]

    if verbose:
        print("Closest candidates:")
        for individual in most_similar_individuals:
            print(individual)

    return most_similar_individuals


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Features exploration.")
    parser.add_argument("audio_file", help="Path to the audio file")
    args = parser.parse_args()

    # csv built with build_dataset.py
    df = pd.read_csv("track_features.csv")

    most_similar(df, audio_path=args.audio_file, verbose=True)
