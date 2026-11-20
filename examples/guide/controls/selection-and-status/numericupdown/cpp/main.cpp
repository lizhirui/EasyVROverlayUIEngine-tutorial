#include <easyvrui.h>
#include <memory>

using namespace std;
using namespace easyvrui;

shared_ptr<window> create_numericupdown_demo()
{
    auto window_main = make_shared<window>(U"window_main");
    window_main->set_title(U"校准增益");
    window_main->set_size(690u, 305u);
    auto label_prompt = make_shared<label>(U"label_prompt");
    label_prompt->set_rect(rectangle_t{36u, 82u, 618u, 42u});
    label_prompt->set_text(U"范围：0.00至2.00");
    window_main->get_control_list().add(label_prompt);
    auto numericupdown_gain = make_shared<numericupdown>(U"numericupdown_gain");
    numericupdown_gain->set_rect(rectangle_t{36u, 145u, 320u, 56u});
    window_main->get_control_list().add(numericupdown_gain);
    auto label_state = make_shared<label>(U"label_state");
    label_state->set_rect(rectangle_t{36u, 220u, 618u, 42u});
    label_state->set_text(U"当前增益低于基准");
    window_main->get_control_list().add(label_state);
    numericupdown_gain->set_maximum(2.0);
    numericupdown_gain->set_step(0.25);
    numericupdown_gain->set_decimal_places(2u);
    numericupdown_gain->set_value(0.75);

    numericupdown_gain->on_value_changed += [label_state](control_base &source, event_args_t &)
    {
        auto gain = static_cast<numericupdown &>(source).get_value();
        label_state->set_text((gain >= 1.0) ? U"当前增益达到或超过基准" : U"当前增益低于基准");
    };

    return window_main;
}

#if !defined(TUTORIAL_CAPTURE_controls_second)
int main(){auto window_main = create_numericupdown_demo(); window_main->show(); easyvrui::run(U"tutorial_numericupdown"); return 0;}

#endif