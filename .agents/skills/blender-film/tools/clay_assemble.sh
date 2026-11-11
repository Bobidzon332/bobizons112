#!/bin/bash
# Clay build-up clip: A night 300-347 | hard cut | B clay 1-168 | 0.25 s wipe down (night enters from the top) | C night 348-411
# usage: clay_assemble.sh <frames dir with night/ and clay/> <out.mp4> <ext jpg|png> <crf>
D=$1; OUT=$2; X=${3:-jpg}; CRF=${4:-18}
ffmpeg -y -loglevel error -framerate 24 -start_number 300 -i "$D/night/n_%04d.$X" -framerate 24 -start_number 1 -i "$D/clay/c_%04d.$X" \
  -filter_complex "[0]trim=end_frame=48,setpts=PTS-STARTPTS[a];[1]trim=end_frame=168,setpts=PTS-STARTPTS[b];[0]trim=start_frame=48:end_frame=112,setpts=PTS-STARTPTS[c];[a][b]concat=n=2:v=1:a=0,settb=1/24[ab];[c]settb=1/24[c2];[ab][c2]xfade=transition=wipedown:duration=0.25:offset=8.75,format=yuv420p[v]" \
  -map "[v]" -c:v libx264 -crf $CRF -preset slow -r 24 -movflags +faststart "$OUT" && echo "ASSEMBLED $OUT"
