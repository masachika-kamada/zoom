import cv2
import numpy as np


def features_matching(img, template):
    """特徴点対応
    templateのサイズが小さすぎると、マッチングでエラーになる
    グレースケールに変更した時に特徴点が少ないと良い結果が得られない

    Args:
        img (numpy.ndarray): 元画像
        template (numpy.ndarray): テンプレート画像

    Returns:
        point (int, int): 特徴点が一致した座標
    """
    img_g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template_g = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    template_g = cv2.resize(template_g, (100, 100))

    # 特徴点の検出
    akaze = cv2.AKAZE_create()
    kp_01, des_01 = akaze.detectAndCompute(img_g, None)
    kp_02, des_02 = akaze.detectAndCompute(template_g, None)

    # print(des_01.shape)
    # print(type(des_02))
    # print(des_02)

    # マッチング処理
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = bf.match(des_01, des_02)
    # 距離が近い＝似ている
    matches = sorted(matches, key=lambda x: x.distance)[:10]

    match_points = []
    for i in range(len(matches)):
        x, y = kp_01[matches[i].queryIdx].pt
        match_points.append(np.array([int(x), int(y)]))

    # 他の点との距離の和を求める
    distances = {}
    for i in range(len(match_points)):
        distance = 0
        for j in range(len(match_points)):
            if i == j:
                continue
            distance += np.linalg.norm(match_points[i] - match_points[j])
        distances[i] = distance

    # 距離の和が小さい順に3点を選択し、その重心を求める
    sorted_idx = sorted(distances, key=distances.get)
    dst_x = 0
    dst_y = 0
    for i in range(3):
        print(match_points[sorted_idx[i]])
        dst_x += match_points[sorted_idx[i]][0]
        dst_y += match_points[sorted_idx[i]][1]

    return int(dst_x / 3), int(dst_y / 3)


def scale_matching(img, template):
    """スケール対応
    feature_matchingよりも精度が良い

    Args:
        img (numpy.ndarray): 元画像
        template (numpy.ndarray): テンプレート画像

    Returns:
        point (int, int): 特徴点が一致した座標
    """
    img_g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template_g = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    scales = [0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4]
    max_matching_value = 0
    max_matching_point = None
    max_matching_scale = None

    for scale in scales:
        resize = cv2.resize(template_g, (0, 0), fx=scale, fy=scale)
        print(resize.shape)

        res = cv2.matchTemplate(img_g, resize, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val > max_matching_value:
            max_matching_value = max_val
            max_matching_point = max_loc
            max_matching_scale = scale

    dst_x = max_matching_point[0] + int(template_g.shape[1] * max_matching_scale / 2)
    dst_y = max_matching_point[1] + int(template_g.shape[0] * max_matching_scale / 2)

    return dst_x, dst_y


if __name__ == '__main__':
    img_paths = ["./imgs/screen.png", "./imgs/screen.png", "./imgs/screen_meeting.png", "./imgs/screen_meeting.png", "./imgs/screen_exit.png"]
    template_paths = ["./imgs/join.png", "./imgs/home.png", "./imgs/exit.png", "./imgs/joiners.png", "./imgs/exit2.png"]

    cv2.namedWindow("img", cv2.WINDOW_NORMAL)
    for img_path, template_path in zip(img_paths, template_paths):
        img = cv2.imread(img_path)
        template = cv2.imread(template_path)
        x, y = scale_matching(img, template)
        cv2.drawMarker(img, (x, y), (0, 0, 255), cv2.MARKER_CROSS, 10, 2)
        cv2.imshow("img", img)
        cv2.waitKey(0)
        # cv2.destroyAllWindows()
