from easyvrui import label, listbox, rect, run, window

def main():
    window_main = window("window_main")
    window_main.title = "同步任务"
    window_main.set_size(690, 413)
    label_prompt = label("label_prompt")
    label_prompt.rect = rect(36, 78, 618, 38)
    label_prompt.text = "选择要查看的同步任务"
    window_main.control_list.add(label_prompt)
    listbox_task = listbox("listbox_task")
    listbox_task.rect = rect(36, 130, 618, 190)
    window_main.control_list.add(listbox_task)
    label_state = label("label_state")
    label_state.rect = rect(36, 338, 618, 38)
    label_state.text = "尚未选择任务"
    window_main.control_list.add(label_state)
    listbox_task.item_list = ["读取配置", "检查目录", "同步图像", "同步音频", "同步模型", "核验校验和", "清理临时文件", "写入报告",]
    listbox_task.row_height = 38
    listbox_task.clear_selection_on_blank_click = True

    def listbox_task_selection_changed(source, event):
        label_state.text = ("尚未选择任务" if (source.selected_index < 0) else ("选中任务：" + source.selected_item))

    listbox_task.on_selection_changed += listbox_task_selection_changed
    window_main.show()
    run("tutorial_listbox")

if __name__ == "__main__":
    main()