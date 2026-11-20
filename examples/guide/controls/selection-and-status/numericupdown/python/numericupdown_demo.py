from easyvrui import label, numericupdown, rect, run, window

def main():
    window_main = window("window_main")
    window_main.title = "校准增益"
    window_main.set_size(690, 305)
    label_prompt = label("label_prompt")
    label_prompt.rect = rect(36, 82, 618, 42)
    label_prompt.text = "范围：0.00至2.00"
    window_main.control_list.add(label_prompt)
    numericupdown_gain = numericupdown("numericupdown_gain")
    numericupdown_gain.rect = rect(36, 145, 320, 56)
    window_main.control_list.add(numericupdown_gain)
    label_state = label("label_state")
    label_state.rect = rect(36, 220, 618, 42)
    label_state.text = "当前增益低于基准"
    window_main.control_list.add(label_state)
    numericupdown_gain.maximum = 2.0
    numericupdown_gain.step = 0.25
    numericupdown_gain.decimal_places = 2
    numericupdown_gain.value = 0.75

    def numericupdown_gain_value_changed(source, event):
        label_state.text = "当前增益达到或超过基准" if (source.value >= 1.0) else "当前增益低于基准"

    numericupdown_gain.on_value_changed += numericupdown_gain_value_changed
    window_main.show()
    run("tutorial_numericupdown")

if __name__ == "__main__":
    main()