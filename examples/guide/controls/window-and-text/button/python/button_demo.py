from easyvrui import button, label, rect, run, window

def main():
    window_main = window("window_main")
    window_main.title = "提交设置"
    window_main.set_size(650, 300)
    label_state = label("label_state")
    label_state.rect = rect(32, 84, 580, 47)
    label_state.text = "设置尚未提交"
    window_main.control_list.add(label_state)
    button_submit = button("button_submit")
    button_submit.rect = rect(32, 155, 212, 54)
    button_submit.text = "提交设置"
    window_main.control_list.add(button_submit)
    button_reset = button("button_reset")
    button_reset.rect = rect(266, 155, 212, 54)
    button_reset.text = "重新编辑"
    window_main.control_list.add(button_reset)
    button_submit.tab_index = 0
    button_reset.tab_index = 1
    button_reset.enabled = False

    def button_submit_click(source, event):
        source.enabled = False
        button_reset.enabled = True
        label_state.text = "设置已提交"

    def button_reset_click(source, event):
        source.enabled = False
        button_submit.enabled = True
        label_state.text = "设置尚未提交"

    button_submit.on_click += button_submit_click
    button_reset.on_click += button_reset_click
    window_main.show()
    run("tutorial_button")

if __name__ == "__main__":
    main()