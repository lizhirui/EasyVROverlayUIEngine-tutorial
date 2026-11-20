from easyvrui import blank, button, label, panel, rect, run, window

def main():
    window_main = window("window_main")
    window_main.title = "延迟安装内容"
    window_main.set_size(680, 340)
    content = panel("panel_content")
    content.rect = rect(36, 83, 608, 127)
    placeholder = blank("blank_content")
    placeholder.rect = rect(16, 23, 536, 59)
    content.control_list.add(placeholder)
    button_load = button("button_load")
    button_load.rect = rect(36, 240, 220, 47)
    button_load.text = "加载内容"

    def button_load_click(source, event):
        collection = content.control_list
        index = collection.index_of(placeholder)
        item = label("label_content")
        item.rect = placeholder.rect
        item.text = "内容已加载"
        collection.remove(placeholder)
        collection.insert(index, item)
        source.enabled = False

    button_load.on_click += button_load_click
    window_main.control_list.add(content)
    window_main.control_list.add(button_load)
    window_main.show()
    run("tutorial_blank")

if __name__ == "__main__":
    main()