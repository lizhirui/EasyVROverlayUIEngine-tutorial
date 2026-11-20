from pathlib import Path
import easyvrui

class quick_shout_window(easyvrui.window):
    def __init__(self, name = "quick_shout_window"):
        super().__init__(name)
        self.label_hint = easyvrui.label("label_hint")
        self.textbox_message = easyvrui.textbox("textbox_message")
        self.button_send = easyvrui.button("button_send")
        self.control_list.add(self.label_hint)
        self.control_list.add(self.textbox_message)
        self.control_list.add(self.button_send)
        self.rect = easyvrui.rect(0, 0, 520, 258)
        self.title = "\U00009759\U000097f3\U00005feb\U00006377\U0000558a\U00008bdd\U00006761"
        self.label_hint.rect = easyvrui.rect(24, 74, 472, 30)
        self.label_hint.text = "\U00008f93\U00005165\U000060f3\U00008bf4\U00007684\U00008bdd\U0000ff1a"
        self.textbox_message.rect = easyvrui.rect(24, 116, 472, 46)
        self.textbox_message.tag = "chatbox_input"
        self.textbox_message.text = ""
        self.button_send.rect = easyvrui.rect(24, 180, 150, 44)
        self.button_send.text = "\U000053d1\U00009001"
        self.button_send.tooltip_text = "\U0000628a\U00006587\U0000672c\U00006846\U000091cc\U00007684\U00005185\U00005bb9\U000053d1\U000051fa\U000053bb"