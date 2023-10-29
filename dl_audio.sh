#!/usr/bin/bash

if [ -z "$1" ]
  then
    echo "Usage: $0 <url> <audio_name>"
    echo '<url> should be surrounded by quotation marks: e.g "https://www.youtube.com/watch?v=9StMS1iXdho"'
    exit
fi

SCRIPT_DIR=`dirname "$0"`

yt-dlp "$1" --add-header User-Agent:"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15" \
    -o "$SCRIPT_DIR/youtube-downloaded/out.%(ext)s" \
    -x --remux-video "webm>ogg/opus>ogg/m4a>ogg" \
    -f "bestaudio" \
    --add-metadata
    --no-part

ffmpeg -i "$SCRIPT_DIR/youtube-downloaded/out.ogg"  -ar 44100 -b:a 256k -map_metadata 0 -map_metadata 0:s:0 -id3v2_version 3 -vn "$SCRIPT_DIR/youtube-downloaded/out.mp3"

mv "$SCRIPT_DIR/youtube-downloaded/out.mp3" "$SCRIPT_DIR/youtube-downloaded/$2.mp3"

rm "$SCRIPT_DIR/youtube-downloaded/out.ogg"
