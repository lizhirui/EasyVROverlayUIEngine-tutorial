#include <easyvrui.h>
#include <cstdint>
#include <memory>

using namespace std;
using namespace easyvrui;

shared_ptr<window> create_label_demo()
{
    auto window_main = make_shared<window>(U"window_main");
    window_main->set_title(U"连接状态");
    window_main->set_size(650u, 295u);
    auto label_caption = make_shared<label>(U"label_caption");
    label_caption->set_rect(rectangle_t{32u, 84u, 586u, 52u});
    label_caption->set_text(U"工作区连接");
    window_main->get_control_list().add(label_caption);
    auto label_state = make_shared<label>(U"label_state");
    label_state->set_rect(rectangle_t{32u, 157u, 586u, 49u});
    label_state->set_text(U"已连接 · 测试服务");
    window_main->get_control_list().add(label_state);
    auto label_detail = make_shared<label>(U"label_detail");
    label_detail->set_rect(rectangle_t{32u, 220u, 586u, 42u});
    label_detail->set_text(U"可以开始同步设置");
    window_main->get_control_list().add(label_detail);
    label_caption->set_font(font_t{U"Microsoft YaHei UI", 28u, true});
    label_state->set_background_color(0x173b38ffu);
    label_state->set_foreground_color(0xa7efc9ffu);
    label_state->set_font(font_t{U"Microsoft YaHei UI", 22u});
    return window_main;
}

#if !defined(TUTORIAL_CAPTURE_controls)
int main(){auto window_main = create_label_demo(); window_main->show(); easyvrui::run(U"tutorial_label"); return 0;}

#endif