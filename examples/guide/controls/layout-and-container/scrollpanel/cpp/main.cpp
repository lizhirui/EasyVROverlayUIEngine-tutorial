#include <easyvrui.h>
#include <memory>

using namespace std;
using namespace easyvrui;

shared_ptr<window> create_scrollpanel_demo()
{
    auto window_main = make_shared<window>(U"window_main");
    window_main->set_title(U"同步日志");
    window_main->set_size(690u, 405u);
    auto label_prompt = make_shared<label>(U"label_prompt");
    label_prompt->set_rect(rectangle_t{36u, 76u, 618u, 48u});
    label_prompt->set_text(U"滚动查看同步步骤");
    window_main->get_control_list().add(label_prompt);
    auto scrollpanel_log = make_shared<scrollpanel>(U"scrollpanel_log");
    scrollpanel_log->set_rect(rectangle_t{36u, 135u, 618u, 188u});
    window_main->get_control_list().add(scrollpanel_log);
    auto label_log_1 = make_shared<label>(U"label_log_1");
    label_log_1->set_rect(rectangle_t{14u, 8u, 560u, 42u});
    label_log_1->set_text(U"01 读取配置");
    scrollpanel_log->get_control_list().add(label_log_1);
    auto label_log_2 = make_shared<label>(U"label_log_2");
    label_log_2->set_rect(rectangle_t{14u, 68u, 560u, 42u});
    label_log_2->set_text(U"02 检查目录");
    scrollpanel_log->get_control_list().add(label_log_2);
    auto label_log_3 = make_shared<label>(U"label_log_3");
    label_log_3->set_rect(rectangle_t{14u, 128u, 560u, 42u});
    label_log_3->set_text(U"03 建立连接");
    scrollpanel_log->get_control_list().add(label_log_3);
    auto label_log_4 = make_shared<label>(U"label_log_4");
    label_log_4->set_rect(rectangle_t{14u, 188u, 560u, 42u});
    label_log_4->set_text(U"04 同步图像");
    scrollpanel_log->get_control_list().add(label_log_4);
    auto label_log_5 = make_shared<label>(U"label_log_5");
    label_log_5->set_rect(rectangle_t{14u, 248u, 560u, 42u});
    label_log_5->set_text(U"05 校验数据");
    scrollpanel_log->get_control_list().add(label_log_5);
    auto label_log_6 = make_shared<label>(U"label_log_6");
    label_log_6->set_rect(rectangle_t{14u, 308u, 560u, 42u});
    label_log_6->set_text(U"06 生成报告");
    scrollpanel_log->get_control_list().add(label_log_6);
    auto label_footer = make_shared<label>(U"label_footer");
    label_footer->set_rect(rectangle_t{36u, 334u, 618u, 37u});
    label_footer->set_text(U"日志记录按时间排列");
    window_main->get_control_list().add(label_footer);
    scrollpanel_log->set_horizontal_scrollbar_visible(false);
    label_log_1->set_background_color(0x243b50ffu);
    label_log_2->set_background_color(0x1d2f43ffu);
    label_log_3->set_background_color(0x243b50ffu);
    label_log_4->set_background_color(0x1d2f43ffu);
    label_log_5->set_background_color(0x243b50ffu);
    label_log_6->set_background_color(0x1d2f43ffu);
    return window_main;
}

#if !defined(TUTORIAL_CAPTURE_controls_second)
int main(){auto window_main = create_scrollpanel_demo(); window_main->show(); easyvrui::run(U"tutorial_scrollpanel"); return 0;}

#endif