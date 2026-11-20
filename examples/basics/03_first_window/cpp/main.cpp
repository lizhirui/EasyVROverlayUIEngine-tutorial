#include <easyvrui.h>
#include <memory>

using namespace std;

shared_ptr<easyvrui::window> create_first_window()
{
    auto window_main = make_shared<easyvrui::window>(U"window_main");
    window_main->set_title(U"我的第一个VR窗口");
    window_main->set_rect(easyvrui::rectangle_t{0u, 0u, 520u, 260u});
    auto label_status = make_shared<easyvrui::label>(U"label_status");
    label_status->set_rect(easyvrui::rectangle_t{36u, 76u, 448u, 48u});
    label_status->set_text(U"点一下下面的按钮试试看！");
    auto button_hello = make_shared<easyvrui::button>(U"button_hello");
    button_hello->set_rect(easyvrui::rectangle_t{36u, 150u, 200u, 48u});
    button_hello->set_text(U"点我打招呼");

    button_hello->on_click += [label_status](easyvrui::control_base &source, easyvrui::event_args_t &event)
    {
        label_status->set_text(U"你好，VR世界！");
    };

    window_main->get_control_list().add(label_status);
    window_main->get_control_list().add(button_hello);
    return window_main;
}

#if !defined(TUTORIAL_CAPTURE_project_story)
int main(){auto window_main = create_first_window(); window_main->show(); easyvrui::run(U"my_first_vr_app"); return 0;}

#endif