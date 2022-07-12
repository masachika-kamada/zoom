import pyautogui as pgui
import pywinauto as pwa
import cv2
import numpy as np


def record_command():
    pwa.keyboard.send_keys("{VK_LWIN down}%r{VK_LWIN up}")


def full_screen():
    pwa.keyboard.send_keys("{VK_LWIN down}{VK_UP}{VK_LWIN up}")


def click_button(img_path, scale, fail_exit=True):
    screenshot = pgui.screenshot()
    x, y = scale_matching(screenshot, img_path, scale)
    if x is None or y is None:
        print("Matching failed", img_path)
        if fail_exit:
            exit()
    else:
        pgui.doubleClick(x, y)


def scale_matching(img, template_path, scale, matching_threshold=0.7):
    """スケール対応
    feature_matchingよりも精度が良い

    Args:
        img (PIL.Image.Image): スクリーンショット
        template_path (path): テンプレート画像のパス
        matching_threshold (float): 信頼度の閾値

    Returns:
        point (int, int): 特徴点が一致した座標
    """
    img = pil2cv(img)
    img_g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

    scales = scale + np.arange(-0.2, 0.3, 0.1)  # -0.2 ~ +0.2
    max_matching_value = 0
    max_matching_point = None
    max_matching_scale = None

    for scale in scales:
        resize = cv2.resize(template, (0, 0), fx=scale, fy=scale)

        res = cv2.matchTemplate(img_g, resize, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val > max_matching_value:
            max_matching_value = max_val
            max_matching_point = max_loc
            max_matching_scale = scale

    if max_matching_value < matching_threshold:
        print(max_matching_value)
        return None, None

    dst_x = max_matching_point[0] + int(template.shape[1] * max_matching_scale / 2)
    dst_y = max_matching_point[1] + int(template.shape[0] * max_matching_scale / 2)

    return dst_x, dst_y


def pil2cv(img):
    img = np.array(img, dtype=np.uint8)
    return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)


if __name__ == "__main__":
    from PIL import Image
    img_path = "./test_img/img3.png"
    template_path = "./imgs/join.png"

    cv2.namedWindow("img", cv2.WINDOW_NORMAL)
    img = Image.open(img_path)
    x, y = scale_matching(img, template_path, 1800 / 1080)
    img = pil2cv(img)
    print(x, y)
    if x is not None:
        cv2.drawMarker(img, (x, y), (0, 0, 255), cv2.MARKER_CROSS, 30, 10)
    img = cv2.resize(img, (1920, 1080))
    cv2.imshow("img", img)
    cv2.waitKey(0)
