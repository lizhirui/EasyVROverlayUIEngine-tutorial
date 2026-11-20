#include <easyvrui.h>
#include <cstdint>
#include <memory>

using namespace std;
using namespace easyvrui;

shared_ptr<window> create_button_demo()
{
    auto window_main = make_shared<window>(U"window_main");
    window_main->set_title(U"提交设置");
    window_main->set_size(650u, 300u);
    auto label_state = make_shared<label>(U"label_state");
    label_state->set_rect(rectangle_t{32u, 84u, 580u, 47u});
    label_state->set_text(U"设置尚未提交");
    window_main->get_control_list().add(label_state);
    auto button_submit = make_shared<button>(U"button_submit");
    button_submit->set_rect(rectangle_t{32u, 155u, 212u, 54u});
    button_submit->set_text(U"提交设置");
    window_main->get_control_list().add(button_submit);
    auto button_reset = make_shared<button>(U"button_reset");
    button_reset->set_rect(rectangle_t{266u, 155u, 212u, 54u});
    button_reset->set_text(U"重新编辑");
    window_main->get_control_list().add(button_reset);
    button_submit->set_tab_index(0u);
    button_reset->set_tab_index(1u);
    button_reset->set_enabled(false);

    button_submit->on_click += [label_state, reset = button_reset.get()](control_base &source, event_args_t &)
    {
        static_cast<button &>(source).set_enabled(false);
        reset->set_enabled(true);
        label_state->set_text(U"设置已提交");
    };

    button_reset->on_click += [label_state, submit = button_submit.get()](control_base &source, event_args_t &)
    {
        static_cast<button &>(source).set_enabled(false);
        submit->set_enabled(true);
        label_state->set_text(U"设置尚未提交");
    };

    return window_main;
}

#if !defined(TUTORIAL_CAPTURE_controls)
int main(){auto window_main = create_button_demo(); window_main->show(); easyvrui::run(U"tutorial_button"); return 0;}

#endif