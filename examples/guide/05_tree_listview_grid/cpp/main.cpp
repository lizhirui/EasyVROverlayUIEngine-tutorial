#include <easyvrui.h>
#include <memory>
#include <string>
#include <vector>

using namespace std;

int main()
{
    auto window_main = make_shared<easyvrui::window>(U"window_main");
    window_main->set_title(U"简易收藏夹与参数表");
    window_main->set_rect(easyvrui::rectangle_t{0u, 0u, 860u, 500u});

    auto tree_fav = make_shared<easyvrui::treeview>(U"tree_fav");
    tree_fav->set_rect(easyvrui::rectangle_t{20u, 56u, 220u, 380u});
    auto node_worlds = make_shared<easyvrui::tree_node>(U"收藏世界", true, U"worlds");
    node_worlds->get_node_list().add(make_shared<easyvrui::tree_node>(U"日语闲聊区", false, U"worlds/jp"));
    node_worlds->get_node_list().add(make_shared<easyvrui::tree_node>(U"睡眠/放空区", false, U"worlds/sleep"));
    auto node_avatars = make_shared<easyvrui::tree_node>(U"Avatar预设", true, U"avatars");
    node_avatars->get_node_list().add(make_shared<easyvrui::tree_node>(U"日常猫耳", false, U"avatars/cat"));
    tree_fav->get_node_list().add(node_worlds);
    tree_fav->get_node_list().add(node_avatars);

    auto list_items = make_shared<easyvrui::listview>(U"list_items");
    list_items->set_rect(easyvrui::rectangle_t{256u, 56u, 584u, 170u});
    list_items->get_column_list().add(make_shared<easyvrui::listview_column>(U"名称", 240u));
    list_items->get_column_list().add(make_shared<easyvrui::listview_column>(U"类型", 140u));
    list_items->get_column_list().add(make_shared<easyvrui::listview_column>(U"备注", 180u));
    list_items->get_item_list().add(make_shared<easyvrui::listview_item>(vector<u32string>{U"FUJIYAMA", U"世界", U"日语闲聊"}, nullptr, U"fuji"));
    list_items->get_item_list().add(make_shared<easyvrui::listview_item>(vector<u32string>{U"NAGiSA", U"世界", U"1对1聊天"}, nullptr, U"nagisa"));
    list_items->get_item_list().add(make_shared<easyvrui::listview_item>(vector<u32string>{U"猫耳卫衣", U"Avatar", U"轻量级"}, nullptr, U"cat"));

    struct param_row_t
    {
        u32string name;
        double value;
        bool enabled;
    };

    auto param_rows = make_shared<vector<param_row_t>>(vector<param_row_t>{{U"EarTwitchSpeed", 1.5, true}, {U"TailWagAmp", 0.8, true}, {U"GlowIntensity", 2.0, false}});
    auto grid_params = make_shared<easyvrui::grid>(U"grid_params");
    grid_params->set_rect(easyvrui::rectangle_t{256u, 240u, 584u, 196u});
    grid_params->set_column_list({{U"参数名", 240u, false}, {U"浮点数值", 170u, true}, {U"启用", 140u, true}});
    grid_params->set_data_provider(
        param_rows->size(),
        [=](uint64_t row, uint64_t col) -> easyvrui::grid_value_t
        {
            const auto &item = (*param_rows)[row];
            if(col == 0u)
            {
                return item.name;
            }
            if(col == 1u)
            {
                return item.value;
            }
            return item.enabled;
        },
        [=](uint64_t row, uint64_t col, const easyvrui::grid_value_t &val, u32string &) -> bool
        {
            if(col == 1u)
            {
                (*param_rows)[row].value = get<double>(val);
            }
            else if(col == 2u)
            {
                (*param_rows)[row].enabled = get<bool>(val);
            }
            return true;
        });
    grid_params->set_edit_validator([](easyvrui::grid_cell_t cell, const easyvrui::grid_value_t &val, u32string &error) -> bool
    {
        if(cell.column == 1u)
        {
            double num = get<double>(val);
            if((num < 0.0) || (num > 10.0))
            {
                error = U"数值必须在 0.0 到 10.0 之间！";
                return false;
            }
        }
        return true;
    });

    auto label_status = make_shared<easyvrui::label>(U"label_status");
    label_status->set_rect(easyvrui::rectangle_t{20u, 450u, 820u, 32u});
    label_status->set_text(U"点击左侧树节点查看详情");

    tree_fav->on_selection_changed += [=](easyvrui::control_base &, easyvrui::tree_node_event_args_t &event)
    {
        auto *node = event.node;
        label_status->set_text(node ? (U"选中节点：" + node->get_text()) : u32string(U"未选中节点"));
    };
    list_items->on_row_double_click += [=](easyvrui::control_base &, easyvrui::listview_item_event_args_t &event)
    {
        if(event.item != nullptr)
        {
            label_status->set_text(U"双击激活行：" + event.item->get_cell_list()[0]);
        }
    };
    grid_params->on_cell_value_changed += [=](easyvrui::control_base &, easyvrui::grid_cell_event_args_t &event)
    {
        auto row_text = to_string(event.row);
        label_status->set_text(U"参数已更新：第 " + u32string(row_text.begin(), row_text.end()) + U" 行");
    };
    grid_params->on_edit_failed += [=](easyvrui::control_base &, easyvrui::grid_cell_event_args_t &event)
    {
        label_status->set_text(U"校验失败：" + event.error);
    };

    window_main->get_control_list().add(tree_fav);
    window_main->get_control_list().add(list_items);
    window_main->get_control_list().add(grid_params);
    window_main->get_control_list().add(label_status);
    window_main->show();
    easyvrui::run(U"fav_and_params");
    return 0;
}