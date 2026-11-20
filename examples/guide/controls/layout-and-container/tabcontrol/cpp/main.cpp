#include <easyvrui.h>
#include <memory>

using namespace std;
using namespace easyvrui;

shared_ptr<window> create_tabcontrol_demo()
{
    auto window_main = make_shared<window>(U"window_main");
    window_main->set_title(U"同步工作台");
    window_main->set_size(690u, 400u);
    auto tabcontrol_workspace = make_shared<tabcontrol>(U"tabcontrol_workspace");
    tabcontrol_workspace->set_rect(rectangle_t{36u, 83u, 618u, 270u});
    window_main->get_control_list().add(tabcontrol_workspace);
    auto tabpage_status = make_shared<tabpage>(U"tabpage_status");
    tabpage_status->set_text(U"概览");
    tabcontrol_workspace->get_page_list().add(tabpage_status);
    auto label_summary = make_shared<label>(U"label_summary");
    label_summary->set_rect(rectangle_t{18u, 20u, 520u, 49u});
    label_summary->set_text(U"同步服务已连接");
    tabpage_status->get_control_list().add(label_summary);
    auto tabpage_history = make_shared<tabpage>(U"tabpage_history");
    tabpage_history->set_text(U"历史");
    tabcontrol_workspace->get_page_list().add(tabpage_history);
    auto label_last = make_shared<label>(U"label_last");
    label_last->set_rect(rectangle_t{18u, 20u, 520u, 49u});
    label_last->set_text(U"最近一次同步已完成");
    tabpage_history->get_control_list().add(label_last);
    auto label_count = make_shared<label>(U"label_count");
    label_count->set_rect(rectangle_t{18u, 83u, 520u, 49u});
    label_count->set_text(U"已核验12份文件");
    tabpage_history->get_control_list().add(label_count);
    tabcontrol_workspace->set_tab_size(42u);
    tabcontrol_workspace->set_selected_tab_background_color(0x31615dffu);
    return window_main;
}

#if !defined(TUTORIAL_CAPTURE_controls_second)
int main(){auto window_main = create_tabcontrol_demo(); window_main->show(); easyvrui::run(U"tutorial_tabcontrol"); return 0;}

#endif