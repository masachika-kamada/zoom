import cv2


img = cv2.imread("./imgs/join.png")
print(img.shape)
h, w = img.shape[:2]
for i in range(1, 8):
    ratio = i / 4
    img_resize = cv2.resize(img, (int(w * ratio), int(h * ratio)))
    cv2.imwrite(f"./imgs/join_{i}.png", img_resize)
