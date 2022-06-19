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
    screen_share_img_path = "./imgs/screen_share.png"
    choice_app_img_path = "./imgs/choice_app.png"
    computer_audio_img_path = "./imgs/computer_audio.png"
    info_icon_img_path = "./imgs/info_icon.png"
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
        self.set_moderator = False
        if data[0]:
            self.set_moderator = True
        self.record = False
        if data[1]:
            self.record = True

    def start(self):
        s = sched.scheduler(time.time, time.sleep)
        now = datetime.datetime.now()
        # 1分前に入室
        s.enter((self.start_time - now).total_seconds() - 60, 1, self.join_meeting)
        s.enter((self.start_time - now).total_seconds() - 20, 1, self.display_joiners_tab)
        if self.record:
            s.enter((self.start_time - now).total_seconds(), 1, record_command)
        if self.auto_exit is False:
            s.enter((self.end_time - now).total_seconds(), 1, self.exit_meeting)
        else:
            self.tesseract = Tesseract()
            s.enter((self.start_time - now).total_seconds() + 5, 1, self.watch_joiners)
        if self.set_moderator is True:
            # s.enter((self.start_time - now).total_seconds() - 10, 1, self.share_audio)
            s.enter((self.start_time - now).total_seconds(), 1, self.moderator)
        s.run()

    def join_meeting(self):
        print("=== Join Meeting ===")
        os.system("taskkill /im Zoom.exe /f")
        time.sleep(1)
        os.system(f"start {self.zoom_path}")
        time.sleep(5)
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
            save_path = "./joiners_res.png"
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

    def share_audio(self):
        print("=== Share Audio ===")
        # pgui.click(x=10, y=100)
        # time.sleep(0.2)
        click_button(self.screen_share_img_path)
        time.sleep(0.5)
        click_button(self.choice_app_img_path)
        time.sleep(0.5)
        click_button(self.computer_audio_img_path)

    def moderator(self):
        print("=== Moderator ===")
        audio_file = "test.wav"
        last_share_state = False
        while True:
            pgui.click(x=10, y=100)
            screenshot = pgui.screenshot(region=(0, 0, 60, 100))
            # ミーティング情報のアイコンが左上にある場合画面共有していない
            x, y = scale_matching(screenshot, self.info_icon_img_path)
            if x is None and y is None:
                print("発表者が画面共有中")
                last_share_state = True
            else:  # 画面共有なしの場合
                if last_share_state is True:
                    print("発表者が画面共有終了")
                    self.share_audio()
                    os.system(audio_file)
                    # break
                    exit()
                last_share_state = False
                print("発表者が画面共有中ではない")
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
        print("Matching failed", img_path)
        exit()
    pgui.doubleClick(x, y)


if __name__ == "__main__":
    zoom = Zoom()
