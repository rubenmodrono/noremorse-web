# Reels · nØr3mors3

Cinco Reels verticales (1080×1920, H.264 + AAC) con locución en castellano, música original sin copyright y datos reales del motor de `next-gen-dj-set-builder`.

| # | Archivo | Día sugerido | Duración | Gancho |
|---|---|---|---|---|
| 1 | `reel1-la-curva.mp4` | 1 | 31 s | Tu set no es una lista, es una curva |
| 2 | `reel2-camelot.mp4` | 2 | 31 s | Mismo tempo no es buena mezcla (rueda Camelot) |
| 3 | `reel3-antes-y-despues.mp4` | 3 | 29 s | Mismos temas, dos sets: al azar frente a con curva |
| 4 | `reel4-dos-horas.mp4` | 4 | 35 s | Cómo repartir un set de dos horas |
| 5 | `reel5-oferta.mp4` | 7 | 29 s | Plan de Set en 24 h · 19 € · 5 plazas |

`reel1-portada.png` es la portada sugerida del Reel 1.

## Captions y hashtags

**Reel 1**
> Un set no es una lista de buenos temas. Es una curva. 🎚️ Warmup → Peak → Closing, con ruta armónica Camelot. Comenta CURVA y te cuento cómo.

**Reel 2**
> Mismo tempo no significa que suene bien. Desde 8A tienes 3 movimientos seguros: misma clave, ±1 y su relativa (8B). Guárdalo para tu próximo set. 📌

**Reel 3**
> Mismos 10 temas, dos sets. Al azar: 4 de 9 transiciones encajan. Con curva: 8 de 9. ¿Cuál pincharías? Comenta A o B.
> *(Cifras reales del motor con una colección sintética. En 500 mezclas al azar salen unas 4 de 9 de media.)*

**Reel 4**
> Cómo repartir un set de 2 horas: 30' calentamiento · 60' pico · 30' cierre. Y no subas demasiado pronto. ¿Quieres tu set así? Comenta CURVA.

**Reel 5**
> Plan de Set en 24 h: tú me cuentas género, duración y sala; yo te devuelvo la curva, la tracklist con tempo/energía/clave y, con tu colección, el archivo para importar. 19 € · 5 plazas · si no te sirve, te devuelvo el dinero. Comenta SET.

**Hashtags (todos):** `#djtips #djsets #djlife #rekordbox #mixingtips #camelotwheel #harmonicmixing #djproduction`

Publica con el **audio original** del vídeo (voz + música propia).

## Voz
La locución usa la voz "Daniel" de vidIQ. **Ninguna voz de vidIQ está marcada como español de España**: los guiones están escritos en castellano (vocabulario y giros peninsulares), pero el acento depende del modelo. Si no te convence, tienes dos salidas sin tocar los vídeos:
1. Grabar tú los 5 guiones (están en `src/reelN.json`, campo `phrases`) y sustituir `src/voice/reelN.mp3`.
2. Importar una voz nativa de España como "voz personalizada" en vidIQ y regenerar.

En ambos casos los subtítulos se re-sincronizan solos: `python src/build.py N`.

## Estructura
```
src/build.py       alinea la voz, renderiza (30 fps), sintetiza la música y monta el MP4
src/align.py       reparte el tiempo de la voz entre las frases del guion
src/music.py       música original (126 BPM, La menor / 8A)
src/common.*       estilo y utilidades comunes (marca nØr3mors3)
src/reelN.html     escena animada de cada Reel · src/reelN.json guion y arreglo musical
src/set*.json      datos reales del motor (set de 60 min, antes/después, set de 120 min)
src/voice/         locuciones
```
Requisitos: `playwright` (Chromium), `scipy`, `numpy`, `pillow`, `ffmpeg`.
