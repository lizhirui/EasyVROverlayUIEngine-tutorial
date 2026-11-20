#include <easyvrui.h>
#include <memory>

using namespace std;
using namespace easyvrui;

shared_ptr<window> create_panel_demo()
{
    auto window_main = make_shared<window>(U"window_main");
    window_main->set_title(U"连接分组");
    window_main->set_size(690u, 363u);
    auto panel_connection = make_shared<panel>(U"panel_connection");
    panel_connection->set_rect(rectangle_t{36u, 80u, 618u, 238u});
    window_main->get_control_list().add(panel_connection);
    auto label_title = make_shared<label>(U"label_title");
    label_title->set_rect(rectangle_t{16u, 12u, 520u, 46u});
    label_title->set_text(U"同步服务");
    panel_connection->get_control_list().add(label_title);
    auto panel_detail = make_shared<panel>(U"panel_detail");
    panel_detail->set_rect(rectangle_t{16u, 66u, 586u, 64u});
    panel_connection->get_control_list().add(panel_detail);
    auto label_detail = make_shared<label>(U"label_detail");
    label_detail->set_rect(rectangle_t{14u, 8u, 550u, 44u});
    label_detail->set_text(U"连接正常，可以开始同步");
    panel_detail->get_control_list().add(label_detail);
    auto button_detail = make_shared<button>(U"button_detail");
    button_detail->set_rect(rectangle_t{16u, 159u, 220u, 48u});
    button_detail->set_text(U"隐藏连接详情");
    panel_connection->get_control_list().add(button_detail);
    panel_connection->set_background_color(0x203046ffu);
    panel_detail->set_background_color(0x1b403affu);

    button_detail->on_click += [detail = panel_detail.get()](control_base &source, event_args_t &)
    {
        bool visible = !detail->get_visible();
        detail->set_visible(visible);
        static_cast<button &>(source).set_text(visible ? U"隐藏连接详情" : U"显示连接详情");
    };

    return window_main;
}

#if !defined(TUTORIAL_CAPTURE_controls_second)
int main(){auto window_main = create_panel_demo(); window_main->show(); easyvrui::run(U"tutorial_panel"); return 0;}

#endif