from easyvrui import (grid, grid_column, label, listview, listview_column, listview_item, rect, run, tree_node, treeview, window,)

def main():
    window_main = window("window_main")
    window_main.title = "简易收藏夹与参数表"
    window_main.rect = rect(0, 0, 860, 500)
    tree_fav = treeview("tree_fav")
    tree_fav.rect = rect(20, 56, 220, 380)
    node_worlds = tree_node("收藏世界", expanded = True, tag = "worlds")
    node_worlds.node_list.append(tree_node("日语闲聊区", tag = "worlds/jp"))
    node_worlds.node_list.append(tree_node("睡眠/放空区", tag = "worlds/sleep"))
    node_avatars = tree_node("Avatar预设", expanded = True, tag = "avatars")
    node_avatars.node_list.append(tree_node("日常猫耳", tag = "avatars/cat"))
    tree_fav.node_list.add(node_worlds)
    tree_fav.node_list.add(node_avatars)
    list_items = listview("list_items")
    list_items.rect = rect(256, 56, 584, 170)
    list_items.column_list.assign([listview_column("名称", 240), listview_column("类型", 140), listview_column("备注", 180)])
    list_items.item_list.assign([listview_item(["FUJIYAMA", "世界", "日语闲聊"], tag = "fuji"), listview_item(["NAGiSA", "世界", "1对1聊天"], tag = "nagisa"), listview_item(["猫耳卫衣", "Avatar", "轻量级"], tag = "cat"),])
    param_rows = [["EarTwitchSpeed", 1.5, True], ["TailWagAmp", 0.8, True], ["GlowIntensity", 2.0, False]]
    grid_params = grid("grid_params")
    grid_params.rect = rect(256, 240, 584, 196)
    grid_params.column_list = [grid_column("参数名", 240, editable = False), grid_column("浮点数值", 170, editable = True), grid_column("启用", 140, editable = True),]
    grid_params.set_data_provider(len(param_rows), lambda r, c: param_rows[r][c], lambda r, c, v: (param_rows[r].__setitem__(c, v) or True),)
    grid_params.set_edit_validator(lambda cell, val: ((False, "数值必须在 0.0 到 10.0 之间！") if ((cell.column == 1) and ((val < 0.0) or (val > 10.0))) else True))
    label_status = label("label_status")
    label_status.rect = rect(20, 450, 820, 32)
    label_status.text = "点击左侧树节点查看详情"
    sort_asc = [True]

    def list_items_column_click(source, event):
        if event.index == 0:
            sort_asc[0] = not sort_asc[0]
            list_items.item_list.assign(sorted(list(list_items.item_list), key = lambda row: row.cell_list[0], reverse = not sort_asc[0]))

    tree_fav.on_selection_changed += lambda source, event: setattr(label_status, "text", f"选中节点：{tree_fav.selected_node.text}（tag={tree_fav.selected_node.tag}）" if tree_fav.selected_node else "未选中节点",)
    list_items.on_column_click += list_items_column_click
    list_items.on_row_double_click += lambda source, event: setattr(label_status, "text", f"双击激活行：{event.item.cell_list[0]} (tag={event.item.tag})")
    grid_params.on_cell_value_changed += lambda source, event: setattr(label_status, "text", f"参数已更新：[{event.row}, {event.column}] = {param_rows[event.row][event.column]}",)
    grid_params.on_edit_failed += lambda source, event: setattr(label_status, "text", f"校验失败：{event.error}")
    window_main.control_list.extend([tree_fav, list_items, grid_params, label_status])
    window_main.show()
    run("fav_and_params")

if __name__ == "__main__":
    main()