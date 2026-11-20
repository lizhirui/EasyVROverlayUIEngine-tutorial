#include "quick_shout_window.h"
#include <easyvrui.h>
#include <cstddef>
#include <cstdint>
#include <filesystem>
#include <limits>
#include <list>
#include <memory>
#include <optional>
#include <set>
#include <string>
#include <vector>

quick_shout_window::quick_shout_window(const std::u32string &name) : easyvrui::window(name)
{
    this->label_hint = std::make_shared<easyvrui::label>(std::u32string{U"label_hint", std::size_t{10u}});
    this->textbox_message = std::make_shared<easyvrui::textbox>(std::u32string{U"textbox_message", std::size_t{15u}});
    this->button_send = std::make_shared<easyvrui::button>(std::u32string{U"button_send", std::size_t{11u}});
    this->get_control_list().add(this->label_hint);
    this->get_control_list().add(this->textbox_message);
    this->get_control_list().add(this->button_send);
    this->set_rect(easyvrui::rectangle_t{0ull, 0ull, 520ull, 258ull});
    this->set_title(std::u32string{U"\U00009759\U000097f3\U00005feb\U00006377\U0000558a\U00008bdd\U00006761", std::size_t{7u}});
    this->label_hint->set_rect(easyvrui::rectangle_t{24ull, 74ull, 472ull, 30ull});
    this->label_hint->set_text(std::u32string{U"\U00008f93\U00005165\U000060f3\U00008bf4\U00007684\U00008bdd\U0000ff1a", std::size_t{7u}});
    this->textbox_message->set_rect(easyvrui::rectangle_t{24ull, 116ull, 472ull, 46ull});
    this->textbox_message->set_tag(std::u32string{U"chatbox_input", std::size_t{13u}});
    this->textbox_message->set_text(std::u32string{U"", std::size_t{0u}});
    this->button_send->set_rect(easyvrui::rectangle_t{24ull, 180ull, 150ull, 44ull});
    this->button_send->set_text(std::u32string{U"\U000053d1\U00009001", std::size_t{2u}});
    this->button_send->set_tooltip_text(std::u32string{U"\U0000628a\U00006587\U0000672c\U00006846\U000091cc\U00007684\U00005185\U00005bb9\U000053d1\U000051fa\U000053bb", std::size_t{11u}});
}