from threading import Event, Thread
from easyvrui import button, font, inputbox, label, rect, run, window

def main():
    window_main = window("window_main")
    window_main.title = "同步计时器"
    window_main.set_size(540, 258)
    label_time = label("label_time")
    label_time.rect = rect(36, 80, 468, 56)
    label_time.font = font("Microsoft YaHei UI", 27)
    label_time.text = "剩余25秒"
    button_note = button("button_note")
    button_note.rect = rect(36, 160, 220, 48)
    button_note.text = "填写任务备注"
    stop = Event()

    def button_note_click(source, event):
        value = inputbox("填写本次同步的备注", "任务备注", max_length = 48, owner = window_main)

        if value is not None:
            source.text = "备注已填写"

    def update_label(remaining):
        label_time.text = f"剩余{remaining}秒"

    def run_worker():
        for remaining in range(24, -1, -1):
            if stop.wait(1.0):
                return

            label_time.begin_invoke(lambda remaining = remaining: update_label(remaining))

    button_note.on_click += button_note_click
    window_main.control_list.add(label_time)
    window_main.control_list.add(button_note)
    window_main.show()
    worker = Thread(target = run_worker)
    worker.start()

    try:
        run("tutorial_timer")
    finally:
        stop.set()
        worker.join()

if __name__ == "__main__":
    main()