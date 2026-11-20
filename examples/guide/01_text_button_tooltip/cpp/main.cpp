#include <easyvrui.h>
#include <memory>
#include <string>
#include <vector>

using namespace std;

int main()
{
    auto window_main = make_shared<easyvrui::window>(U"window_main");
    window_main->set_title(U"VRChat 情绪标签牌");
    window_main->set_rect(easyvrui::rectangle_t{0u, 0u, 560u, 420u});

    auto label_preview = make_shared<easyvrui::label>(U"label_preview");
    label_preview->set_rect(easyvrui::rectangle_t{24u, 60u, 512u, 48u});
    label_preview->set_font(easyvrui::font_t{U"Segoe UI", 22u, true, false});
    label_preview->set_foreground_color(0x7FE3FFFFu);

    auto textbox_mood = make_shared<easyvrui::textbox>(U"textbox_mood");
    textbox_mood->set_rect(easyvrui::rectangle_t{24u, 120u, 512u, 130u});
    textbox_mood->set_text(U"在线发呆中...");
    textbox_mood->set_multiline(true);
    textbox_mood->set_vertical_scrollbar_visible(true);
    textbox_mood->set_max_length(80u);
    textbox_mood->set_tooltip_text(U"最多80个字符，支持多行输入");

    auto label_status = make_shared<easyvrui::label>(U"label_status");
    label_status->set_rect(easyvrui::rectangle_t{24u, 260u, 512u, 32u});

    auto button_undo = make_shared<easyvrui::button>(U"button_undo");
    button_undo->set_rect(easyvrui::rectangle_t{24u, 360u, 120u, 40u});
    button_undo->set_text(U"撤销");
    button_undo->set_tooltip_text(U"撤销上一步编辑（Ctrl+Z）");

    auto button_redo = make_shared<easyvrui::button>(U"button_redo");
    button_redo->set_rect(easyvrui::rectangle_t{156u, 360u, 120u, 40u});
    button_redo->set_text(U"重做");
    button_redo->set_tooltip_text(U"恢复刚才的撤销（Ctrl+Y）");

    auto button_select_all = make_shared<easyvrui::button>(U"button_select_all");
    button_select_all->set_rect(easyvrui::rectangle_t{288u, 360u, 120u, 40u});
    button_select_all->set_text(U"全选");

    window_main->get_control_list().add(label_preview);
    window_main->get_control_list().add(textbox_mood);
    window_main->get_control_list().add(label_status);
    window_main->get_control_list().add(button_undo);
    window_main->get_control_list().add(button_redo);
    window_main->get_control_list().add(button_select_all);

    auto update_status = [=]()
    {
        auto text = textbox_mood->get_text();
        label_preview->set_text(U"当前心情：" + text);
        auto count_str = to_string(text.size());
        label_status->set_text(U"字数：" + u32string(count_str.begin(), count_str.end()) + U"/80");
        button_undo->set_enabled(textbox_mood->get_can_undo());
        button_redo->set_enabled(textbox_mood->get_can_redo());
    };

    struct preset_item_t
    {
        u32string name;
        u32string caption;
        u32string snippet;
        uint64_t left;
    };

    vector<preset_item_t> preset_list = {{U"button_mute", U"静音中", U"🔇 麦坏了/Mute中，请看气泡 ", 24u}, {U"button_afk", U"挂机喝茶", U"☕ 暂时离开一下，马上回来 ", 190u}, {U"button_talk", U"欢迎聊天", U"🎮 欢迎过来唠嗑！", 356u}};
    for(const auto &item : preset_list)
    {
        auto btn = make_shared<easyvrui::button>(item.name);
        btn->set_rect(easyvrui::rectangle_t{item.left, 304u, 150u, 42u});
        btn->set_text(item.caption);
        btn->set_tag(item.snippet);
        btn->set_tooltip_text(U"在光标处插入：" + item.snippet);
        btn->on_click += [=](easyvrui::control_base &source, easyvrui::event_args_t &)
        {
            textbox_mood->set_selected_text(source.get_tag());
            textbox_mood->focus();
        };
        window_main->get_control_list().add(btn);
    }

    textbox_mood->on_text_changed += [=](easyvrui::control_base &, easyvrui::event_args_t &)
    {
        update_status();
    };
    textbox_mood->on_selection_changed += [=](easyvrui::control_base &, easyvrui::event_args_t &)
    {
        update_status();
    };
    button_undo->on_click += [=](easyvrui::control_base &, easyvrui::event_args_t &)
    {
        textbox_mood->undo();
        update_status();
    };
    button_redo->on_click += [=](easyvrui::control_base &, easyvrui::event_args_t &)
    {
        textbox_mood->redo();
        update_status();
    };
    button_select_all->on_click += [=](easyvrui::control_base &, easyvrui::event_args_t &)
    {
        textbox_mood->select(0u, textbox_mood->get_text().size());
        textbox_mood->focus();
    };

    update_status();
    window_main->show();
    easyvrui::run(U"mood_board");
    return 0;
}