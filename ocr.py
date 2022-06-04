import pyocr
import pyocr.builders
from PIL import Image
import re
import cv2


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
        img = make_ocr_image(img_path)
        if img is None:
            return None

        try:
            # tesseract_layoutは下記のリンクを参照
            # https://web-lh.fromation.co.jp/archives/10000061001
            result = self.tool.image_to_string(
                img,
                lang="eng",
                builder=pyocr.builders.TextBuilder(tesseract_layout=7)
            )
            print("text", result)
            try:
                return int(re.sub(r"\D", "", result))
            except ValueError:
                print("ValueError")
                return 0
        except cv2.error:
            print("cv2.error")
            return 0


def make_ocr_image(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]
    img = cv2.resize(img, (0, 0), fx=2, fy=2)

    cnts, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts) <= 1:
        return None
    margin = 3
    xmin = min([cv2.boundingRect(cnt)[0] for cnt in cnts[1:]]) - margin
    xmax = max([cv2.boundingRect(cnt)[0] + cv2.boundingRect(cnt)[2] for cnt in cnts[1:]]) + margin

    kakko_width = 12
    white = (255, 255, 255)
    cv2.rectangle(img, (xmin, 0), (xmin + kakko_width, img.shape[0]), white, -1)
    cv2.rectangle(img, (xmax - kakko_width, 0), (xmax, img.shape[0]), white, -1)

    return Image.fromarray(img)
