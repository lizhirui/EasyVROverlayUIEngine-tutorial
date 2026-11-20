from easyvrui import label, panel, rect, run, splitter, window

def main():
    window_main = window("window_main")
    window_main.title = "双区工作台"
    window_main.set_size(690, 422)
    splitter_workspace = splitter("splitter_workspace")
    splitter_workspace.rect = rect(36, 85, 618, 226)
    window_main.control_list.add(splitter_workspace)
    panel_task = panel("panel_task")
    splitter_workspace.control_list.add(panel_task)
    label_task = label("label_task")
    label_task.rect = rect(12, 18, 144, 42)
    label_task.text = "任务队列"
    panel_task.control_list.add(label_task)
    panel_result = panel("panel_result")
    splitter_workspace.control_list.add(panel_result)
    label_result = label("label_result")
    label_result.rect = rect(12, 18, 144, 42)
    label_result.text = "同步摘要"
    panel_result.control_list.add(label_result)
    label_state = label("label_state")
    label_state.rect = rect(36, 333, 618, 43)
    label_state.text = "拖动分隔条调整布局"
    window_main.control_list.add(label_state)
    splitter_workspace.split_position = 0.42
    panel_task.background_color = 0x203C56FF
    panel_result.background_color = 0x203D36FF

    def splitter_workspace_split_end(source, event):
        if not event.cancelled:
            label_state.text = "布局比例已更新"

    splitter_workspace.on_split_end += splitter_workspace_split_end
    window_main.show()
    run("tutorial_splitter")

if __name__ == "__main__":
    main()