#include <easyvrui.h>
#include <memory>

using namespace std;

int main()
{
    auto window_main = make_shared<easyvrui::window>(U"window_main");
    window_main->set_title(U"VRChat 世界传送清单");
    window_main->set_rect(easyvrui::rectangle_t{0u, 0u, 560u, 440u});

    auto combobox_category = make_shared<easyvrui::combobox>(U"combobox_category");
    combobox_category->set_rect(easyvrui::rectangle_t{24u, 60u, 200u, 38u});
    combobox_category->set_dropdown_style(easyvrui::combobox_dropdown_style_t::dropdown_list);
    combobox_category->get_item_list().assign({U"全部", U"日语聊天", U"聚会/游戏"});
    combobox_category->set_selected_index(0);

    auto combobox_add = make_shared<easyvrui::combobox>(U"combobox_add");
    combobox_add->set_rect(easyvrui::rectangle_t{240u, 60u, 196u, 38u});
    combobox_add->set_dropdown_style(easyvrui::combobox_dropdown_style_t::dropdown);
    combobox_add->get_item_list().assign({U"Prism Search", U"Rest & Sleep", U"VRC Cinema"});
    combobox_add->set_text(U"输入或选新世界");

    auto button_add = make_shared<easyvrui::button>(U"button_add");
    button_add->set_rect(easyvrui::rectangle_t{446u, 60u, 90u, 38u});
    button_add->set_text(U"加入");

    auto listbox_worlds = make_shared<easyvrui::listbox>(U"listbox_worlds");
    listbox_worlds->set_rect(easyvrui::rectangle_t{24u, 110u, 512u, 230u});
    listbox_worlds->set_row_height(34u);
    listbox_worlds->set_clear_selection_on_blank_click(true);
    listbox_worlds->get_item_list().assign({U"Just B Club 3", U"FUJIYAMA (日本語雑談)", U"Midnight Rooftop", U"Murder 4", U"Drinking Night"});

    auto button_remove = make_shared<easyvrui::button>(U"button_remove");
    button_remove->set_rect(easyvrui::rectangle_t{24u, 350u, 140u, 38u});
    button_remove->set_text(U"移除选中");

    auto button_toggle_drop = make_shared<easyvrui::button>(U"button_toggle_drop");
    button_toggle_drop->set_rect(easyvrui::rectangle_t{180u, 350u, 180u, 38u});
    button_toggle_drop->set_text(U"展开/收起分类");

    auto label_status = make_shared<easyvrui::label>(U"label_status");
    label_status->set_rect(easyvrui::rectangle_t{24u, 396u, 512u, 32u});
    label_status->set_text(U"请点选一个世界");

    window_main->get_control_list().add(combobox_category);
    window_main->get_control_list().add(combobox_add);
    window_main->get_control_list().add(button_add);
    window_main->get_control_list().add(listbox_worlds);
    window_main->get_control_list().add(button_remove);
    window_main->get_control_list().add(button_toggle_drop);
    window_main->get_control_list().add(label_status);

    combobox_category->on_selected_index_changed += [=](easyvrui::control_base &, easyvrui::event_args_t &)
    {
        auto idx = combobox_category->get_selected_index();
        if(idx == 0)
        {
            listbox_worlds->get_item_list().assign({U"Just B Club 3", U"FUJIYAMA (日本語雑談)", U"Midnight Rooftop", U"Murder 4", U"Drinking Night"});
        }
        else if(idx == 1)
        {
            listbox_worlds->get_item_list().assign({U"FUJIYAMA (日本語雑談)", U"NAGiSA", U"ポピー横丁"});
        }
        else
        {
            listbox_worlds->get_item_list().assign({U"Murder 4", U"Among Us", U"Drinking Night", U"Just B Club 3"});
        }
    };

    listbox_worlds->on_selection_changed += [=](easyvrui::control_base &, easyvrui::event_args_t &)
    {
        if(listbox_worlds->get_selected_index() >= 0)
        {
            label_status->set_text(U"准备传送：" + listbox_worlds->get_selected_item());
        }
        else
        {
            label_status->set_text(U"未选择任何世界");
        }
    };

    button_add->on_click += [=](easyvrui::control_base &, easyvrui::event_args_t &)
    {
        auto name = combobox_add->get_text();
        if(!name.empty())
        {
            listbox_worlds->get_item_list().insert(0u, name);
            listbox_worlds->set_selected_index(0);
        }
    };

    button_remove->on_click += [=](easyvrui::control_base &, easyvrui::event_args_t &)
    {
        auto idx = listbox_worlds->get_selected_index();
        if(idx >= 0)
        {
            listbox_worlds->get_item_list().remove(static_cast<size_t>(idx));
        }
    };

    button_toggle_drop->on_click += [=](easyvrui::control_base &, easyvrui::event_args_t &)
    {
        combobox_category->set_dropped_down(!combobox_category->get_dropped_down());
    };

    window_main->show();
    easyvrui::run(U"world_teleporter");
    return 0;
}