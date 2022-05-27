import cv2
import pyautogui as pgui


screenshot = pgui.screenshot()
save_path = "./imgs/screen.png"
screenshot.save(save_path)
img = cv2.imread(save_path)

template = cv2.imread("./imgs/join.png")
print(template.shape)
h, w = template.shape[:2]
for i in range(1, 8):
    ratio = i / 4
    img_resize = cv2.resize(template, (int(w * ratio), int(h * ratio)))
    cv2.imwrite(f"./imgs/join_{i}.png", img_resize)
    try:
        p = pgui.locateOnScreen(f"./imgs/join_{i}.png", confidence=0.5)
        res = cv2.rectangle(
            img.copy(), (p.left, p.top), (p.left + p.width, p.top + p.height), (255, 0, 0), 5)
        cv2.imwrite(f"./imgs/res_{i}.png", res)
        print(f"./imgs/res_{i}.png")
    except Exception:
        continue


"""
結論
pyautoguiのlocateOnScreenでは画像サイズが異なると検出できない
"""
