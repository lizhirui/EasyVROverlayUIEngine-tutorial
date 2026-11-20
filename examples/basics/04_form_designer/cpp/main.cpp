#include "quick_shout_window.h"
#include <easyvrui.h>
#include <functional>
#include <memory>

class my_shout_app
{
    private:
        std::shared_ptr<quick_shout_window> ui;

        void button_send_click(easyvrui::control_base &, easyvrui::event_args_t &)
        {
            auto message = ui->textbox_message->get_text();
            ui->label_hint->set_text(U"已发送：" + message);
        }

    public:
        my_shout_app() : ui(std::make_shared<quick_shout_window>())
        {
            ui->button_send->on_click += [this](easyvrui::control_base &source, easyvrui::event_args_t &event)
            {
                button_send_click(source, event);
            };
        }

        void show()
        {
            ui->show();
        }

        const std::shared_ptr<quick_shout_window> &get_window() const
        {
            return ui;
        }
};

#if defined(TUTORIAL_CAPTURE_project_story)

void use_shout_window(const std::function<void(const std::shared_ptr<easyvrui::window> &)> &capture)
{
    my_shout_app app_main;
    capture(app_main.get_window());
}

#else

int main(){my_shout_app app_main; app_main.show(); easyvrui::run(U"quick_shout_app"); return 0;}

#endif