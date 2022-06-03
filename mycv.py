import cv2
import numpy as np


def template_matching(img, template):
    img_g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template_g = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # 特徴点の検出
    type = cv2.AKAZE_create()
    kp_01, des_01 = type.detectAndCompute(img_g, None)
    kp_02, des_02 = type.detectAndCompute(template_g, None)

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


if __name__ == '__main__':
    img_path = "imgs/screen.png"
    template_path = "imgs/join.png"

    img = cv2.imread(img_path)
    template = cv2.imread(template_path)
    x, y = template_matching(img, template)
    cv2.drawMarker(img, (x, y), (0, 0, 255), cv2.MARKER_CROSS, 10, 2)
    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
