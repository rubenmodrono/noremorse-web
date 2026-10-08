"""Construye un Reel: alinea la voz, renderiza la escena (30 fps), sintetiza la música y lo junta todo.
Uso:  python build.py N [--preview t1,t2,...]      N = 1..5
Salida: ../reelN-nombre.mp4  (1080x1920, H.264 + AAC)   Requiere: playwright, scipy, ffmpeg."""
import json, pathlib, subprocess, sys, shutil
from align import align, duration
HERE = pathlib.Path(__file__).parent; OUT = HERE.parent
n = sys.argv[1]; cfg = json.loads((HERE / f"reel{n}.json").read_text(encoding="utf-8"))
work = pathlib.Path("/tmp/claude-0/work") / f"reel{n}"; shutil.rmtree(work, ignore_errors=True); work.mkdir(parents=True)
voice = HERE / cfg["voice"]; vd = duration(str(voice)); total = round(vd + cfg["tail"], 2)
cues = align(str(voice), cfg["phrases"])
(HERE / f"cues{n}.js").write_text("window.CUES=%s;window.DUR=%s;" % (json.dumps([[round(a, 2), round(b, 2)] for a, b in cues]), total))
(HERE / "data.js").write_text("window.SET1=%s;window.SET3=%s;window.SET4=%s;" % tuple(json.dumps(json.loads((HERE / f).read_text())) for f in ("set.json", "set3.json", "set4.json")))
from playwright.sync_api import sync_playwright
def page(p):
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium", args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 1080, "height": 1920}); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.goto((HERE / cfg["html"]).resolve().as_uri()); pg.wait_for_timeout(500); return b, pg, errs
if "--preview" in sys.argv:
    ts = [float(x) for x in sys.argv[sys.argv.index("--preview") + 1].split(",")]
    with sync_playwright() as p:
        b, pg, errs = page(p)
        for t in ts: pg.evaluate(f"render({t})"); pg.screenshot(path=str(work / f"p{t}.png"))
        print("errores JS:", errs); b.close()
    from PIL import Image
    ims = [Image.open(work / f"p{t}.png").resize((360, 640)) for t in ts]; W = Image.new("RGB", (360 * min(4, len(ims)), 640 * ((len(ims) + 3) // 4)))
    for i, im in enumerate(ims): W.paste(im, ((i % 4) * 360, (i // 4) * 640))
    W.save(work / "sheet.png"); print(work / "sheet.png"); sys.exit()
fps = 30
with sync_playwright() as p:
    b, pg, errs = page(p)
    for f in range(int(total * fps)):
        pg.evaluate(f"render({f / fps})"); pg.screenshot(path=str(work / f"{f:05d}.jpg"), type="jpeg", quality=93)
    print("errores JS:", errs); b.close()
k, bs, cl = (cues[i][0] for i in cfg["music_cues"])
subprocess.run([sys.executable, str(HERE / "music.py"), str(work / "music.wav"), str(total), "--kick", str(k), "--bass", str(bs), "--clap", str(cl), "--seed", str(cfg["seed"])], check=True)
mp4 = OUT / f"{cfg['name']}.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(fps), "-i", str(work / "%05d.jpg"), "-i", str(voice), "-i", str(work / "music.wav"), "-filter_complex",
  f"[1:a]apad=whole_dur={total},volume=1.25,asplit=2[v1][v2];[2:a]volume=0.55[m];[m][v1]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=300[md];[v2][md]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,atrim=0:{total}[a]",
  "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(fps), "-c:a", "aac", "-b:a", "192k", "-t", str(total), "-movflags", "+faststart", str(mp4)], check=True)
print("OK", mp4, total, "s")
