import tkinter as tk
import math
import random
import time
import sys

hearts, all_wins = [], []

tips = ['学业有成', '好好爱自己', '好好吃饭', '保持好心情',
        '身体健康', '顺顺利利', '别熬夜', '天凉了多穿衣服']

colors = ['pink', 'lightblue', 'lightgreen', 'lemonchiffon',
          'hotpink', 'skyblue']

root = None


def heart_points(n, screen_w, screen_h):
    points = []
    for i in range(n):
        t = i / n * 2 * math.pi
        x = 16 * math.sin(t) ** 3
        y = (13 * math.cos(t) - 5 * math.cos(2 * t)
             - 2 * math.cos(3 * t) - math.cos(4 * t))
        sx = int(screen_w / 2 + x * 20 - 50)
        sy = int(screen_h / 2 - y * 20 - 80)
        sx = max(0, min(sx, screen_w - 150))
        sy = max(0, min(sy, screen_h - 60))
        points.append([sx, sy])
    return points


def close_all(event=None):
    for w in hearts + all_wins:
        try:
            if isinstance(w, tk.Toplevel) and w.winfo_exists():
                w.destroy()
        except tk.TclError:
            pass
    try:
        if root is not None and root.winfo_exists():
            root.destroy()
    except tk.TclError:
        pass
    sys.exit(0)


def create_popup(x, y, tip=None):
    win = tk.Toplevel()
    win.geometry(f'150x60+{x}+{y}')
    win.title('提示')
    win.attributes('-topmost', 1)
    text = tip or random.choice(tips)
    bg = random.choice(colors)
    tk.Label(win, text=text, bg=bg, font=('微软雅黑', 14),
             width=20, height=3).pack()
    return win


def main():
    global root
    root = tk.Tk()
    root.withdraw()
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()

    # 第一步：按心形坐标依次弹出“我喜欢你”，拼成一个爱心
    points = heart_points(100, sw, sh)
    for i, (x, y) in enumerate(points):
        tip = "我喜欢你" if i == len(points) - 1 else None
        win = create_popup(x, y, tip)
        hearts.append(win)
        root.update()
        time.sleep(0.03)
    time.sleep(1)

    # 爱心保留 1 秒后清除
    for w in hearts:
        try:
            if w.winfo_exists():
                w.destroy()
        except tk.TclError:
            pass

    # 第二步：随机铺满整个屏幕的祝福弹窗
    count = (sw // 150) * (sh // 40) + 50
    for _ in range(count):
        x = random.randint(0, sw - 150)
        y = random.randint(0, sh - 60)
        win = create_popup(x, y)
        all_wins.append(win)
        root.update()
        time.sleep(0.005)

    # 保持 10 秒后，按顺序逐一关闭
    time.sleep(10)
    interval = 1.0 / len(all_wins) if all_wins else 0
    for win in all_wins:
        try:
            if win.winfo_exists():
                win.destroy()
        except tk.TclError:
            pass
        root.update()
        time.sleep(interval)

    try:
        root.destroy()
    except tk.TclError:
        pass


if __name__ == "__main__":
    main()
