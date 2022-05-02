import PySimpleGUI as sg


class GUI:
    font = ('Meiryo UI', 15)
    input_text_size = (2, 1)

    def __init__(self):
        sg.theme("DarkRed2")
        layout_date = [
            [self.text_temp("入室時間")],
            [self.input_text_temp("start_M", self.input_text_size), self.text_temp("/"),
             self.input_text_temp("start_d", self.input_text_size), self.text_temp(" "),
             self.input_text_temp("start_h", self.input_text_size), self.text_temp(":"),
             self.input_text_temp("start_m", self.input_text_size)],
            [self.text_temp("退室時間")],
            # 退室条件を選択できるようにする: 時間 or 人数
            [self.input_text_temp("end_M", self.input_text_size), self.text_temp("/"),
             self.input_text_temp("end_d", self.input_text_size), self.text_temp(" "),
             self.input_text_temp("end_h", self.input_text_size), self.text_temp(":"),
             self.input_text_temp("end_m", self.input_text_size)],
        ]
        layout_join = [
            [self.text_temp("URL")],
            [self.input_text_temp(size=(70, 1), key="url")],
            [self.text_temp("ID(スペースキー不要)")],
            [self.input_text_temp(size=(35, 1), key="id")],
            [self.text_temp("パスワード(あれば)")],
            [self.input_text_temp(size=(35, 1), key="password")],
            [self.text_temp("招待リンクから参加する")],
            [sg.Multiline(font=self.font, size=(70, 5), key="link")]
        ]
        self.layout = [
            [sg.Frame("ミーティング時刻", layout_date, font=self.font, pad=[(10, 10), (10, 10)])],
            [sg.Frame("ミーティング情報", layout_join, font=self.font)],
            [sg.Checkbox("ミーティングを録画する", default=False, pad=[(0, 280), (0, 0)]),
             sg.Button("終了", font=self.font),
             sg.Button("実行", font=self.font)]
        ]

    def input_text_temp(self, key, size):
        return sg.InputText(
            size=size,
            justification='right',
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
                startEvent(event)

            elif (event is None) or (event == "終了"):
                endEvent(event, window)


if __name__ == "__main__":
    # themeの一覧
    # sg.theme_previewer()
    gui = GUI()
    gui.display()
