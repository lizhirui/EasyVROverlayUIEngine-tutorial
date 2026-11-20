from easyvrui import label, progressbar, rect, run, slider, window

def main():
    window_main = window("window_main")
    window_main.title = "监听音量"
    window_main.set_size(690, 310)
    label_level = label("label_level")
    label_level.rect = rect(36, 82, 606, 42)
    label_level.text = "音量较低"
    window_main.control_list.add(label_level)
    slider_level = slider("slider_level")
    slider_level.rect = rect(36, 148, 618, 52)
    window_main.control_list.add(slider_level)
    progressbar_level = progressbar("progressbar_level")
    progressbar_level.rect = rect(36, 228, 618, 29)
    window_main.control_list.add(progressbar_level)
    slider_level.value = 35
    progressbar_level.value = 35

    def slider_level_value_changed(source, event):
        progressbar_level.value = source.value
        label_level.text = "音量较高" if (source.value >= 60) else "音量较低"

    slider_level.on_value_changed += slider_level_value_changed
    window_main.show()
    run("tutorial_slider")

if __name__ == "__main__":
    main()