from easyvrui import label, listview, listview_column, listview_item, rect, run, window

def main():
    window_main = window("window_main")
    window_main.title = "同步结果"
    window_main.set_size(680, 375)
    list_result = listview("list_result")
    list_result.rect = rect(36, 84, 608, 180)
    list_result.column_list = [listview_column("任务", 230), listview_column("状态", 160), listview_column("文件数", 130),]
    list_result.item_list = [listview_item(["同步图像", "完成", "12"]), listview_item(["同步音频", "待处理", "4"]), listview_item(["核验清单", "完成", "1"]),]
    label_state = label("label_state")
    label_state.rect = rect(36, 285, 608, 45)
    label_state.text = "请选择同步记录"

    def list_result_selection_changed(source, event):
        item = source.selected_item
        label_state.text = f"当前记录：{item.cell_list[0]}" if (item is not None) else "请选择同步记录"

    list_result.on_selection_changed += list_result_selection_changed
    window_main.control_list.add(list_result)
    window_main.control_list.add(label_state)
    window_main.show()
    run("tutorial_listview")

if __name__ == "__main__":
    main()