# builds audio/mix.wav (20 s) from sfx + voice + music
cd ~/blender-car-film/audio
# name start_s volume trim_s fade_in fade_out
ffmpeg -v error -y \
 -i norm/wind.wav -i norm/lampbuzz.wav -i norm/start.wav -i norm/pullaway.wav -i norm/drive.wav -i norm/whoosh.wav -i norm/whoosh.wav -i norm/interior.wav -i norm/brake.wav -i norm/tick.wav -i norm/click.wav -i norm/vo1.wav -i norm/vo2.wav -i norm/music.wav -i norm/music.wav \
 -filter_complex "
 [0]atrim=0:20,volume=0.35,afade=t=out:st=18.5:d=1.5[a0];
 [1]atrim=0:3.3,volume=0.3,afade=t=out:st=2.8:d=0.5[a1];
 [2]volume=0.9,adelay=3200|3200[a2];
 [3]volume=0.8,adelay=5000|5000[a3];
 [4]atrim=0:4.2,volume=0.55,afade=t=in:d=0.3,afade=t=out:st=3.8:d=0.4,adelay=7000|7000[a4];
 [5]volume=0.45,adelay=8900|8900[a5];
 [6]volume=0.45,adelay=10200|10200[a6];
 [7]atrim=0:3.6,volume=0.6,afade=t=in:d=0.15,afade=t=out:st=3.2:d=0.4,adelay=11000|11000[a7];
 [8]volume=0.85,adelay=14100|14100[a8];
 [9]volume=0.5,adelay=17200|17200[a9];
 [10]volume=0.9,adelay=17500|17500[a10];
 [11]volume=1.0,adelay=8500|8500[v1];
 [12]volume=1.0,adelay=17900|17900[v2];
 [13]atrim=0:9.5,volume=0.22,afade=t=in:d=1.5,afade=t=out:st=7.5:d=2,adelay=7000|7000[m1];
 [14]atrim=0:2.5,volume=0.2,afade=t=out:st=1.2:d=1.3,adelay=17500|17500[m2];
 [a0][a1][a2][a3][a4][a5][a6][a7][a8][a9][a10][m1][m2]amix=inputs=13:normalize=0,volume=0.3:enable='between(t,8.35,10.35)+between(t,17.75,19.95)'[bus];[bus][v1][v2]amix=inputs=3:normalize=0,atrim=0:20,afade=t=out:st=19:d=1,alimiter=limit=0.9[out]" \
 -map "[out]" -ar 48000 -ac 2 mix.wav && echo "mix ok"
