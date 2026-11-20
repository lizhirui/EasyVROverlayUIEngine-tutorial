#include <easyvrui.h>
#include <memory>

using namespace std;
using namespace easyvrui;

shared_ptr<window> create_listbox_demo()
{
    auto window_main = make_shared<window>(U"window_main");
    window_main->set_title(U"同步任务");
    window_main->set_size(690u, 413u);
    auto label_prompt = make_shared<label>(U"label_prompt");
    label_prompt->set_rect(rectangle_t{36u, 78u, 618u, 38u});
    label_prompt->set_text(U"选择要查看的同步任务");
    window_main->get_control_list().add(label_prompt);
    auto listbox_task = make_shared<listbox>(U"listbox_task");
    listbox_task->set_rect(rectangle_t{36u, 130u, 618u, 190u});
    window_main->get_control_list().add(listbox_task);
    auto label_state = make_shared<label>(U"label_state");
    label_state->set_rect(rectangle_t{36u, 338u, 618u, 38u});
    label_state->set_text(U"尚未选择任务");
    window_main->get_control_list().add(label_state);
    listbox_task->get_item_list().assign({U"读取配置", U"检查目录", U"同步图像", U"同步音频", U"同步模型", U"核验校验和", U"清理临时文件", U"写入报告"});
    listbox_task->set_row_height(38u);
    listbox_task->set_clear_selection_on_blank_click(true);

    listbox_task->on_selection_changed += [label_state](control_base &source, event_args_t &)
    {
        auto &task = static_cast<listbox &>(source);
        label_state->set_text((task.get_selected_index() < 0) ? U"尚未选择任务" : (U"选中任务：" + task.get_selected_item()));
    };

    return window_main;
}

#if !defined(TUTORIAL_CAPTURE_controls_second)
int main(){auto window_main = create_listbox_demo(); window_main->show(); easyvrui::run(U"tutorial_listbox"); return 0;}

#endif