from easyvrui import label, rect, run, scrollpanel, window

def main():
    window_main = window("window_main")
    window_main.title = "同步日志"
    window_main.set_size(690, 405)
    label_prompt = label("label_prompt")
    label_prompt.rect = rect(36, 76, 618, 48)
    label_prompt.text = "滚动查看同步步骤"
    window_main.control_list.add(label_prompt)
    scrollpanel_log = scrollpanel("scrollpanel_log")
    scrollpanel_log.rect = rect(36, 135, 618, 188)
    window_main.control_list.add(scrollpanel_log)
    label_log_1 = label("label_log_1")
    label_log_1.rect = rect(14, 8, 560, 42)
    label_log_1.text = "01 读取配置"
    scrollpanel_log.control_list.add(label_log_1)
    label_log_2 = label("label_log_2")
    label_log_2.rect = rect(14, 68, 560, 42)
    label_log_2.text = "02 检查目录"
    scrollpanel_log.control_list.add(label_log_2)
    label_log_3 = label("label_log_3")
    label_log_3.rect = rect(14, 128, 560, 42)
    label_log_3.text = "03 建立连接"
    scrollpanel_log.control_list.add(label_log_3)
    label_log_4 = label("label_log_4")
    label_log_4.rect = rect(14, 188, 560, 42)
    label_log_4.text = "04 同步图像"
    scrollpanel_log.control_list.add(label_log_4)
    label_log_5 = label("label_log_5")
    label_log_5.rect = rect(14, 248, 560, 42)
    label_log_5.text = "05 校验数据"
    scrollpanel_log.control_list.add(label_log_5)
    label_log_6 = label("label_log_6")
    label_log_6.rect = rect(14, 308, 560, 42)
    label_log_6.text = "06 生成报告"
    scrollpanel_log.control_list.add(label_log_6)
    label_footer = label("label_footer")
    label_footer.rect = rect(36, 334, 618, 37)
    label_footer.text = "日志记录按时间排列"
    window_main.control_list.add(label_footer)
    scrollpanel_log.horizontal_scrollbar_visible = False
    label_log_1.background_color = 0x243B50FF
    label_log_2.background_color = 0x1D2F43FF
    label_log_3.background_color = 0x243B50FF
    label_log_4.background_color = 0x1D2F43FF
    label_log_5.background_color = 0x243B50FF
    label_log_6.background_color = 0x1D2F43FF
    window_main.show()
    run("tutorial_scrollpanel")

if __name__ == "__main__":
    main()