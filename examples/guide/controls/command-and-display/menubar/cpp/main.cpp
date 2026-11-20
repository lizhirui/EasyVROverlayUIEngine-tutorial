#include <easyvrui.h>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

using namespace std;
using namespace easyvrui;

shared_ptr<window> create_menubar_demo()
{
    auto window_main = make_shared<window>(U"window_main");
    window_main->set_title(U"工作区命令");
    window_main->set_size(680u, 315u);
    auto menu_main = make_shared<menubar>(U"menu_main");
    auto menu_task = make_shared<menuitem>(U"menu_task");
    menu_task->set_text(U"任务(&T)");
    auto menu_refresh = make_shared<menuitem>(U"menu_refresh");
    menu_refresh->set_text(U"刷新记录");
    menu_refresh->set_shortcut(U"Ctrl+R");
    auto label_state = make_shared<label>(U"label_state");
    label_state->set_rect({36u, 217u, 608u, 49u});
    label_state->set_text(U"等待刷新");

    menu_refresh->on_click += [label_state](control_base &, event_args_t &)
    {
        label_state->set_text(U"同步记录已刷新");
    };

    menu_task->get_control_list().add(menu_refresh);
    menu_main->get_control_list().add(menu_task);
    window_main->set_menu(menu_main);
    window_main->get_control_list().add(label_state);
    return window_main;
}

#if !defined(TUTORIAL_CAPTURE_controls_third)
int main(){auto window_main = create_menubar_demo(); window_main->show(); easyvrui::run(U"tutorial_menubar"); return 0;}

#endif