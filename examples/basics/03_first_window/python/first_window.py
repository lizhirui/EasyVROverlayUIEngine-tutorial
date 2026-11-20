from easyvrui import button, label, rect, run, window

def main():
    window_main = window("window_main")
    window_main.title = "我的第一个VR窗口"
    window_main.rect = rect(0, 0, 520, 260)
    label_status = label("label_status")
    label_status.rect = rect(36, 76, 448, 48)
    label_status.text = "点一下下面的按钮试试看！"
    button_hello = button("button_hello")
    button_hello.rect = rect(36, 150, 200, 48)
    button_hello.text = "点我打招呼"

    def button_hello_click(source, event):
        label_status.text = "你好，VR世界！"

    button_hello.on_click += button_hello_click
    window_main.control_list.add(label_status)
    window_main.control_list.add(button_hello)
    window_main.show()
    run("my_first_vr_app")

if __name__ == "__main__":
    main()