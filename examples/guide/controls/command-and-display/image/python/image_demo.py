from easyvrui import button, drawing_image, image, image_stretch_mode, rect, run, window

def main():
    window_main = window("window_main")
    window_main.title = "素材预览"
    window_main.set_size(680, 360)
    image_preview = image("image_preview")
    image_preview.rect = rect(36, 84, 608, 170)
    blue = bytes((56, 151, 207, 255))
    green = bytes((68, 197, 147, 255))
    image_preview.source = drawing_image(4, 2, (((blue * 2) + (green * 2)) + ((green * 2) + (blue * 2))))
    button_mode = button("button_mode")
    button_mode.rect = rect(36, 275, 235, 45)
    button_mode.text = "切换等比填充"

    def button_mode_click(source, event):
        image_preview.stretch_mode = (image_stretch_mode.cover if (image_preview.stretch_mode == image_stretch_mode.contain) else image_stretch_mode.contain)

    button_mode.on_click += button_mode_click
    window_main.control_list.add(image_preview)
    window_main.control_list.add(button_mode)
    window_main.show()
    run("tutorial_image")

if __name__ == "__main__":
    main()