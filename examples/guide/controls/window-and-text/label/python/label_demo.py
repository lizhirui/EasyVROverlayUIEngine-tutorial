from easyvrui import font, label, rect, run, window

def main():
    window_main = window("window_main")
    window_main.title = "连接状态"
    window_main.set_size(650, 295)
    label_caption = label("label_caption")
    label_caption.rect = rect(32, 84, 586, 52)
    label_caption.text = "工作区连接"
    window_main.control_list.add(label_caption)
    label_state = label("label_state")
    label_state.rect = rect(32, 157, 586, 49)
    label_state.text = "已连接 · 测试服务"
    window_main.control_list.add(label_state)
    label_detail = label("label_detail")
    label_detail.rect = rect(32, 220, 586, 42)
    label_detail.text = "可以开始同步设置"
    window_main.control_list.add(label_detail)
    label_caption.font = font("Microsoft YaHei UI", 28, True)
    label_state.background_color = 0x173B38FF
    label_state.foreground_color = 0xA7EFC9FF
    label_state.font = font("Microsoft YaHei UI", 22)
    window_main.show()
    run("tutorial_label")

if __name__ == "__main__":
    main()