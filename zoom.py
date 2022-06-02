import pyautogui as pgui
import pywinauto as pwa
import sched
import datetime
import os
import time


class Zoom:
    # zoomのpathを設定できるようにする必要がある
    # simple guiの方でフォルダを参照して検索できるようにできるとよい
    zoom_path = r"C:\Users\MK\AppData\Roaming\Zoom\bin\Zoom.exe"
    home_img_path = "./home.png"
    join_img_path = "./join.png"
    exit_img_path = "./exit.png"
    exit2_img_path = "./exit2.png"

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
        if self.record:
            s.enter((self.start_time - now).total_seconds(), 1, record_command)
        if self.auto_exit is False:
            s.enter((self.end_time - now).total_seconds(), 1, self.exit_meeting)
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
        pgui.hotkey("alt", "f")
        # TODO : カーソルを画面の端に寄せる

    def exit_meeting(self):
        print("=== Exit Meeting ===")
        pgui.hotkey("alt", "f")  # recordは画面サイズ変更時に停止する
        time.sleep(1)
        try:
            click_button(self.exit_img_path)
            time.sleep(1)
            click_button(self.exit2_img_path)
        except Exception:
            pass
        return


def record_command():
    pwa.keyboard.send_keys("{VK_LWIN down}%r{VK_LWIN up}")


def click_button(img_path):
    p = pgui.locateOnScreen(img_path, confidence=0.8)
    x, y = pgui.center(p)
    pgui.doubleClick(x, y)


if __name__ == "__main__":
    zoom = Zoom()