#include <easyvrui.h>
#include <cstdint>
#include <memory>
#include <string>

using namespace std;
using namespace easyvrui;

shared_ptr<window> create_progressbar_demo()
{
    auto window_main = make_shared<window>(U"window_main");
    window_main->set_title(U"同步进度");
    window_main->set_size(650u, 310u);
    auto label_state = make_shared<label>(U"label_state");
    label_state->set_rect(rectangle_t{32u, 79u, 586u, 47u});
    label_state->set_text(U"已同步2/8项");
    window_main->get_control_list().add(label_state);
    auto progressbar_sync = make_shared<progressbar>(U"progressbar_sync");
    progressbar_sync->set_rect(rectangle_t{32u, 140u, 586u, 31u});
    window_main->get_control_list().add(progressbar_sync);
    auto button_next = make_shared<button>(U"button_next");
    button_next->set_rect(rectangle_t{32u, 204u, 212u, 49u});
    button_next->set_text(U"完成下一项");
    window_main->get_control_list().add(button_next);
    progressbar_sync->set_maximum(8);
    progressbar_sync->set_value(2);

    progressbar_sync->on_value_changed += [label_state, next = button_next.get()](control_base &source, event_args_t &)
    {
        auto &progress = static_cast<progressbar &>(source);
        bool complete = progress.get_value() == progress.get_maximum();
        string count = to_string(progress.get_value());
        label_state->set_text(complete ? U"同步完成" : ((U"已同步" + u32string(count.begin(), count.end())) + U"/8项"));
        next->set_enabled(!complete);
    };

    button_next->on_click += [progressbar_sync](control_base &, event_args_t &)
    {
        progressbar_sync->set_value(progressbar_sync->get_value() + int64_t{1});
    };

    return window_main;
}

#if !defined(TUTORIAL_CAPTURE_controls)
int main(){auto window_main = create_progressbar_demo(); window_main->show(); easyvrui::run(U"tutorial_progressbar"); return 0;}

#endif