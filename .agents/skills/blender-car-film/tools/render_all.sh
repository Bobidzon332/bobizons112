#!/bin/bash
# Renders all remaining shots one by one, encodes each shot + the full film. Resumable: rerun after a power cut.
cd ~/blender-car-film
B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
LOG=build/render_all.log
# wait for any other background Blender render to finish (GPU is shared)
while powershell -NoProfile -c "if (Get-CimInstance Win32_Process -Filter \"Name='blender.exe'\" | ?{ \$_.CommandLine -match ' -b ' }) { exit 0 } else { exit 1 }"; do sleep 20; done
enc() { # name first last
  local n=$1 s=$2 e=$3; local cnt=$((e - s + 1)); local off=$(python -c "print(($s-1)/30)"); local dur=$(python -c "print($cnt/30)")
  ffmpeg -v error -y -framerate 30 -start_number $s -i frames/f_%04d.png -ss $off -i audio/mix.wav -frames:v $cnt -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -c:a aac -b:a 256k -t $dur video/$n.mp4
}
for spec in "shot3 152 211" "shot4 212 331" "shot5 332 436" "shot6 437 600"; do
  set -- $spec
  echo "$(date +%T) start $1 ($2-$3)" >> $LOG
  "$B" -b "$(cygpath -w last_drive_home.blend)" --python "$(cygpath -w build/render_frames.py)" -s $2 -e $3 -a > build/$1.log 2>&1
  echo "$(date +%T) rendered $1: $(ls frames | wc -l) frames total" >> $LOG
  enc $1 $2 $3 && echo "$(date +%T) encoded video/$1.mp4" >> $LOG
done
# full film: fade in from black, fade out at the end
ffmpeg -v error -y -framerate 30 -start_number 1 -i frames/f_%04d.png -i audio/mix.wav -frames:v 600 \
  -vf "fade=t=in:st=0:d=0.6,fade=t=out:st=19.0:d=1.0" -af "afade=t=in:d=0.6,afade=t=out:st=19.0:d=1.0" \
  -c:v libx264 -preset slow -crf 15 -pix_fmt yuv420p -c:a aac -b:a 320k -t 20 video/last_drive_home_FINAL.mp4 \
  && echo "$(date +%T) FINAL video/last_drive_home_FINAL.mp4" >> $LOG
