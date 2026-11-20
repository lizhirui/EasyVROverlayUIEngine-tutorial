#include <easyvrui.h>
#include <cstdint>
#include <memory>

using namespace std;
using namespace easyvrui;

shared_ptr<window> create_radiobutton_demo()
{
    auto window_main = make_shared<window>(U"window_main");
    window_main->set_title(U"通知模式");
    window_main->set_size(650u, 320u);
    auto panel_mode = make_shared<panel>(U"panel_mode");
    panel_mode->set_rect(rectangle_t{32u, 82u, 586u, 126u});
    window_main->get_control_list().add(panel_mode);
    auto radiobutton_all = make_shared<radiobutton>(U"radiobutton_all");
    radiobutton_all->set_rect(rectangle_t{16u, 8u, 554u, 46u});
    radiobutton_all->set_text(U"接收全部通知");
    panel_mode->get_control_list().add(radiobutton_all);
    auto radiobutton_important = make_shared<radiobutton>(U"radiobutton_important");
    radiobutton_important->set_rect(rectangle_t{16u, 68u, 554u, 46u});
    radiobutton_important->set_text(U"仅接收重要通知");
    panel_mode->get_control_list().add(radiobutton_important);
    auto label_state = make_shared<label>(U"label_state");
    label_state->set_rect(rectangle_t{32u, 226u, 586u, 50u});
    label_state->set_text(U"当前模式：仅接收重要通知");
    window_main->get_control_list().add(label_state);
    radiobutton_important->set_checked(true);

    auto radiobutton_mode_checked_changed = [label_state](control_base &source, event_args_t &)
    {
        auto &choice = static_cast<radiobutton &>(source);

        if(choice.get_checked())
        {
            label_state->set_text(U"当前模式：" + choice.get_text());
        }
    };

    radiobutton_all->on_checked_changed += radiobutton_mode_checked_changed;
    radiobutton_important->on_checked_changed += radiobutton_mode_checked_changed;
    return window_main;
}

#if !defined(TUTORIAL_CAPTURE_controls)
int main(){auto window_main = create_radiobutton_demo(); window_main->show(); easyvrui::run(U"tutorial_radiobutton"); return 0;}

#endif