import math
import time
from easyvrui import (blank, button, control, font, rect, reference_object, reference_object_type, run, screen, startup_position, vec3, window,)

class mic_meter_control(control):
    def __init__(self, name):
        super().__init__(name)
        self._level = 0.4
        self._font = font("Segoe UI", 16, bold = True)

    def set_level(self, level):
        self._level = max(0.0, min(1.0, level))
        self.invalidate()

    def render(self, context):
        super().render(context)
        left, top, width, height = context.get_rectangle(self)
        context.fill_rounded_rectangle((left, top, width, height), 8, 8, 0x162738FF)
        bar_width = max(0.0, (width - 16) * self._level)
        context.fill_rounded_rectangle((left + 8, top + 8, bar_width, height - 16), 6, 6, 0x4CAF50FF)
        context.draw_text(f"MIC {int(self._level * 100)}%", self._font, (left, top, width, height), 0xFFFFFFFF, center = True)

def main():
    window_wrist = window("window_wrist")
    window_wrist.title = "左手腕 HUD"
    window_wrist.rect = rect(0, 0, 260, 220)
    window_wrist.physical_scale = 0.65
    window_wrist.startup_position = startup_position.none
    window_wrist.reference_object = reference_object(reference_object_type.left)
    window_wrist.position = vec3(-0.08, 0.08, -0.10)
    window_wrist.rotation = vec3(-35.0, 0.0, 0.0)
    blank_meter = blank("blank_meter")
    blank_meter.rect = rect(16, 64, 228, 56)
    meter_mic = mic_meter_control("meter_mic")
    meter_mic.rect = blank_meter.rect
    button_toggle_screen = button("button_toggle_screen")
    button_toggle_screen.rect = rect(16, 134, 228, 40)
    button_toggle_screen.text = "显示/隐藏弯曲副屏"
    window_subscreen = window("window_subscreen")
    window_subscreen.title = "弧面电脑副屏"
    window_subscreen.rect = rect(0, 0, 960, 560)
    window_subscreen.curvature = 0.65
    window_subscreen.reference_object = reference_object(reference_object_type.body)
    screen_main = screen("screen_main")
    screen_main.rect = rect(16, 64, 928, 480)
    screen_main.screen_id = 0
    window_subscreen.control_list.add(screen_main)

    def button_toggle_screen_click(source, event):
        if window_subscreen.visible:
            window_subscreen.hide()
        else:
            window_subscreen.show()

    button_toggle_screen.on_click += button_toggle_screen_click
    window_wrist.control_list.add(meter_mic)
    window_wrist.control_list.add(button_toggle_screen)
    window_wrist.show()
    run("vrc_wrist_hud")

if __name__ == "__main__":
    main()