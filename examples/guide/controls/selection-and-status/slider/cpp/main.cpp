#include <easyvrui.h>
#include <memory>

using namespace std;
using namespace easyvrui;

shared_ptr<window> create_slider_demo()
{
    auto window_main = make_shared<window>(U"window_main");
    window_main->set_title(U"监听音量");
    window_main->set_size(690u, 310u);
    auto label_level = make_shared<label>(U"label_level");
    label_level->set_rect(rectangle_t{36u, 82u, 606u, 42u});
    label_level->set_text(U"音量较低");
    window_main->get_control_list().add(label_level);
    auto slider_level = make_shared<slider>(U"slider_level");
    slider_level->set_rect(rectangle_t{36u, 148u, 618u, 52u});
    window_main->get_control_list().add(slider_level);
    auto progressbar_level = make_shared<progressbar>(U"progressbar_level");
    progressbar_level->set_rect(rectangle_t{36u, 228u, 618u, 29u});
    window_main->get_control_list().add(progressbar_level);
    slider_level->set_value(35);
    progressbar_level->set_value(35);

    slider_level->on_value_changed += [label_level, progressbar_level](control_base &source, event_args_t &)
    {
        auto level = static_cast<slider &>(source).get_value();
        progressbar_level->set_value(level);
        label_level->set_text((level >= 60) ? U"音量较高" : U"音量较低");
    };

    return window_main;
}

#if !defined(TUTORIAL_CAPTURE_controls_second)
int main(){auto window_main = create_slider_demo(); window_main->show(); easyvrui::run(U"tutorial_slider"); return 0;}

#endif