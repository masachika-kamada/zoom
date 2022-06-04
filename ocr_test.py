import cv2
import pyocr
import pyocr.builders
from PIL import Image
import re
import numpy as np
# from ocr import Tesseract


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
        img = Image.open(img_path)
        result = self.tool.image_to_string(
            img,
            lang="eng",
            builder=pyocr.builders.TextBuilder(tesseract_layout=6)
        )
        print("text", result)
        result = self.tool.image_to_string(
            img,
            lang="eng",
            builder=pyocr.builders.DigitBuilder()
        )
        print("num", result)
        print(re.sub(r"\D", "", result))
        result = int(re.sub(r"\D", "", result))
        return result


def main():
    # tesseract = Tesseract()
    # res = tesseract.ocr("./joiners.png")
    # print(res)
    img = cv2.imread("./joiners.png", cv2.IMREAD_GRAYSCALE)
    img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]
    img = cv2.resize(img, (0, 0), fx=2, fy=2)
    cv2.imshow("img", img)
    kernel = np.ones((3, 3), np.uint8)
    erosion = cv2.erode(img, kernel, iterations=1)

    cnts, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    margin = 3
    xmin = min([cv2.boundingRect(cnt)[0] for cnt in cnts[1:]]) - margin
    xmax = max([cv2.boundingRect(cnt)[0] + cv2.boundingRect(cnt)[2] for cnt in cnts[1:]]) + margin

    img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    cnts = cnts[1:]
    print(cnts)
    res = cv2.drawContours(img_rgb, cnts, -1, (0, 255, 0), 1)
    kakko_width = 12
    white = (255, 255, 255)
    cv2.rectangle(res, (xmin, 0), (xmin + kakko_width, img.shape[0]), white, -1)
    cv2.rectangle(res, (xmax - kakko_width, 0), (xmax, img.shape[0]), white, -1)
    cv2.drawMarker(res, (xmin, 0), (0, 0, 255), cv2.MARKER_CROSS, 10, 2)
    cv2.drawMarker(res, (xmax, 0), (0, 0, 255), cv2.MARKER_CROSS, 10, 2)

    cv2.imshow("dilation", erosion)
    cv2.imshow("res", res)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
