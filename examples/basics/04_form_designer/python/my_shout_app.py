from easyvrui import run
from quick_shout_window import quick_shout_window

class my_shout_app:
    def __init__(self):
        self.ui = quick_shout_window()
        self.ui.button_send.on_click += self.button_send_click

    def button_send_click(self, source, event):
        message = self.ui.textbox_message.text
        self.ui.label_hint.text = f"已发送：{message}"

    def show(self):
        self.ui.show()

def main():
    app_main = my_shout_app()
    app_main.show()
    run("quick_shout_app")

if __name__ == "__main__":
    main()