from easyvrui import button, label, rect, run, window

def main():
    window_main = window("window_main")
    window_main.title = "会话窗口"
    window_main.set_size(650, 290)
    label_state = label("label_state")
    label_state.rect = rect(32, 88, 580, 48)
    label_state.text = "当前窗口已显示"
    window_main.control_list.add(label_state)
    button_title = button("button_title")
    button_title.rect = rect(32, 163, 220, 50)
    button_title.text = "切换标题栏配色"
    window_main.control_list.add(button_title)
    window_main.title_background_color = 0x21495EFF

    def button_title_click(source, event):
        window_main.title_background_color = (0x465C82FF if (window_main.title_background_color == 0x21495EFF) else 0x21495EFF)

    button_title.on_click += button_title_click
    window_main.show()
    run("tutorial_window")

if __name__ == "__main__":
    main()