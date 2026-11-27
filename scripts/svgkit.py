"""Tiny SVG helper: draws text as vector paths so it looks identical everywhere."""
import json, pathlib

FONTS = json.loads((pathlib.Path(__file__).parent / "glyphs.json").read_text())

BG, PANEL, LINE = "#0A0E15", "#101723", "#1F2A3B"
INK, MUTED = "#EDF2F7", "#8493A8"
EMBER, GOLD, LEAF, SKY, VIOLET = "#FF8A3D", "#FFC857", "#7EE05A", "#58C7FF", "#BD9DFF"


class SVG:
    def __init__(self, w, h, label):
        self.w, self.h, self.label = w, h, label
        self.body, self.defs, self.glyphs, self.css = [], [], {}, []

    def add(self, s):
        self.body.append(s)

    def width(self, s, size, font="r"):
        f = FONTS[font]
        return sum(f["g"][c][0] for c in s) * size / f["upm"]

    def uses(self, s, x, y, size, font="r"):
        f = FONTS[font]
        k, pen, out = size / f["upm"], 0.0, []
        for c in s:
            adv, d = f["g"][c]
            if d:
                gid = f"{font}{ord(c)}"
                self.glyphs[gid] = d
                out.append((gid, f"translate({x + pen:.2f} {y:.2f}) scale({k:.5f} {-k:.5f})"))
            pen += adv * k
        return out

    def text(self, s, x, y, size, fill=INK, font="r", anchor="start"):
        w = self.width(s, size, font)
        x -= w / 2 if anchor == "middle" else w if anchor == "end" else 0
        inner = "".join(f'<use href="#{g}" transform="{t}"/>' for g, t in self.uses(s, x, y, size, font))
        self.add(f'<g fill="{fill}">{inner}</g>')
        return w

    def panel(self, x=0, y=0, w=None, h=None, r=22, fill=BG, stroke=LINE):
        w, h = w or self.w, h or self.h
        self.add(f'<rect x="{x+.75}" y="{y+.75}" width="{w-1.5}" height="{h-1.5}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')

    def save(self, path):
        glyphs = "".join(f'<path id="{i}" d="{d}"/>' for i, d in self.glyphs.items())
        css = "".join(self.css)
        if css:
            css = f"<style>{css}@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>"
        pathlib.Path(path).write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" height="{self.h}" role="img" aria-label="{self.label}">'
            f'<title>{self.label}</title>{css}<defs>{glyphs}{"".join(self.defs)}</defs>{"".join(self.body)}</svg>', encoding="utf-8")
