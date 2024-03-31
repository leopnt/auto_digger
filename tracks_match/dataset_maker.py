import pandas as pd
from audio_matrix import AudioMatrix
import os
import random
import streamlit as st


def list_files_in_directory(directory):
    files = []
    for filename in os.listdir(directory):
        files.append(filename)
    return files


def get_n_random_candidates(tracklist: list[str], n: int, seed: int = 42):
    tracklist_cpy = tracklist.copy()
    random.Random(seed).shuffle(tracklist_cpy)

    return tracklist_cpy[:n]


def generate_key_pairs(list1, list2):
    key_pairs = set()
    for item1 in list1:
        for item2 in list2:
            key_pairs.add(tuple(sorted((item1, item2))))
    return key_pairs


def generate_random_order_key_pairs(list1, list2):
    key_pairs = list(generate_key_pairs(list1, list2))
    random.shuffle(key_pairs)
    return key_pairs


if "candidates" not in st.session_state:
    files = list_files_in_directory("./tracks")
    candidates = get_n_random_candidates(files, len(files))
    st.session_state["candidates"] = candidates

if "am" not in st.session_state:
    am = AudioMatrix()
    try:
        am.from_dataframe(pd.read_csv("audio_matrix.csv"))
    except FileNotFoundError:
        print("Cannot load audio_matrix.csv")

    st.session_state["am"] = am


if "random_order_key_pairs" not in st.session_state:
    random_order_key_pairs = generate_random_order_key_pairs(candidates, candidates)

    # filter to keep only missing pairs
    pairs = []
    for left, right in random_order_key_pairs:
        if left != right and not st.session_state.am.pair_exists(left, right):
            pairs.append((left, right))

    st.session_state["random_order_key_pairs"] = iter(pairs)

try:
    candidate_left, candidate_right = next(st.session_state.random_order_key_pairs)
except StopIteration:
    st.session_state.am.to_dataframe().to_csv("audio_matrix.csv", index=False)
    st.warning("No more key pairs. Data saved to `audio_matrix.csv`")
    st.stop()

st.write(candidate_left)
st.audio("./tracks/" + candidate_left)
st.write(candidate_right)
st.audio("./tracks/" + candidate_right)

st.header(f"is it a good match?")
col1, col2 = st.columns(2)
col1.button(
    "no",
    on_click=st.session_state.am.set_match,
    args=[candidate_left, candidate_right, False],
)
col2.button(
    "yes",
    on_click=st.session_state.am.set_match,
    args=[candidate_left, candidate_right, True],
)

st.divider()

st.button(
    "save",
    on_click=st.session_state.am.to_dataframe().to_csv("audio_matrix.csv", index=False),
)

st.write(f"len(dataframe): {len(st.session_state.am.to_dataframe())}")

st.dataframe(
    st.session_state.am.to_dataframe(), use_container_width=True, hide_index=True
)
