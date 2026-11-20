from easyvrui import (drawing_image, image, image_stretch_mode, label, menubar, menuitem, rect, run, screen, toolbar, toolbar_button, window,)

def create_checker_image():
    pixels = bytearray()

    for row in range(64):
        for col in range(64):
            is_blue = (((row // 8) + (col // 8)) % 2) == 0
            pixels.extend((60, 160, 235, 255) if is_blue else (32, 48, 72, 255))

    return drawing_image(64, 64, bytes(pixels))

def make_swatch(r, g, b):
    return drawing_image(1, 1, bytes((r, g, b, 255)))

def main():
    window_main = window("window_main")
    window_main.title = "VR 迷你看图与副屏切换窗"
    window_main.rect = rect(0, 0, 760, 480)
    menubar_main = menubar("menubar_main")
    menu_view = menuitem("menu_view")
    menu_view.text = "视图(&V)"
    menu_toggle_screen = menuitem("menu_toggle_screen")
    menu_toggle_screen.text = "显示实时副屏(&S)"
    menu_toggle_screen.shortcut = "Ctrl+M"
    menu_toggle_screen.checkable = True
    menu_toggle_screen.checked = True
    menu_view.control_list.add(menu_toggle_screen)
    menubar_main.control_list.add(menu_view)
    window_main.menu = menubar_main
    toolbar_main = toolbar("toolbar_main")
    toolbar_main.rect = rect(20, 88, 720, 40)
    toolbar_main.tool_size = 36
    toolbar_main.spacing = 8.0
    btn_fit = toolbar_button("btn_fit")
    btn_fit.icon = make_swatch(80, 200, 160)
    btn_fit.tooltip_text = "切换图片缩放模式（contain / fill / cover）"
    btn_sep = toolbar_button("btn_sep")
    btn_sep.separator = True
    btn_next_screen = toolbar_button("btn_next_screen")
    btn_next_screen.icon = make_swatch(240, 170, 70)
    btn_next_screen.tooltip_text = "切换显示器编号（0 / 1）"
    toolbar_main.button_list.add(btn_fit)
    toolbar_main.button_list.add(btn_sep)
    toolbar_main.button_list.add(btn_next_screen)
    image_preview = image("image_preview")
    image_preview.rect = rect(20, 136, 350, 290)
    image_preview.source = create_checker_image()
    image_preview.stretch_mode = image_stretch_mode.contain
    screen_monitor = screen("screen_monitor")
    screen_monitor.rect = rect(390, 136, 350, 290)
    screen_monitor.screen_id = 0
    label_status = label("label_status")
    label_status.rect = rect(20, 438, 720, 32)
    label_status.text = "当前模式：image=contain"
    stretch_cycle = [image_stretch_mode.contain, image_stretch_mode.fill, image_stretch_mode.cover]
    stretch_pos = [0]

    def btn_fit_click(source, event):
        stretch_pos[0] = (stretch_pos[0] + 1) % len(stretch_cycle)
        image_preview.stretch_mode = stretch_cycle[stretch_pos[0]]
        label_status.text = f"图片拉伸模式切换为：{stretch_cycle[stretch_pos[0]].name}"

    def btn_next_screen_click(source, event):
        screen_monitor.screen_id = 1 if (screen_monitor.screen_id == 0) else 0
        label_status.text = (f"切换到显示器 #{screen_monitor.screen_id}（可用={screen_monitor.screen_available}）")

    def menu_toggle_screen_click(source, event):
        menu_toggle_screen.checked = not menu_toggle_screen.checked
        screen_monitor.visible = menu_toggle_screen.checked

    btn_fit.on_click += btn_fit_click
    btn_next_screen.on_click += btn_next_screen_click
    menu_toggle_screen.on_click += menu_toggle_screen_click
    screen_monitor.on_screen_unavailable += lambda source, event: setattr(label_status, "text", f"屏幕 {screen_monitor.screen_id} 暂不可用")
    screen_monitor.on_screen_restored += lambda source, event: setattr(label_status, "text", f"屏幕 {screen_monitor.screen_id} 已恢复捕获")
    window_main.control_list.extend([toolbar_main, image_preview, screen_monitor, label_status])
    window_main.show()
    run("media_viewer")

if __name__ == "__main__":
    main()