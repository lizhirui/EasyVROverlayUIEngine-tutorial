#pragma once

#include <easyvrui.h>
#include <memory>
#include <string>

class quick_shout_window : public easyvrui::window
{
    public:
        std::shared_ptr<easyvrui::label> label_hint;
        std::shared_ptr<easyvrui::textbox> textbox_message;
        std::shared_ptr<easyvrui::button> button_send;

        explicit quick_shout_window(const std::u32string &name = U"quick_shout_window");
};