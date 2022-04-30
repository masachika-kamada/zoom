import PySimpleGUI as sg


class GUI:
    font = ('Meiryo UI', 15)
    input_text_size = (2, 1)

    def __init__(self):
        sg.theme("DarkRed2")
        layout_date = [
            [sg.Text("入室時間")],
            [self.input_text_temp("start_M"), self.text_temp("/"),
             self.input_text_temp("start_d"), self.text_temp(" "),
             self.input_text_temp("start_h"), self.text_temp(":"),
             self.input_text_temp("start_m")],
            [sg.Text("退室時間")],
            [self.input_text_temp("end_M"), self.text_temp("/"),
             self.input_text_temp("end_d"), self.text_temp(" "),
             self.input_text_temp("end_h"), self.text_temp(":"),
             self.input_text_temp("end_m")],
        ]
        layout_url = [
            [sg.Text("URL")],
            [sg.InputText(size=(35, 1), key="url")],
            [sg.Text("パスワード(あれば)")],
            [sg.InputText(size=(35, 1), key="password")]
        ]
        layout_id = [
            [sg.Text("ID(スペースキー不要)")],
            [sg.InputText(size=(35, 1), key="id")],
            [sg.Text("パスワード")],
            [sg.InputText(size=(35, 1), key="password")]
        ]
        self.layout = [
            [sg.Frame("ミーティング時刻", layout_date)],
            [sg.Frame("URLから入室する場合", layout_url),
             sg.Frame("IDから入室する場合", layout_id)],
            [sg.Checkbox("ミーティングを録画する", default=False, pad=[(0, 380), (0, 0)]),
             sg.Button("終了", font=("", 13)), sg.Button("実行", font=("", 13))]
        ]

    def input_text_temp(self, key):
        return sg.InputText(
            size=self.input_text_size,
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
