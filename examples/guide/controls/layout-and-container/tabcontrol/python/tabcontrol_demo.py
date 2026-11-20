from easyvrui import label, rect, run, tabcontrol, tabpage, window

def main():
    window_main = window("window_main")
    window_main.title = "同步工作台"
    window_main.set_size(690, 400)
    tabcontrol_workspace = tabcontrol("tabcontrol_workspace")
    tabcontrol_workspace.rect = rect(36, 83, 618, 270)
    window_main.control_list.add(tabcontrol_workspace)
    tabpage_status = tabpage("tabpage_status")
    tabpage_status.text = "概览"
    tabcontrol_workspace.page_list.add(tabpage_status)
    label_summary = label("label_summary")
    label_summary.rect = rect(18, 20, 520, 49)
    label_summary.text = "同步服务已连接"
    tabpage_status.control_list.add(label_summary)
    tabpage_history = tabpage("tabpage_history")
    tabpage_history.text = "历史"
    tabcontrol_workspace.page_list.add(tabpage_history)
    label_last = label("label_last")
    label_last.rect = rect(18, 20, 520, 49)
    label_last.text = "最近一次同步已完成"
    tabpage_history.control_list.add(label_last)
    label_count = label("label_count")
    label_count.rect = rect(18, 83, 520, 49)
    label_count.text = "已核验12份文件"
    tabpage_history.control_list.add(label_count)
    tabcontrol_workspace.tab_size = 42
    tabcontrol_workspace.selected_tab_background_color = 0x31615DFF
    window_main.show()
    run("tutorial_tabcontrol")

if __name__ == "__main__":
    main()