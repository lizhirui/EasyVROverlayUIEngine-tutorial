# 空间定位、自定义绘图与Desktop登记

前几章使用的都是内置默认外观的控件，窗口默认放置在`world`参考系中。本章介绍如何通过`render_context`和`drawing_path`实现自定义绘图，使用`reference_object`与`curvature`将窗口固定在左手腕（`left`参考系），并通过`.easyvrui`清单将其注册到Desktop启动器。

---

## 一、`window`空间定位、`vec3`/`quat`/`pose`与`blank`

`world`用于固定空间，`head`跟随头显，`body`跟随人体平移并保留校准朝向，`left`和`right`分别跟随左右手柄。用`reference_object`选择参考对象，以米配置局部偏移。跟踪设备和位姿由SteamVR运行时提供。

![SteamVR的五种空间参考对象示意](/images/zh/vr_spatial_anchors.png)

下图用WARP绘制配置视图。实际定位用`get_world_transform()`或Python的`world_transform`读取结果，结合`is_tracking_available()`确认参考对象可用。

![五种空间参考对象的配置视图](/images/zh/spatial_anchor_config.png)

### 1. `window`空间与外观属性/方法

|属性/方法|类型（Python / C++）|默认值|读写|说明与注意事项|
|---|---|---|---|---|
|`reference_object`|`reference_object`（Python也接受枚举或字符串）|`world`|读写|空间锚点：`world`（世界固定）、`body`（跟随身体）、`head`（跟随头显）、`left`（左手柄）、`right`（右手柄）。|
|`position`|`vec3` / `vec3_t`|`vec3(0, 0, 0)`|读写|窗口**左上角**相对参考目标的偏移，单位**米**。|
|`rotation`|`vec3` / `vec3_t`|`vec3(0, 0, 0)`|读写|XYZ欧拉角（单位**度**，组合顺序`Rz * Ry * Rx`）。|
|`physical_scale`|`float` / `double`|`1.0`|读写|物理缩放倍数（须为正有限数）。`1.0`时`1`逻辑像素 = `1毫米`！|
|`physical_width` / `physical_height`|`float` / `double`|计算值|只读|实际物理宽高（米）= `rect.width * physical_scale / 1000.0`。|
|`curvature`|`float` / `double`|`0.0`|读写|圆柱曲率（单位`m⁻¹`），`0`为平面；须满足`k >= 0`且`k * physical_width < 2π`（手柄交互上限为`160°`）。|
|`startup_position`|`startup_position` / `startup_position_t`|`center`|读写|`center`首次显示自动居中在头显/来源窗前方；自己设`position`绑手腕时务必改成`none`！|
|`tracking_mode_set`|`set[reference_object_type]`|五种全含|读写|标题栏`⊕`按钮可选模式集合；设为空集合`set()`隐藏切换按钮。|
|`show_title_bar` / `show_close_button` / `movable` / `resizable` / `curvature_adjustable`|`bool`|全`True`|读写|标题栏、关闭按钮、抓取移动、右下角缩放、左下角曲率柄开关。|
|`reparent(ref, keep_world = False)`|方法|—|—|切换参考系；`keep_world = True`可让窗口在换锚点瞬间保持在原地不瞬移！|
|`center_at_view(distance) -> bool`|方法|—|—|把窗口直接拉到当前视线前方`distance`米处居中。|
|`world_transform`（C++：`get_world_transform()`）|`pose \| None` / `optional<pose_t>`|—|只读|返回窗口**中心点**当前在世界空间中的`pose`（跟踪不可用时返回`None`）。|

### 2. `vec3`、`quat`、`pose`与`blank`

- **`vec3(x, y, z)`**：支持`+`/`-`/标量`*`、`calculate_dot_product`、`calculate_cross_product`、`length`、`normalized`。
- **`quat(x, y, z, w)`**：默认单位旋转`(0,0,0,1)`，支持`*`组合、`euler`、`rotate(v)`、`slerp(target, t)`、`create_from_euler(angles)`、`create_from_axis_angle(axis, angle)`。
- **`pose(position, rotation)`**：`a * b`（Python也支持`a @ b`）、`inverse`、`matrix`、`transform_point(v)`。
- **`blank(name)`**：继承`control`的纯矩形占位对象（只保留`name`/`rect`与几何/释放事件，访问`visible`/`enabled`/`render`等会抛`AttributeError`）。

---

## 二、`render_context`常用绘图接口与`drawing_path`

绘图时先通过`get_rectangle()`取得控件的目标区域，再用归一化数据计算局部点位。下图中的绘图控件用`fill_rounded_rectangle()`绘制背景，以`draw_line()`连接采样点，并通过`push_clip()`和`pop_clip()`限制绘制边界。应用只在数据发生变化或动画推进时调用`invalidate()`，提交由SDK调度。

![自定义采样折线的WARP渲染效果](/images/zh/spatial_custom_drawing.png)

派生自`control`并覆盖`render(self, context)`（或C++`render(render_context &context) const override`），即可使用`render_context`绘图：

|常用方法|用途|
|---|---|
|`context.rectangle` / `get_rectangle(item)`|获取当前控件绘制矩形`(left, top, width, height)`。|
|`is_hovered(item)` / `is_focused(item)`|查询悬停与焦点状态，方便画高亮效果。|
|`fill(rect, color)` / `outline(rect, color, thickness=1.0)`|填充或描边矩形（颜色为`0xRRGGBBAA`整数）。|
|`fill_rounded_rectangle(rect, rx, ry, color)` / `outline_rounded_rectangle(...)`|圆角矩形。|
|`fill_circle(cx, cy, r, color)` / `draw_circle(cx, cy, r, color, thickness=1.0)`|填充圆与圆边框。|
|`fill_ellipse` / `outline_ellipse` / `draw_line`|椭圆与线段。|
|`draw_text(text, font, rect, color, center=False)` / `measure(text, font)`|绘制文字与测量文字宽度。|
|`draw_image(img, rect, opacity=1.0)` / `draw_screen(id, rect)`|绘制图片或实时显示器画面。|
|`fill_path(path, color)` / `outline_path(path, color, thickness=1.0)`|绘制`drawing_path`矢量路径。|
|`push_clip(rect)` / `pop_clip()`|矩形裁剪压栈与出栈（必须成对调用）。|

**`drawing_path`**：支持链式调用`move_to(x, y)`、`line_to(x, y)`、`quadratic_to(...)`、`cubic_to(...)`、`arc_to(...)`、`close()`，`fill_rule`可选`even_odd`或`non_zero`。

---

## 三、分步实现：《左手腕小表盘并上架Desktop》

### 第1步：派生`control`用`render_context`和`drawing_path`画一个表盘控件

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

### 第2步：把窗口绑到左手腕（`left`参考系）并调成迷你表盘尺寸

把`startup_position`设为`none`，关闭标题栏，用`physical_scale = 0.5`把220×220逻辑像素缩成11厘米见方的小表盘，并加上`curvature = 1.2`让它微弯贴合手腕！

::: code-group
```python [Python（第2步新增）]
from easyvrui import reference_object_type, startup_position, vec3

window_main.show_title_bar = False
window_main.startup_position = startup_position.none
window_main.reference_object = reference_object_type.left
window_main.physical_scale = 0.5
window_main.curvature = 1.2
window_main.position = vec3(-0.05, 0.06, 0.08)
window_main.rotation = vec3(-45.0, 20.0, 0.0)
```

```cpp [C++（第2步新增）]
window_main->set_show_title_bar(false);
window_main->set_startup_position(easyvrui::startup_position_t::none);
window_main->set_reference_object(easyvrui::reference_object_t{easyvrui::reference_object_type_t::left});
window_main->set_physical_scale(0.5);
window_main->set_curvature(1.2);
window_main->set_position(easyvrui::vec3_t{-0.05, 0.06, 0.08});
window_main->set_rotation(easyvrui::vec3_t{-45.0, 20.0, 0.0});
```
:::

---

### 第3步：点一下表盘，用`reparent(..., keep_world=True)`在手腕与世界空间间切换

点一下表盘就把表盘“摘下来”悬停在空中（保持当前世界位置不瞬移），再点一下就吸回左手腕！

::: code-group
```python [Python（第3步新增）]
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
```

```cpp [C++（第3步新增）]
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
```
:::

---

### 第4步：写一份`.easyvrui`应用清单并上架Desktop（含远程连接4参数）

例如，将脚本和清单都放在`D:\Tools\EasyVRUI\app\wrist_watch\`。`launch.script`以清单所在目录为基准。将清单的绝对路径加入Desktop用户配置的`application_list`，然后在Desktop刷新。内置普通应用的清单由安装器登记到`app/desktop/config.json`。两种登记方式见[应用清单](/reference/application_manifest)。

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

Desktop通过SDK启动Python脚本时，将安装的`sdk/api/python/`前置到子进程的`PYTHONPATH`。在另一台计算机的CMD直接运行时，先配置该机的SDK路径，再传入[远程接入参数](/reference/engine_protocol)。

```cmd
set "PYTHONPATH=D:\Tools\EasyVRUI\sdk\api\python;%PYTHONPATH%"
python -B "D:\Tools\EasyVRUI\app\wrist_watch\wrist_watch.py" --easyvrui-host=192.168.1.50 --easyvrui-port=49537 --easyvrui-access-credential="你的凭据" --easyvrui-public-key-fingerprint=服务公钥SHA256指纹
```

---

## 四、常见问题与实践

1. **改`position`无效？检查`startup_position`**：如果`startup_position`还是默认的`center`，第一次`show()`时引擎会帮你自动居中覆盖掉你预设的`position`；绑定手腕或固定位置时务必设成`startup_position.none`。
2. **自定义控件改了成员变量却不刷新**：SDK只监听自带属性，你自己加的Python/C++成员改完后，记得调用`self.invalidate()`！
3. **`curvature * physical_width`别超`2π`**：调大`physical_scale`或`rect.width`前，先留意当前曲率是否会超过一整圈。

---

::: details 查看本章完整可运行源码
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