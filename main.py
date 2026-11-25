#!/usr/bin/env python3
"""news-image-20261124: draw a newspaper front page summing up the world
news of Tuesday 24 November 2026, and write it to /output/entry.png.

Pure Python 3.13 standard library only (zlib/struct/os). No network, no
randomness, no time dependence: two runs write byte-identical output.
The image is drawn from scratch in this file; the stories below were
researched from live news sources on 25 November 2026 and all happened
or were first reported on 24 November 2026.
"""

import binascii
import os
import struct
import zlib

W, H = 1024, 1024

PAPER = (250, 247, 240)
INK = (17, 17, 17)
RED = (176, 32, 32)
BLUE = (27, 58, 107)
GREEN = (34, 120, 60)
GOLD = (198, 158, 40)
GREY = (112, 112, 106)
PANEL = (236, 232, 223)
LIGHT = (242, 239, 232)

# ---------------------------------------------------------------- font
# 5x7 bitmap font. Each glyph is 7 rows of 5 bits ('#' = on).
FONT = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "C": ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    "G": ["01110", "10001", "10000", "10111", "10001", "10001", "01111"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["01110", "00100", "00100", "00100", "00100", "00100", "01110"],
    "J": ["00111", "00010", "00010", "00010", "00010", "10010", "01100"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "Q": ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    "W": ["10001", "10001", "10001", "10101", "10101", "11011", "10001"],
    "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    "a": ["00000", "00000", "01110", "00001", "01111", "10001", "01111"],
    "b": ["10000", "10000", "11110", "10001", "10001", "10001", "11110"],
    "c": ["00000", "00000", "01110", "10000", "10000", "10001", "01110"],
    "d": ["00001", "00001", "01111", "10001", "10001", "10001", "01111"],
    "e": ["00000", "00000", "01110", "10001", "11111", "10000", "01110"],
    "f": ["00110", "01000", "01000", "11110", "01000", "01000", "01000"],
    "g": ["00000", "01111", "10001", "10001", "01111", "00001", "01110"],
    "h": ["10000", "10000", "11110", "10001", "10001", "10001", "10001"],
    "i": ["00100", "00000", "01100", "00100", "00100", "00100", "01110"],
    "j": ["00010", "00000", "00110", "00010", "00010", "00010", "01100"],
    "k": ["10000", "10000", "10010", "10100", "11000", "10100", "10010"],
    "l": ["01100", "00100", "00100", "00100", "00100", "00100", "01110"],
    "m": ["00000", "00000", "11010", "10101", "10101", "10101", "10101"],
    "n": ["00000", "00000", "11110", "10001", "10001", "10001", "10001"],
    "o": ["00000", "00000", "01110", "10001", "10001", "10001", "01110"],
    "p": ["00000", "00000", "11110", "10001", "10001", "11110", "10000"],
    "q": ["00000", "00000", "01111", "10001", "10001", "01111", "00001"],
    "r": ["00000", "00000", "10110", "11001", "10000", "10000", "10000"],
    "s": ["00000", "00000", "01111", "10000", "01110", "00001", "11110"],
    "t": ["01000", "01000", "11100", "01000", "01000", "01000", "00110"],
    "u": ["00000", "00000", "10001", "10001", "10001", "10011", "01101"],
    "v": ["00000", "00000", "10001", "10001", "10001", "01010", "00100"],
    "w": ["00000", "00000", "10001", "10101", "10101", "10101", "01010"],
    "x": ["00000", "00000", "10001", "01010", "00100", "01010", "10001"],
    "y": ["00000", "00000", "10001", "10001", "01111", "00001", "01110"],
    "z": ["00000", "00000", "11111", "00010", "00100", "01000", "11111"],
    "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00110", "01000", "10000", "11111"],
    "3": ["11111", "00010", "00100", "00010", "00001", "10001", "01110"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    "5": ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    "6": ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    "9": ["01110", "10001", "10001", "01111", "00001", "00010", "01100"],
    " ": ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
    ".": ["00000", "00000", "00000", "00000", "00000", "01100", "01100"],
    ",": ["00000", "00000", "00000", "00000", "01100", "00100", "01000"],
    ":": ["00000", "01100", "01100", "00000", "01100", "01100", "00000"],
    ";": ["00000", "01100", "01100", "00000", "01100", "00100", "01000"],
    "!": ["00100", "00100", "00100", "00100", "00100", "00000", "00100"],
    "?": ["01110", "10001", "00001", "00110", "00100", "00000", "00100"],
    "'": ["00100", "00100", "01000", "00000", "00000", "00000", "00000"],
    '"': ["01010", "01010", "00000", "00000", "00000", "00000", "00000"],
    "-": ["00000", "00000", "00000", "01110", "00000", "00000", "00000"],
    "(": ["00010", "00100", "01000", "01000", "01000", "00100", "00010"],
    ")": ["01000", "00100", "00010", "00010", "00010", "00100", "01000"],
    "/": ["00001", "00010", "00010", "00100", "01000", "01000", "10000"],
    "%": ["11001", "11010", "00010", "00100", "01000", "01011", "10011"],
    "$": ["00100", "01111", "10100", "01110", "00101", "11110", "00100"],
    "&": ["01100", "10010", "10100", "01000", "10101", "10010", "01101"],
    "+": ["00000", "00100", "00100", "11111", "00100", "00100", "00000"],
    "=": ["00000", "00000", "11111", "00000", "11111", "00000", "00000"],
    "*": ["00000", "00100", "10101", "01110", "10101", "00100", "00000"],
    "#": ["01010", "01010", "11111", "01010", "11111", "01010", "01010"],
    "@": ["01110", "10001", "10111", "10101", "10110", "10000", "01110"],
    "_": ["00000", "00000", "00000", "00000", "00000", "00000", "11111"],
}

CHAR_ADV = 6  # advance per character in font units


def text_w(s, scale):
    return len(s) * CHAR_ADV * scale


def wrap(text, max_w, scale):
    """Greedy word wrap; returns list of lines fitting max_w pixels."""
    words = text.split(" ")
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_w(trial, scale) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(w * h * 3)
        self.fill(0, 0, w, h, bg)

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = c

    def fill(self, x0, y0, x1, y1, c):
        x0 = max(0, x0)
        y0 = max(0, y0)
        x1 = min(self.w, x1)
        y1 = min(self.h, y1)
        for y in range(y0, y1):
            base = (y * self.w + x0) * 3
            for x in range(x0, x1):
                i = base + (x - x0) * 3
                self.px[i], self.px[i + 1], self.px[i + 2] = c

    def rect(self, x0, y0, x1, y1, c, t=1):
        self.fill(x0, y0, x1, y0 + t, c)
        self.fill(x0, y1 - t, x1, y1, c)
        self.fill(x0, y0, x0 + t, y1, c)
        self.fill(x1 - t, y0, x1, y1, c)

    def line(self, x0, y0, x1, y1, c, t=1):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        x, y = x0, y0
        while True:
            self.fill(x, y, x + t, y + t, c)
            if x == x1 and y == y1:
                return
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy

    def disc(self, cx, cy, r, c):
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                    self.set(x, y, c)

    def text(self, x, y, s, scale, c):
        cx = x
        for ch in s:
            g = FONT.get(ch)
            if g is None:
                ch = "?"
                g = FONT["?"]
            for row in range(7):
                bits = g[row]
                for col in range(5):
                    if bits[col] == "1":
                        self.fill(cx + col * scale, y + row * scale,
                                  cx + (col + 1) * scale,
                                  y + (row + 1) * scale, c)
            cx += CHAR_ADV * scale
        return cx

    def text_center(self, y, s, scale, c, x0=0, x1=None):
        if x1 is None:
            x1 = self.w
        w = text_w(s, scale)
        self.text(x0 + (x1 - x0 - w) // 2, y, s, scale, c)


# ---------------------------------------------------------------- icons
def icon_chip(cv, x, y, s):
    """A green computer chip with pins."""
    cv.fill(x + 8, y + 8, x + s - 8, y + s - 8, GREEN)
    cv.rect(x + 8, y + 8, x + s - 8, y + s - 8, INK, 2)
    for i in range(4):
        px = x + 14 + i * ((s - 28) // 3)
        cv.fill(px, y, px + 4, y + 8, INK)
        cv.fill(px, y + s - 8, px + 4, y + s, INK)
        py = y + 14 + i * ((s - 28) // 3)
        cv.fill(x, py, x + 8, py + 4, INK)
        cv.fill(x + s - 8, py, x + s, py + 4, INK)
    cv.fill(x + s // 2 - 14, y + s // 2 - 10, x + s // 2 + 14, y + s // 2 + 10,
            PAPER)
    cv.text(x + s // 2 - 12, y + s // 2 - 7, "AI", 2, GREEN)


def icon_burst(cv, x, y, s):
    """Explosion burst for the Gaza strike."""
    cx, cy = x + s // 2, y + s // 2
    for k in range(12):
        import math
        a = k * math.pi / 6
        r1 = s // 4
        r2 = s // 2
        cv.line(cx + int(r1 * math.cos(a)), cy + int(r1 * math.sin(a)),
                cx + int(r2 * math.cos(a)), cy + int(r2 * math.sin(a)),
                RED if k % 2 == 0 else GOLD, 3)
    cv.disc(cx, cy, s // 5, RED)
    cv.disc(cx, cy, s // 9, GOLD)


def icon_building(cv, x, y, s):
    """Apartment block with a crack, for Zaporizhzhia."""
    cv.fill(x + 12, y + 6, x + s - 12, y + s - 6, GREY)
    cv.rect(x + 12, y + 6, x + s - 12, y + s - 6, INK, 2)
    for r in range(4):
        for c in range(3):
            wx = x + 20 + c * ((s - 48) // 2)
            wy = y + 14 + r * ((s - 28) // 3)
            cv.fill(wx, wy, wx + 10, wy + 10, PAPER)
    cv.line(x + s // 2, y + 6, x + s // 2 - 8, y + s // 2, INK, 3)
    cv.line(x + s // 2 - 8, y + s // 2, x + s // 2 + 6, y + s - 6, INK, 3)


def icon_house(cv, x, y, s):
    """A country house with a roof, for Anmer Hall."""
    cv.line(x + 6, y + s // 2, x + s // 2, y + 8, INK, 4)
    cv.line(x + s // 2, y + 8, x + s - 6, y + s // 2, INK, 4)
    cv.fill(x + 14, y + s // 2, x + s - 14, y + s - 8, BLUE)
    cv.rect(x + 14, y + s // 2, x + s - 14, y + s - 8, INK, 2)
    cv.fill(x + s // 2 - 7, y + s - 30, x + s // 2 + 7, y + s - 8, GOLD)
    cv.fill(x + 22, y + s // 2 + 8, x + 34, y + s // 2 + 20, PAPER)
    cv.fill(x + s - 34, y + s // 2 + 8, x + s - 22, y + s // 2 + 20, PAPER)


def icon_tower(cv, x, y, s):
    """A tall skyscraper, for the Riyadh PIF tower."""
    cv.fill(x + s // 2 - 12, y + 4, x + s // 2 + 12, y + s - 6, BLUE)
    cv.rect(x + s // 2 - 12, y + 4, x + s // 2 + 12, y + s - 6, INK, 2)
    for r in range(5):
        wy = y + 12 + r * ((s - 24) // 4)
        cv.fill(x + s // 2 - 8, wy, x + s // 2 + 8, wy + 5, GOLD)
    cv.line(x + s // 2 - 22, y + s - 6, x + s // 2 + 22, y + s - 6, INK, 3)
    cv.disc(x + s // 2, y + s - 16, 4, RED)


def icon_bars(cv, x, y, s):
    """Rising bars, for the hacked Russian casualty data."""
    base = y + s - 10
    for i, h in enumerate((s // 4, s // 2, (3 * s) // 4)):
        bx = x + 10 + i * ((s - 20) // 3)
        cv.fill(bx, base - h, bx + 16, base, RED if i == 2 else GREY)
        cv.rect(bx, base - h, bx + 16, base, INK, 1)
    cv.line(x + 6, base, x + s - 6, base, INK, 2)


# ---------------------------------------------------------------- layout
def draw_page():
    cv = Canvas(W, H, PAPER)
    m = 28  # margin
    inner = W - 2 * m

    # ---- masthead
    cv.fill(m, 18, W - m, 20, INK)
    cv.text_center(30, "THE WORLD IN ONE DAY", 5, INK)
    cv.text_center(76, "TUESDAY, 24 NOVEMBER 2026", 2, RED)
    cv.fill(m, 104, W - m, 107, INK)
    cv.fill(m, 110, W - m, 112, INK)

    # ---- lead story: Nvidia / Huang
    ly = 126
    cv.fill(m, ly, W - m, ly + 2, INK)
    cv.text(m, ly + 12, "CHIPS  -  CALIFORNIA", 2, RED)
    cv.text(m, ly + 40, "HUANG: 'TERRIBLE MISTAKES'", 3, INK)
    icon_chip(cv, W - m - 120, ly + 12, 120)
    sub = ("A day after his return as Nvidia chief, Jensen Huang tells staff "
           "he is in therapy, as the comeback rally fades.")
    yy = ly + 82
    for ln in wrap(sub, W - m - 150 - m, 2):
        cv.text(m, yy, ln, 2, INK)
        yy += 20
    cv.fill(m, ly + 168, W - m, ly + 170, INK)

    # ---- story grid: two columns, two rows
    gx, gy = m, 312
    cw = (inner - 16) // 2
    ch = 196

    def story(x, y, w, kicker, headline, body, icon):
        cv.fill(x, y, x + w, y + ch, LIGHT)
        cv.rect(x, y, x + w, y + ch, INK, 2)
        icon(cv, x + w - 84, y + 10, 72)
        tx = x + 12
        tw = w - 100
        cv.text(tx, y + 12, kicker, 2, RED)
        hy = y + 36
        for ln in wrap(headline, tw, 3):
            cv.text(tx, hy, ln, 3, INK)
            hy += 26
        by = hy + 6
        for ln in wrap(body, tw, 2)[:3]:
            cv.text(tx, by, ln, 2, INK)
            by += 20

    story(gx, gy, cw, "GAZA",
          "ISRAELI STRIKE KILLS HAMAS SECURITY CHIEF",
          "Naeem Abu Nahal and six others die in a Gaza City strike, "
          "despite the ceasefire.", icon_burst)
    story(gx + cw + 16, gy, cw, "UKRAINE",
          "2 KILLED IN STRIKE ON ZAPORIZHZHIA FLAT",
          "A Russian overnight attack hits a flat block; 40 are wounded, "
          "four of them children.", icon_building)
    story(gx, gy + ch + 14, cw, "BRITAIN",
          "TWO HELD AFTER BREAK-IN AT WILLIAM'S HOME",
          "Masked men entered Anmer Hall in Norfolk. The Prince and "
          "Princess of Wales were away.", icon_house)
    story(gx + cw + 16, gy + ch + 14, cw, "SAUDI ARABIA",
          "RIYADH TOWER HIT TWICE IN A WEEK",
          "Saudi Arabia condemns a 'terrorist attack' on the PIF tower, "
          "home of its wealth fund.", icon_tower)

    # ---- fifth story, full width
    ry = gy + 2 * ch + 28
    cv.fill(m, ry, W - m, ry + 96, LIGHT)
    cv.rect(m, ry, W - m, ry + 96, INK, 2)
    icon_bars(cv, W - m - 110, ry + 8, 80)
    cv.text(m + 12, ry + 12, "RUSSIA  -  UKRAINE WAR", 2, RED)
    cv.text(m + 12, ry + 38, "HACKED DATA: NEARLY 500,000 RUSSIAN DEAD",
            3, INK)
    cv.text(m + 12, ry + 70,
            "Leaked Russian figures put the war's death toll close to half a million.",
            2, INK)

    # ---- also-today strip
    ay = ry + 110
    cv.fill(m, ay, W - m, ay + 2, INK)
    cv.text(m, ay + 12, "ALSO TODAY:", 2, RED)
    ticker = ("Trump gives Giuliani the Medal of Freedom  -  NATO answers "
              "reports of a nuclear-armed satellite  -  Landmine toll hits "
              "a 5-year high: 7,000  -  Seoul offers $375,000 to catch "
              "AI exam cheats")
    yy = ay + 40
    for ln in wrap(ticker, inner, 2):
        cv.text(m, yy, ln, 2, INK)
        yy += 20

    # ---- footer
    cv.fill(m, 988, W - m, 990, INK)
    cv.text_center(996, "THE WORLD IN ONE DAY  -  24 NOVEMBER 2026",
                   2, GREY)
    return cv


# ---------------------------------------------------------------- png
def png_bytes(cv):
    raw = bytearray()
    for y in range(cv.h):
        raw.append(0)  # filter: None
        raw += cv.px[y * cv.w * 3:(y + 1) * cv.w * 3]
    comp = zlib.compress(bytes(raw), 6)

    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        return out + struct.pack(">I", binascii.crc32(tag + data) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", comp) + chunk(b"IEND", b""))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    data = png_bytes(draw_page())
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as f:
        f.write(data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
