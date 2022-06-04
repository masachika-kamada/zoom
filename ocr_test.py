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
        # img = cv2.resize(img, (0, 0), fx=2, fy=2)

        cnts, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # margin = 3
        margin = 1
        xmin = min([cv2.boundingRect(cnt)[0] for cnt in cnts[1:]]) - margin
        xmax = max([cv2.boundingRect(cnt)[0] + cv2.boundingRect(cnt)[2] for cnt in cnts[1:]]) + margin

        # kakko_width = 12
        kakko_width = 6
        white = (255, 255, 255)
        cv2.rectangle(img, (xmin, 0), (xmin + kakko_width, img.shape[0]), white, -1)
        cv2.rectangle(img, (xmax - kakko_width, 0), (xmax, img.shape[0]), white, -1)
        cv2.imshow("img", img)
        cv2.waitKey(0)

        # img = cv2pil(img)

        try:
            result = self.tool.image_to_string(
                Image.fromarray(img),
                lang="eng",
                builder=pyocr.builders.TextBuilder(tesseract_layout=6)
            )
            print("text", result)
            return int(re.sub(r"\D", "", result))
        except cv2.error:
            print("cv2.error")
            return 0


def main():
    tesseract = Tesseract()
    res = tesseract.ocr("./joiners.png")
    print(res)


if __name__ == "__main__":
    main()
