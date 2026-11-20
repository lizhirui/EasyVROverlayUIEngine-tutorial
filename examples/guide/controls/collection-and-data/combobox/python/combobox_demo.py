from easyvrui import combobox, label, rect, run, window

def main():
    window_main = window("window_main")
    window_main.title = "同步周期"
    window_main.set_size(690, 390)
    label_prompt = label("label_prompt")
    label_prompt.rect = rect(36, 76, 618, 44)
    label_prompt.text = "选择一个同步周期"
    window_main.control_list.add(label_prompt)
    combobox_interval = combobox("combobox_interval")
    combobox_interval.rect = rect(36, 130, 340, 52)
    window_main.control_list.add(combobox_interval)
    label_state = label("label_state")
    label_state.rect = rect(36, 310, 618, 45)
    label_state.text = "当前周期：每5分钟"
    window_main.control_list.add(label_state)
    combobox_interval.item_list = ["每5分钟", "每15分钟", "每30分钟"]
    combobox_interval.selected_index = 0

    def combobox_interval_selection_changed(source, event):
        label_state.text = "当前周期：" + source.selected_item

    combobox_interval.on_selection_changed += combobox_interval_selection_changed
    window_main.show()
    run("tutorial_combobox")

if __name__ == "__main__":
    main()