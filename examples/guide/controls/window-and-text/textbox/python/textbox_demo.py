from easyvrui import button, label, rect, run, textbox, window

def main():
    window_main = window("window_main")
    window_main.title = "编辑备注"
    window_main.set_size(650, 420)
    label_caption = label("label_caption")
    label_caption.rect = rect(32, 82, 580, 40)
    label_caption.text = "备注（最多80个字符）"
    window_main.control_list.add(label_caption)
    textbox_note = textbox("textbox_note")
    textbox_note.rect = rect(32, 132, 586, 125)
    window_main.control_list.add(textbox_note)
    label_state = label("label_state")
    label_state.rect = rect(32, 274, 580, 46)
    label_state.text = "请编辑或选择备注"
    window_main.control_list.add(label_state)
    button_select = button("button_select")
    button_select.rect = rect(32, 329, 176, 42)
    button_select.text = "全选备注"
    window_main.control_list.add(button_select)
    textbox_note.multiline = True
    textbox_note.vertical_scrollbar_visible = True
    textbox_note.max_length = 80
    textbox_note.text = "第一行：检查连接\n第二行：同步配置"

    def textbox_note_text_changed(source, event):
        label_state.text = "备注已修改"

    def button_select_click(source, event):
        textbox_note.focus()
        textbox_note.select(0, len(textbox_note.text))

    textbox_note.on_text_changed += textbox_note_text_changed
    button_select.on_click += button_select_click
    window_main.show()
    run("tutorial_textbox")

if __name__ == "__main__":
    main()