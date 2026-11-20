from easyvrui import button, combobox, combobox_dropdown_style, label, listbox, rect, run, window

def main():
    window_main = window("window_main")
    window_main.title = "VRChat 世界传送清单"
    window_main.rect = rect(0, 0, 560, 440)
    world_map = {"全部": ["Just B Club 3", "FUJIYAMA (日本語雑談)", "Midnight Rooftop", "Murder 4", "Drinking Night"], "日语聊天": ["FUJIYAMA (日本語雑談)", "NAGiSA", "ポピー横丁"], "聚会/游戏": ["Murder 4", "Among Us", "Drinking Night", "Just B Club 3"],}
    combobox_category = combobox("combobox_category")
    combobox_category.rect = rect(24, 60, 200, 38)
    combobox_category.dropdown_style = combobox_dropdown_style.dropdown_list
    combobox_category.item_list.assign(["全部", "日语聊天", "聚会/游戏"])
    combobox_category.selected_index = 0
    combobox_add = combobox("combobox_add")
    combobox_add.rect = rect(240, 60, 196, 38)
    combobox_add.dropdown_style = combobox_dropdown_style.dropdown
    combobox_add.item_list.assign(["Prism Search", "Rest & Sleep", "VRC Cinema"])
    combobox_add.text = "输入或选新世界"
    button_add = button("button_add")
    button_add.rect = rect(446, 60, 90, 38)
    button_add.text = "加入"
    listbox_worlds = listbox("listbox_worlds")
    listbox_worlds.rect = rect(24, 110, 512, 230)
    listbox_worlds.row_height = 34
    listbox_worlds.clear_selection_on_blank_click = True
    listbox_worlds.item_list.assign(world_map["全部"])
    button_remove = button("button_remove")
    button_remove.rect = rect(24, 350, 140, 38)
    button_remove.text = "移除选中"
    button_toggle_drop = button("button_toggle_drop")
    button_toggle_drop.rect = rect(180, 350, 180, 38)
    button_toggle_drop.text = "展开/收起分类"
    label_status = label("label_status")
    label_status.rect = rect(24, 396, 512, 32)
    label_status.text = "请点选一个世界"
    window_main.control_list.extend([combobox_category, combobox_add, button_add, listbox_worlds, button_remove, button_toggle_drop, label_status,])

    def sync_status():
        if listbox_worlds.selected_index >= 0:
            label_status.text = (f"准备传送：{listbox_worlds.selected_item}（第 {listbox_worlds.selected_index + 1} 项）")
        else:
            label_status.text = "未选择任何世界"

    def combobox_category_changed(source, event):
        category = combobox_category.selected_item

        if category in world_map:
            listbox_worlds.item_list.assign(world_map[category])
            listbox_worlds.selected_index = 0 if (len(listbox_worlds.item_list) > 0) else (-1)
            sync_status()

    def button_add_click(source, event):
        name = combobox_add.text.strip()

        if name:
            listbox_worlds.item_list.insert(0, name)
            listbox_worlds.selected_index = 0

            if name not in combobox_add.item_list:
                combobox_add.item_list.add(name)

            sync_status()

    combobox_category.on_selected_index_changed += combobox_category_changed
    listbox_worlds.on_selection_changed += lambda source, event: sync_status()
    button_add.on_click += button_add_click
    button_remove.on_click += lambda source, event: (listbox_worlds.item_list.remove(listbox_worlds.selected_index) if (listbox_worlds.selected_index >= 0) else None)
    button_toggle_drop.on_click += lambda source, event: setattr(combobox_category, "dropped_down", not combobox_category.dropped_down)
    window_main.show()
    run("world_teleporter")

if __name__ == "__main__":
    main()