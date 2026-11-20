#include <easyvrui.h>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

using namespace std;
using namespace easyvrui;

shared_ptr<window> create_treeview_demo()
{
    auto window_main = make_shared<window>(U"window_main");
    window_main->set_title(U"任务分类");
    window_main->set_size(680u, 380u);
    auto tree_task = make_shared<treeview>(U"tree_task");
    tree_task->set_rect({36u, 84u, 608u, 184u});
    auto folder = make_shared<tree_node>(U"同步任务", true, U"sync");
    auto report = make_shared<tree_node>(U"检查报告", false, U"report");
    folder->get_node_list().add(make_shared<tree_node>(U"同步图像", false, U"image"));
    folder->get_node_list().add(report);
    tree_task->get_node_list().add(folder);
    tree_task->get_node_list().add(make_shared<tree_node>(U"本地配置", false, U"config"));
    auto label_state = make_shared<label>(U"label_state");
    label_state->set_rect({36u, 290u, 608u, 44u});
    label_state->set_text(U"请选择任务");

    tree_task->on_selection_changed += [label_state](control_base &, tree_node_event_args_t &event)
    {
        label_state->set_text(event.node ? (U"选中：" + event.node->get_text()) : U"请选择任务");
    };

    window_main->get_control_list().add(tree_task);
    window_main->get_control_list().add(label_state);
    return window_main;
}

#if !defined(TUTORIAL_CAPTURE_controls_third)
int main(){auto window_main = create_treeview_demo(); window_main->show(); easyvrui::run(U"tutorial_treeview"); return 0;}

#endif