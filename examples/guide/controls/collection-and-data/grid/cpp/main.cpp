#include <easyvrui.h>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

using namespace std;
using namespace easyvrui;

shared_ptr<window> create_grid_demo()
{
    auto window_main = make_shared<window>(U"window_main");
    window_main->set_title(U"编辑同步参数");
    window_main->set_size(680u, 390u);
    auto grid_config = make_shared<grid>(U"grid_config");
    grid_config->set_rect({36u, 85u, 608u, 165u});
    grid_config->set_column_list({grid_column_t{U"参数", 270u, false}, grid_column_t{U"值", 210u, true}});
    grid_config->set_row_count(2u);
    grid_config->set_cell_value(0u, 0u, u32string(U"并行任务"));
    grid_config->set_cell_value(0u, 1u, int64_t{4});
    grid_config->set_cell_value(1u, 0u, u32string(U"重试次数"));
    grid_config->set_cell_value(1u, 1u, int64_t{2});
    auto label_state = make_shared<label>(U"label_state");
    label_state->set_rect({36u, 282u, 608u, 46u});
    label_state->set_text(U"双击值所在单元格进行编辑");

    grid_config->on_edit_committed += [label_state](control_base &, grid_cell_event_args_t &)
    {
        label_state->set_text(U"参数修改已提交");
    };

    window_main->get_control_list().add(grid_config);
    window_main->get_control_list().add(label_state);
    return window_main;
}

#if !defined(TUTORIAL_CAPTURE_controls_third)
int main(){auto window_main = create_grid_demo(); window_main->show(); easyvrui::run(U"tutorial_grid"); return 0;}

#endif