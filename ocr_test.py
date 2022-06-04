import cv2
import pyocr
import pyocr.builders
from PIL import Image
import re
# from ocr import Tesseract


def cv2pil(image):
    ''' OpenCV型 -> PIL型 '''
    new_image = image.copy()
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGRA2RGBA)
    new_image = Image.fromarray(new_image)
    return new_image


class Tesseract:
    def __init__(self):
        pyocr.tesseract.TESSERACT_CMD = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
        self.tool = pyocr.get_available_tools()[0]

    def ocr(self, img_path):
        """tesseractでOCR

        Args:
            img_path (str): 画像のパス
        Returns:
            result (int): OCR結果
        """
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]
        img = cv2.resize(img, (0, 0), fx=2, fy=2)

        cnts, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        margin = 3
        xmin = min([cv2.boundingRect(cnt)[0] for cnt in cnts[1:]]) - margin
        xmax = max([cv2.boundingRect(cnt)[0] + cv2.boundingRect(cnt)[2] for cnt in cnts[1:]]) + margin

        kakko_width = 12
        white = (255, 255, 255)
        cv2.rectangle(img, (xmin, 0), (xmin + kakko_width, img.shape[0]), white, -1)
        cv2.rectangle(img, (xmax - kakko_width, 0), (xmax, img.shape[0]), white, -1)
        cv2.imshow("img", img)
        # cv2.waitKey(0)

        # img = cv2pil(img)

        try:
            # tesseract_layoutは下記のリンクを参照
            # https://web-lh.fromation.co.jp/archives/10000061001
            result = self.tool.image_to_string(
                Image.fromarray(img),
                lang="eng",
                builder=pyocr.builders.TextBuilder(tesseract_layout=7)
            )
            print("text", result)
            try:
                return int(re.sub(r"\D", "", result))
            except ValueError:
                cv2.waitKey(0)
                return 0
        except cv2.error:
            print("cv2.error")
            return 0


def movie():
    from mycv import scale_matching
    capture = cv2.VideoCapture("./movies/geek-camp_trim.mp4")
    save_path = "./joiners.png"
    tesseract = Tesseract()
    x, y = 0, 0
    first = True
    time = 0
    h, w = cv2.imread("./imgs/n_joiners.png").shape[:2]
    while(True):
        ret, frame = capture.read()
        if not ret:
            break
        if time < 4:
            time += 1
            continue
        elif time == 4:
            time = 0

        if first is True:
            x, y = scale_matching(cv2pil(frame), "./imgs/n_joiners.png")
            xmin = x + int(w / 2)
            ymin = y - int(h / 2)
            first = False
        dst = frame[ymin:ymin + h, xmin:xmin + 50]
        cv2.imwrite(save_path, dst)
        res = tesseract.ocr(save_path)
        print(res)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()


def one_shot():
    tesseract = Tesseract()
    res = tesseract.ocr("./joiners.png")
    print(res)


if __name__ == "__main__":
    movie()
    # one_shot()
