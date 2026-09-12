# -*- coding: utf-8 -*-
"""Foregrounds adaptatifs plein-bleed + XML anydpi."""
import struct, zlib, os

def png(w, h, px):
    raw = b''.join(b'\x00' + bytes(px[y * w:(y + 1) * w]) for y in range(h))
    def chunk(t, d):
        c = t + d
        return struct.pack('>I', len(d)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
    ihdr = struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0)
    return b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr) + chunk(b'IDAT', zlib.compress(bytes(raw), 9)) + chunk(b'IEND', b'')

def flat(px):
    o = []
    for p in px:
        o += list(p)
    return o

def vgrad3(w, h, c1, c2, c3):
    px = []
    for y in range(h):
        t = y / (h - 1)
        if t < 0.5:
            u, a, b = t * 2, c1, c2
        else:
            u, a, b = (t - 0.5) * 2, c2, c3
        px.append(tuple(int(a[i] + (b[i] - a[i]) * u) for i in range(3)) + (255,))
    return [p for row in [[q] * w for q in px] for p in row]

def rect(buf, W, H, x0, y0, x1, y1, col):
    for y in range(max(0, y0), min(H, y1)):
        for x in range(max(0, x0), min(W, x1)):
            buf[y * W + x] = col

def poly(buf, W, H, pts, col):
    ys = sorted(set(p[1] for p in pts))
    for y in range(max(0, min(ys)), min(H, max(ys) + 1)):
        xs = []
        n = len(pts)
        for i in range(n):
            x1, y1 = pts[i]
            x2, y2 = pts[(i + 1) % n]
            if (y1 <= y < y2) or (y2 <= y < y1):
                xs.append(int(x1 + (y - y1) * (x2 - x1) / (y2 - y1)))
        xs.sort()
        for i in range(0, len(xs) - 1, 2):
            for x in range(max(0, xs[i]), min(W, xs[i + 1] + 1)):
                buf[y * W + x] = col

FONT = {'3': ["01110","00010","00010","01110","00010","00010","01110"],
        'A': ["01110","10001","10001","11111","10001","10001","10001"],
        'S': ["01111","10000","10000","01110","00001","00001","11110"],
        'L': ["10000","10000","10000","10000","10000","10000","11111"],
        'G': ["01110","10001","10000","10111","10001","10001","01111"],
        'D': ["11100","10010","10001","10001","10001","10010","11100"],
        'M': ["10001","11011","10101","10101","10001","10001","10001"],
        'I': ["01110","00100","00100","00100","00100","00100","01110"],
        'N': ["10001","11001","10101","10011","10001","10001","10001"]}

def text(buf, W, H, s, cx, y, sc, col, shadow=None):
    tot = (sum(5 for _ in s) + 1 * (len(s) - 1)) * sc
    xi = int(cx - tot / 2)
    for ch in s:
        for r, row in enumerate(FONT[ch]):
            for c in range(5):
                if row[c] == '1':
                    xx, yy = xi + c * sc, y + r * sc
                    if shadow:
                        rect(buf, W, H, xx + 4, yy + 4, xx + sc + 4, yy + sc + 4, shadow)
                    rect(buf, W, H, xx, yy, xx + sc, yy + sc, col)
        xi += 6 * sc

def school(buf, W, H, dy=0):
    bx0, bx1, by0, by1 = 136, 376, 262 + dy, 420 + dy
    rect(buf, W, H, bx0, by0, bx1, by1, (255, 255, 255, 255))
    poly(buf, W, H, [(110, by0), (402, by0), (256, 180 + dy)], (251, 191, 36, 255))
    poly(buf, W, H, [(140, by0), (372, by0), (256, 204 + dy)], (15, 23, 42, 255))
    rect(buf, W, H, 238, by1 - 80, 274, by1, (251, 191, 36, 255))
    for wx in (162, 222, 302):
        for wy in (by0 + 26, by0 + 76):
            rect(buf, W, H, wx, wy, wx + 38, wy + 34, (147, 197, 253, 255))

def downscale(buf, W, H, w, h):
    out, sx, sy = [], W / w, H / h
    for y in range(h):
        for x in range(w):
            rs = gs = bs = n = 0
            for yy in range(int(y * sy), int((y + 1) * sy)):
                for xx in range(int(x * sx), int((x + 1) * sx)):
                    p = buf[yy * W + xx]
                    rs += p[0]; gs += p[1]; bs += p[2]; n += 1
            out.append((rs // n, gs // n, bs // n, 255))
    return out

def build(kind):
    W = H = 512
    buf = vgrad3(W, H, (37, 99, 235), (124, 58, 237), (76, 29, 149))
    if kind == 'eleve':
        text(buf, W, H, '3AS', W // 2, 120, 15, (255, 255, 255, 255), (20, 10, 60, 120))
        text(buf, W, H, 'LG', W // 2, 270, 12, (253, 224, 71, 255), (20, 10, 60, 120))
        rect(buf, W, H, 176, 392, 336, 404, (253, 224, 71, 255))
    else:
        text(buf, W, H, 'ADMIN', W // 2, 84, 10, (255, 255, 255, 255), (20, 10, 60, 120))
        school(buf, W, H, dy=10)
    return buf

SIZES = {'mipmap-mdpi': 48, 'mipmap-hdpi': 72, 'mipmap-xhdpi': 96,
         'mipmap-xxhdpi': 144, 'mipmap-xxxhdpi': 192}
for kind in ('eleve', 'admin'):
    base = build(kind)
    for d, s in SIZES.items():
        pp = f'/root/3as-lg-apps/android/{kind}/src/main/res/{d}/ic_launcher_foreground.png'
        small = downscale(base, 512, 512, s, s)
        open(pp, 'wb').write(bytes(png(s, s, flat(small))))
    print(kind, 'foregrounds done')
