from easyvrui import label, menubar, menuitem, rect, run, window

def main():
    window_main = window("window_main")
    window_main.title = "工作区命令"
    window_main.set_size(680, 315)
    menu_main = menubar("menu_main")
    menu_task = menuitem("menu_task")
    menu_task.text = "任务(&T)"
    menu_refresh = menuitem("menu_refresh")
    menu_refresh.text = "刷新记录"
    menu_refresh.shortcut = "Ctrl+R"
    label_state = label("label_state")
    label_state.rect = rect(36, 217, 608, 49)
    label_state.text = "等待刷新"

    def menu_refresh_click(source, event):
        label_state.text = "同步记录已刷新"

    menu_refresh.on_click += menu_refresh_click
    menu_task.control_list.add(menu_refresh)
    menu_main.control_list.add(menu_task)
    window_main.menu = menu_main
    window_main.control_list.add(label_state)
    window_main.show()
    run("tutorial_menubar")

if __name__ == "__main__":
    main()