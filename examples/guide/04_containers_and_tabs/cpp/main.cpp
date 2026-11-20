#include <easyvrui.h>
#include <memory>
#include <string>

using namespace std;

int main()
{
    auto window_main = make_shared<easyvrui::window>(U"window_main");
    window_main->set_title(U"多功能 VR 设置中心");
    window_main->set_rect(easyvrui::rectangle_t{0u, 0u, 620u, 440u});

    auto tabcontrol_main = make_shared<easyvrui::tabcontrol>(U"tabcontrol_main");
    tabcontrol_main->set_rect(easyvrui::rectangle_t{20u, 56u, 580u, 330u});
    tabcontrol_main->set_tab_position(easyvrui::tab_position_t::top);
    tabcontrol_main->set_tab_size(38u);
    tabcontrol_main->set_page_close_button_visible(true);

    auto page_general = make_shared<easyvrui::tabpage>(U"page_general");
    page_general->set_text(U"常规设置");

    auto button_new_tab = make_shared<easyvrui::button>(U"button_new_tab");
    button_new_tab->set_rect(easyvrui::rectangle_t{20u, 20u, 200u, 40u});
    button_new_tab->set_text(U"新建临时配置页");
    page_general->get_control_list().add(button_new_tab);

    auto page_advanced = make_shared<easyvrui::tabpage>(U"page_advanced");
    page_advanced->set_text(U"高级布局");

    auto splitter_main = make_shared<easyvrui::splitter>(U"splitter_main");
    splitter_main->set_rect(easyvrui::rectangle_t{12u, 12u, 556u, 268u});
    splitter_main->set_orientation(easyvrui::orientation_t::vertical);
    splitter_main->set_split_position(0.35);

    auto panel_nav = make_shared<easyvrui::panel>(U"panel_nav");
    auto label_nav = make_shared<easyvrui::label>(U"label_nav");
    label_nav->set_rect(easyvrui::rectangle_t{12u, 16u, 150u, 32u});
    label_nav->set_text(U"左侧分栏（可拖动）");
    panel_nav->get_control_list().add(label_nav);

    auto scrollpanel_options = make_shared<easyvrui::scrollpanel>(U"scrollpanel_options");
    for(uint64_t idx = 0u;idx < 10u;idx++)
    {
        auto num_str = to_string(idx + 1u);
        auto u32_num = u32string(num_str.begin(), num_str.end());
        auto item = make_shared<easyvrui::checkbox>(U"checkbox_opt_" + u32_num);
        item->set_rect(easyvrui::rectangle_t{16u, 12u + (idx * 44u), 260u, 34u});
        item->set_text(U"实验性 VR 选项 #" + u32_num);
        scrollpanel_options->get_control_list().add(item);
    }

    splitter_main->get_control_list().add(panel_nav);
    splitter_main->get_control_list().add(scrollpanel_options);
    page_advanced->get_control_list().add(splitter_main);

    tabcontrol_main->get_page_list().add(page_general);
    tabcontrol_main->get_page_list().add(page_advanced);
    tabcontrol_main->set_selected_index(0);

    auto label_status = make_shared<easyvrui::label>(U"label_status");
    label_status->set_rect(easyvrui::rectangle_t{20u, 396u, 580u, 32u});
    label_status->set_text(U"当前页签：常规设置");

    auto extra_counter = make_shared<int>(0);
    button_new_tab->on_click += [=](easyvrui::control_base &, easyvrui::event_args_t &)
    {
        (*extra_counter)++;
        auto num_str = to_string(*extra_counter);
        auto u32_num = u32string(num_str.begin(), num_str.end());
        auto page_extra = make_shared<easyvrui::tabpage>(U"page_extra_" + u32_num);
        page_extra->set_text(U"配置 #" + u32_num);
        tabcontrol_main->get_page_list().add(page_extra);
        tabcontrol_main->set_selected_index(static_cast<int64_t>(tabcontrol_main->get_page_list().get_size()) - 1);
    };

    tabcontrol_main->on_page_close += [=](easyvrui::control_base &, easyvrui::tabpage_event_args_t &event)
    {
        if((event.index >= 2u) && (event.page != nullptr))
        {
            tabcontrol_main->get_page_list().remove(event.index);
        }
        else
        {
            label_status->set_text(U"基础页签不可关闭！");
        }
    };

    tabcontrol_main->on_selection_changed += [=](easyvrui::control_base &, easyvrui::event_args_t &)
    {
        auto *page = tabcontrol_main->get_selected_page();
        label_status->set_text(page ? (U"当前页签：" + page->get_text()) : u32string(U"无选中页"));
    };

    splitter_main->on_split_position_changed += [=](easyvrui::control_base &, easyvrui::event_args_t &)
    {
        auto pos_str = to_string(splitter_main->get_split_position());
        label_status->set_text(U"分隔比例：" + u32string(pos_str.begin(), pos_str.end()));
    };

    scrollpanel_options->on_viewport_changed += [=](easyvrui::control_base &, easyvrui::event_args_t &)
    {
        label_status->set_text(U"右侧设置面板正在滚动...");
    };

    window_main->get_control_list().add(tabcontrol_main);
    window_main->get_control_list().add(label_status);
    window_main->show();
    easyvrui::run(U"settings_hub");
    return 0;
}