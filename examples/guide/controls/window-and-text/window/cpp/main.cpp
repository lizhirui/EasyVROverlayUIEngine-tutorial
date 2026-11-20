#include <easyvrui.h>
#include <cstdint>
#include <memory>

using namespace std;
using namespace easyvrui;

shared_ptr<window> create_window_demo()
{
    auto window_main = make_shared<window>(U"window_main");
    window_main->set_title(U"会话窗口");
    window_main->set_size(650u, 290u);
    auto label_state = make_shared<label>(U"label_state");
    label_state->set_rect(rectangle_t{32u, 88u, 580u, 48u});
    label_state->set_text(U"当前窗口已显示");
    window_main->get_control_list().add(label_state);
    auto button_title = make_shared<button>(U"button_title");
    button_title->set_rect(rectangle_t{32u, 163u, 220u, 50u});
    button_title->set_text(U"切换标题栏配色");
    window_main->get_control_list().add(button_title);
    window_main->set_title_background_color(0x21495effu);

    button_title->on_click += [owner = window_main.get()](control_base &, event_args_t &)
    {
        constexpr uint32_t TITLE_COLOR = 0x21495effu;
        constexpr uint32_t SELECTED_COLOR = 0x465c82ffu;
        owner->set_title_background_color((owner->get_title_background_color() == TITLE_COLOR) ? SELECTED_COLOR : TITLE_COLOR);
    };

    return window_main;
}

#if !defined(TUTORIAL_CAPTURE_controls)
int main(){auto window_main = create_window_demo(); window_main->show(); easyvrui::run(U"tutorial_window"); return 0;}

#endif