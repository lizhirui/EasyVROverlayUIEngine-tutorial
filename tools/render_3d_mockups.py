from argparse import ArgumentParser
from functools import cache
import json
from math import cos, radians, sin
import os
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
SITE = Path(__file__).resolve().parents[1]
OUTPUT = ((SITE / "docs") / "public") / "images"
PARTS = (SITE / ".work") / "parts"
LOCALE_LIST = ("zh", "en", "ja")
SIZE = (2400, 1440)
CENTER = (1200.0, 760.0)
FOCAL = 1500.0
INK = "#eef7ff"
MUTED = "#adbed4"
BLUE = "#79baff"
CYAN = "#52d9e8"
MINT = "#7de5b4"
VIOLET = "#c7a8ff"
AMBER = "#ffd09a"
FONT_DIRECTORY = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts"
FONT_MAP = {"zh": ("msyh.ttc", "msyhbd.ttc"), "en": ("segoeui.ttf", "segoeuib.ttf"), "ja": ("YuGothM.ttc", "YuGothB.ttc"),}

class projected_window:
    def __init__(self, center, width, aspect, yaw = 0.0, pitch = 0.0, curve = 0.0):
        self.center = np.asarray(center, dtype = float)
        self.width = width
        self.height = width / aspect
        self.arc = radians(curve)
        turn = radians(yaw)
        tilt = radians(pitch)
        turn_matrix = np.asarray(((cos(turn), 0.0, sin(turn)), (0.0, 1.0, 0.0), (-sin(turn), 0.0, cos(turn))))
        tilt_matrix = np.asarray(((1.0, 0.0, 0.0), (0.0, cos(tilt), -sin(tilt)), (0.0, sin(tilt), cos(tilt))))
        self.basis = turn_matrix @ tilt_matrix

    def get_point(self, u, v):
        x = (u - 0.5) * self.width
        y = (0.5 - v) * self.height

        if self.arc:
            radius = self.width / self.arc
            angle = (u - 0.5) * self.arc
            x = radius * sin(angle)
            z = radius * (cos(angle) - 1.0)
        else:
            z = 0.0

        return self.center + (np.asarray((x, y, z)) @ self.basis.T)

    def get_screen_point(self, u, v):
        return project(self.get_point(u, v))

    def get_outline(self):
        sample = np.linspace(0.0, 1.0, 65)
        top = [self.get_screen_point(u, 0.0) for u in sample]
        bottom = [self.get_screen_point(u, 1.0) for u in reversed(sample)]
        return (top + bottom) + [top[0]]

    def cast_ray(self, ray):
        origin = (-self.center) @ self.basis
        direction = ray @ self.basis
        dx, dy, dz = np.moveaxis(direction, -1, 0)
        ox, oy, oz = origin

        if not self.arc:
            with np.errstate(divide = "ignore", invalid = "ignore"):
                depth = (-oz) / dz

            u = ((ox + (depth * dx)) / self.width) + 0.5
            v = 0.5 - ((oy + (depth * dy)) / self.height)
            return u, v, depth > 0.0

        radius = self.width / self.arc
        a = (dx * dx) + (dz * dz)
        b = 2.0 * ((ox * dx) + ((oz + radius) * dz))
        c = ((ox * ox) + ((oz + radius) ** 2.0)) - (radius * radius)
        discriminant = (b * b) - ((4.0 * a) * c)
        root = np.sqrt(np.maximum(0.0, discriminant))
        best_depth = np.full(dx.shape, np.inf)
        best_u = np.zeros(dx.shape)
        best_v = np.zeros(dx.shape)

        with np.errstate(divide = "ignore", invalid = "ignore"):
            for sign in (-1.0, 1.0):
                depth = ((-b) + (sign * root)) / (2.0 * a)
                local_x = ox + (dx * depth)
                local_z = oz + (dz * depth)
                angle = np.arctan2(local_x, local_z + radius)
                u = (angle / self.arc) + 0.5
                v = 0.5 - ((oy + (dy * depth)) / self.height)
                hit = ((((((discriminant >= 0.0) & (depth > 0.0)) & (depth < best_depth)) & (u >= 0.0)) & (u <= 1.0)) & (v >= 0.0)) & (v <= 1.0)
                best_depth[hit] = depth[hit]
                best_u[hit] = u[hit]
                best_v[hit] = v[hit]

        return best_u, best_v, np.isfinite(best_depth)

def project(point):
    x, y, z = point
    return CENTER[0] + ((FOCAL * x) / z), CENTER[1] - ((FOCAL * y) / z)

def make_ray(left, top, right, bottom):
    x, y = np.meshgrid(np.arange(left, right, dtype = float) + 0.5, np.arange(top, bottom, dtype = float) + 0.5)
    return np.stack(((x - CENTER[0]) / FOCAL, (CENTER[1] - y) / FOCAL, np.ones_like(x)), axis = -1)

def paint_window(image, source, window, edge = BLUE):
    outline = window.get_outline()
    point_array = np.asarray(outline)
    low = np.floor(point_array.min(axis = 0)).astype(int) - 2
    high = np.ceil(point_array.max(axis = 0)).astype(int) + 2
    left, top = np.maximum(low, (0, 0))
    right, bottom = np.minimum(high, SIZE)

    if (right <= left) or (bottom <= top):
        raise ValueError("Projected window is outside the image")

    u, v, forward = window.cast_ray(make_ray(left, top, right, bottom))
    mask = (((forward & (u >= 0.0)) & (u <= 1.0)) & (v >= 0.0)) & (v <= 1.0)
    u = np.clip(np.nan_to_num(u[mask]), 0.0, 1.0)
    v = np.clip(np.nan_to_num(v[mask]), 0.0, 1.0)
    source_array = np.asarray(source.convert("RGBA"))
    x = u * (source.width - 1)
    y = v * (source.height - 1)
    x0, y0 = x.astype(int), y.astype(int)
    x1 = np.minimum(x0 + 1, source.width - 1)
    y1 = np.minimum(y0 + 1, source.height - 1)
    fx, fy = (x - x0)[: , None], (y - y0)[: , None]
    upper = (source_array[y0, x0] * (1.0 - fx)) + (source_array[y0, x1] * fx)
    lower = (source_array[y1, x0] * (1.0 - fx)) + (source_array[y1, x1] * fx)
    patch = np.zeros((bottom - top, right - left, 4), dtype = np.uint8)
    patch[mask] = np.uint8((upper * (1.0 - fy)) + (lower * fy))
    image.alpha_composite(Image.fromarray(patch), (int(left), int(top)))
    ImageDraw.Draw(image).line(outline, fill = edge, width = 3, joint = "curve")

@cache
def get_font(locale, size, bold = False):
    item = FONT_MAP[locale][int(bold)]
    return ImageFont.truetype(str(FONT_DIRECTORY / item), size)

def tr(locale, zh, en, ja):
    return (zh, en, ja)[LOCALE_LIST.index(locale)]

def make_background():
    y, x = np.ogrid[0: SIZE[1], 0: SIZE[0]]
    glow = np.exp(-((((x - 1180.0) / 1150.0) ** 2.0) + (((y - 470.0) / 1000.0) ** 2.0)))
    rgb = np.stack((10.0 + (11.0 * glow), 17.0 + (20.0 * glow), 30.0 + (31.0 * glow)), axis = -1).astype(np.uint8)
    image = Image.fromarray(rgb).convert("RGBA")
    draw = ImageDraw.Draw(image)

    for x in np.linspace(-19.0, 19.0, 65):
        draw.line((project((x, -1.7, 1.65)), project((x, -1.7, 34.0))), fill = "#213249", width = 2)

    for z in np.geomspace(1.75, 32.0, 19):
        draw.line((project((-24.0, -1.7, z)), project((24.0, -1.7, z))), fill = "#24364d", width = 2)

    return image

def put_header(image, locale, title, detail):
    draw = ImageDraw.Draw(image)
    draw.text((88, 66), title, fill = INK, font = get_font(locale, 58, True))
    draw.text((92, 151), detail, fill = MUTED, font = get_font(locale, 25))
    draw.line((92, 205, 2308, 205), fill = "#394c63", width = 2)

def put_label(draw, locale, label, position, color = CYAN, detail = None):
    x, y = position
    heading = get_font(locale, 32, True)
    body = get_font(locale, 25)
    headline_box = draw.textbbox((0, 0), label, font = heading, anchor = "lt")
    detail_box = draw.textbbox((0, 0), detail, font = body, anchor = "lt") if detail else (0, 0, 0, 0)
    width = max(headline_box[2], detail_box[2]) + 46
    height = (headline_box[3] + 22) if (detail is None) else ((headline_box[3] + detail_box[3]) + 33)

    if ((x + width) > (SIZE[0] - 24)) or ((y + height) > (SIZE[1] - 24)):
        raise ValueError(f"Annotation exceeds image bounds: {label}")

    draw.rounded_rectangle((x, y, x + width, y + height), radius = 13, fill = "#101d2c", outline = "#384d66", width = 2)
    draw.line((x + 11, y + 15, x + 11, (y + height) - 15), fill = color, width = 3)
    draw.text((x + 22, y + 11), label, fill = color, font = heading, anchor = "lt")

    if detail:
        draw.text((x + 22, (y + 22) + headline_box[3]), detail, fill = MUTED, font = body, anchor = "lt")

def put_ray(draw, point_list, color, width = 6):
    draw.line(point_list, fill = color, width = width, joint = "curve")
    center = point_list[-1]
    x, y = center
    draw.ellipse((x - 11, y - 11, x + 11, y + 11), outline = color, width = 3)
    draw.ellipse((x - 4, y - 4, x + 4, y + 4), fill = INK)

def open_image(path):
    with Image.open(path) as source:
        return source.convert("RGBA")

def make_hero(locale, folder):
    image = make_background()
    put_header(image, locale, tr(locale, "VR空间工作区", "A workspace in VR", "VR空間のワークスペース"), tr(locale, "主窗口与曲面副屏独立摆放，双手激光分别指向窗口。", "A main window and a curved companion sit at independent poses.", "メインウィンドウと湾曲したサブ画面を、別々の位置に配置します。",),)
    main = open_image(folder / "desktop.png")
    secondary = open_image(folder / "file_manager.png")
    side_window = projected_window((1.93, 0.41, 5.15), 2.45, secondary.width / secondary.height, yaw = -16.0, curve = 64.0)
    main_window = projected_window((-1.02, -0.12, 4.2), 3.22, main.width / main.height, yaw = 8.0)
    paint_window(image, secondary, side_window, VIOLET)
    paint_window(image, main, main_window, BLUE)
    draw = ImageDraw.Draw(image)
    put_label(draw, locale, tr(locale, "主窗口", "Main window", "メインウィンドウ"), (314, 237), BLUE)
    put_label(draw, locale, tr(locale, "曲面副屏", "Curved companion", "湾曲したサブ画面"), (1600, 270), VIOLET)
    put_ray(draw, [(377, 1360), main_window.get_screen_point(0.60, 0.76)], CYAN)
    put_ray(draw, [(2070, 1330), side_window.get_screen_point(0.58, 0.67)], VIOLET)
    return image

def make_anchors(locale):
    image = make_background()
    put_header(image, locale, tr(locale, "五种空间参考系", "Five spatial anchors", "5つの空間アンカー"), tr(locale, "参考系决定窗口跟随的位置和朝向。", "The selected anchor controls how the window follows position and rotation.", "アンカーによって、ウィンドウが追従する位置と向きが決まります。",),)
    draw = ImageDraw.Draw(image)
    draw.ellipse((954, 744, 1450, 1018), outline = "#536f8a", width = 3)
    draw.line((1200, 548, 1200, 1070), fill = "#56748c", width = 4)
    draw.rounded_rectangle((1020, 492, 1380, 670), radius = 56, fill = "#182b40", outline = BLUE, width = 5)
    draw.rounded_rectangle((1054, 528, 1346, 629), radius = 34, outline = "#85adc7", width = 3)
    draw.arc((1108, 638, 1292, 812), 15, 165, fill = MINT, width = 5)
    draw.line((1065, 780, 996, 985, 1404, 985, 1335, 780), fill = "#6e9caf", width = 6)

    for x, color in ((809, CYAN), (1591, VIOLET)):
        draw.ellipse((x - 51, 745, x + 51, 847), outline = color, width = 5)
        draw.rounded_rectangle((x - 27, 794, x + 27, 928), radius = 19, fill = "#182b40", outline = color, width = 4)

    draw.ellipse((661, 593, 695, 627), outline = AMBER, width = 3)
    draw.line((678, 586, 678, 633), fill = AMBER, width = 2)
    draw.line((654, 610, 704, 610), fill = AMBER, width = 2)
    sample_list = (("World", tr(locale, "固定于SteamVR跟踪空间", "Fixed in SteamVR tracking space", "SteamVRのトラッキング空間に固定",), AMBER, (150, 295), [(420, 400), (567, 518), (678, 610)],), ("Head", tr(locale, "跟随头显位置与旋转", "Follows the headset pose", "ヘッドセットの位置と回転に追従"), BLUE, (1640, 295), [(1670, 400), (1515, 520), (1380, 568)],), ("Left", tr(locale, "跟随左手柄", "Follows the left controller", "左コントローラーに追従"), CYAN, (145, 884), [(395, 918), (631, 918), (809, 832)],), ("Right", tr(locale, "跟随右手柄", "Follows the right controller", "右コントローラーに追従"), VIOLET, (1776, 884), [(1776, 918), (1720, 918), (1591, 832)],), ("Body", tr(locale, "跟随身体平移，朝向按校准基准保留", "Follows translation with a calibrated heading", "体の移動に追従し、校正した向きを維持",), MINT, (956, 1138), [(1200, 1150), (1200, 1032), (1200, 937)],),)

    for name, detail, color, position, points in sample_list:
        put_ray(draw, points, color, 3)
        put_label(draw, locale, name, position, color, detail)

    return image

def make_curvature(locale, folder):
    image = make_background()
    put_header(image, locale, tr(locale, "窗口曲率与双手控制环", "Window curvature and two-hand rotation", "ウィンドウの曲率と両手回転リング",), tr(locale, "四边中点为长条，四角为方块。双手各侧握一个控制点后开始旋转。", "Hold a grip on two perimeter blocks to rotate around a constrained axis.", "左右のグリップで外周の2つのブロックをつかみ、軸を制限して回転します。",),)
    source = open_image(folder / "demo_controls.png")
    window = projected_window((-0.62, 0.12, 4.9), 2.62, source.width / source.height, yaw = -9.0, pitch = 11.0, curve = 82.0)
    paint_window(image, source, window, BLUE)
    draw = ImageDraw.Draw(image)
    lower_left = window.get_screen_point(0.045, 0.948)
    lower_right = window.get_screen_point(0.953, 0.948)
    put_ray(draw, [(471, 1245), (600, 1210), lower_left], CYAN, 4)
    put_ray(draw, [(1330, 1240), (1315, 1200), lower_right], VIOLET, 4)
    put_label(draw, locale, tr(locale, "曲率手柄", "Curvature handle", "曲率ハンドル"), (340, 1260), CYAN)
    put_label(draw, locale, tr(locale, "缩放手柄", "Scale handle", "拡大縮小ハンドル"), (1240, 1260), VIOLET)
    put_label(draw, locale, tr(locale, "窗口局部坐标轴", "Window-local axes", "ウィンドウのローカル軸"), (1797, 430), BLUE,)
    anchor = np.array((2.98, -0.06, 5.35))
    origin = project(anchor)

    for index, (label, color) in enumerate((("X", "#ff929e"), ("Y", MINT), ("Z", BLUE))):
        axis = window.basis[: , index] * (0.72 if (index != 2) else 1.10)
        target = project(anchor + axis)
        delta = np.asarray(target) - origin
        unit = delta / np.linalg.norm(delta)
        cross = np.asarray((-unit[1], unit[0]))
        draw.line((origin, target), fill = color, width = 6)
        draw.polygon((tuple(target), tuple((target - (24 * unit)) + (10 * cross)), tuple((target - (24 * unit)) - (10 * cross)),), fill = color,)
        offset = 24.0 * unit
        draw.text(tuple(target + offset), label, anchor = "mm", font = get_font("en", 32, True), fill = color)

    return image

def make_input(locale, folder, part):
    image = make_background()
    put_header(image, locale, tr(locale, "输入区的三层堆叠", "The text input stack", "文字入力の3段構成"), tr(locale, "输入条、候选窗与虚拟键盘沿输入区中心线排列。", "The switch bar, candidates, and keyboard share the input area's center line.", "入力バー、変換候補、仮想キーボードは入力欄の中心線に沿って配置されます。",),)
    input_box = open_image(part / "input_box.png")
    component_list = (input_box, open_image(part / "input_bar.png"), open_image(part / "candidate.png"), open_image(folder / "layout_keyboard.png"),)
    label_list = (tr(locale, "应用输入区", "Application input area", "アプリの入力欄"), tr(locale, "输入条", "Input switch bar", "入力バー"), tr(locale, "IME候选窗", "IME candidates", "IME変換候補"), tr(locale, "虚拟键盘", "Virtual keyboard", "仮想キーボード"),)
    max_width = max(value.width for value in component_list)
    height_sum = sum(value.height for value in component_list)
    gap = 26
    scale = min(4.3 / max_width, 2.65 / (height_sum + (3 * gap)))
    origin_top = 1.38
    path = []
    position = origin_top
    draw = ImageDraw.Draw(image)
    center_top = project((-0.63, origin_top + 0.10, 4.4))
    center_bottom = project((-0.63, (origin_top - (scale * (height_sum + (3 * gap)))) - 0.10, 4.4))

    for index in range(33):
        value = index / 32
        y = center_top[1] + ((center_bottom[1] - center_top[1]) * value)
        x = center_top[0]
        draw.line((x - 4, y, x + 4, y), fill = "#a8d7ed", width = 2)

    for index, component in enumerate(component_list):
        height = component.height * scale
        window = projected_window((-0.63, position - (height * 0.5), 4.4), component.width * scale, component.width / component.height,)
        color = (BLUE, CYAN, VIOLET, MINT)[index]
        paint_window(image, component, window, color)
        edge = window.get_screen_point(1.0, 0.5)
        path.append((label_list[index], edge, color))
        position -= height + (gap * scale)

    draw = ImageDraw.Draw(image)
    previous_y = 0

    for label, edge, color in path:
        y = max(round(edge[1]) - 25, previous_y + 70)
        previous_y = y
        draw.line((edge, (1740, edge[1]), (1760, y + 26)), fill = color, width = 3)
        put_label(draw, locale, label, (1765, y), color)

    return image

def make_designer(locale, folder, part):
    image = make_background()
    put_header(image, locale, tr(locale, "窗体设计器工作区", "The Form Designer workspace", "フォームデザイナーの作業領域"), tr(locale, "用工具箱选择控件，在画布布局，再通过属性栏编辑选中项。", "Choose a control from the toolbox, place it on the canvas, and edit its properties.", "ツールボックスから選び、キャンバスに配置して、プロパティを編集します。",),)
    source = open_image(folder / "form_designer.png")
    region_map = json.loads((part / "designer_regions.json").read_text(encoding = "utf-8"))
    ratio = min(2120 / source.width, 1000 / source.height)
    width, height = round(source.width * ratio), round(source.height * ratio)
    offset_x = (SIZE[0] - width) // 2
    offset_y = 237
    image.alpha_composite(source.resize((width, height), Image.Resampling.LANCZOS), (offset_x, offset_y))
    draw = ImageDraw.Draw(image)
    color_list = (AMBER, CYAN, BLUE, MINT)
    label_list = (tr(locale, "menubar与toolbar", "Menus and toolbar", "メニューとツールバー"), tr(locale, "控件工具箱", "Control toolbox", "コントロールツールボックス"), tr(locale, "设计画布", "Design canvas", "デザインキャンバス"), tr(locale, "属性栏", "Properties", "プロパティ"),)

    for index, key in enumerate(("command", "toolbox", "canvas", "property")):
        left, top, width, height = region_map[key]
        x0 = offset_x + round(left * ratio)
        y0 = offset_y + round(top * ratio)
        x1 = min(SIZE[0] - 1, x0 + round(width * ratio))
        y1 = min(SIZE[1] - 1, y0 + round(height * ratio))
        color = color_list[index]
        draw.rectangle((x0 + 3, y0 + 2, x1 - 3, y1 - 2), outline = color, width = 5)
        put_label(draw, locale, label_list[index], (150 + (index * 550), 1301), color)

    return image

def render_locale(locale, directory, part_directory):
    folder = directory / locale
    parts = part_directory / locale
    renderer_map = {"vr_hero_workspace": lambda: make_hero(locale, folder), "vr_spatial_anchors": lambda: make_anchors(locale), "vr_curvature_and_handles": lambda: make_curvature(locale, folder), "vr_input_stack": lambda: make_input(locale, folder, parts), "vr_designer_annotated": lambda: make_designer(locale, folder, parts),}

    for name, render in renderer_map.items():
        image = render().convert("RGB")
        target = folder / f"{name}.png"
        image.save(target)
        print(f"{locale}/{target.name}\t{image.width}x{image.height}")

def run():
    parser = ArgumentParser(description = "Project WARP screenshots onto planar and cylindrical surfaces and render localized diagrams.")
    parser.add_argument("--images", type = Path, default = OUTPUT)
    parser.add_argument("--parts", type = Path, default = PARTS)
    parser.add_argument("--locale", choices = LOCALE_LIST, action = "append")
    option = parser.parse_args()

    for locale in dict.fromkeys(option.locale or LOCALE_LIST):
        render_locale(locale, option.images, option.parts)

if __name__ == "__main__":
    run()