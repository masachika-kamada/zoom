import pyautogui as pgui
import time
import os
import re
from funcs import click_button, scale_matching


class Moderator:
    screen_share_img_path = "./imgs/screen_share.png"
    choice_app_img_path = "./imgs/choice_app.png"
    computer_audio_img_path = "./imgs/computer_audio.png"
    info_icon_img_path = "./imgs/info_icon.png"

    def __init__(self, data):
        self.name_list = re.split("[ 　]", data)

    def run(self):
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

    def share_audio(self):
        print("=== Share Audio ===")
        # pgui.click(x=10, y=100)
        # time.sleep(0.2)
        click_button(self.screen_share_img_path)
        time.sleep(0.5)
        click_button(self.choice_app_img_path)
        time.sleep(0.5)
        click_button(self.computer_audio_img_path)
