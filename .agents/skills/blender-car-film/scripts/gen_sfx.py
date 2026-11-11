import json, os, sys, urllib.request, urllib.error
key = os.environ["ELEVENLABS_API_KEY"]
S = {
 "wind": ("cold quiet winter night ambience, soft wind, gentle falling snow hiss, distant nothing", 20),
 "lampbuzz": ("old sodium street lamp electrical hum buzzing quietly at night", 6),
 "start": ("old 1970s car, key turns in ignition, starter motor cranks twice, petrol engine starts and settles into rough idle", 4),
 "pullaway": ("old car tyres slowly rolling over crunchy fresh snow, engine revs as car pulls away", 3),
 "drive": ("old petrol car driving at 45 km/h on a slushy snowy road at night, exterior, engine and tyre slush", 6),
 "whoosh": ("fast car pass-by whoosh close to camera on wet road", 1.5),
 "interior": ("inside an old car driving at night, muffled engine drone, windscreen wipers thunk back and forth, heater fan", 5),
 "brake": ("old car brakes squeak as it slows and stops on snowy slush, then the engine is switched off", 4),
 "tick": ("hot car engine metal ticking as it cools down, quiet snowy night", 4),
 "click": ("single outdoor porch light switch click", 1),
}
for name, (text, dur) in S.items():
    out = f"{name}.mp3"
    if os.path.exists(out): continue
    body = json.dumps({"text": text, "duration_seconds": dur, "prompt_influence": 0.5}).encode()
    req = urllib.request.Request("https://api.elevenlabs.io/v1/sound-generation", data=body, headers={"xi-api-key": key, "Content-Type": "application/json"})
    try: open(out, "wb").write(urllib.request.urlopen(req, timeout=180).read()); print("ok", name)
    except urllib.error.HTTPError as e: print("fail", name, e.code, e.read()[:200])
# music
if not os.path.exists("../music.mp3"):
    body = json.dumps({"prompt": "soft melancholic solo piano, sparse gentle notes, warm, cinematic, slow, nostalgic, no drums", "music_length_ms": 14000}).encode()
    req = urllib.request.Request("https://api.elevenlabs.io/v1/music", data=body, headers={"xi-api-key": key, "Content-Type": "application/json"})
    try: open("../music.mp3", "wb").write(urllib.request.urlopen(req, timeout=300).read()); print("ok music")
    except urllib.error.HTTPError as e: print("fail music", e.code, e.read()[:200])
