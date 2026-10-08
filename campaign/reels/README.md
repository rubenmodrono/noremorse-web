# Reels · No Remorse

## Reel 1 · "La curva" (Día 1)

| Archivo | Qué es |
|---|---|
| `reel1-la-curva.mp4` | Reel final, 1080×1920, 25,8 s, H.264 + AAC |
| `reel1-portada.png` | Portada sugerida (elige "Añadir desde el carrete" al publicar) |
| `src/reel1.html` | Escena animada. Los datos del set (`set.json`) salen del motor real de `next-gen-dj-set-builder` |
| `src/render.py` | Renderiza la escena a fotogramas (30 fps) con Playwright |
| `src/music.py` | Música original sintetizada (126 BPM, La menor / 8A). Sin copyright |
| `src/reel1-voz.mp3` | Locución en español (vidIQ) |

**Caption para publicar:**
> Un set no es una lista de buenos temas. Es una curva. 🎚️
> Warmup → Peak → Closing, con la energía bajo control y ruta armónica Camelot.
> Comenta CURVA y te cuento cómo.

**Hashtags:** `#djtips #djsets #djlife #rekordbox #mixingtips #camelotwheel #harmonicmixing #djproduction`

**Audio:** al subirlo a Instagram, mantén el audio original del vídeo (voz + música propia).

### Regenerar
```bash
python src/music.py music.wav 26
python src/render.py frames 25.8
ffmpeg -framerate 30 -i frames/%05d.jpg -i src/reel1-voz.mp3 -i music.wav \
  -filter_complex "[1:a]apad=whole_dur=25.8,volume=1.25,asplit=2[vo1][vo2];[2:a]volume=0.55[m];[m][vo1]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=300[md];[vo2][md]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,atrim=0:25.8[a]" \
  -map 0:v -map "[a]" -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -t 25.8 reel1-la-curva.mp4
```
Los tiempos de los subtítulos están sincronizados con esta locución. Si cambias el guion, ajusta las marcas de tiempo en `cap()` y `render()` de `reel1.html`.
