"""Sukuria po atskirą kvietimą kiekvienam svečiui iš sveciai.txt į aplanką _site/."""
import html, os, re, shutil, sys, unicodedata

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "_site")

def slugify(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

template = open(os.path.join(ROOT, "template.html"), encoding="utf-8").read()
shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT)

seen = {}
for line in open(os.path.join(ROOT, "sveciai.txt"), encoding="utf-8"):
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    name, _, slug = (p.strip() for p in line.partition("|"))
    slug = slugify(slug or name)
    if not slug:
        sys.exit(f"Nepavyko sukurti nuorodos vardui: {name!r}")
    if slug in seen:
        sys.exit(f"Nuoroda '{slug}' kartojasi ({seen[slug]!r} ir {name!r}). Pridėkite '| kita-nuoroda'.")
    seen[slug] = name
    os.makedirs(os.path.join(OUT, slug))
    with open(os.path.join(OUT, slug, "index.html"), "w", encoding="utf-8") as f:
        f.write(template.replace("{{VARDAS}}", html.escape(name)))
    print(f"/{slug}/  ->  {name}")

# Pagrindinis puslapis nerodo svečių sąrašo
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(
    '<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex">'
    '<meta name="viewport" content="width=device-width,initial-scale=1"><title>Kvietimas</title>'
    '<body style="margin:0;min-height:100vh;display:grid;place-items:center;background:#f3eee5;'
    'font-family:Georgia,serif;color:#604514;letter-spacing:.15em">VIKTORIJA &amp; VIKTAS · 2027 · 07 · 20</body>')
open(os.path.join(OUT, ".nojekyll"), "w").close()
print(f"Iš viso kvietimų: {len(seen)}")
