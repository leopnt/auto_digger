import subprocess
import pandas as pd

df = pd.read_csv("tracks_sample.csv")
df = df.drop_duplicates(subset=["id"])

for id, row in df.iterrows():
    url = "{}".format(row["url"])
    id = row["id"]

    args = ["./dl_audio.sh", url, str(id)]

    print(f'executing: {" ".join(args)}')
    out = subprocess.run(args)

    print("The exit code was: %d" % out.returncode)
