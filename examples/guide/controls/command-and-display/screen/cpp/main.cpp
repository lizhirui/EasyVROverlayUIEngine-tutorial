#include <easyvrui.h>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

using namespace std;
using namespace easyvrui;

shared_ptr<window> create_screen_demo()
{
    auto window_main = make_shared<window>(U"window_main");
    window_main->set_title(U"显示输出监视");
    window_main->set_size(680u, 357u);
    auto screen_preview = make_shared<screen>(U"screen_preview");
    screen_preview->set_rect({36u, 86u, 608u, 168u});
    auto label_state = make_shared<label>(U"label_state");
    label_state->set_rect({36u, 267u, 608u, 48u});
    label_state->set_text(U"等待显示器画面");

    screen_preview->on_screen_restored += [label_state](control_base &, event_args_t &)
    {
        label_state->set_text(U"采集源可用");
    };

    screen_preview->on_screen_unavailable += [label_state](control_base &, event_args_t &)
    {
        label_state->set_text(U"采集源不可用");
    };

    window_main->get_control_list().add(screen_preview);
    window_main->get_control_list().add(label_state);
    return window_main;
}

#if !defined(TUTORIAL_CAPTURE_controls_third)
int main(){auto window_main = create_screen_demo(); window_main->show(); easyvrui::run(U"tutorial_screen"); return 0;}

#endif