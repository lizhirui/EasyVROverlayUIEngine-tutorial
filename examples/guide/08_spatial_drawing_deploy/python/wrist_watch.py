from easyvrui import (control, drawing_path, font, rect, reference_object_type, run, startup_position, vec3, window,)

class wrist_dial_control(control):
    def __init__(self, name):
        super().__init__(name)
        self.label_text = "12:00"
        self.accent_color = 0x38BDF8FF

    def render(self, context):
        left, top, width, height = context.rectangle
        cx = left + (width * 0.5)
        cy = top + (height * 0.5)
        radius = min(width, height) * 0.44
        bg_color = 0x1E3A5FFF if context.is_hovered(self) else 0x0F172AFF
        context.fill_circle(cx, cy, radius, bg_color)
        context.draw_circle(cx, cy, radius, self.accent_color, 3.0)
        pointer = drawing_path()
        pointer.move_to(cx, cy).line_to(cx, cy - (radius * 0.65))
        context.outline_path(pointer, 0xFACC15FF, 3.0)
        context.draw_text(self.label_text, font("Segoe UI", 22, True, False), (left, cy + 12.0, width, 34.0), 0xFFFFFFFF, True,)

def main():
    window_main = window("window_main")
    window_main.rect = rect(0, 0, 220, 220)
    window_main.show_title_bar = False
    window_main.startup_position = startup_position.none
    window_main.reference_object = reference_object_type.left
    window_main.physical_scale = 0.5
    window_main.curvature = 1.2
    window_main.position = vec3(-0.05, 0.06, 0.08)
    window_main.rotation = vec3(-45.0, 20.0, 0.0)
    dial_watch = wrist_dial_control("dial_watch")
    dial_watch.rect = rect(0, 0, 220, 220)

    def dial_watch_click(source, event):
        if window_main.reference_object.type == reference_object_type.left:
            window_main.reparent(reference_object_type.world, keep_world = True)
            dial_watch.accent_color = 0x4ADE80FF
        else:
            window_main.reference_object = reference_object_type.left
            window_main.position = vec3(-0.05, 0.06, 0.08)
            window_main.rotation = vec3(-45.0, 20.0, 0.0)
            dial_watch.accent_color = 0x38BDF8FF

        dial_watch.invalidate()

    dial_watch.on_click += dial_watch_click
    window_main.control_list.add(dial_watch)
    window_main.show()
    run("wrist_watch")

if __name__ == "__main__":
    main()