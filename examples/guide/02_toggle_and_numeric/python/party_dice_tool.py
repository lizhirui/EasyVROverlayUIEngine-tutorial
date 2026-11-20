from easyvrui import (checkbox, label, numericupdown, orientation, panel, progressbar, radiobutton, rect, run, slider, window,)

def main():
    window_main = window("window_main")
    window_main.title = "头显环境调音台"
    window_main.rect = rect(0, 0, 560, 420)
    label_summary = label("label_summary")
    label_summary.rect = rect(24, 56, 512, 36)
    checkbox_mute = checkbox("checkbox_mute")
    checkbox_mute.rect = rect(24, 104, 220, 36)
    checkbox_mute.text = "全局静音"
    checkbox_ducking = checkbox("checkbox_ducking")
    checkbox_ducking.rect = rect(260, 104, 276, 36)
    checkbox_ducking.text = "说话时自动压低音乐"
    checkbox_ducking.checked = True
    panel_scene = panel("panel_scene")
    panel_scene.rect = rect(24, 156, 220, 140)
    radio_party = radiobutton("radio_party")
    radio_party.rect = rect(12, 12, 196, 32)
    radio_party.text = "聚会模式（全响）"
    radio_party.checked = True
    radio_cinema = radiobutton("radio_cinema")
    radio_cinema.rect = rect(12, 52, 196, 32)
    radio_cinema.text = "影院模式（重低音）"
    radio_sleep = radiobutton("radio_sleep")
    radio_sleep.rect = rect(12, 92, 196, 32)
    radio_sleep.text = "睡眠模式（柔和）"
    panel_scene.control_list.extend([radio_party, radio_cinema, radio_sleep])
    slider_master = slider("slider_master")
    slider_master.rect = rect(260, 160, 210, 36)
    slider_master.value = 75
    slider_bgm = slider("slider_bgm")
    slider_bgm.rect = rect(492, 156, 36, 140)
    slider_bgm.orientation = orientation.vertical
    slider_bgm.value = 60
    numeric_gain = numericupdown("numeric_gain")
    numeric_gain.rect = rect(260, 220, 210, 40)
    numeric_gain.minimum = -12.0
    numeric_gain.maximum = 12.0
    numeric_gain.step = 0.5
    numeric_gain.decimal_places = 1
    numeric_gain.value = 1.5
    progressbar_level = progressbar("progressbar_level")
    progressbar_level.rect = rect(24, 360, 512, 28)
    window_main.control_list.extend([label_summary, checkbox_mute, checkbox_ducking, panel_scene, slider_master, slider_bgm, numeric_gain, progressbar_level,])

    def refresh_mixer():
        state = "已静音" if checkbox_mute.checked else "正常播放"
        duck = "开启" if checkbox_ducking.checked else "关闭"
        progressbar_level.value = (0 if checkbox_mute.checked else ((slider_master.value * slider_bgm.value) // 100))
        label_summary.text = f"状态：{state} | 自动压低：{duck} | 增益：{numeric_gain.value:.1f} dB"

    checkbox_mute.on_checked_changed += lambda source, event: refresh_mixer()
    checkbox_ducking.on_checked_changed += lambda source, event: refresh_mixer()
    slider_master.on_value_changed += lambda source, event: refresh_mixer()
    slider_bgm.on_value_changed += lambda source, event: refresh_mixer()
    numeric_gain.on_value_changed += lambda source, event: refresh_mixer()
    refresh_mixer()
    window_main.show()
    run("vr_mixer")

if __name__ == "__main__":
    main()