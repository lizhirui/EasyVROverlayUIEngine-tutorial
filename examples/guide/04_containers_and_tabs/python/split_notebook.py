from easyvrui import (button, checkbox, label, orientation, panel, rect, run, scrollpanel, splitter, tab_position, tabcontrol, tabpage, window,)

def main():
    window_main = window("window_main")
    window_main.title = "多功能 VR 设置中心"
    window_main.rect = rect(0, 0, 620, 440)
    tabcontrol_main = tabcontrol("tabcontrol_main")
    tabcontrol_main.rect = rect(20, 56, 580, 330)
    tabcontrol_main.tab_position = tab_position.top
    tabcontrol_main.tab_size = 38
    tabcontrol_main.page_close_button_visible = True
    page_general = tabpage("page_general")
    page_general.text = "常规设置"
    button_new_tab = button("button_new_tab")
    button_new_tab.rect = rect(20, 20, 200, 40)
    button_new_tab.text = "新建临时配置页"
    page_general.control_list.add(button_new_tab)
    page_advanced = tabpage("page_advanced")
    page_advanced.text = "高级布局"
    splitter_main = splitter("splitter_main")
    splitter_main.rect = rect(12, 12, 556, 268)
    splitter_main.orientation = orientation.vertical
    splitter_main.split_position = 0.35
    panel_nav = panel("panel_nav")
    label_nav = label("label_nav")
    label_nav.rect = rect(12, 16, 150, 32)
    label_nav.text = "左侧分栏（可拖动）"
    panel_nav.control_list.add(label_nav)
    scrollpanel_options = scrollpanel("scrollpanel_options")

    for idx in range(10):
        item = checkbox(f"checkbox_opt_{idx}")
        item.rect = rect(16, 12 + (idx * 44), 260, 34)
        item.text = f"实验性 VR 选项 #{idx + 1}"
        scrollpanel_options.control_list.add(item)

    splitter_main.control_list.extend([panel_nav, scrollpanel_options])
    page_advanced.control_list.add(splitter_main)
    tabcontrol_main.page_list.extend([page_general, page_advanced])
    tabcontrol_main.selected_index = 0
    label_status = label("label_status")
    label_status.rect = rect(20, 396, 580, 32)
    label_status.text = "当前页签：常规设置"
    extra_counter = [0]

    def button_new_tab_click(source, event):
        extra_counter[0] += 1
        page_extra = tabpage(f"page_extra_{extra_counter[0]}")
        page_extra.text = f"配置 #{extra_counter[0]}"
        tabcontrol_main.page_list.add(page_extra)
        tabcontrol_main.selected_index = len(tabcontrol_main.page_list) - 1

    def tabcontrol_main_page_close(source, event):
        if (event.index >= 2) and (event.page is not None):
            tabcontrol_main.page_list.remove(event.page)
        else:
            label_status.text = "基础页签不可关闭！"

    button_new_tab.on_click += button_new_tab_click
    tabcontrol_main.on_page_close += tabcontrol_main_page_close
    tabcontrol_main.on_selection_changed += lambda source, event: setattr(label_status, "text", f"当前页签：{tabcontrol_main.selected_page.text}" if tabcontrol_main.selected_page else "无选中页",)
    splitter_main.on_split_position_changed += lambda source, event: setattr(label_status, "text", f"分隔比例：{splitter_main.split_position:.2f}")
    scrollpanel_options.on_viewport_changed += lambda source, event: setattr(label_status, "text", "右侧设置面板正在滚动...")
    window_main.control_list.extend([tabcontrol_main, label_status])
    window_main.show()
    run("settings_hub")

if __name__ == "__main__":
    main()