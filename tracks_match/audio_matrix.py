import pandas as pd


class AudioMatrix:
    def __init__(self):
        self.matrix = {}

    def set_match(self, audio1, audio2, match: bool):
        pair = tuple(sorted((audio1, audio2)))
        self.matrix[pair] = match

    def remove_match(self, audio1, audio2):
        pair = tuple(sorted((audio1, audio2)))
        if pair in self.matrix:
            del self.matrix[pair]

    def get_match(self, audio1, audio2):
        pair = tuple(sorted((audio1, audio2)))
        return self.matrix.get(pair, None)

    def pair_exists(self, audio1, audio2):
        pair = tuple(sorted((audio1, audio2)))
        return pair in self.matrix

    def to_dataframe(self):
        data = []
        for pair, match in self.matrix.items():
            audio1, audio2 = pair
            data.append([audio1, audio2, match])
        return pd.DataFrame(data, columns=["left", "right", "match"])

    def from_dataframe(self, df):
        for _, row in df.iterrows():
            self.set_match(row["left"], row["right"], row["match"])


if __name__ == "__main__":
    audio_matrix = AudioMatrix()

    audio_matrix.set_match("audio1.wav", "audio2.wav", True)
    audio_matrix.set_match("audio1.wav", "audio3.wav", False)
    audio_matrix.set_match("audio2.wav", "audio3.wav", True)

    print(audio_matrix.get_match("audio1.wav", "audio2.wav"))
    print(audio_matrix.get_match("audio2.wav", "audio1.wav"))
    print(audio_matrix.get_match("audio1.wav", "audio3.wav"))
    print(audio_matrix.get_match("audio3.wav", "audio1.wav"))
    print(audio_matrix.get_match("audio2.wav", "audio3.wav"))
    print(audio_matrix.get_match("audio_abcd.wav", "audio3.wav"))

    print(audio_matrix.to_dataframe())
