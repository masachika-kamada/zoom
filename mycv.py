import cv2
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
    print(matches[0].distance)
    print(matches[0].imgIdx)
    print(matches[0].queryIdx)
    print(matches[0].trainIdx)
    matches = sorted(matches, key=lambda x: x.distance)
    # print(matches[:10])
    print(kp_01[0].pt)
    mutch_image_src = cv2.drawMatches(
        color_base_src, kp_01, color_temp_src, kp_02, matches[:10], None, flags=2)

    for i in range(len(matches[:10])):
        print(
            matches[i].distance,
            matches[i].imgIdx,
            matches[i].queryIdx,
            matches[i].trainIdx)
        img_idx = matches[i].imgIdx
        query_idx = matches[i].queryIdx
        train_idx = matches[i].trainIdx
        idx = query_idx
        cv2.drawMarker(
            color_base_src, (int(
                kp_01[idx].pt[0]), int(
                kp_01[idx].pt[1])), (0, 255, 255), cv2.MARKER_CROSS, 30, 5)
        cv2.drawMarker(
            color_base_src, (int(
                kp_02[idx].pt[0]), int(
                kp_02[idx].pt[1])), (255, 0, 255), cv2.MARKER_CROSS, 30, 5)

    # 結果の表示
    cv2.imshow("mutch_image_src", color_base_src)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
