#include <easyvrui.h>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

using namespace std;
using namespace easyvrui;

shared_ptr<window> create_image_demo()
{
    auto window_main = make_shared<window>(U"window_main");
    window_main->set_title(U"素材预览");
    window_main->set_size(680u, 360u);
    auto image_preview = make_shared<image>(U"image_preview");
    image_preview->set_rect({36u, 84u, 608u, 170u});
    image_preview->set_source(make_shared<drawing_image>(4u, 2u, vector<uint8_t>{56u, 151u, 207u, 255u, 56u, 151u, 207u, 255u, 68u, 197u, 147u, 255u, 68u, 197u, 147u, 255u, 68u, 197u, 147u, 255u, 68u, 197u, 147u, 255u, 56u, 151u, 207u, 255u, 56u, 151u, 207u, 255u}));
    auto button_mode = make_shared<button>(U"button_mode");
    button_mode->set_rect({36u, 275u, 235u, 45u});
    button_mode->set_text(U"切换等比填充");

    button_mode->on_click += [image_preview](control_base &, event_args_t &)
    {
        auto mode = image_preview->get_stretch_mode();
        image_preview->set_stretch_mode((mode == image_stretch_mode_t::contain) ? image_stretch_mode_t::cover : image_stretch_mode_t::contain);
    };

    window_main->get_control_list().add(image_preview);
    window_main->get_control_list().add(button_mode);
    return window_main;
}

#if !defined(TUTORIAL_CAPTURE_controls_third)
int main(){auto window_main = create_image_demo(); window_main->show(); easyvrui::run(U"tutorial_image"); return 0;}

#endif