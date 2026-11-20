import os
import threading
from pathlib import Path
from easyvrui import (combobox, combobox_dropdown_style, drawing_image, file_filter, file_open_dialog, file_save_dialog, image, image_stretch_mode, inputbox, label, listview, listview_column, listview_item, menubar, menuitem, rect, run, tabcontrol, tabpage, toolbar, toolbar_button, tree_node, treeview, window,)

def main():
    VRC_LOG_DIR = Path(os.path.expandvars(r"%USERPROFILE%\AppData\LocalLow\VRChat\VRChat"))
    VRC_PHOTO_DIR = Path(os.path.expandvars(r"%USERPROFILE%\Pictures\VRChat"))
    window_main = window("window_main")
    window_main.title = "VRChat 日志与相册管理器"
    window_main.rect = rect(0, 0, 820, 520)
    menubar_main = menubar("menubar_main")
    menuitem_file = menuitem("menuitem_file")
    menuitem_file.text = "文件(&F)"
    menuitem_open_dir = menuitem("menuitem_open_dir")
    menuitem_open_dir.text = "选择照片..."
    menuitem_open_dir.shortcut = "Ctrl+O"
    menuitem_export_log = menuitem("menuitem_export_log")
    menuitem_export_log.text = "导出日志..."
    menuitem_export_log.shortcut = "Ctrl+S"
    menuitem_file.control_list.add(menuitem_open_dir)
    menuitem_file.control_list.add(menuitem_export_log)
    menubar_main.control_list.add(menuitem_file)
    tabcontrol_main = tabcontrol("tabcontrol_main")
    tabcontrol_main.rect = rect(16, 86, 788, 418)
    tabpage_logs = tabpage("tabpage_logs")
    tabpage_logs.text = "房间进出日志"
    combobox_filter = combobox("combobox_filter")
    combobox_filter.rect = rect(12, 12, 220, 38)
    combobox_filter.dropdown_style = combobox_dropdown_style.dropdown_list
    combobox_filter.item_list = ["全部事件", "仅加入 (Joined)", "仅离开 (Left)"]
    combobox_filter.selected_index = 0
    listview_logs = listview("listview_logs")
    listview_logs.rect = rect(12, 60, 744, 296)
    listview_logs.column_list.add(listview_column("时间", 140))
    listview_logs.column_list.add(listview_column("动作", 110))
    listview_logs.column_list.add(listview_column("玩家昵称", 470))
    tabpage_logs.control_list.add(combobox_filter)
    tabpage_logs.control_list.add(listview_logs)
    tabpage_gallery = tabpage("tabpage_gallery")
    tabpage_gallery.text = "VRChat相册"
    toolbar_gallery = toolbar("toolbar_gallery")
    toolbar_gallery.rect = rect(12, 10, 744, 38)
    btn_contain = toolbar_button("btn_contain")
    btn_contain.icon = drawing_image(1, 1, bytes((105, 182, 246, 255)))
    btn_contain.tooltip_text = "等比适应"
    btn_cover = toolbar_button("btn_cover")
    btn_cover.icon = drawing_image(1, 1, bytes((92, 201, 159, 255)))
    btn_cover.tooltip_text = "等比铺满"
    btn_note = toolbar_button("btn_note")
    btn_note.icon = drawing_image(1, 1, bytes((220, 167, 96, 255)))
    btn_note.tooltip_text = "添加备注"
    toolbar_gallery.button_list.add(btn_contain)
    toolbar_gallery.button_list.add(btn_cover)
    toolbar_gallery.button_list.add(btn_note)
    treeview_months = treeview("treeview_months")
    treeview_months.rect = rect(12, 56, 230, 298)
    image_photo = image("image_photo")
    image_photo.rect = rect(254, 56, 502, 260)
    image_photo.stretch_mode = image_stretch_mode.contain
    label_photo_note = label("label_photo_note")
    label_photo_note.rect = rect(254, 322, 502, 32)
    label_photo_note.text = "从左侧选择月份照片，或通过菜单加载任意图片"

    for item in (toolbar_gallery, treeview_months, image_photo, label_photo_note):
        tabpage_gallery.control_list.add(item)

    tabcontrol_main.page_list.add(tabpage_logs)
    tabcontrol_main.page_list.add(tabpage_gallery)
    all_log_rows = []
    stopped = threading.Event()

    def refresh_log_view():
        mode = combobox_filter.selected_index
        listview_logs.item_list.clear()

        for timestamp, action, player in all_log_rows[-100: ]:
            if (mode == 1) and (action != "Joined"):
                continue

            if (mode == 2) and (action != "Left"):
                continue

            listview_logs.item_list.add(listview_item([timestamp, action, player], tag = f"{action}:{player}"))

    def scan_photos():
        treeview_months.node_list.clear()

        if not VRC_PHOTO_DIR.is_dir():
            demo_node = tree_node("示例相册（未检测到VRC拍照目录）", expanded = True, tag = "demo")
            treeview_months.node_list.add(demo_node)
            return

        for month_dir in sorted(VRC_PHOTO_DIR.iterdir(), reverse = True):
            if not month_dir.is_dir():
                continue

            month_node = tree_node(month_dir.name, expanded = False, tag = str(month_dir))

            for photo_path in sorted(month_dir.glob("*.png"), reverse = True)[: 30]:
                month_node.node_list.add(tree_node(photo_path.name, tag = str(photo_path)))

            treeview_months.node_list.add(month_node)

    def tail_vrc_logs():
        log_files = (sorted(VRC_LOG_DIR.glob("output_log_*.txt"), key = lambda p: p.stat().st_mtime, reverse = True) if VRC_LOG_DIR.is_dir() else [])

        if not log_files:
            def add_demo():
                all_log_rows.append(("12:00:01", "Joined", "Mika (示例日志)"))
                all_log_rows.append(("12:03:15", "Left", "Ren (示例日志)"))
                refresh_log_view()

            listview_logs.begin_invoke(add_demo)
            return

        with log_files[0].open("r", encoding = "utf-8", errors = "ignore") as handle:
            while not stopped.is_set():
                line = handle.readline()

                if not line:
                    stopped.wait(0.5)
                    continue

                if ("OnPlayerJoined " in line) or ("OnPlayerLeft " in line):
                    action = "Joined" if ("OnPlayerJoined " in line) else "Left"
                    player = line.split(f"OnPlayer{action} ", 1)[1].strip()
                    timestamp = line[11: 19] if (len(line) > 19) else "--:--:--"

                    def push_row(t = timestamp, a = action, p = player):
                        if not listview_logs.disposed:
                            all_log_rows.append((t, a, p))
                            refresh_log_view()

                    listview_logs.begin_invoke(push_row)

    def treeview_months_selection_changed(source, event):
        node = treeview_months.selected_node

        if (node is not None) and node.tag.lower().endswith(".png"):
            load_photo(Path(node.tag))

    def load_photo(path):
        try:
            image_photo.source = drawing_image.load_file(str(path))
            label_photo_note.text = f"正在预览：{path.name}"
        except (OSError, RuntimeError, ValueError):
            label_photo_note.text = "无法读取所选照片"

    def menuitem_open_dir_click(source, event):
        paths = file_open_dialog("选择图片", str(VRC_PHOTO_DIR if VRC_PHOTO_DIR.is_dir() else Path.home()), "", [file_filter("PNG图片", ["*.png", "*.jpg"])], 0, False, "", window_main,)

        if paths:
            load_photo(Path(paths[0]))

    def menuitem_export_log_click(source, event):
        target = file_save_dialog("导出进出日志", str(Path.home()), "vrc_room_log.txt", [file_filter("文本文件", ["*.txt"])], 0, "txt", True, "", window_main,)

        if target is not None:
            Path(target).write_text("\n".join(f"{t}\t{a}\t{p}" for t, a, p in all_log_rows), encoding = "utf-8")

    def btn_note_click(source, event):
        note = inputbox("为当前照片输入备注：", "照片备注", "", 64, window_main)

        if note:
            label_photo_note.text = f"备注：{note}"

    combobox_filter.on_selection_changed += lambda s, e: refresh_log_view()
    treeview_months.on_selection_changed += treeview_months_selection_changed
    menuitem_open_dir.on_click += menuitem_open_dir_click
    menuitem_export_log.on_click += menuitem_export_log_click
    btn_contain.on_click += lambda s, e: setattr(image_photo, "stretch_mode", image_stretch_mode.contain)
    btn_cover.on_click += lambda s, e: setattr(image_photo, "stretch_mode", image_stretch_mode.cover)
    btn_note.on_click += btn_note_click
    window_main.menu = menubar_main
    window_main.control_list.add(tabcontrol_main)
    scan_photos()
    window_main.show()
    worker = threading.Thread(target = tail_vrc_logs)
    worker.start()

    try:
        run("vrc_log_and_gallery")
    finally:
        stopped.set()
        worker.join()

if __name__ == "__main__":
    main()