# Spatial Positioning, Custom Drawing, and Desktop Registration

The controls used in the previous chapters have built-in default appearances, and windows are placed in the `world` reference frame by default. This chapter introduces how to achieve custom drawing using `render_context` and `drawing_path`. Use `reference_object` and `curvature` to fix the window on the left wrist (`left` reference frame), and register it with the Desktop launcher through `.easyvrui`.

---

## I. `window` Spatial Positioning, `vec3` / `quat` / `pose`, and `blank`

`world` is used to fix the space. `head` follows the headset, `body` follows the body's translation while maintaining calibration orientation, and `left` and `right` follow the left and right handles, respectively. Use `reference_object` to select the reference object, with local offsets configured in meters. Tracking devices and pose are provided by SteamVR runtime.

![: A schematic representation of the five spatial reference objects in SteamVR.](/images/en/vr_spatial_anchors.png)

The following figure shows the configuration view drawn with WARP. Actual positioning is done using `get_world_transform()` or the result read by Python's `world_transform`, combined with `is_tracking_available()` to confirm that the reference object is available.

![Five Space Reference Objects Configuration Views](/images/en/spatial_anchor_config.png)

### 1. `window` Space and Appearance Properties/Methods

|Properties/Methods|Type ( Python / C++)|Default|Reading and Writing|Description and Notes|
|---|---|---|---|---|
|`reference_object`|`reference_object` (Python also accepts enumeration or strings)|`world`|Reading and Writing|Spatial Anchors: `world` (World Fixed), `body` (Follows Body), `head` (Follows Headset), `left` (Left Handheld), `right` (Right Handheld).|
|`position`|`vec3` / `vec3_t`|`vec3(0, 0, 0)`|Reading and Writing|The offset of the window's **upper left corner**relative to the reference target, in**meters**.|
|`rotation`|`vec3` / `vec3_t`|`vec3(0, 0, 0)`|Reading and Writing|XYZ Euler angles (in **degrees**, in the order `Rz * Ry * Rx`).|
|`physical_scale`|`float` / `double`|`1.0`|Reading and Writing|Physical scaling factor (must be a positive finite number). When `1.0`, `1` logical pixels = `1毫米`!|
|`physical_width` / `physical_height`|`float` / `double`|Calculated Values|Read-only|Actual physical width and height (meters) = `rect.width * physical_scale / 1000.0`.|
|`curvature`|`float` / `double`|`0.0`|Reading and Writing|Cylindrical curvature (in `m⁻¹`), with `0` being a plane; must satisfy `k >= 0` and `k * physical_width < 2π` (the upper limit for handle interaction is `160°`).|
|`startup_position`|`startup_position` / `startup_position_t`|`center`|Reading and Writing|`center` automatically centers in front of the headset/source window when first displayed; when setting `position` to bind to the wrist, make sure to change it to `none`!|
|`tracking_mode_set`|`set[reference_object_type]`|Five Full Sets|Reading and Writing|Title bar: `⊕` button optional mode set; set it to an empty set for `set()` to hide the toggle button.|
|`show_title_bar` / `show_close_button` / `movable` / `resizable` / `curvature_adjustable`|`bool`|Full `True`|Reading and Writing|Title bar, close button, grab movement, bottom right zoom, bottom left curvature handle switch.|
|`reparent(ref, keep_world = False)`|Method|—|—|Switch reference frames; `keep_world = True` can keep the window in place during the instant when the anchor point changes!|
|`center_at_view(distance) -> bool`|Method|—|—|Drag the window directly to the center at `distance` meters ahead of the current line of sight.|
|`world_transform`（C++：`get_world_transform()`）|`pose \| None` / `optional<pose_t>`|—|Read-only|Return the **center point** of the window to its current position in world space at `pose` (return to `None` if tracking is unavailable).|

### 2. `vec3`, `quat`, `pose`, and `blank`

- **`vec3(x, y, z)`**: Supports `+` / `-` / scalar `*`, `calculate_dot_product`, `calculate_cross_product`, `length`, `normalized`.
- **`quat(x, y, z, w)`**: Default unit rotation is `(0,0,0,1)`, supports combinations of `*`, `euler`, `rotate(v)`, `slerp(target, t)`, `create_from_euler(angles)`, `create_from_axis_angle(axis, angle)`.
- **`pose(position, rotation)`**: `a * b` (Python also supports `a @ b`), `inverse`, `matrix`, `transform_point(v)`.
- **`blank(name)`**: Inherits pure rectangular placeholder objects from `control` (only retain `name`/`rect` and geometric/release events; accessing `visible`/`enabled`/`render` will throw `AttributeError`).

---

## II. Common drawing interfaces for `render_context` and `drawing_path`

During drawing, first obtain the target area of the control through `get_rectangle()`, then calculate the local position using normalized data. In the figure below, the drawing control uses `fill_rounded_rectangle()` for the background, `draw_line()` to connect sampling points, and `push_clip()` and `pop_clip()` to limit the drawing boundaries. `invalidate()` is called only when data changes or the animation progresses, and submission is scheduled by the SDK.

![customizes the WARP rendering effect for sampled polylines with](/images/en/spatial_custom_drawing.png)

Deriving from `control` and overriding `render(self, context)` (or C++ `render(render_context &context) const override`), you can use `render_context` for drawing:

|Common methods|Purpose|
|---|---|
|`context.rectangle` / `get_rectangle(item)`|Get the current control's drawn rectangle `(left, top, width, height)`.|
|`is_hovered(item)` / `is_focused(item)`|Query the hover and focus states for easy highlighting effects.|
|`fill(rect, color)` / `outline(rect, color, thickness=1.0)`|Fill or stroke a rectangle with color as an integer `0xRRGGBBAA`.|
|`fill_rounded_rectangle(rect, rx, ry, color)` / `outline_rounded_rectangle(...)`|Rounded rectangles.|
|`fill_circle(cx, cy, r, color)` / `draw_circle(cx, cy, r, color, thickness=1.0)`|Fill circles and round borders.|
|`fill_ellipse` / `outline_ellipse` / `draw_line`|Ellipses and line segments.|
|`draw_text(text, font, rect, color, center=False)` / `measure(text, font)`|Draw text and measure text width.|
|`draw_image(img, rect, opacity=1.0)` / `draw_screen(id, rect)`|Draw images or real-time display screens.|
|`fill_path(path, color)` / `outline_path(path, color, thickness=1.0)`|Draw `drawing_path` vector paths.|
|`push_clip(rect)` / `pop_clip()`|Rectangular clipping and pushing stack items (must be called in pairs).|

**`drawing_path`**: Supports chained calls of `move_to(x, y)`, `line_to(x, y)`, `quadratic_to(...)`, `cubic_to(...)`, `arc_to(...)`, `close()`, with `fill_rule` optional `even_odd` or `non_zero`.

---

## III. Step-by-step Implementation: "Left Wrist Small Dial and Mounting on Desktop"

### Step 1: Derive `control`, use `render_context` and `drawing_path` to create a dial control

::: code-group
```python [Python（第1步）]
import math
from easyvrui import control, drawing_path, font, rect, run, window

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
        context.draw_text(self.label_text, font("Segoe UI", 22, True, False), (left, cy + 12.0, width, 34.0), 0xFFFFFFFF, True)

window_main = window("window_main")
window_main.rect = rect(0, 0, 220, 220)
dial_watch = wrist_dial_control("dial_watch")
dial_watch.rect = rect(0, 0, 220, 220)
window_main.control_list.add(dial_watch)
window_main.show()
run("wrist_watch")
```

```cpp [C++（第1步）]
#include <algorithm>
#include <easyvrui.h>
#include <memory>

using namespace std;

class wrist_dial_control : public easyvrui::control
{
    public:
        explicit wrist_dial_control(const u32string &name) : easyvrui::control(name)
        {
        }

    protected:
        void render(easyvrui::render_context &context) const override
        {
            auto rc = context.get_rectangle(*this);
            double cx = rc.left + (rc.width * 0.5);
            double cy = rc.top + (rc.height * 0.5);
            double radius = min(rc.width, rc.height) * 0.44;
            uint32_t bg = context.is_hovered(*this) ? 0x1E3A5FFFu : 0x0F172AFFu;
            context.fill_circle(cx, cy, radius, bg);
            context.draw_circle(cx, cy, radius, 0x38BDF8FFu, 3.0);
            drawing_path pointer;
            pointer.move_to(cx, cy).line_to(cx, cy - (radius * 0.65));
            context.outline_path(pointer, 0xFACC15FFu, 3.0);
            context.draw_text(U"12:00", easyvrui::font_t{U"Segoe UI", 22u, true, false}, easyvrui::render_rectangle_t{rc.left, cy + 12.0, rc.width, 34.0}, 0xFFFFFFFFu, true);
        }
};

int main()
{
    auto window_main = make_shared<easyvrui::window>(U"window_main");
    window_main->set_rect(easyvrui::rectangle_t{0u, 0u, 220u, 220u});
    auto dial_watch = make_shared<wrist_dial_control>(U"dial_watch");
    dial_watch->set_rect(easyvrui::rectangle_t{0u, 0u, 220u, 220u});
    window_main->get_control_list().add(dial_watch);
    window_main->show();
    easyvrui::run(U"wrist_watch");
    return 0;
}
```
:::

---

### Step 2: Bind the window to the left wrist (`left` reference frame) and adjust it to mini dial size

Set `startup_position` to `none`, close the title bar, use `physical_scale = 0.5` to reduce the 220×220 logical pixels to a 11 cm square small dial, and add `curvature = 1.2` to make it slightly curved and fit the wrist!

::: code-group
```python [Python (Step 2)]
from easyvrui import reference_object, startup_position, vec3

window_main.show_title_bar = False
window_main.startup_position = startup_position.none
window_main.reference_object = reference_object.left
window_main.physical_scale = 0.5
window_main.curvature = 1.2
window_main.position = vec3(-0.05, 0.06, 0.08)
window_main.rotation = vec3(-45.0, 20.0, 0.0)
```

```cpp [C++ (Step 2)]
window_main->set_show_title_bar(false);
window_main->set_startup_position(easyvrui::startup_position_t::none);
window_main->set_reference_object(easyvrui::reference_object_t::left);
window_main->set_physical_scale(0.5);
window_main->set_curvature(1.2);
window_main->set_position(easyvrui::vec3_t{-0.05, 0.06, 0.08});
window_main->set_rotation(easyvrui::vec3_t{-45.0, 20.0, 0.0});
```
:::

---

### Step 3: Click on the dial, use `reparent(..., keep_world=True)` to switch between the wrist and world space

Click on the dial to "remove" the dial and hover it in the air (keep the current world position unchanged), then click again to snap back to the left wrist!

::: code-group
```python [Python (Step 3)]
def dial_watch_click(source, event):
    if window_main.reference_object == reference_object.left:
        window_main.reparent(reference_object.world, keep_world = True)
        dial_watch.accent_color = 0x4ADE80FF
    else:
        window_main.reference_object = reference_object.left
        window_main.position = vec3(-0.05, 0.06, 0.08)
        window_main.rotation = vec3(-45.0, 20.0, 0.0)
        dial_watch.accent_color = 0x38BDF8FF
    dial_watch.invalidate()

dial_watch.on_click += dial_watch_click
```

```cpp [C++ (Step 3)]
dial_watch->on_click += [=](easyvrui::control_base &, easyvrui::event_args_t &)
{
    if(window_main->get_reference_object() == easyvrui::reference_object_t::left)
    {
        window_main->reparent(easyvrui::reference_object_t::world, true);
    }
    else
    {
        window_main->set_reference_object(easyvrui::reference_object_t::left);
        window_main->set_position(easyvrui::vec3_t{-0.05, 0.06, 0.08});
        window_main->set_rotation(easyvrui::vec3_t{-45.0, 20.0, 0.0});
    }
};
```
:::

---

### Step 4: Write an application list for `.easyvrui` and mount it on Desktop (including 4 remote connection parameters)

For example, place both the script and the list in `D:\Tools\EasyVRUI\app\wrist_watch\`. `launch.script` uses the directory where the list is located as a reference. Add the absolute path of the list to `application_list` in Desktop's user configuration, then refresh on Desktop. The list of built-in applications is registered by the installer to `app/desktop/config.json`. See [application list and](/en/reference/application_manifest) for both registration methods.

```json
{
    "id": "wrist_watch",
    "type": "application",
    "name":
    {
        "zh": "左手腕小表盘",
        "en": "Wrist Watch",
        "ja": "左手首ウォッチ"
    },
    "launch":
    {
        "runtime": "python",
        "script": "wrist_watch.py",
        "argument_list": []
    }
}
```

When Desktop starts the Python script through SDK, the installed `sdk/api/python/` is placed in `PYTHONPATH` of the sub-process. When running directly in the CMD of another computer, first configure the SDK path of that machine, then pass in the remote access parameters](/en/reference/engine_protocol) for [.

```cmd
set "PYTHONPATH=D:\Tools\EasyVRUI\sdk\api\python;%PYTHONPATH%"
python -B "D:\Tools\EasyVRUI\app\wrist_watch\wrist_watch.py" --easyvrui-host=192.168.1.50 --easyvrui-port=49537 --easyvrui-access-credential="你的凭据" --easyvrui-public-key-fingerprint=服务公钥SHA256指纹
```

---

## IV. Common Problems and Practices

1. **Why doesn't changing `position` work? Check `startup_position`**: If `startup_position` is still the default `center`, the engine will automatically center and overwrite your preset `position` during the first `show()`; when binding to the wrist or fixing the position, make sure to set it to `startup_position.none`.
2. **Custom controls don't refresh after changing member variables**: SDK only listens to built-in properties. After changing the Python/C++ member variables you added, remember to call `self.invalidate()`!
3. **Don't exceed `2π` for `curvature * physical_width`**: Before increasing `physical_scale` or `rect.width`, first check if the current curvature will exceed a full circle.

---

::: details Complete runnable example
::: code-group
```python [Python（完全版） · wrist_watch.py]
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
```

```cpp [C++（完全版） · main.cpp]
#include <algorithm>
#include <easyvrui.h>
#include <memory>

using namespace std;

class wrist_dial_control : public easyvrui::control
{
    public:
        explicit wrist_dial_control(const u32string &name) : easyvrui::control(name)
        {
        }

    protected:
        void render(easyvrui::render_context &context) const override
        {
            auto rc = context.get_rectangle(*this);
            double cx = rc.left + (rc.width * 0.5);
            double cy = rc.top + (rc.height * 0.5);
            double radius = min(rc.width, rc.height) * 0.44;
            uint32_t bg = context.is_hovered(*this) ? 0x1E3A5FFFu : 0x0F172AFFu;
            context.fill_circle(cx, cy, radius, bg);
            context.draw_circle(cx, cy, radius, 0x38BDF8FFu, 3.0);
            drawing_path pointer;
            pointer.move_to(cx, cy).line_to(cx, cy - (radius * 0.65));
            context.outline_path(pointer, 0xFACC15FFu, 3.0);
            context.draw_text(U"12:00", easyvrui::font_t{U"Segoe UI", 22u, true, false}, easyvrui::render_rectangle_t{rc.left, cy + 12.0, rc.width, 34.0}, 0xFFFFFFFFu, true);
        }
};

int main()
{
    auto window_main = make_shared<easyvrui::window>(U"window_main");
    window_main->set_rect(easyvrui::rectangle_t{0u, 0u, 220u, 220u});
    window_main->set_show_title_bar(false);
    window_main->set_startup_position(easyvrui::startup_position_t::none);
    window_main->set_reference_object(easyvrui::reference_object_t{easyvrui::reference_object_type_t::left});
    window_main->set_physical_scale(0.5);
    window_main->set_curvature(1.2);
    window_main->set_position(easyvrui::vec3_t{-0.05, 0.06, 0.08});
    window_main->set_rotation(easyvrui::vec3_t{-45.0, 20.0, 0.0});

    auto dial_watch = make_shared<wrist_dial_control>(U"dial_watch");
    dial_watch->set_rect(easyvrui::rectangle_t{0u, 0u, 220u, 220u});
    dial_watch->on_click += [=](easyvrui::control_base &, easyvrui::event_args_t &)
    {
        if(window_main->get_reference_object().type == easyvrui::reference_object_type_t::left)
        {
            window_main->reparent(easyvrui::reference_object_t{easyvrui::reference_object_type_t::world}, true);
        }
        else
        {
            window_main->set_reference_object(easyvrui::reference_object_t{easyvrui::reference_object_type_t::left});
            window_main->set_position(easyvrui::vec3_t{-0.05, 0.06, 0.08});
            window_main->set_rotation(easyvrui::vec3_t{-45.0, 20.0, 0.0});
        }
    };

    window_main->get_control_list().add(dial_watch);
    window_main->show();
    easyvrui::run(U"wrist_watch");
    return 0;
}
```
:::
:::