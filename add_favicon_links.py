"""One-shot: inject favicon <link> tags after the viewport meta in every HTML file."""
from pathlib import Path

ROOT = Path(__file__).parent
INJECT = """  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
  <link rel="shortcut icon" href="/favicon.ico">
"""
MARKER = '<meta name="viewport"'

skipped = []
done = []
for html in ROOT.glob("*.html"):
    text = html.read_text(encoding="utf-8")
    if 'rel="icon"' in text or 'rel="shortcut icon"' in text:
        skipped.append(f"{html.name} (already has favicon)")
        continue
    lines = text.splitlines(keepends=True)
    new_lines = []
    inserted = False
    for line in lines:
        new_lines.append(line)
        if not inserted and MARKER in line:
            new_lines.append(INJECT)
            inserted = True
    if not inserted:
        skipped.append(f"{html.name} (no viewport meta)")
        continue
    html.write_text("".join(new_lines), encoding="utf-8")
    done.append(html.name)

print(f"Updated {len(done)} files:")
for n in done:
    print(f"  + {n}")
if skipped:
    print(f"\nSkipped {len(skipped)}:")
    for n in skipped:
        print(f"  - {n}")
