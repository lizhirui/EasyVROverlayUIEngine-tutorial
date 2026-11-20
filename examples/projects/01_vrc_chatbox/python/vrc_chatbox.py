import socket
import threading
import time
from easyvrui import (button, checkbox, dialog_result, keyboard_key, label, listbox, messagebox, messagebox_button_set, messagebox_icon, parse_keyboard_key, progressbar, rect, run, textbox, window,)

def encode_osc_string(text):
    raw = text.encode("utf-8") + b"\x00"
    padding = (4 - (len(raw) % 4)) % 4
    return raw + (b"\x00" * padding)

def send_vrc_chatbox(text, immediate = True, notify = True):
    tag = (",s" + ("T" if immediate else "F")) + ("T" if notify else "F")
    packet = (encode_osc_string("/chatbox/input") + encode_osc_string(tag)) + encode_osc_string(text)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        sock.sendto(packet, ("127.0.0.1", 9000))
    finally:
        sock.close()

class vrc_chatbox_window(window):
    def __init__(self, name = "vrc_chatbox_window"):
        super().__init__(name)
        self.title = "VRChat 快捷聊天框 (OSC)"
        self.rect = rect(0, 0, 720, 440)
        self.listbox_phrases = listbox("listbox_phrases")
        self.listbox_phrases.rect = rect(20, 64, 240, 310)
        self.listbox_phrases.item_list = ["你好呀！我是静音玩家~", "我去喝口水马上回来 (AFK)", "请问这首BGM叫什么名字？", "大家晚安，下次再一起玩！", "(｡･ω･｡)ﾉ♡ 贴贴！",]
        self.listbox_phrases.tooltip_text = "点选常用短语快速填入输入框"
        self.textbox_chat = textbox("textbox_chat")
        self.textbox_chat.rect = rect(278, 64, 422, 140)
        self.textbox_chat.multiline = True
        self.textbox_chat.max_length = 144
        self.textbox_chat.vertical_scrollbar_visible = True
        self.textbox_chat.tooltip_text = "支持中文拼音/日语/英文输入，按Enter发送"
        self.progressbar_length = progressbar("progressbar_length")
        self.progressbar_length.rect = rect(278, 214, 422, 22)
        self.progressbar_length.minimum = 0
        self.progressbar_length.maximum = 144
        self.checkbox_live_osc = checkbox("checkbox_live_osc")
        self.checkbox_live_osc.rect = rect(278, 248, 250, 36)
        self.checkbox_live_osc.text = "启用实时OSC (127.0.0.1:9000)"
        self.checkbox_live_osc.checked = False
        self.button_send = button("button_send")
        self.button_send.rect = rect(540, 248, 160, 42)
        self.button_send.text = "发送 Chatbox"
        self.button_send.tooltip_text = "发送到VRChat头顶聊天气泡"
        self.button_clear = button("button_clear")
        self.button_clear.rect = rect(278, 300, 160, 40)
        self.button_clear.text = "清空气泡"
        self.button_clear.tooltip_text = "发送空字符串清空头顶显示"
        self.label_status = label("label_status")
        self.label_status.rect = rect(20, 390, 680, 32)
        self.label_status.text = "状态：离线模拟模式（勾选实时OSC即可连接VRChat）"
        self.submission_id = 0

        for item in (self.listbox_phrases, self.textbox_chat, self.progressbar_length, self.checkbox_live_osc, self.button_send, self.button_clear, self.label_status,):
            self.control_list.add(item)

        self.listbox_phrases.on_selection_changed += self.listbox_phrases_selection_changed
        self.textbox_chat.on_text_changed += self.textbox_chat_text_changed
        self.textbox_chat.on_key_down += self.textbox_chat_key_down
        self.button_send.on_click += self.button_send_click
        self.button_clear.on_click += self.button_clear_click
        self.on_closing += self.window_closing

    def dispatch_chatbox(self, text):
        self.submission_id += 1
        submission = self.submission_id

        if self.checkbox_live_osc.checked:
            try:
                send_vrc_chatbox(text)
            except (OSError, UnicodeError):
                self.label_status.text = "OSC提交失败 · 草稿已保留"
                return False

            self.label_status.text = "OSC数据报已提交" if text else "已提交清空指令"
        else:
            self.label_status.text = "模拟消息已提交" if text else "已模拟提交清空指令"

        def reset_status_later():
            time.sleep(3.0)

            def update_ui():
                if (not self.label_status.disposed) and (self.submission_id == submission):
                    self.label_status.text = "状态：等待下一条消息..."

            self.label_status.begin_invoke(update_ui)

        threading.Thread(target = reset_status_later, daemon = True).start()
        return True

    def listbox_phrases_selection_changed(self, source, event):
        if self.listbox_phrases.selected_index >= 0:
            self.textbox_chat.text = self.listbox_phrases.selected_item
            self.textbox_chat.focus()

    def textbox_chat_text_changed(self, source, event):
        self.progressbar_length.value = len(self.textbox_chat.text)

    def textbox_chat_key_down(self, source, event):
        if parse_keyboard_key(event.key) == keyboard_key.enter:
            message = self.textbox_chat.text.strip()

            if message and self.dispatch_chatbox(message):
                self.textbox_chat.text = ""

            event.handled = True

    def button_send_click(self, source, event):
        message = self.textbox_chat.text.strip()

        if message and self.dispatch_chatbox(message):
            self.textbox_chat.text = ""

    def button_clear_click(self, source, event):
        self.dispatch_chatbox("")

    def window_closing(self, source, event):
        if self.checkbox_live_osc.checked:
            answer = messagebox("当前处于实时OSC模式，确定退出聊天框吗？", "确认退出", messagebox_button_set.yes_no, messagebox_icon.question, dialog_result.no, self,)

            if answer != dialog_result.yes:
                event.cancel = True

def main():
    window_main = vrc_chatbox_window()
    window_main.show()
    run("vrc_chatbox")

if __name__ == "__main__":
    main()