import pyocr
import pyocr.builders
from PIL import Image
import re


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
            builder=pyocr.builders.TextBuilder(tesseract_layout=8)
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
