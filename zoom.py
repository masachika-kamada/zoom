import cv2
import pyautogui as pgui
import pywinauto as pwa
import sched
import datetime
import os
import time
from mycv import scale_matching
from ocr import Tesseract


class Zoom:
    # zoomのpathを設定できるようにする必要がある
    # simple guiの方でフォルダを参照して検索できるようにできるとよい
    zoom_path = r"C:\Users\MK\AppData\Roaming\Zoom\bin\Zoom.exe"
    home_img_path = "./imgs/home.png"
    join_img_path = "./imgs/join.png"
    joiners_img_path = "./imgs/joiners.png"
    n_joiners_img_path = "./imgs/n_joiners.png"
    exit_img_path = "./imgs/exit.png"
    exit2_img_path = "./imgs/exit2.png"

    def __init__(self, data):
        if data["link"] is not None:
            for item in data["link"].split("\n"):
                if "https" in item:
                    data["url"] = item
        if data["url"] is not None:
            info = data["url"].split("?pwd=")
            self.ID = info[0].split("/")[-1]
            self.PASSWORD = info[-1]
        else:
            self.ID = data["id"].replace(" ", "")
            self.PASSWORD = data["password"]
        if data["start_M"] == "":
            self.start_time = datetime.datetime.now()
        else:
            self.start_time = datetime.datetime(
                year=datetime.datetime.now().year,
                month=int(data["start_M"]),
                day=int(data["start_d"]),
                hour=int(data["start_h"]),
                minute=int(data["start_m"])
            )
        if data["end_M"] == "":
            self.auto_exit = True
        else:
            self.auto_exit = False
            self.end_time = datetime.datetime(
                year=datetime.datetime.now().year,
                month=int(data["end_M"]),
                day=int(data["end_d"]),
                hour=int(data["end_h"]),
                minute=int(data["end_m"])
            )
        self.record = False
        if data[0]:
            self.record = True

    def start(self):
        s = sched.scheduler(time.time, time.sleep)
        now = datetime.datetime.now()
        # 1分前に入室
        s.enter((self.start_time - now).total_seconds() - 60, 1, self.join_meeting)
        s.enter((self.start_time - now).total_seconds() - 10, 1, self.display_joiners_tab)
        if self.record:
            s.enter((self.start_time - now).total_seconds(), 1, record_command)
        if self.auto_exit is False:
            s.enter((self.end_time - now).total_seconds(), 1, self.exit_meeting)
        else:
            # TODO : 参加者の数に応じて自動退室
            self.tesseract = Tesseract()
            s.enter((self.start_time - now).total_seconds() + 5, 1, self.watch_joiners)
            # s.enter((self.start_time - now).total_seconds() + 10, 1, self.exit_meeting)
        s.run()

    def join_meeting(self):
        print("=== Join Meeting ===")
        os.system(f"start {self.zoom_path}")
        time.sleep(3)
        try:
            click_button(self.home_img_path)
        except Exception:
            pass
        time.sleep(2)
        click_button(self.join_img_path)
        time.sleep(2)
        pgui.typewrite(self.ID + "\n")
        time.sleep(2)
        pgui.typewrite(self.PASSWORD + "\n")
        time.sleep(10)
        full_screen()
        # pgui.hotkey("alt", "f")  # full screenにすると参加者を表示できないので
        # TODO : カーソルを画面の端に寄せる
        # カーソルが録画時に映らないように設定できたので必要ないかも

    def display_joiners_tab(self):
        print("=== Display Number of Joiners ===")
        pgui.click(x=10, y=100)
        click_button(self.joiners_img_path)

    def watch_joiners(self):
        screenshot = pgui.screenshot()
        x, y = scale_matching(screenshot, self.n_joiners_img_path)
        h, w = cv2.imread(self.n_joiners_img_path).shape[:2]
        xmin = x + int(w / 2)
        ymin = y - int(h / 2)
        max_joiners = 0
        while True:
            # region=(左上のx座標, 左上のy座標, xの長さ, yの長さ)
            joiners_ocr_img = pgui.screenshot(region=(xmin, ymin, 50, h))
            save_path = "./joiners.png"
            joiners_ocr_img.save(save_path)
            res = self.tesseract.ocr(save_path)
            print(f"tesseract read : {res}")
            # if max_joiners / 2 >= res:
            if res is None or max_joiners - 1 >= res:
                self.exit_meeting()
                break
            elif max_joiners < res:
                max_joiners = res
            time.sleep(1)

    def exit_meeting(self):
        print("=== Exit Meeting ===")
        pgui.click(x=10, y=100)
        try:
            click_button(self.exit_img_path)
            time.sleep(1)
            click_button(self.exit2_img_path)
        except Exception:
            pass
        return


def record_command():
    pwa.keyboard.send_keys("{VK_LWIN down}%r{VK_LWIN up}")


def full_screen():
    pwa.keyboard.send_keys("{VK_LWIN down}{VK_UP}{VK_LWIN up}")


def click_button(img_path):
    screenshot = pgui.screenshot()
    x, y = scale_matching(screenshot, img_path)
    if x is None or y is None:
        print("Matching failed")
        exit()
    pgui.doubleClick(x, y)


if __name__ == "__main__":
    zoom = Zoom()
