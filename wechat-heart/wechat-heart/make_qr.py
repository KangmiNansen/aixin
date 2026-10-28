# -*- coding: utf-8 -*-
"""生成微信可扫描的二维码与「扫码卡片」海报。

用法:
    python make_qr.py "https://你的网址"

产物（保存在本目录）:
    二维码.png    —— 纯二维码，微信「扫一扫」可直接识别
    扫码卡片.png  —— 带标题的二维码海报，适合转发，长按图片也能识别
"""
import os
import sys
import urllib.parse
import urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))

# 优先使用项目自带库（.qrlib 目录），保证离线可用
_QR_LIB = os.path.join(BASE, ".qrlib")
if os.path.isdir(_QR_LIB):
    sys.path.insert(0, _QR_LIB)

URL = (sys.argv[1] if len(sys.argv) > 1 else "").strip()
if not URL.startswith(("http://", "https://")):
    print('用法: python make_qr.py "https://你的网址"')
    sys.exit(1)

QR_PATH = os.path.join(BASE, "二维码.png")
POSTER_PATH = os.path.join(BASE, "扫码卡片.png")


def fetch_qr():
    """本地没有 qrcode 库时，用公开二维码接口生成。"""
    api = ("https://api.qrserver.com/v1/create-qr-code/?size=640x640&margin=10&data="
           + urllib.parse.quote(URL))
    req = urllib.request.Request(api, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r, open(QR_PATH, "wb") as f:
        f.write(r.read())


# 1. 生成二维码：优先本地 qrcode 库，否则联网接口
try:
    import qrcode  # noqa: F401
    img = qrcode.make(URL)
    img = img.convert("RGB").resize((640, 640))
    img.save(QR_PATH)
except ImportError:
    fetch_qr()
print("二维码已生成:", QR_PATH)

# 2. 生成扫码卡片海报（需要 Pillow）
try:
    from PIL import Image, ImageDraw, ImageFont

    qr = Image.open(QR_PATH).convert("RGB").resize((560, 560))
    W, H = 900, 1180
    card = Image.new("RGB", (W, H), "#FFF6FA")
    d = ImageDraw.Draw(card)

    def font(size):
        for path in ("C:/Windows/Fonts/msyh.ttc", "C:/Windows/Fonts/simhei.ttf"):
            if os.path.exists(path):
                return ImageFont.truetype(path, size)
        return ImageFont.load_default()

    f_big, f_mid, f_small = font(64), font(34), font(26)

    # 顶部与底部装饰
    d.ellipse([-80, -80, 320, 320], fill="#FFD6E7")
    d.ellipse([W - 300, -120, W + 120, 300], fill="#DCE9FF")
    d.ellipse([-60, H - 140, 300, H + 120], fill="#FFD6E7")
    d.ellipse([W - 320, H - 200, W + 60, H + 100], fill="#DCE9FF")

    d.text((W / 2, 150), "有份小惊喜", font=f_big, fill="#E0568F", anchor="mm")
    d.text((W / 2, 240), "用微信「扫一扫」打开", font=f_mid, fill="#888888", anchor="mm")

    box = ((W - 600) // 2, 300, (W - 600) // 2 + 600, 900)
    d.rectangle(box, outline="#F3C6DA", width=4)
    card.paste(qr, ((W - 560) // 2, 320))

    short = URL if len(URL) <= 52 else URL[:49] + "…"
    d.text((W / 2, 980), short, font=f_small, fill="#B9B9B9", anchor="mm")
    d.text((W / 2, 1060), "长按图片也可识别 · 点开始运行", font=f_small, fill="#B9B9B9", anchor="mm")

    card.save(POSTER_PATH)
    print("扫码卡片已生成:", POSTER_PATH)
except ImportError:
    print("提示: 未安装 Pillow，已跳过海报生成（二维码可直接使用）")
