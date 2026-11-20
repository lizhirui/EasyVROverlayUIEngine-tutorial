#include <easyvrui.h>
#include <memory>

using namespace std;
using namespace easyvrui;

shared_ptr<window> create_combobox_demo()
{
    auto window_main = make_shared<window>(U"window_main");
    window_main->set_title(U"同步周期");
    window_main->set_size(690u, 390u);
    auto label_prompt = make_shared<label>(U"label_prompt");
    label_prompt->set_rect(rectangle_t{36u, 76u, 618u, 44u});
    label_prompt->set_text(U"选择一个同步周期");
    window_main->get_control_list().add(label_prompt);
    auto combobox_interval = make_shared<combobox>(U"combobox_interval");
    combobox_interval->set_rect(rectangle_t{36u, 130u, 340u, 52u});
    window_main->get_control_list().add(combobox_interval);
    auto label_state = make_shared<label>(U"label_state");
    label_state->set_rect(rectangle_t{36u, 310u, 618u, 45u});
    label_state->set_text(U"当前周期：每5分钟");
    window_main->get_control_list().add(label_state);
    combobox_interval->get_item_list().assign({U"每5分钟", U"每15分钟", U"每30分钟"});
    combobox_interval->set_selected_index(0);

    combobox_interval->on_selection_changed += [label_state](control_base &source, event_args_t &)
    {
        auto &choice = static_cast<combobox &>(source);
        label_state->set_text(U"当前周期：" + choice.get_selected_item());
    };

    return window_main;
}

#if !defined(TUTORIAL_CAPTURE_controls_second)
int main(){auto window_main = create_combobox_demo(); window_main->show(); easyvrui::run(U"tutorial_combobox"); return 0;}

#endif