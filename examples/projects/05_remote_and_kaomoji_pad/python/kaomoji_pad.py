from easyvrui import button, input_event, input_provider, input_role, rect, window

class kaomoji_ime(input_provider):
    def __init__(self):
        super().__init__()
        self.pad = window("kaomoji_pad")
        self.pad.title = "颜文字小键盘"
        self.pad.rect = rect(0, 0, 520, 150)
        self.pad.show_title_bar = False
        self.pad.auxiliary = True
        kaomoji_list = ["(｡･ω･｡)ﾉ♡", "(つд⊂)ｴｰﾝ", "(ﾉ´ヮ`)ﾉ*:･ﾟ✧", "(*￣3￣)╭"]

        for index, text in enumerate(kaomoji_list):
            btn = button(f"btn_kaomoji_{index}")
            btn.rect = rect(12 + (index * 126), 16, 118, 48)
            btn.text = text

            def on_click(source, event, value = text):
                self.begin_input_task()

                try:
                    item = input_event()
                    item.event_type = "ime_submit"
                    item.text = value
                    self.send_event(item)
                finally:
                    self.finish_input_task()

            btn.on_click += on_click
            self.pad.control_list.add(btn)

    def process_state(self, state):
        if state.active:
            self.pad.show()
        else:
            self.pad.hide()

    def process_input(self, event):
        self.send_event(event)

def main():
    pad_provider = kaomoji_ime()
    pad_provider.register_provider(input_role.ime, name = "Kaomoji Pad", language = "en")
    pad_provider.run()

if __name__ == "__main__":
    main()