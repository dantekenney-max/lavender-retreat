from PIL import Image
import os

src = r"C:\Users\dante\Downloads\ChatGPT Image May 19, 2026, 06_08_00 PM.png"
out = r"C:\Users\dante\lavender-retreat\images"
os.makedirs(out, exist_ok=True)

img = Image.open(src)

# Moodboard grid: 2 cols x 7 rows on right side of 1024x1536 image
# Left col x: 537-771, Right col x: 779-1013
# Rows start at y=95, each row ~188px (image ~158px + label ~22px + gap ~8px)

lx1, lx2 = 563, 766   # left column x range (trimmed borders)
rx1, rx2 = 795, 1008  # right column x range (trimmed borders)
row_starts = [95, 283, 471, 659, 847, 1035, 1223]
img_h = 118  # image height (excluding label text at bottom)

crops = [
    ("hero_barn",        lx1, row_starts[0], lx2, row_starts[0]+img_h),
    ("hero_lavender",    rx1, row_starts[0], rx2, row_starts[0]+img_h),
    ("fountain",         lx1, row_starts[1], lx2, row_starts[1]+img_h),
    ("firepit",          rx1, row_starts[1], rx2, row_starts[1]+img_h),
    ("glamping",         lx1, row_starts[2], lx2, row_starts[2]+img_h),
    ("lavender_path",    rx1, row_starts[2], rx2, row_starts[2]+img_h),
    ("drone_view",       lx1, row_starts[3], lx2, row_starts[3]+img_h),
    ("barn_interior",    rx1, row_starts[3], rx2, row_starts[3]+img_h),
    ("romantic",         lx1, row_starts[4], lx2, row_starts[4]+img_h),
    ("womens_retreat",   rx1, row_starts[4], rx2, row_starts[4]+img_h),
    ("lavender_bloom",   lx1, row_starts[5], lx2, row_starts[5]+img_h),
    ("rock_pathway",     rx1, row_starts[5], rx2, row_starts[5]+img_h),
    ("outdoor_dining",   lx1, row_starts[6], lx2, row_starts[6]+img_h),
    ("night_lighting",   rx1, row_starts[6], rx2, row_starts[6]+img_h),
]

for name, x1, y1, x2, y2 in crops:
    crop = img.crop((x1, y1, x2, y2))
    # Upscale 3x for better quality on the web
    w, h = crop.size
    crop = crop.resize((w*3, h*3), Image.LANCZOS)
    path = os.path.join(out, f"{name}.jpg")
    crop.save(path, "JPEG", quality=90)
    print(f"Saved {name}.jpg ({w*3}x{h*3})")

print("Done!")
