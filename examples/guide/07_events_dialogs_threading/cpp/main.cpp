#include <chrono>
#include <cstdint>
#include <easyvrui.h>
#include <memory>
#include <string>
#include <thread>

using namespace std;
using namespace easyvrui;

int main()
{
    auto window_main = make_shared<window>(U"window_main");
    window_main->set_title(U"同步计时器");
    window_main->set_size(540u, 258u);
    auto label_time = make_shared<label>(U"label_time");
    label_time->set_rect({36u, 80u, 468u, 56u});
    label_time->set_font(font_t{U"Microsoft YaHei UI", 27u});
    label_time->set_text(U"剩余25秒");
    auto button_note = make_shared<button>(U"button_note");
    button_note->set_rect({36u, 160u, 220u, 48u});
    button_note->set_text(U"填写任务备注");

    button_note->on_click += [owner = window_main.get()](control_base &source, event_args_t &)
    {
        auto value = inputbox(U"填写本次同步的备注", U"任务备注", {}, 48u, owner);

        if(value)
        {
            static_cast<button &>(source).set_text(U"备注已填写");
        }
    };

    window_main->get_control_list().add(label_time);
    window_main->get_control_list().add(button_note);
    window_main->show();
    weak_ptr<label> destination = label_time;

    jthread worker([destination](stop_token stop)
    {
        for(int64_t remaining = 24;remaining >= 0;remaining--)
        {
            this_thread::sleep_for(chrono::seconds(1));

            if(stop.stop_requested())
            {
                return;
            }

            if(auto target = destination.lock())
            {
                target->begin_invoke([destination, remaining]()
                {
                    if(auto current = destination.lock())
                    {
                        string counter = to_string(remaining);
                        current->set_text((U"剩余" + u32string(counter.begin(), counter.end())) + U"秒");
                    }
                });
            }
        }
    });

    easyvrui::run(U"tutorial_timer");
    worker.request_stop();
    return 0;
}