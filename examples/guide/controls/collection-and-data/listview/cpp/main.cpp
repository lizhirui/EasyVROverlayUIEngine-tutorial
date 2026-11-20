#include <easyvrui.h>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

using namespace std;
using namespace easyvrui;

shared_ptr<window> create_listview_demo()
{
    auto window_main = make_shared<window>(U"window_main");
    window_main->set_title(U"同步结果");
    window_main->set_size(680u, 375u);
    auto list_result = make_shared<listview>(U"list_result");
    list_result->set_rect({36u, 84u, 608u, 180u});
    list_result->get_column_list().assign({make_shared<listview_column>(U"任务", 230u), make_shared<listview_column>(U"状态", 160u), make_shared<listview_column>(U"文件数", 130u)});
    list_result->get_item_list().assign({make_shared<listview_item>(vector<u32string>{U"同步图像", U"完成", U"12"}), make_shared<listview_item>(vector<u32string>{U"同步音频", U"待处理", U"4"}), make_shared<listview_item>(vector<u32string>{U"核验清单", U"完成", U"1"})});
    auto label_state = make_shared<label>(U"label_state");
    label_state->set_rect({36u, 285u, 608u, 45u});
    label_state->set_text(U"请选择同步记录");

    list_result->on_selection_changed += [label_state](control_base &source, event_args_t &)
    {
        const auto *item = static_cast<listview &>(source).get_selected_item();
        label_state->set_text(item ? (U"当前记录：" + item->get_cell_list()[0u]) : U"请选择同步记录");
    };

    window_main->get_control_list().add(list_result);
    window_main->get_control_list().add(label_state);
    return window_main;
}

#if !defined(TUTORIAL_CAPTURE_controls_third)
int main(){auto window_main = create_listview_demo(); window_main->show(); easyvrui::run(U"tutorial_listview"); return 0;}

#endif