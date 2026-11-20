from easyvrui import button, font, label, rect, run, textbox, window

def main():
    window_main = window("window_main")
    window_main.title = "VRChat 情绪标签牌"
    window_main.rect = rect(0, 0, 560, 420)
    label_preview = label("label_preview")
    label_preview.rect = rect(24, 60, 512, 48)
    label_preview.font = font("Segoe UI", 22, True, False)
    label_preview.foreground_color = 0x7FE3FFFF
    textbox_mood = textbox("textbox_mood")
    textbox_mood.rect = rect(24, 120, 512, 130)
    textbox_mood.text = "在线发呆中..."
    textbox_mood.multiline = True
    textbox_mood.vertical_scrollbar_visible = True
    textbox_mood.max_length = 80
    textbox_mood.tooltip_text = "最多80个字符，支持多行输入"
    label_status = label("label_status")
    label_status.rect = rect(24, 260, 512, 32)
    button_undo = button("button_undo")
    button_undo.rect = rect(24, 360, 120, 40)
    button_undo.text = "撤销"
    button_undo.tooltip_text = "撤销上一步编辑（Ctrl+Z）"
    button_redo = button("button_redo")
    button_redo.rect = rect(156, 360, 120, 40)
    button_redo.text = "重做"
    button_redo.tooltip_text = "恢复刚才的撤销（Ctrl+Y）"
    button_select_all = button("button_select_all")
    button_select_all.rect = rect(288, 360, 120, 40)
    button_select_all.text = "全选"
    window_main.control_list.extend([label_preview, textbox_mood, label_status, button_undo, button_redo, button_select_all])

    def update_status():
        total = len(textbox_mood.text)
        label_preview.text = f"当前心情：{textbox_mood.text}"
        label_status.text = (f"字数：{total}/80 | 选区：[{textbox_mood.selection_start}, +{textbox_mood.selection_length}]")
        button_undo.enabled = textbox_mood.can_undo
        button_redo.enabled = textbox_mood.can_redo

    def button_preset_click(source, event):
        textbox_mood.selected_text = source.tag
        textbox_mood.focus()

    preset_list = [("button_mute", "静音中", "🔇 麦坏了/Mute中，请看气泡 ", 24), ("button_afk", "挂机喝茶", "☕ 暂时离开一下，马上回来 ", 190), ("button_talk", "欢迎聊天", "🎮 欢迎过来唠嗑！", 356),]

    for control_name, caption, snippet, left in preset_list:
        btn = button(control_name)
        btn.rect = rect(left, 304, 150, 42)
        btn.text = caption
        btn.tag = snippet
        btn.tooltip_text = f"在光标处插入：{snippet}"
        btn.on_click += button_preset_click
        window_main.control_list.add(btn)

    textbox_mood.on_text_changed += lambda source, event: update_status()
    textbox_mood.on_selection_changed += lambda source, event: update_status()
    button_undo.on_click += lambda source, event: textbox_mood.undo()
    button_redo.on_click += lambda source, event: textbox_mood.redo()
    button_select_all.on_click += lambda source, event: (textbox_mood.select(0, len(textbox_mood.text)), textbox_mood.focus(),)
    update_status()
    window_main.show()
    run("mood_board")

if __name__ == "__main__":
    main()