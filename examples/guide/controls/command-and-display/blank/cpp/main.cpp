#include <easyvrui.h>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

using namespace std;
using namespace easyvrui;

shared_ptr<window> create_blank_demo()
{
    auto window_main = make_shared<window>(U"window_main");
    window_main->set_title(U"延迟安装内容");
    window_main->set_size(680u, 340u);
    auto content = make_shared<panel>(U"panel_content");
    content->set_rect({36u, 83u, 608u, 127u});
    auto placeholder = make_shared<blank>(U"blank_content");
    placeholder->set_rect({16u, 23u, 536u, 59u});
    content->get_control_list().add(placeholder);
    auto button_load = make_shared<button>(U"button_load");
    button_load->set_rect({36u, 240u, 220u, 47u});
    button_load->set_text(U"加载内容");

    button_load->on_click += [content, placeholder](control_base &source, event_args_t &)
    {
        auto &collection = content->get_control_list();
        auto index = collection.get_index(*placeholder);
        auto item = make_shared<label>(U"label_content");
        item->set_rect(placeholder->get_rect());
        item->set_text(U"内容已加载");
        collection.remove(index);
        collection.insert(index, item);
        static_cast<button &>(source).set_enabled(false);
    };

    window_main->get_control_list().add(content);
    window_main->get_control_list().add(button_load);
    return window_main;
}

#if !defined(TUTORIAL_CAPTURE_controls_third)
int main(){auto window_main = create_blank_demo(); window_main->show(); easyvrui::run(U"tutorial_blank"); return 0;}

#endif