from easyvrui import label, rect, run, tree_node, treeview, window

def main():
    window_main = window("window_main")
    window_main.title = "任务分类"
    window_main.set_size(680, 380)
    tree_task = treeview("tree_task")
    tree_task.rect = rect(36, 84, 608, 184)
    folder = tree_node("同步任务", True, "sync")
    report = tree_node("检查报告", False, "report")
    folder.node_list.add(tree_node("同步图像", False, "image"))
    folder.node_list.add(report)
    tree_task.node_list.add(folder)
    tree_task.node_list.add(tree_node("本地配置", False, "config"))
    label_state = label("label_state")
    label_state.rect = rect(36, 290, 608, 44)
    label_state.text = "请选择任务"

    def tree_task_selection_changed(source, event):
        label_state.text = f"选中：{event.node.text}" if (event.node is not None) else "请选择任务"

    tree_task.on_selection_changed += tree_task_selection_changed
    window_main.control_list.add(tree_task)
    window_main.control_list.add(label_state)
    window_main.show()
    run("tutorial_treeview")

if __name__ == "__main__":
    main()