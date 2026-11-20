#include <easyvrui.h>
#include <cstdint>
#include <memory>

using namespace std;
using namespace easyvrui;

shared_ptr<window> create_textbox_demo()
{
    auto window_main = make_shared<window>(U"window_main");
    window_main->set_title(U"编辑备注");
    window_main->set_size(650u, 420u);
    auto label_caption = make_shared<label>(U"label_caption");
    label_caption->set_rect(rectangle_t{32u, 82u, 580u, 40u});
    label_caption->set_text(U"备注（最多80个字符）");
    window_main->get_control_list().add(label_caption);
    auto textbox_note = make_shared<textbox>(U"textbox_note");
    textbox_note->set_rect(rectangle_t{32u, 132u, 586u, 125u});
    window_main->get_control_list().add(textbox_note);
    auto label_state = make_shared<label>(U"label_state");
    label_state->set_rect(rectangle_t{32u, 274u, 580u, 46u});
    label_state->set_text(U"请编辑或选择备注");
    window_main->get_control_list().add(label_state);
    auto button_select = make_shared<button>(U"button_select");
    button_select->set_rect(rectangle_t{32u, 329u, 176u, 42u});
    button_select->set_text(U"全选备注");
    window_main->get_control_list().add(button_select);
    textbox_note->set_multiline(true);
    textbox_note->set_vertical_scrollbar_visible(true);
    textbox_note->set_max_length(80u);
    textbox_note->set_text(U"第一行：检查连接\n第二行：同步配置");

    textbox_note->on_text_changed += [label_state](control_base &, event_args_t &)
    {
        label_state->set_text(U"备注已修改");
    };

    button_select->on_click += [textbox_note](control_base &, event_args_t &)
    {
        textbox_note->focus();
        textbox_note->select(0u, static_cast<uint64_t>(textbox_note->get_text().size()));
    };

    return window_main;
}

#if !defined(TUTORIAL_CAPTURE_controls)
int main(){auto window_main = create_textbox_demo(); window_main->show(); easyvrui::run(U"tutorial_textbox"); return 0;}

#endif