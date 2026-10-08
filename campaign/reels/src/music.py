"""Música original (sin copyright) para el Reel 1: 126 BPM en La menor (8A). Uso: python music.py out.wav [duracion]"""
import sys, numpy as np
from scipy.signal import butter, lfilter
from scipy.io import wavfile
SR = 44100; BPM = 126; DUR = float(sys.argv[2]) if len(sys.argv) > 2 else 26.0
rng = np.random.default_rng(7)
n = int(SR * DUR); t = np.arange(n) / SR
beat = 60 / BPM; step = beat / 4
def lp(x, f, o=2): b, a = butter(o, f / (SR / 2)); return lfilter(b, a, x)
def hp(x, f, o=2): b, a = butter(o, f / (SR / 2), 'high'); return lfilter(b, a, x)
def env(tt, a, r): return np.minimum(tt / a, 1) * np.exp(-tt / r)
def ramp(a, b): return np.clip((t - a) / (b - a), 0, 1)
kick = np.zeros(n); hat = np.zeros(n); clap = np.zeros(n); bass = np.zeros(n)
notes = {0: 55.0, 3: 55.0, 6: 65.41, 8: 55.0, 11: 82.41, 14: 65.41}   # patron de 16 pasos en A, C, E
for k in range(int(DUR / beat) + 1):
    i0 = int(k * beat * SR); L = int(0.28 * SR); tt = np.arange(L) / SR
    f = 45 + 110 * np.exp(-tt * 28); ph = 2 * np.pi * np.cumsum(f) / SR
    seg = (np.sin(ph) * env(tt, .001, .11))[: max(0, min(L, n - i0))]; kick[i0:i0 + len(seg)] += seg
for s in range(int(DUR / step) + 1):
    i0 = int(s * step * SR)
    if s % 4 == 2:  # hi-hat a contratiempo
        L = int(.05 * SR); tt = np.arange(L) / SR
        seg = (hp(rng.standard_normal(L), 7000) * env(tt, .001, .018))[: max(0, min(L, n - i0))]; hat[i0:i0 + len(seg)] += seg * .5
    if s % 2 == 1:  # hat cerrado suave
        L = int(.03 * SR); tt = np.arange(L) / SR
        seg = (hp(rng.standard_normal(L), 9000) * env(tt, .001, .008))[: max(0, min(L, n - i0))]; hat[i0:i0 + len(seg)] += seg * .22
    if s % 8 == 4:  # clap en 2 y 4
        L = int(.18 * SR); tt = np.arange(L) / SR
        seg = (hp(lp(rng.standard_normal(L), 4500), 900) * env(tt, .002, .05))[: max(0, min(L, n - i0))]; clap[i0:i0 + len(seg)] += seg * .55
    if s % 16 in notes:  # bajo
        L = int(.22 * SR); tt = np.arange(L) / SR; fr = notes[s % 16]
        saw = 2 * ((tt * fr) % 1) - 1; seg = (lp(saw, 420) * env(tt, .003, .16))[: max(0, min(L, n - i0))]; bass[i0:i0 + len(seg)] += seg
pad = np.zeros(n)
for fr in (110.0, 130.81, 164.81, 220.0):  # acorde Am
    for dt in (-.004, 0, .004):
        pad += (2 * ((t * fr * (1 + dt)) % 1) - 1) * .12
pad = lp(pad, 900) * (.6 + .4 * np.sin(2 * np.pi * t / (beat * 8)))
# arreglo: intro con pad + hat -> kick desde 4.5 -> bajo 11.3 -> clap 11.3 -> pico 16.7 -> cierre
g_kick = ramp(4.4, 4.5) * (1 - ramp(24.0, 25.4) * .0)
g_bass = ramp(11.3, 11.8); g_clap = ramp(11.3, 11.8); g_hat = .35 + .65 * ramp(4.5, 5.0)
sweep = ramp(0, 4.5) * .8 + .2                                   # apertura de filtro del pad
mix = kick * g_kick * .95 + bass * g_bass * .55 + (hat * g_hat + clap * g_clap) * .7 + pad * (.55 + .35 * sweep) * (1 - ramp(22.0, DUR) * .6)
fade = np.clip(np.minimum(t / .05, (DUR - t) / 1.2), 0, 1)
mix = np.tanh(mix * 1.1) * fade
mix = mix / np.max(np.abs(mix)) * .9
wavfile.write(sys.argv[1], SR, (mix * 32767).astype(np.int16))
