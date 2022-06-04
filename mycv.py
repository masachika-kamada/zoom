import cv2
import numpy as np


def scale_matching(img, template_path):
    """スケール対応
    feature_matchingよりも精度が良い

    Args:
        img (PIL.Image.Image): スクリーンショット
        template_path (path): テンプレート画像のパス

    Returns:
        point (int, int): 特徴点が一致した座標
    """
    img = pil2cv(img)
    img_g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

    scales = [0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4]
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

    dst_x = max_matching_point[0] + int(template.shape[1] * max_matching_scale / 2)
    dst_y = max_matching_point[1] + int(template.shape[0] * max_matching_scale / 2)

    return dst_x, dst_y


def pil2cv(img):
    img = np.array(img, dtype=np.uint8)
    return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)


if __name__ == "__main__":
    img_paths = ["./imgs/screen.png", "./imgs/screen.png", "./imgs/screen_meeting.png", "./imgs/screen_meeting.png", "./imgs/screen_exit.png"]
    template_paths = ["./imgs/join.png", "./imgs/home.png", "./imgs/exit.png", "./imgs/joiners.png", "./imgs/exit2.png"]

    cv2.namedWindow("img", cv2.WINDOW_NORMAL)

    scales = [0.75, 0.86, 0.93, 1.05, 1.18, 1.23]
    for img_path, template_path in zip(img_paths, template_paths):
        img = cv2.imread(img_path)
        template = cv2.imread(template_path)
        for scale in scales:
            img_resize = cv2.resize(img, (0, 0), fx=scale, fy=scale)
            x, y = scale_matching(img_resize, template)
            cv2.drawMarker(img_resize, (x, y), (0, 0, 255), cv2.MARKER_CROSS, 10, 2)
            cv2.imshow("img", img_resize)
            cv2.waitKey(0)
            # cv2.destroyAllWindows()
