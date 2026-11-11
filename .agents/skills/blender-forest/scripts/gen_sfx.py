"""Generate the clip's sound effects with your ElevenLabs account (sound-generation API).
Standard library only. Writes audio/<name>.mp3."""
import json, os, sys, urllib.request

KEY = os.environ.get("ELEVENLABS_API_KEY")
OUT = os.path.join(os.path.expanduser("~"), "blender-forest", "audio")
SFX = {
    "forest_amb":  ("Calm summer forest ambience, birds chirping in the distance, gentle wind moving through leaves, no people", 14.0),
    "car_far":     ("Porsche 911 GT3 RS flat-six engine approaching from a distance on a gravel forest road, tyres crunching gravel, driving past slowly", 5.0),
    "car_onboard": ("Close-up recording at the rear wheel of a sports car driving fast on a gravel road, loud flat-six engine, gravel crunching and small stones hitting the underbody, wind rush", 4.0),
    "car_away":    ("Sports car with a flat-six engine driving away on a gravel forest road, engine fading into the distance, birds in the background", 4.0),
    "whoosh":      ("Short subtle cinematic whoosh transition, airy, soft", 1.0),
}
if not KEY:
    sys.exit("ELEVENLABS_API_KEY not set")
os.makedirs(OUT, exist_ok=True)
for name, (text, dur) in SFX.items():
    path = os.path.join(OUT, name + ".mp3")
    if os.path.exists(path):
        print("skip", name); continue
    req = urllib.request.Request(
        "https://api.elevenlabs.io/v1/sound-generation",
        data=json.dumps({"text": text, "duration_seconds": dur, "prompt_influence": 0.45}).encode(),
        headers={"xi-api-key": KEY, "Content-Type": "application/json", "Accept": "audio/mpeg"})
    with urllib.request.urlopen(req, timeout=120) as r:
        open(path, "wb").write(r.read())
    print("ok", name, os.path.getsize(path), "bytes")
