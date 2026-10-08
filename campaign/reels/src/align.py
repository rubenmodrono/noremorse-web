"""Alinea frases del guion con la locución: reparte el tiempo hablado (sin silencios) según los caracteres de cada frase.
Uso: python align.py voz.mp3 "frase 1|frase 2|..."   → imprime inicio/fin de cada frase en segundos."""
import re, subprocess, sys

def silences(path):
    out = subprocess.run(["ffmpeg", "-i", path, "-af", "silencedetect=noise=-35dB:d=0.2", "-f", "null", "-"], capture_output=True, text=True).stderr
    v = [float(x) for x in re.findall(r"silence_(?:start|end): ([0-9.]+)", out)]
    return list(zip(v[0::2], v[1::2]))

def duration(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path], capture_output=True, text=True).stdout)

def align(path, phrases):
    D = duration(path); sil = silences(path)
    speech, t = [], 0.0
    for a, b in sil:
        if a > t: speech.append((t, a))
        t = b
    if t < D: speech.append((t, D))
    total = sum(b - a for a, b in speech)
    w = [len(p) for p in phrases]; W = sum(w); cuts = [0.0]
    for x in w: cuts.append(cuts[-1] + x / W * total)
    def real(s):  # tiempo hablado acumulado -> tiempo real
        acc = 0.0
        for a, b in speech:
            if s <= acc + (b - a): return a + (s - acc)
            acc += b - a
        return D
    ends = [b for _, b in sil]
    starts = [0.0]
    for c in cuts[1:-1]:                       # ajusta cada inicio de frase a la pausa real más cercana
        r = real(c); near = min(ends, key=lambda e: abs(e - r), default=r)
        starts.append(near if abs(near - r) < 0.9 else r)
    starts.append(D)
    return [(starts[i], starts[i + 1]) for i in range(len(phrases))]

if __name__ == "__main__":
    ph = sys.argv[2].split("|")
    for p, (a, b) in zip(ph, align(sys.argv[1], ph)): print(f"{a:6.2f} {b:6.2f}  {p}")
