"""Música original (sin copyright): 126 BPM en La menor (8A).
Uso: python music.py out.wav DURACION [--kick T] [--bass T] [--clap T] [--seed N] [--outro T]"""
import argparse, numpy as np
from scipy.signal import butter, lfilter
from scipy.io import wavfile
ap = argparse.ArgumentParser(); ap.add_argument("out"); ap.add_argument("dur", type=float)
ap.add_argument("--kick", type=float, default=4.5); ap.add_argument("--bass", type=float, default=11.3)
ap.add_argument("--clap", type=float, default=11.3); ap.add_argument("--outro", type=float, default=-1)
ap.add_argument("--seed", type=int, default=7); a = ap.parse_args()
SR = 44100; BPM = 126; DUR = a.dur; OUTRO = a.outro if a.outro > 0 else DUR - 3.5
rng = np.random.default_rng(a.seed); n = int(SR * DUR); t = np.arange(n) / SR
beat = 60 / BPM; step = beat / 4
def lp(x, f, o=2): b, c = butter(o, f / (SR / 2)); return lfilter(b, c, x)
def hp(x, f, o=2): b, c = butter(o, f / (SR / 2), 'high'); return lfilter(b, c, x)
def env(tt, at, r): return np.minimum(tt / at, 1) * np.exp(-tt / r)
def ramp(x0, x1): return np.clip((t - x0) / (x1 - x0), 0, 1)
kick = np.zeros(n); hat = np.zeros(n); clap = np.zeros(n); bass = np.zeros(n)
notes = {0: 55.0, 3: 55.0, 6: 65.41, 8: 55.0, 11: 82.41, 14: 65.41}
def put(buf, i0, seg, gain=1.0):
    seg = seg[: max(0, min(len(seg), n - i0))]; buf[i0:i0 + len(seg)] += seg * gain
for k in range(int(DUR / beat) + 1):
    i0 = int(k * beat * SR); L = int(.28 * SR); tt = np.arange(L) / SR
    ph = 2 * np.pi * np.cumsum(45 + 110 * np.exp(-tt * 28)) / SR; put(kick, i0, np.sin(ph) * env(tt, .001, .11))
for s in range(int(DUR / step) + 1):
    i0 = int(s * step * SR)
    if s % 4 == 2: L = int(.05 * SR); tt = np.arange(L) / SR; put(hat, i0, hp(rng.standard_normal(L), 7000) * env(tt, .001, .018), .5)
    if s % 2 == 1: L = int(.03 * SR); tt = np.arange(L) / SR; put(hat, i0, hp(rng.standard_normal(L), 9000) * env(tt, .001, .008), .22)
    if s % 8 == 4: L = int(.18 * SR); tt = np.arange(L) / SR; put(clap, i0, hp(lp(rng.standard_normal(L), 4500), 900) * env(tt, .002, .05), .55)
    if s % 16 in notes: L = int(.22 * SR); tt = np.arange(L) / SR; fr = notes[s % 16]; put(bass, i0, lp(2 * ((tt * fr) % 1) - 1, 420) * env(tt, .003, .16))
pad = np.zeros(n)
for fr in (110.0, 130.81, 164.81, 220.0):
    for dt in (-.004, 0, .004): pad += (2 * ((t * fr * (1 + dt)) % 1) - 1) * .12
pad = lp(pad, 900) * (.6 + .4 * np.sin(2 * np.pi * t / (beat * 8)))
g_kick = ramp(a.kick - .1, a.kick) * (1 - ramp(OUTRO, OUTRO + 1.2) * .0)
g_bass = ramp(a.bass, a.bass + .5) * (1 - ramp(OUTRO, DUR) * .5); g_clap = ramp(a.clap, a.clap + .5); g_hat = .35 + .65 * ramp(a.kick, a.kick + .5)
sweep = ramp(0, max(a.kick, 1)) * .8 + .2
mix = kick * g_kick * .95 + bass * g_bass * .55 + (hat * g_hat + clap * g_clap) * .7 + pad * (.55 + .35 * sweep) * (1 - ramp(OUTRO, DUR) * .6)
mix = np.tanh(mix * 1.1) * np.clip(np.minimum(t / .05, (DUR - t) / 1.2), 0, 1)
wavfile.write(a.out, SR, (mix / np.max(np.abs(mix)) * .9 * 32767).astype(np.int16))
