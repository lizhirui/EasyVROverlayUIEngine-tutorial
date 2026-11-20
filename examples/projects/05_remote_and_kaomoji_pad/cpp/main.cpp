#include <easyvrui.h>
#include <memory>
#include <string>
#include <vector>

using namespace std;

class kaomoji_ime : public easyvrui::input_provider
{
    private:
        shared_ptr<easyvrui::window> pad;

    protected:
        void process_state(easyvrui::input_ui_state_t &state) override
        {
            if(state.active)
            {
                pad->show();
            }
            else
            {
                pad->hide();
            }
        }

        void process_input(easyvrui::input_event_t &event) override
        {
            send_event(event);
        }

    public:
        kaomoji_ime()
        {
            pad = make_shared<easyvrui::window>(U"kaomoji_pad");
            pad->set_title(U"颜文字小键盘");
            pad->set_rect(easyvrui::rectangle_t{0u, 0u, 520u, 150u});
            pad->set_show_title_bar(false);
            pad->set_auxiliary(true);

            vector<u32string> kaomoji_list{U"(｡･ω･｡)ﾉ♡", U"(つд⊂)ｴｰﾝ", U"(ﾉ´ヮ`)ﾉ*:･ﾟ✧", U"(*￣3￣)╭"};

            for(size_t index = 0u;index < kaomoji_list.size();index++)
            {
                auto suffix = to_string(index);
                auto btn = make_shared<easyvrui::button>(U"btn_kaomoji_" + u32string(suffix.begin(), suffix.end()));
                btn->set_rect(easyvrui::rectangle_t{12u + (index * 126u), 16u, 118u, 48u});
                btn->set_text(kaomoji_list[index]);
                u32string value = kaomoji_list[index];

                btn->on_click += [this, value](easyvrui::control_base &, easyvrui::event_args_t &)
                {
                    begin_input_task();
                    try
                    {
                        easyvrui::input_event_t item;
                        item.event_type = "ime_submit";
                        item.text = value;
                        send_event(item);
                    }
                    catch(...)
                    {
                        finish_input_task();
                        throw;
                    }

                    finish_input_task();
                };

                pad->get_control_list().add(btn);
            }
        }
};

int main()
{
    kaomoji_ime pad_provider;
    pad_provider.register_provider(easyvrui::input_role_t::ime, false, U"Kaomoji Pad", U"en");
    pad_provider.run();
    return 0;
}