import pyautogui as pgui
from gtts import gTTS
import time
# import os
import playsound
import re
from funcs import click_button, scale_matching


class Moderator:
    screen_share_img_path = "./imgs/screen_share.png"
    choice_app_img_path = "./imgs/choice_app.png"
    computer_audio_img_path = "./imgs/computer_audio.png"
    info_icon_img_path = "./imgs/info_icon.png"
    audio_file = "zoomoderator.mp3"
    share_img_path = "./imgs/share.png"

    def __init__(self, data, scale):
        self.name_list = re.split("[ 　]", data)
        self.presentation_count = 0
        self.scale = scale
        self.run_flag = True

    def run(self):
        print("=== Moderator ===")
        last_share_state = False
        while self.run_flag:
            pgui.click(x=10, y=100)
            screenshot = pgui.screenshot(region=(0, 0, 60, 100))
            # ミーティング情報のアイコンが左上にある場合画面共有していない
            x, y = scale_matching(screenshot, self.info_icon_img_path, self.scale)
            if x is None and y is None:
                print("発表者が画面共有中")
                last_share_state = True
            else:  # 画面共有なしの場合
                if last_share_state is True:
                    print("発表者が画面共有終了")
                    self.share_audio()
                    playsound.playsound(self.audio_file)
                last_share_state = False
                print("発表者が画面共有中ではない")
            time.sleep(1)
            if self.presentation_count == len(self.name_list):
                self.run_flag = False

    def share_audio(self):
        print("=== Share Audio ===")
        click_button(self.screen_share_img_path, self.scale)
        if self.presentation_count == 0:
            time.sleep(0.2)
            click_button(self.choice_app_img_path, self.scale)
            self.generate_audio_file()
            click_button(self.computer_audio_img_path, self.scale)
        else:  # 2回目以降は1回目の選択が適用されるので共有ボタンを押すだけ
            self.generate_audio_file()
            click_button(self.share_img_path, self.scale)

    def generate_audio_file(self):
        # 発表者をアナウンスする直前に呼び出して、音声ファイルを生成する
        print("=== Generate Audio File ===")
        if self.presentation_count == 0:
            text = f"最初の発表者は{self.name_list[0]}さんです。宜しくお願いします。"
        else:
            text = f"{self.name_list[self.presentation_count - 1]}さんありがとうございました。\
                      次の発表者は{self.name_list[self.presentation_count]}さんです。宜しくお願いします。"
        tts = gTTS(text=text, lang="ja", slow=False)
        tts.save(self.audio_file)
        self.presentation_count += 1
