import pandas as pd
import os
import shutil

df = pd.read_csv("/Users/leopnt/Data/tracks_similarity.csv")

df_labelled = df.dropna(subset="estimated_similarity")

def copy_to_local_dir(absolute_path: str):
    shutil.copy(absolute_path, "./tracks")

def get_local_path(original_path: str):
    filename = os.path.basename(original_path)
    cwd = os.getcwd()
    relative_new_directory = os.path.relpath("/Users/leopnt/Data/tracks_similarity/tracks", cwd)
    new_path = os.path.join(relative_new_directory, filename)
    return new_path

# copy target tracks to local dir
for audio_target_track in df_labelled["target"].unique():
    copy_to_local_dir(audio_target_track)

# copy tracks to local dir
for audio_track in df_labelled["audio_track"]:
    copy_to_local_dir(audio_track)

# update the paths to be relative
df_labelled_updated_path = df_labelled.copy()
df_labelled_updated_path["audio_track"] = df_labelled_updated_path["audio_track"].apply(get_local_path)
df_labelled_updated_path["target"] = df_labelled_updated_path["target"].apply(get_local_path)

df_labelled_updated_path.to_csv("tracks_similarity.csv", index=False)

print(df_labelled_updated_path)

