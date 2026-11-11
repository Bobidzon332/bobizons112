"""Sound design for the 10 s night FPV edit, driven by the real 3D motion (audio/motion.json).
Real recordings (BigSoundBank CC0) + a little synthesis, all placed and shaped per frame:
  drone      real DJI quadcopter loop, pitch = throttle (motor RPM) x Doppler, gain = 1/distance, air absorption, pan,
             + a thin synthetic 4-motor buzz for the racing-quad edge, + prop-wash bursts on throttle punches,
             + spray hiss when it hovers low over the wet asphalt, roll flutter during the barrel roll
  wind       camera-speed driven rumble + whistle (the chase cam is moving at up to 28 m/s)
  city       Paris-at-1am balcony bed (distant city), wet-road traffic rumble that grows as the camera gets low,
             rooftop air-con unit on the roof shot, idling traffic + wet street at street level
  cars       pass-bys placed at each moving car's closest approach (gain/pan from the scene), wet-tyre hiss layer
  events     taxi horn during the swoop over the taxis, distant siren wailing across the city, launch whoosh
  space      street-canyon reverb send (early reflections off the facades + 1.4 s tail)
Writes audio/sfx_mix.wav (48 kHz stereo) and audio/stems/*.wav.
"""
import json, os, subprocess, math
import numpy as np
from scipy import signal
from scipy.io import wavfile

ROOT = os.path.join(os.environ.get("FILM_ROOT", os.path.expanduser("~/blender-film")), "audio")
SRC = os.path.join(ROOT, "src")
SR = 48000
M = json.load(open(os.path.join(ROOT, "motion.json")))
FR = M["frames"]
NF = len(FR)
N = int(round(NF / 24 * SR))
t = np.arange(N) / SR
rng = np.random.default_rng(7)
os.makedirs(os.path.join(ROOT, "stems"), exist_ok=True)


def load(name, stereo=False):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(SRC, name), "-ac", "2" if stereo else "1",
                          "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
    x = np.frombuffer(raw, np.float32).astype(np.float64)
    return x.reshape(-1, 2) if stereo else x


def ctl(key, fn=None):
    """per-frame value -> per-sample curve (frame k covers [(k-1)/24, k/24))"""
    v = np.array([(fn(f) if fn else f[key]) for f in FR], dtype=np.float64)
    tc = (np.arange(NF) + 0.5) / 24
    return np.interp(t, tc, v)


def smooth(x, tau):
    a = math.exp(-1.0 / (tau * SR))
    return signal.lfilter([1 - a], [1, -a], x)


def onepole_lp_var(x, fc):
    """time-varying one-pole low-pass (fc per sample)"""
    a = np.exp(-2 * np.pi * np.clip(fc, 20, 20000) / SR)
    y = np.empty_like(x); s = 0.0
    for i in range(len(x)):
        s = (1 - a[i]) * x[i] + a[i] * s; y[i] = s
    return y


def bp(x, lo, hi, order=2):
    sos = signal.butter(order, [lo, hi], "bandpass", fs=SR, output="sos"); return signal.sosfilt(sos, x, axis=0)


def hp(x, f, order=2):
    sos = signal.butter(order, f, "highpass", fs=SR, output="sos"); return signal.sosfilt(sos, x, axis=0)


def lp(x, f, order=2):
    sos = signal.butter(order, f, "lowpass", fs=SR, output="sos"); return signal.sosfilt(sos, x, axis=0)


def loop_to(x, n, start=0):
    x = x[start:] if start < len(x) else x
    if len(x) >= n: return x[:n].copy()
    reps = int(np.ceil(n / len(x))) + 1
    xf = int(0.05 * SR)
    out = x.copy()
    for _ in range(reps):        # crossfaded loop
        w = np.linspace(0, 1, xf)
        if out.ndim == 2: w = w[:, None]
        out = np.concatenate([out[:-xf], out[-xf:] * (1 - w) + x[:xf] * w, x[xf:]])
        if len(out) >= n: break
    return out[:n]


def pan2(x, p):
    """equal-power pan, p in [-1, 1] (scalar or per-sample)"""
    a = (np.asarray(p) + 1) * np.pi / 4
    return np.stack([x * np.cos(a), x * np.sin(a)], axis=1)


def norm(x):
    return x / (np.sqrt(np.mean(x ** 2)) + 1e-9)


def db(v):
    return 10 ** (v / 20)


shot = ctl("shot")
shot_i = np.rint(shot).astype(int)
starts = [next(f["k"] for f in FR if f["shot"] == s) for s in range(6)]
cut_s = [int(round((k - 1) / 24 * SR)) for k in starts]
def shot_gain(values, tau=0.012):
    """piecewise per-shot gain, de-clicked at the cuts"""
    g = np.array([values[s] for s in shot_i], dtype=np.float64)
    return smooth(g, tau)

stems = {}

# =============================== DRONE =================================
dist = ctl("dist"); radial = ctl("radial"); pan = ctl("pan"); front = ctl("front")
thr_raw = ctl("throttle")
# motors on the roof: off until spin-up (scene f6 -> edit k5), arming ramp to take-off (f12 -> k11)
kk = t * 24 + 1
spin = np.clip((kk - 5) / 6.0, 0, 1) ** 1.6
thr = smooth(np.where(kk < 11, 0.35 + 0.65 * spin, thr_raw), 0.06)          # ESC + motor inertia ~60 ms
rpm = np.clip(0.70 + 0.30 * np.power(np.maximum(thr, 0.05), 0.62), 0.66, 1.75)  # 1 g hover = 1.0x
rpm = np.where(kk < 11, 0.25 + 0.75 * spin, rpm)
doppler = 343.0 / (343.0 + np.clip(radial, -60, 60))
rate = smooth(rpm * doppler, 0.01)

d4 = load("3548_drone4.wav"); d2 = load("3546_drone2.wav"); d7 = load("3551_drone7.wav")
srcloop = np.concatenate([norm(d4[int(1.5 * SR):int(11.2 * SR)]), norm(d7[int(18 * SR):int(30 * SR)]), norm(d2[int(22 * SR):int(33 * SR)])])
srcloop = hp(srcloop, 90)
phase = np.cumsum(rate) + 1.2 * SR
idx = np.mod(phase, len(srcloop) - 2)
i0 = idx.astype(int); fr_ = idx - i0
real = srcloop[i0] * (1 - fr_) + srcloop[i0 + 1] * fr_

# synthetic racing-quad edge: 4 motors, blade-pass buzz (~ 3 blades x RPM), harmonics, slight detune
f0 = 360.0 * rate
synth = np.zeros(N)
for m, det in enumerate((1.0, 1.011, 0.992, 1.024)):
    ph = 2 * np.pi * np.cumsum(f0 * det) / SR + m * 1.3
    for h in range(1, 9):
        synth += np.sin(h * ph) / (h ** 1.15) * (1.0 if h % 3 else 1.35)
synth = hp(synth, 200) + 0.15 * hp(rng.standard_normal(N), 3000) * norm(lp(np.abs(real), 40))
synth = norm(lp(synth, 8500))

brightness = np.clip(0.4 + 0.22 * thr, 0.3, 1.45)                         # harder throttle = brighter, raspier
real_b = real + 0.6 * (brightness - 0.6) * hp(real, 2500)
drone_mono = 0.82 * norm(real_b) + 0.24 * synth * np.clip(thr, 0.2, 1.6) / 1.6 + 0.08 * synth
# amplitude: motors louder with throttle, zero before spin-up
amp = np.clip(0.55 + 0.30 * np.sqrt(np.maximum(thr, 0)), 0.45, 1.5) * np.where(kk < 5, 0, 1) * np.where(kk < 11, spin, 1)
# hero yaw (scene f481-515 -> during the stare turn): one motor pair works harder -> beating + slight pitch split
yaw = np.zeros(N)
for f in FR:
    if f["cam"] == "CAM_HERO" and 481 <= f["frame"] <= 515:
        k = f["k"]; s = int((k - 1) / 24 * SR); yaw[s:s + SR // 24] = 1
yaw = smooth(yaw, 0.15)
drone_mono = drone_mono * (1 + 0.12 * yaw * np.sin(2 * np.pi * 7.5 * t))
# barrel roll flutter (props sweep past the lens): roll window in scene frames 312-336 (chase shot 4)
roll = np.zeros(N)
for f in FR:
    if f["cam"] == "Camera" and 312 <= f["frame"] <= 336:
        k = f["k"]; s = int((k - 1) / 24 * SR); roll[s:s + SR // 24] = 1
roll = smooth(roll, 0.05)
drone_mono = drone_mono * (1 - 0.28 * roll * (0.5 + 0.5 * np.sin(2 * np.pi * 2.3 * t)))
# distance: inverse law re 1.2 m, air absorption + less high end when far
g_dist = 1.2 / np.maximum(dist, 0.6)
drone_mono = onepole_lp_var(drone_mono, 16000 / (1 + dist / 6.0)) * amp * g_dist
# chase cam rides behind the quad: slight occlusion of the front props by the frame
drone_mono = drone_mono * np.where(shot_i == 1, 0.95, 1.0)
stems["drone"] = pan2(drone_mono * shot_gain({0: 1, 1: 1, 2: 1, 3: 1, 4: 1.6, 5: 1}), np.clip(pan * 0.8, -0.8, 0.8))

# prop wash: turbulent air bursts on throttle punches (big positive throttle steps)
dthr = np.gradient(smooth(thr, 0.03)) * SR
burst = np.clip(dthr / 25.0, 0, 1.0) + np.clip((thr - 2.2) / 4.0, 0, 0.7)
burst = smooth(burst, 0.08)
wf = load("0595_wind_foley.wav")
wash = bp(loop_to(norm(wf), N, int(20 * SR)), 250, 4000)
wash = norm(wash) * burst * g_dist * 0.75
thump = lp(rng.standard_normal(N), 110) * smooth(np.clip(dthr / 30.0, 0, 1), 0.06) * g_dist   # air pressure of a punch
wash = wash + norm(lp(rng.standard_normal(N), 110)) * smooth(np.clip(dthr / 30.0, 0, 1), 0.06) * g_dist * 0.9
# street-level dive: the air rushing in ahead of the quad (grows with approach speed and closeness) + braking blast
dsp = ctl("drone_speed")
decel = smooth(np.clip(-np.gradient(smooth(dsp, 0.05)) * SR / 25.0, 0, 1), 0.08)
approach = np.clip(-radial / 18.0, 0, 1) * (shot_i == 4)
rush = bp(loop_to(norm(wf), N, int(70 * SR)), 500, 7000)
wash = wash + norm(rush) * smooth(approach, 0.05) * g_dist * 0.55 + norm(bp(rng.standard_normal(N), 150, 3000)) * decel * g_dist * 0.8 * (shot_i == 4)
stems["propwash"] = pan2(wash, np.clip(pan * 0.6, -0.6, 0.6))

# spray: prop wash hitting the wet asphalt when the quad is low (street-level + hero shots)
dz = ctl("drone_z")
low = np.clip((2.4 - dz) / 1.2, 0, 1) * np.isin(shot_i, [4, 5])
pud = load("1290_rain_puddle.wav")
spray = hp(loop_to(norm(pud), N, int(5 * SR)), 1800) + 0.5 * hp(rng.standard_normal(N), 5000) * 0.25
spray = norm(spray) * smooth(low, 0.2) * np.clip(thr, 0.5, 3) / 3 * g_dist * 0.32
stems["spray"] = pan2(spray, 0.05)

# =============================== WIND (camera motion) =================================
cs = ctl("cam_speed")
wv = np.clip(cs / 26.0, 0, 1.25) ** 2
gust = 0.75 + 0.25 * smooth(rng.standard_normal(N), 0.25) * 4
wind_low = bp(loop_to(norm(wf), N, int(45 * SR)), 90, 700)
ww = load("0155_wind_whistle2.wav")
wind_hi = bp(loop_to(norm(ww), N, int(8 * SR)), 900, 6000)
wind = norm(wind_low) * 0.9 + norm(wind_hi) * 0.35 * np.clip(wv * 1.4, 0, 1)
wind = wind * (wv * 0.85 + 0.03) * np.clip(gust, 0.4, 1.4)
# roof: a light breeze up there
wind = wind + norm(lp(loop_to(norm(wf), N, int(60 * SR)), 900)) * 0.10 * (shot_i == 0)
wind_st = np.stack([wind * (1 + 0.15 * np.sin(2 * np.pi * 0.31 * t)), wind * (1 - 0.15 * np.sin(2 * np.pi * 0.31 * t + 1))], axis=1)
stems["wind"] = wind_st * shot_gain({0: 1.0, 1: 1.0, 2: 1.0, 3: 1.0, 4: 0.25, 5: 0.15})[:, None]

# =============================== CITY =================================
camz = ctl("cam_z")
paris = load("0680_paris_night.wav", stereo=True)
city_bed = loop_to(paris, N, int(12 * SR))
city_bed = city_bed / (np.sqrt(np.mean(city_bed ** 2)) + 1e-9)
streetness = np.clip((16 - camz) / 13.0, 0, 1)                      # closer to the street = more road
wet = load("0621_night_after_rain.wav", stereo=True)
wet_road = loop_to(wet, N, int(20 * SR)); wet_road = wet_road / (np.sqrt(np.mean(wet_road ** 2)) + 1e-9)
cross = load("2722_crossroads.wav", stereo=True)
idle = loop_to(cross, N, int(140 * SR)); idle = lp(idle / (np.sqrt(np.mean(idle ** 2)) + 1e-9), 1800)
hw = load("0122_highway.wav")
rumble = lp(loop_to(norm(hw), N, int(10 * SR)), 220)
city = city_bed * shot_gain({0: 0.28, 1: 0.36, 2: 0.32, 3: 0.36, 4: 0.13, 5: 0.15}, 0.15)[:, None]
city += wet_road * (smooth(streetness, 0.3) * 0.50 * shot_gain({0: 0.3, 1: 1, 2: 1, 3: 1, 4: 0.6, 5: 0.55}))[:, None]
city += idle * shot_gain({0: 0, 1: 0, 2: 0.10, 3: 0.05, 4: 0.22, 5: 0.14}, 0.15)[:, None]
city += pan2(norm(rumble), 0) * (0.05 + 0.10 * smooth(streetness, 0.3))[:, None]
# high up during the back flip: the city drops away, just the far wash
city = city * (1 - 0.35 * smooth(np.clip((camz - 24) / 10, 0, 1), 0.3))[:, None]
stems["city"] = hp(city, 55)
# rooftop air-con unit next to the camera (roof shot only)
ac = load("1471_aircon.wav")
ac = lp(loop_to(norm(ac), N, int(30 * SR)), 2500)
stems["aircon"] = pan2(ac * 0.22 * shot_gain({0: 1, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}), 0.65)

# =============================== CARS (pass-bys at closest approach) =================================
pass_a = load("2996_car_pass50_12.wav"); pass_b = load("2987_car_pass50_3.wav")
def peak_time(x):
    e = smooth(np.abs(x), 0.05); return int(np.argmax(e))
cars = np.zeros((N, 2))
tires = np.zeros((N, 2))
events = []
by_car = {}
for f in FR:
    for c in f["cars"]:
        if c["speed"] < 2: continue
        key = (c["name"], f["shot"])
        if key not in by_car or c["dist"] < by_car[key][0]:
            by_car[key] = (c["dist"], f["k"], c["pan"], c["speed"])
for (name, s), (dmin, k, p, spd) in sorted(by_car.items(), key=lambda kv: kv[1][1]):
    if dmin > 16: continue
    src = pass_a if (hash(name) % 2) else pass_b
    pk = peak_time(src)
    at = int((k - 1) / 24 * SR)
    a0 = at - pk
    seg_start = max(0, -a0); a0 = max(0, a0)
    clip = src[seg_start:seg_start + (N - a0)]
    shot_lo, shot_hi = cut_s[s], (cut_s[s + 1] if s + 1 < len(cut_s) else N)
    env = np.zeros(N); env[a0:a0 + len(clip)] = clip
    win = np.zeros(N); win[shot_lo:shot_hi] = 1; win = smooth(win, 0.01)    # a car only exists inside its shot
    g = min(1.0, 4.0 / max(dmin, 2.5)) * (spd / 9.0)
    sig = norm(clip) if len(clip) else clip
    env[a0:a0 + len(clip)] = sig
    env = env * win * g
    cars += pan2(hp(lp(env, 9000), 70) * 0.22, np.clip(p, -0.9, 0.9))
    tires += pan2(bp(env, 2500, 9000) * 0.30, np.clip(p, -0.9, 0.9))      # wet tyres: the hiss
    events.append(("car", name, s, round((k - 1) / 24, 2), round(dmin, 1)))
stems["cars"] = cars * shot_gain({0: 1, 1: 1, 2: 1, 3: 1, 4: 0.45, 5: 1})[:, None]
stems["wet_tyres"] = tires

# =============================== EVENTS =================================
ev = np.zeros((N, 2))
def place(x, at_s, gain, p, lpf=None):
    x = x.copy()
    if lpf: x = lp(x, lpf)
    a = int(at_s * SR); n = min(len(x), N - a)
    if n > 0: ev[a:a + n] += pan2(x[:n] * gain, p)
horn = load("0258_car_horn2.wav")
place(norm(horn), (starts[2] - 1) / 24 + 0.62, 0.22, -0.55, 4500)          # taxi below honks at the swoop
place(norm(horn)[: int(0.35 * SR)], (starts[2] - 1) / 24 + 1.25, 0.10, 0.6, 3500)   # answer, further away
bus = load("3593_bus_horns.wav")
place(norm(bus), (starts[5] - 1) / 24 + 0.9, 0.05, -0.7, 1800)            # far down the avenue during the stare
sir = load("2731_vehicle_siren.wav")
siren = lp(norm(sir[int(30 * SR):]), 2200)
s0 = int(((starts[3] - 1) / 24 + 1.2) * SR)
sg = np.zeros(N); sg[s0:] = np.clip(np.arange(N - s0) / (1.5 * SR), 0, 1)
siren_full = np.zeros(N); n = min(len(siren), N - s0); siren_full[s0:s0 + n] = siren[:n]
ev += pan2(siren_full * sg * 0.075, 0.35)
whoosh = load("1796_whoosh4.wav")
place(norm(whoosh), (starts[1] - 1) / 24 - 0.30, 0.30, 0.1)                  # launch off the roof
place(lp(norm(whoosh), 3000), (starts[4] - 1) / 24 - 0.12, 0.18, 0.0)       # into the street-level shot
stems["events"] = ev


# =============================== CITY CHAOS (background) =================================
# continuous street life under everything: dense traffic, a busy bus street, people, honking - closer and brighter
# when the camera is near the street, distant / darker / wetter in reverb when it is high up.
def st_norm(x): return x / (np.sqrt(np.mean(x ** 2)) + 1e-9)
height_far = smooth(np.clip((camz - 4) / 26.0, 0, 1), 0.25)                  # 0 at street level, 1 at roof height
near_street = 1 - height_far
traffic = st_norm(loop_to(load("1080_ring_road.wav", stereo=True), N, int(9 * SR)))
busst = st_norm(loop_to(load("0644_london_bus.wav", stereo=True), N, int(31 * SR)))
crowd = st_norm(loop_to(load("2969_outside_talks2.wav", stereo=True), N, int(40 * SR)))
honks = st_norm(loop_to(load("2372_cheerful_street_horns.wav", stereo=True), N, int(14 * SR)))
traffic = hp(traffic, 60); busst = hp(busst, 70); crowd = bp(crowd, 200, 5000); honks = bp(honks, 300, 3500)
def far_filter(x, amount):
    """blend between the dry layer and a dark distant version of it (air + buildings eat the highs)"""
    return x * (1 - amount)[:, None] + lp(x, 900) * amount[:, None]
chaos = (traffic * 0.55 + busst * 0.65) * (0.55 + 0.45 * near_street)[:, None]
chaos += crowd * (0.30 * near_street)[:, None]
chaos += honks * (0.18 + 0.10 * near_street)[:, None]
chaos = far_filter(chaos, height_far * 0.8)
# scattered horns + city incidents (random but repeatable), each with its own distance and side
hn = [load(f) for f in ("3438_car_honk90.wav", "3506_horn3.wav", "2524_horn5.wav", "2721_truck_horn.wav", "1830_pneumatic_horn1.wav", "0258_car_horn2.wav")]
rr = np.random.default_rng(11)
incidents = np.zeros((N, 2))
for i, at in enumerate((0.35, 1.4, 2.1, 3.15, 4.6, 5.3, 6.4, 7.4, 8.6, 9.3)):
    x = norm(hn[i % len(hn)]); x = x[: int(min(len(x), rr.uniform(0.25, 1.1) * SR))]
    x = x * np.minimum(1, np.linspace(1, 0, len(x)) * 6)                     # release, no hard stops
    dist_m = rr.uniform(25, 140)
    x = lp(x, 9000 / (1 + dist_m / 40)) * (12.0 / dist_m)
    a = int(at * SR); n = min(len(x), N - a)
    incidents[a:a + n] += pan2(x[:n] * 0.5, rr.uniform(-0.9, 0.9))
moto = norm(load("0906_moto_pass90.wav"))
a = int(4.9 * SR); n = min(len(moto), N - a); incidents[a:a + n] += pan2(lp(moto[:n], 3500) * 0.12, -0.6)   # far bike on a cross street
brake = norm(load("1490_pneumatic_brake.wav"))
a = int(7.55 * SR); n = min(len(brake), N - a); incidents[a:a + n] += pan2(lp(brake[:n], 5000) * 0.10, 0.75)  # bus air brakes up the block
truck = norm(lp(loop_to(load("1443_truck_engine2.wav"), N, int(12 * SR)), 900))
incidents += pan2(truck * 0.10 * shot_gain({0: 0, 1: 0, 2: 0, 3: 0, 4: 0.8, 5: 1.0}, 0.15), -0.45)   # idling truck in the jam
drone_env = smooth(np.abs(stems["drone"]).mean(axis=1), 0.18)
duck = 1 - 0.38 * np.clip(drone_env / (np.percentile(drone_env, 92) + 1e-9), 0, 1)       # sidechain: city breathes under the drone
stems["chaos"] = chaos * (shot_gain({0: 0.75, 1: 0.85, 2: 0.95, 3: 0.85, 4: 0.62, 5: 0.65}, 0.15) * duck)[:, None]
stems["city"] = stems["city"] * (0.75 + 0.25 * duck)[:, None]
stems["incidents"] = incidents

# =============================== SPACE (street canyon) =================================
def canyon_ir(length=1.4):
    n = int(length * SR); ir = np.zeros(n)
    for d_ms, g in ((23, 0.55), (41, 0.42), (67, 0.35), (93, 0.25), (131, 0.18)):   # facades both sides
        ir[int(d_ms / 1000 * SR)] += g
    tail = rng.standard_normal(n) * np.exp(-np.arange(n) / (0.32 * SR)) * 0.10
    tail[: int(0.02 * SR)] = 0
    ir += lp(tail, 5000)
    return ir
ir = canyon_ir()
send = stems["drone"] * 0.35 + stems["cars"] * 0.25 + stems["events"] * 0.5 + stems["propwash"] * 0.2 + stems["incidents"] * 0.9 + stems["chaos"] * 0.15
verb = np.stack([signal.fftconvolve(send[:, 0], ir)[:N], signal.fftconvolve(send[:, 1], ir[::-1].copy()[::-1])[:N]], axis=1)
amount = shot_gain({0: 0.35, 1: 0.45, 2: 0.55, 3: 0.5, 4: 0.75, 5: 0.7})
stems["reverb"] = verb * amount[:, None] * 0.6

# =============================== MIX =================================
LEVEL = {"drone": 0.0, "propwash": -2, "spray": -3, "wind": -5, "city": -7, "aircon": -4, "cars": -5, "wet_tyres": -6,
         "events": -1, "reverb": -9, "chaos": -9, "incidents": -4}
mix = np.zeros((N, 2))
for k, x in stems.items():
    y = x * db(LEVEL[k])
    mix += y
    wavfile.write(os.path.join(ROOT, "stems", f"{k}.wav"), SR, (y / 4).astype(np.float32))
mix = hp(mix, 38)
# gentle low-mid cleanup (the 120-250 Hz build-up of many outdoor beds)
b, a = signal.iirpeak(180, 0.9, fs=SR)
mix = mix - 0.25 * signal.lfilter(b, a, mix, axis=0)
pk = np.max(np.abs(mix)); mix = mix / pk * 0.89
wavfile.write(os.path.join(ROOT, "sfx_mix_raw.wav"), SR, mix.astype(np.float32))
print("samples", N, "secs", round(N / SR, 3), "shot cuts (s)", [round(c / SR, 3) for c in cut_s])
for e in events: print(" ", e)
for k, x in stems.items():
    print(f"  {k:10s} rms {20*np.log10(np.sqrt(np.mean((x*db(LEVEL[k]))**2))+1e-9):6.1f} dB")
