#include <easyvrui.h>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

using namespace std;
using namespace easyvrui;

shared_ptr<window> create_toolbar_demo()
{
    auto window_main = make_shared<window>(U"window_main");
    window_main->set_title(U"预览操作");
    window_main->set_size(680u, 310u);
    auto toolbar_main = make_shared<toolbar>(U"toolbar_main");
    toolbar_main->set_rect({36u, 85u, 608u, 67u});
    toolbar_main->set_tool_size(52u);
    toolbar_main->set_spacing(10.0);
    auto button_preview = make_shared<toolbar_button>(U"button_preview");
    button_preview->set_icon(make_shared<drawing_image>(1u, 1u, vector<uint8_t>{104u, 194u, 241u, 255u}));
    button_preview->set_tooltip_text(U"预览结果");
    toolbar_main->get_button_list().add(button_preview);
    auto &separator = toolbar_main->get_button_list().add(U"separator_preview");
    separator.set_separator(true);
    auto label_state = make_shared<label>(U"label_state");
    label_state->set_rect({36u, 194u, 608u, 46u});
    label_state->set_text(U"单击蓝色操作项");

    button_preview->on_click += [label_state](control_base &, event_args_t &)
    {
        label_state->set_text(U"已请求预览");
    };

    window_main->get_control_list().add(toolbar_main);
    window_main->get_control_list().add(label_state);
    return window_main;
}

#if !defined(TUTORIAL_CAPTURE_controls_third)
int main(){auto window_main = create_toolbar_demo(); window_main->show(); easyvrui::run(U"tutorial_toolbar"); return 0;}

#endif