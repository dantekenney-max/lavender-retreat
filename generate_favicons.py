"""One-shot script: render the SVG favicon to PNG/ICO/apple-touch-icon at multiple sizes."""
from PIL import Image, ImageDraw
from pathlib import Path

ROOT = Path(__file__).parent

# Brand palette
BG = (74, 53, 114, 255)        # --lavender-dark
STEM = (143, 177, 122, 255)    # sage green
BUD_DEEP = (123, 91, 168, 255) # mid-deep
BUD_MID = (155, 126, 200, 255) # --lavender
BUD_LIGHT = (212, 197, 232, 255) # --lavender-light
BUD_TIP = (245, 240, 250, 255) # --lavender-pale


def draw_sprig(size: int) -> Image.Image:
    """Render a lavender-sprig icon at `size`x`size`. Supersample 4x for smoothness."""
    s = size * 4
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Background circle
    d.ellipse((0, 0, s, s), fill=BG)

    def scale(coord):
        return tuple(int(c * s / 64) for c in coord)

    def circle(cx, cy, r, fill):
        cx, cy, r = cx * s / 64, cy * s / 64, r * s / 64
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fill)

    # Leaves (rotated ellipses): rasterize on small canvas then paste
    def leaf(cx, cy, rx, ry, angle):
        leaf_img = Image.new("RGBA", (int(rx * 2 * s / 64) + 4, int(ry * 2 * s / 64) + 4), (0, 0, 0, 0))
        ld = ImageDraw.Draw(leaf_img)
        ld.ellipse((2, 2, leaf_img.width - 2, leaf_img.height - 2), fill=STEM)
        leaf_rot = leaf_img.rotate(angle, expand=True, resample=Image.BICUBIC)
        px = int(cx * s / 64 - leaf_rot.width / 2)
        py = int(cy * s / 64 - leaf_rot.height / 2)
        img.paste(leaf_rot, (px, py), leaf_rot)

    leaf(22, 40, 6, 2.6, 35)
    leaf(42, 40, 6, 2.6, -35)

    # Stem
    stem_w = int(3 * s / 64)
    d.line((int(32 * s / 64), int(56 * s / 64), int(32 * s / 64), int(26 * s / 64)),
           fill=STEM, width=stem_w)

    # Bud cluster (bottom to top, getting paler/smaller)
    circle(28, 28, 3.4, BUD_DEEP)
    circle(36, 28, 3.4, BUD_DEEP)
    circle(26, 21, 3.4, BUD_MID)
    circle(32, 20, 3.4, BUD_MID)
    circle(38, 21, 3.4, BUD_MID)
    circle(28, 14, 3, BUD_LIGHT)
    circle(36, 14, 3, BUD_LIGHT)
    circle(32, 9, 2.6, BUD_TIP)

    return img.resize((size, size), Image.LANCZOS)


# Apple touch icon — large, no transparency
apple = draw_sprig(180)
apple_rgb = Image.new("RGB", apple.size, (74, 53, 114))
apple_rgb.paste(apple, mask=apple.split()[3])
apple_rgb.save(ROOT / "apple-touch-icon.png", "PNG")
print(f"Wrote apple-touch-icon.png ({apple_rgb.size})")

# Multi-resolution ICO
sizes = [16, 24, 32, 48, 64]
imgs = [draw_sprig(sz) for sz in sizes]
imgs[0].save(ROOT / "favicon.ico", format="ICO", sizes=[(sz, sz) for sz in sizes], append_images=imgs[1:])
print(f"Wrote favicon.ico (sizes: {sizes})")

# Also write 32x32 PNG for browsers that prefer PNG
imgs[2].save(ROOT / "favicon-32x32.png", "PNG")
imgs[0].save(ROOT / "favicon-16x16.png", "PNG")
print("Wrote favicon-16x16.png and favicon-32x32.png")
