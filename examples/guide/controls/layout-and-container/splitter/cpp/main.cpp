#include <easyvrui.h>
#include <memory>

using namespace std;
using namespace easyvrui;

shared_ptr<window> create_splitter_demo()
{
    auto window_main = make_shared<window>(U"window_main");
    window_main->set_title(U"双区工作台");
    window_main->set_size(690u, 422u);
    auto splitter_workspace = make_shared<splitter>(U"splitter_workspace");
    splitter_workspace->set_rect(rectangle_t{36u, 85u, 618u, 226u});
    window_main->get_control_list().add(splitter_workspace);
    auto panel_task = make_shared<panel>(U"panel_task");
    splitter_workspace->get_control_list().add(panel_task);
    auto label_task = make_shared<label>(U"label_task");
    label_task->set_rect(rectangle_t{12u, 18u, 144u, 42u});
    label_task->set_text(U"任务队列");
    panel_task->get_control_list().add(label_task);
    auto panel_result = make_shared<panel>(U"panel_result");
    splitter_workspace->get_control_list().add(panel_result);
    auto label_result = make_shared<label>(U"label_result");
    label_result->set_rect(rectangle_t{12u, 18u, 144u, 42u});
    label_result->set_text(U"同步摘要");
    panel_result->get_control_list().add(label_result);
    auto label_state = make_shared<label>(U"label_state");
    label_state->set_rect(rectangle_t{36u, 333u, 618u, 43u});
    label_state->set_text(U"拖动分隔条调整布局");
    window_main->get_control_list().add(label_state);
    splitter_workspace->set_split_position(0.42);
    panel_task->set_background_color(0x203c56ffu);
    panel_result->set_background_color(0x203d36ffu);

    splitter_workspace->on_split_end += [label_state](control_base &, interaction_end_event_args_t &event)
    {
        if(!event.cancelled)
        {
            label_state->set_text(U"布局比例已更新");
        }
    };

    return window_main;
}

#if !defined(TUTORIAL_CAPTURE_controls_second)
int main(){auto window_main = create_splitter_demo(); window_main->show(); easyvrui::run(U"tutorial_splitter"); return 0;}

#endif