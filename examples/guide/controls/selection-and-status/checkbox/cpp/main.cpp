#include <easyvrui.h>
#include <cstdint>
#include <memory>

using namespace std;
using namespace easyvrui;

shared_ptr<window> create_checkbox_demo()
{
    auto window_main = make_shared<window>(U"window_main");
    window_main->set_title(U"通知偏好");
    window_main->set_size(650u, 315u);
    auto checkbox_sound = make_shared<checkbox>(U"checkbox_sound");
    checkbox_sound->set_rect(rectangle_t{32u, 80u, 586u, 48u});
    checkbox_sound->set_text(U"播放通知声音");
    window_main->get_control_list().add(checkbox_sound);
    auto checkbox_badge = make_shared<checkbox>(U"checkbox_badge");
    checkbox_badge->set_rect(rectangle_t{32u, 143u, 586u, 48u});
    checkbox_badge->set_text(U"显示未读状态");
    window_main->get_control_list().add(checkbox_badge);
    auto label_state = make_shared<label>(U"label_state");
    label_state->set_rect(rectangle_t{32u, 219u, 586u, 46u});
    label_state->set_text(U"通知声音已关闭");
    window_main->get_control_list().add(label_state);
    checkbox_badge->set_checked(true);

    checkbox_sound->on_checked_changed += [label_state](control_base &source, event_args_t &)
    {
        label_state->set_text(static_cast<checkbox &>(source).get_checked() ? U"通知声音已开启" : U"通知声音已关闭");
    };

    return window_main;
}

#if !defined(TUTORIAL_CAPTURE_controls)
int main(){auto window_main = create_checkbox_demo(); window_main->show(); easyvrui::run(U"tutorial_checkbox"); return 0;}

#endif