"""Renderiza reel1.html fotograma a fotograma (30 fps) con Playwright. Uso: python render.py OUTDIR [DURACION]"""
import sys, pathlib
from playwright.sync_api import sync_playwright
out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
dur = float(sys.argv[2]) if len(sys.argv) > 2 else 25.8
FPS = 30
html = pathlib.Path(__file__).with_name("reel1.html").resolve().as_uri()
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium", args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 1080, "height": 1920}); pg.goto(html); pg.wait_for_timeout(500)
    for f in range(int(dur * FPS)):
        pg.evaluate(f"render({f / FPS})")
        pg.screenshot(path=str(out / f"{f:05d}.jpg"), type="jpeg", quality=93)
    b.close()
