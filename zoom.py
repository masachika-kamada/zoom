import cv2
import pyautogui as pgui
import sched
import datetime
import os
import time
from screeninfo import get_monitors
from funcs import scale_matching, click_button, full_screen, record_command
from moderator import Moderator
from ocr import Tesseract
from concurrent.futures import ThreadPoolExecutor


class Zoom:
    # zoomのpathを設定できるようにする必要がある
    # simple guiの方でフォルダを参照して検索できるようにできるとよい
    with open("./zoom_path.txt", "r") as f:
        zoom_path = f.read()
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
            self.tesseract = Tesseract()
        else:
            self.auto_exit = False
            self.end_time = datetime.datetime(
                year=datetime.datetime.now().year,
                month=int(data["end_M"]),
                day=int(data["end_d"]),
                hour=int(data["end_h"]),
                minute=int(data["end_m"])
            )
        for m in get_monitors():
            if m.is_primary:
                self.scale = m.width / 1920  # FullHDとの比率
                break
        self.record = False
        if data[0] is True:
            self.record = True
        self.set_moderator = False
        self.run_flag = True
        if data[1] is True:
            self.set_moderator = True
            self.moderator = Moderator(data["name_list"], self.scale)

    def start(self):
        s = sched.scheduler(time.time, time.sleep)
        now = datetime.datetime.now()
        # 1分前に入室
        s.enter((self.start_time - now).total_seconds() - 60, 1, self.join_meeting)
        s.enter((self.start_time - now).total_seconds() - 20, 1, self.display_joiners_tab)
        if self.record:
            s.enter((self.start_time - now).total_seconds(), 1, record_command)
        # moderatorが設定されている場合はマルチスレッド
        if self.set_moderator is True:
            if self.auto_exit is True:
                s.enter((self.start_time - now).total_seconds(), 1, self.moderator_auto_exit)
            else:
                s.enter((self.end_time - now).total_seconds(), 1, self.moderator_time_exit)
        # moderatorがない場合は単純な設定
        else:
            if self.auto_exit is True:
                s.enter((self.start_time - now).total_seconds() + 5, 1, self.watch_joiners)
            else:
                s.enter((self.end_time - now).total_seconds(), 1, self.exit_meeting)
        s.run()

    def moderator_auto_exit(self):
        executor = ThreadPoolExecutor(max_workers=2)
        executor.submit(self.moderator.run)
        executor.submit(self.watch_joiners)
        executor.shutdown()

    def moderator_time_exit(self):
        def time_exit():
            now = datetime.datetime.now()
            time.sleep(self.end_time - now)
            self.exit_meeting()

        executor = ThreadPoolExecutor(max_workers=2)
        executor.submit(self.moderator.run)
        executor.submit(time_exit)
        executor.shutdown()

    def join_meeting(self):
        print("=== Join Meeting ===")
        os.system("taskkill /im Zoom.exe /f")
        time.sleep(1)
        os.system(f"start {self.zoom_path}")
        time.sleep(5)
        click_button(self.home_img_path, self.scale, fail_exit=False)
        time.sleep(0.5)
        click_button(self.join_img_path, self.scale)
        time.sleep(2)
        pgui.typewrite(self.ID + "\n")
        time.sleep(2)
        pgui.typewrite(self.PASSWORD + "\n")
        time.sleep(10)
        full_screen()

    def display_joiners_tab(self):
        print("=== Display Number of Joiners ===")
        pgui.click(x=10, y=100)
        click_button(self.joiners_img_path, self.scale)

    # TODO: Zoomミーティングが続いているかどうかも監視する
    def watch_joiners(self):
        screenshot = pgui.screenshot()
        x, y = scale_matching(screenshot, self.n_joiners_img_path, self.scale)
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

    def exit_meeting(self):
        print("=== Exit Meeting ===")
        pgui.click(x=10, y=100)
        try:
            click_button(self.exit_img_path, self.scale)
            time.sleep(1)
            click_button(self.exit2_img_path, self.scale)
        except Exception:
            pass
        return
