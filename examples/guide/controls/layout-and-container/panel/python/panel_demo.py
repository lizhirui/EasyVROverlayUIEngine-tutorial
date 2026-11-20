from easyvrui import button, label, panel, rect, run, window

def main():
    window_main = window("window_main")
    window_main.title = "连接分组"
    window_main.set_size(690, 363)
    panel_connection = panel("panel_connection")
    panel_connection.rect = rect(36, 80, 618, 238)
    window_main.control_list.add(panel_connection)
    label_title = label("label_title")
    label_title.rect = rect(16, 12, 520, 46)
    label_title.text = "同步服务"
    panel_connection.control_list.add(label_title)
    panel_detail = panel("panel_detail")
    panel_detail.rect = rect(16, 66, 586, 64)
    panel_connection.control_list.add(panel_detail)
    label_detail = label("label_detail")
    label_detail.rect = rect(14, 8, 550, 44)
    label_detail.text = "连接正常，可以开始同步"
    panel_detail.control_list.add(label_detail)
    button_detail = button("button_detail")
    button_detail.rect = rect(16, 159, 220, 48)
    button_detail.text = "隐藏连接详情"
    panel_connection.control_list.add(button_detail)
    panel_connection.background_color = 0x203046FF
    panel_detail.background_color = 0x1B403AFF

    def button_detail_click(source, event):
        panel_detail.visible = not panel_detail.visible
        source.text = "隐藏连接详情" if panel_detail.visible else "显示连接详情"

    button_detail.on_click += button_detail_click
    window_main.show()
    run("tutorial_panel")

if __name__ == "__main__":
    main()