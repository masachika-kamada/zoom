import cv2
import numpy as np

if __name__ == '__main__':

    # 対象画像を指定
    base_image_path = "imgs/screen.png"
    temp_image_path = "imgs/join.png"

    # 画像をグレースケールで読み込み
    gray_base_src = cv2.imread(base_image_path, 0)
    gray_temp_src = cv2.imread(temp_image_path, 0)

    # マッチング結果書き出し準備
    # 画像をBGRカラーで読み込み
    color_base_src = cv2.imread(base_image_path, 1)
    color_temp_src = cv2.imread(temp_image_path, 1)

    # 特徴点の検出
    type = cv2.AKAZE_create()
    kp_01, des_01 = type.detectAndCompute(gray_base_src, None)
    kp_02, des_02 = type.detectAndCompute(gray_temp_src, None)

    # マッチング処理
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = bf.match(des_01, des_02)
    # 距離が近い＝似ている
    matches = sorted(matches, key=lambda x: x.distance)[:10]
    mutch_image_src = cv2.drawMatches(
        color_base_src, kp_01, color_temp_src, kp_02, matches[:10], None, flags=2)

    for i in range(len(matches)):
        print(matches[i].distance, matches[i].imgIdx, matches[i].queryIdx, matches[i].trainIdx)
        img_idx = matches[i].imgIdx
        query_idx = matches[i].queryIdx
        train_idx = matches[i].trainIdx
        idx = query_idx
        cv2.drawMarker(color_base_src, (int(kp_01[idx].pt[0]), int(kp_01[idx].pt[1])), (0, 255, 255), cv2.MARKER_CROSS, 30, 5)

    match_points = []

    for i in range(len(matches)):
        x, y = kp_01[matches[i].queryIdx].pt
        match_points.append(np.array([int(x), int(y)]))

    print(match_points)

    distances = {}

    for i in range(len(match_points)):
        distance = 0
        for j in range(len(match_points)):
            if i == j:
                continue
            distance += np.linalg.norm(match_points[i] - match_points[j])
        distances[i] = distance

    print(distances)
    print(sorted(distances, key=distances.get))

    sorted_idx = sorted(distances, key=distances.get)

    for i in range(3):
        print(match_points[sorted_idx[i]])
        cv2.drawMarker(color_base_src, tuple(match_points[sorted_idx[i]]), (0, 0, 255), cv2.MARKER_CROSS, 30, 5)
        cv2.imshow("result", color_base_src)
        cv2.waitKey(0)

    # 結果の表示
    cv2.namedWindow("result", cv2.WINDOW_NORMAL)
    cv2.imshow("result", color_base_src)

    # 結果の表示
    cv2.imshow("02_result08", mutch_image_src)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
