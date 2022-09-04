import PySimpleGUI as sg
import sys
from zoom import Zoom


class GUI:
    font = ('Meiryo UI', 15)
    input_text_size = (2, 1)

    def __init__(self):
        sg.theme("DarkRed2")
        layout_date = [
            [self.text_temp("入室時間")],
            [self.time_input_text_temp("start_M"), self.text_temp("/"),
             self.time_input_text_temp("start_d"), self.text_temp(" "),
             self.time_input_text_temp("start_h"), self.text_temp(":"),
             self.time_input_text_temp("start_m")],
            [self.text_temp("退室時間")],
            # 退室条件を選択できるようにする: 時間 or 人数
            [self.time_input_text_temp("end_M"), self.text_temp("/"),
             self.time_input_text_temp("end_d"), self.text_temp(" "),
             self.time_input_text_temp("end_h"), self.text_temp(":"),
             self.time_input_text_temp("end_m")],
        ]
        options = [
            [sg.Checkbox("ミーティングを録画する", font=self.font, default=False)],
            [sg.Checkbox("モデレーター機能の有効化(発表順にひらがなで名前入力、スペース区切り)",
             font=self.font, default=False)],
            [sg.Multiline(font=self.font, size=(50, 2), key="name_list")]
        ]
        layout_join = [
            [self.text_temp("URL")],
            [self.info_input_text_temp(size=(70, 1), key="url")],
            [self.text_temp("ID")],
            [self.info_input_text_temp(size=(35, 1), key="id")],
            [self.text_temp("パスコード")],
            [self.info_input_text_temp(size=(35, 1), key="passcode")],
            [self.text_temp("招待リンクから参加する")],
            [sg.Multiline(font=self.font, size=(70, 5), key="link")]
        ]
        self.layout = [
            [sg.Frame("ミーティング時刻", layout_date, font=self.font, pad=[(10, 10), (10, 0)]),
             sg.Frame("オプション", options, font=self.font, pad=[(10, 10), (10, 0)])],
            [sg.Frame("ミーティング情報", layout_join, font=self.font, pad=[(10, 10), (10, 0)])],
            [sg.Button("終了", font=self.font, pad=((350, 10), (10, 10))),
             sg.Button("実行", font=self.font, pad=((80, 10), (10, 10)))]
        ]

    def time_input_text_temp(self, key):
        return sg.InputText(
            size=(2, 1),
            justification='right',
            font=self.font,
            key=key
        )

    def info_input_text_temp(self, key, size):
        return sg.InputText(
            size=size,
            font=self.font,
            key=key
        )

    def text_temp(self, text):
        return sg.Text(
            text=text,
            font=self.font
        )

    def display(self):
        window = sg.Window("Zoom自動入退室ツール", self.layout)
        while True:
            event, values = window.read()
            if event == "実行":
                zoom = Zoom(values)
                zoom.start()

            elif (event is None) or (event == "終了"):
                window.close()
                sys.exit()


if __name__ == "__main__":
    # themeの一覧
    # sg.theme_previewer()
    gui = GUI()
    gui.display()
