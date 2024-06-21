"""
Script to generate a dataset of triplet for tracks from personal tags

Each track has a comment ID3 tag like 2,e;d for energy 2, electro; disco
Tracks with similar tags have more chance to be similar than tracks with different tags.

We can use this to compute a distance metrics based on the tags similarity.
Using this distance, we can generate triplets to train a siamese NN:

- Anchor: base track
- Positive: different track with same tags
- Negative: different track with totally different tags
"""

from typing import Optional
from glob import glob
import re

from mutagen.id3 import ID3, COMM
from mutagen.mp3 import MP3
from mutagen.aiff import AIFF

import pandas as pd

class TripletDataset:
    def __init__(self, tracks_folder: str, allow_same: bool = False, n: int = 3) -> None:
        """
        Params
        ======
        `tracks_folder`: folder to track with ID3 comment tagged music
        `allow_same`: allow pairs with the same track
        `n`: number of triplet per anchor
        """

        data = {'track_path': [], 'comment': []}

        for track_path in sorted(glob(f"{tracks_folder}/*")):
            data['track_path'].append(track_path)
            data['comment'].append(TripletDataset._find_id3_comment(track_path))
        
        initial_df = pd.DataFrame(data).dropna(subset='comment')
        
        pairs_df = pd.merge(initial_df, initial_df, how='cross', suffixes=('_left', '_right'))

        if not allow_same:
            pairs_df = pairs_df[pairs_df['track_path_left'] != pairs_df['track_path_right']]
        
        pairs_df['similarity_count'] = pairs_df[['comment_left', 'comment_right']].apply(
            lambda x: TripletDataset._count_similarities(x.iloc[0], x.iloc[1]),
            axis=1
        )

        groups = pairs_df.groupby('track_path_left')

        self.df = groups[pairs_df.columns].apply(
            TripletDataset._generate_triplets,
            n=n,
        ).reset_index(drop=True)

    def _find_id3_comment(file_path) -> Optional[str]:
        id3 = None

        if file_path.lower().endswith('.mp3'):
            id3 = MP3(file_path, ID3=ID3)
        elif file_path.lower().endswith('.aif') or file_path.lower().endswith('.aiff'):
            id3 = AIFF(file_path)
        else:
            return None
        
        comms = [tag.text for tag in id3.tags.values() if isinstance(tag, COMM)]
        for comm in comms:
            for text in comm:
                if TripletDataset._is_class_comment(text):
                    return text

        return None
    
    def _is_class_comment(comment: str) -> bool:
        class_comment_pattern = r'^\d,[aetdfghiobr](?:;[aetdfghiobr])*$'

        return bool(re.match(class_comment_pattern, comment))

    def _count_similarities(comment_a: str, comment_b: str) -> bool:
        energy_str_a, genres_str_a = comment_a.split(",")
        genres_a = genres_str_a.split(";")

        energy_str_b, genres_str_b = comment_b.split(",")
        genres_b = genres_str_b.split(";")

        count = 0

        if energy_str_a == energy_str_b:
            count += 1
        
        for genre_a in genres_a:
            if genre_a in genres_b:
                count += 1

        return count
    
    def _generate_triplets(group, n: int) -> pd.Series:
        triplets = []
        for _ in range(n):
            anchor = group['track_path_left'].iloc[0]
            
            # Positive tracks: randomly select from best candidates
            max_similarity = group['similarity_count'].nlargest(n)
            positive_tracks = group[group['similarity_count'].isin(max_similarity)]
            positive_track = positive_tracks.sample(n=1)['track_path_right'].iloc[0]
            
            # Negative tracks: randomly select from worst candidates
            min_similarity = group['similarity_count'].nsmallest(n)
            negative_tracks = group[group['similarity_count'].isin(min_similarity)]
            negative_track = negative_tracks.sample(n=1)['track_path_right'].iloc[0]
            
            triplets.append([anchor, positive_track, negative_track])
        
        return pd.DataFrame(triplets, columns=['anchor', 'positive', 'negative'])

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "tracks_folder",
        help="path to folder of tracks with comment ID3 tags like '2;e;d'"
    )
    args = parser.parse_args()

    dataset = TripletDataset(args.tracks_folder)
    print(dataset.df)
