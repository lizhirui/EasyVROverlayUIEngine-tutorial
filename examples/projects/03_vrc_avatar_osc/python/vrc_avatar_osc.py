import json
import math
import os
import socket
import struct
from pathlib import Path
from easyvrui import (button, checkbox, color_dialog, dialog_result, grid, grid_column, label, numericupdown, orientation, rect, run, slider, textbox, window,)

def main():
    OSC_AVATAR_ROOT = Path(os.path.expandvars(r"%USERPROFILE%\AppData\LocalLow\VRChat\VRChat\OSC"))

    def send_osc_param(param_name, value):
        address = f"/avatar/parameters/{param_name}".encode("utf-8") + b"\x00"
        address += b"\x00" * ((4 - (len(address) % 4)) % 4)

        if isinstance(value, bool):
            packet = address + (b",T\x00\x00" if value else b",F\x00\x00")
        elif isinstance(value, int):
            packet = (address + b",i\x00\x00") + struct.pack(">i", value)
        else:
            packet = (address + b",f\x00\x00") + struct.pack(">f", float(value))

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            sock.sendto(packet, ("127.0.0.1", 9000))
        finally:
            sock.close()

    class preset_dialog(window):
        def __init__(self):
            super().__init__("preset_dialog")
            self.title = "新建参数预设"
            self.rect = rect(0, 0, 380, 210)
            self.label_name = label("label_name")
            self.label_name.rect = rect(24, 68, 110, 36)
            self.label_name.text = "预设名称："
            self.textbox_name = textbox("textbox_name")
            self.textbox_name.rect = rect(140, 68, 210, 36)
            self.textbox_name.text = "可爱日常模式"
            self.button_ok = button("button_ok")
            self.button_ok.rect = rect(80, 134, 100, 40)
            self.button_ok.text = "保存"
            self.button_cancel = button("button_cancel")
            self.button_cancel.rect = rect(200, 134, 100, 40)
            self.button_cancel.text = "取消"
            self.button_ok.on_click += lambda s, e: setattr(self, "dialog_result", dialog_result.ok)
            self.button_cancel.on_click += lambda s, e: setattr(self, "dialog_result", dialog_result.cancel)

            for item in (self.label_name, self.textbox_name, self.button_ok, self.button_cancel):
                self.control_list.add(item)

    def load_avatar_params():
        if OSC_AVATAR_ROOT.is_dir():
            for json_file in OSC_AVATAR_ROOT.glob("*/Avatars/*.json"):
                data = json.loads(json_file.read_text(encoding = "utf-8-sig"))
                rows = []

                for item in data.get("parameters", []):
                    if "input" in item:
                        rows.append([item["name"], item["input"].get("type", "Float"), "0"])

                if rows:
                    return rows

        return [["EarFlop", "Float", "0.5"], ["TailWag", "Bool", "1"], ["CoatToggle", "Int", "2"]]

    window_main = window("window_main")
    window_main.title = "Avatar OSC 调试与预设面板"
    window_main.rect = rect(0, 0, 740, 480)
    param_rows = load_avatar_params()
    grid_params = grid("grid_params")
    grid_params.rect = rect(20, 64, 460, 290)
    grid_params.column_list = [grid_column("参数名", 200), grid_column("类型", 100), grid_column("当前值", 140),]

    def parse_parameter_value(param_type, text):
        if param_type == "Bool":
            if text not in ("0", "1", "true", "false"):
                raise ValueError(text)

            return text in ("1", "true")

        if param_type == "Int":
            number = int(text)

            if not ((-(2 ** 31)) <= number < (2 ** 31)):
                raise ValueError(text)

            return number

        number = float(text)

        if (not math.isfinite(number)) or (abs(number) > 3.402823466e38):
            raise ValueError(text)

        return number

    def validate_param(cell, value):
        if cell.column != 2:
            return (False, "仅允许修改第3列数值")

        param_type = param_rows[cell.row][1]
        text = str(value).strip()

        try:
            parse_parameter_value(param_type, text)
        except ValueError:
            return (False, f"请输入合法的 {param_type} 数值")

        return True

    def write_param(row, column, value):
        param_rows[row][column] = str(value)
        return True

    grid_params.set_data_provider(len(param_rows), lambda r, c: param_rows[r][c], write_param)
    grid_params.set_edit_validator(validate_param)
    checkbox_live = checkbox("checkbox_live")
    checkbox_live.rect = rect(500, 68, 220, 36)
    checkbox_live.text = "实时发送OSC (9000)"
    slider_float = slider("slider_float")
    slider_float.rect = rect(500, 120, 210, 36)
    slider_float.orientation = orientation.horizontal
    slider_float.minimum = 0
    slider_float.maximum = 100
    slider_float.value = 50
    numeric_step = numericupdown("numeric_step")
    numeric_step.rect = rect(500, 174, 210, 38)
    numeric_step.minimum = 0.0
    numeric_step.maximum = 1.0
    numeric_step.step = 0.05
    numeric_step.decimal_places = 2
    numeric_step.value = 0.50
    button_preset = button("button_preset")
    button_preset.rect = rect(500, 232, 210, 42)
    button_preset.text = "保存为预设..."
    button_theme = button("button_theme")
    button_theme.rect = rect(500, 288, 210, 42)
    button_theme.text = "切换面板背景色"
    label_status = label("label_status")
    label_status.rect = rect(20, 376, 700, 36)
    label_status.text = "双击表格数值列，或拖动右侧滑块调试参数"

    def publish_parameter(row):
        if (row < 0) or (not checkbox_live.checked):
            return

        name, param_type, value = param_rows[row]

        try:
            send_osc_param(name, parse_parameter_value(param_type, value))
            label_status.text = f"OSC: {name} = {value}"
        except (OSError, ValueError, OverflowError):
            label_status.text = "OSC发送失败"

    def slider_float_changed(source, event):
        numeric_step.value = source.value / 100.0

    def numeric_step_changed(source, event):
        row = grid_params.selected_index

        if (row < 0) or (param_rows[row][1] != "Float"):
            return

        param_rows[row][2] = f"{source.value:.2f}"
        grid_params.refresh_data()
        publish_parameter(row)

    def grid_params_edit_committed(source, event):
        publish_parameter(event.row)

    def button_preset_click(source, event):
        dlg = preset_dialog()

        if dlg.show_dialog(window_main) == dialog_result.ok:
            name = dlg.textbox_name.text.strip()

            if not name:
                label_status.text = "无法保存预设"
                return

            path = ((Path.home() / "easyvrui") / "tutorial") / "avatar_presets.jsonl"

            try:
                path.parent.mkdir(parents = True, exist_ok = True)

                with path.open("a", encoding = "utf-8", newline = "\n") as output:
                    record = {"name": name, "values": {row[0]: row[2] for row in param_rows}}
                    output.write(json.dumps(record, ensure_ascii = False) + "\n")
            except OSError:
                label_status.text = "无法保存预设"
                return

            label_status.text = f"已保存预设：{dlg.textbox_name.text}"

    def button_theme_click(source, event):
        picked = color_dialog(window_main.background_color, "选择面板背景色", 0x0D1624FF, window_main)

        if picked is not None:
            window_main.background_color = picked

    slider_float.on_value_changed += slider_float_changed
    numeric_step.on_value_changed += numeric_step_changed
    grid_params.on_edit_committed += grid_params_edit_committed
    button_preset.on_click += button_preset_click
    button_theme.on_click += button_theme_click

    for item in (grid_params, checkbox_live, slider_float, numeric_step, button_preset, button_theme, label_status,):
        window_main.control_list.add(item)

    window_main.show()
    run("vrc_avatar_osc")

if __name__ == "__main__":
    main()