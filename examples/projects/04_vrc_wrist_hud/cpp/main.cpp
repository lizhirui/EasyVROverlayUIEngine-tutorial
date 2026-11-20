#include <easyvrui.h>
#include <algorithm>
#include <memory>
#include <string>

using namespace std;

class mic_meter_control : public easyvrui::control
{
    private:
        double level = 0.4;
        easyvrui::font_t meter_font{U"Segoe UI", 16u, true, false};

    protected:
        void render(easyvrui::render_context &context) const override
        {
            easyvrui::control::render(context);
            auto r = context.get_rectangle(*this);
            context.fill_rounded_rectangle(r, 8.0, 8.0, 0x162738FFu);
            double bar_width = max(0.0, (r.width - 16.0) * level);
            context.fill_rounded_rectangle(easyvrui::render_rectangle_t{r.left + 8.0, r.top + 8.0, bar_width, r.height - 16.0}, 6.0, 6.0, 0x4CAF50FFu);
            context.draw_text(U"MIC 40%", meter_font, r, 0xFFFFFFFFu, true);
        }

    public:
        explicit mic_meter_control(const u32string &name) : easyvrui::control(name)
        {
        }
};

int main()
{
    auto window_wrist = make_shared<easyvrui::window>(U"window_wrist");
    window_wrist->set_title(U"左手腕 HUD");
    window_wrist->set_rect(easyvrui::rectangle_t{0u, 0u, 260u, 220u});
    window_wrist->set_physical_scale(0.65);
    window_wrist->set_startup_position(easyvrui::startup_position_t::none);
    window_wrist->set_reference_object(easyvrui::reference_object_t{easyvrui::reference_object_type_t::left});
    window_wrist->set_position(easyvrui::vec3_t{-0.08, 0.08, -0.10});
    window_wrist->set_rotation(easyvrui::vec3_t{-35.0, 0.0, 0.0});

    auto meter_mic = make_shared<mic_meter_control>(U"meter_mic");
    meter_mic->set_rect(easyvrui::rectangle_t{16u, 64u, 228u, 56u});

    auto button_toggle_screen = make_shared<easyvrui::button>(U"button_toggle_screen");
    button_toggle_screen->set_rect(easyvrui::rectangle_t{16u, 134u, 228u, 40u});
    button_toggle_screen->set_text(U"显示/隐藏弯曲副屏");

    auto window_subscreen = make_shared<easyvrui::window>(U"window_subscreen");
    window_subscreen->set_title(U"弧面电脑副屏");
    window_subscreen->set_rect(easyvrui::rectangle_t{0u, 0u, 960u, 560u});
    window_subscreen->set_curvature(0.65);
    window_subscreen->set_reference_object(easyvrui::reference_object_t{easyvrui::reference_object_type_t::body});

    auto screen_main = make_shared<easyvrui::screen>(U"screen_main");
    screen_main->set_rect(easyvrui::rectangle_t{16u, 64u, 928u, 480u});
    screen_main->set_screen_id(0u);
    window_subscreen->get_control_list().add(screen_main);

    button_toggle_screen->on_click += [window_subscreen](easyvrui::control_base &, easyvrui::event_args_t &)
    {
        if(window_subscreen->get_visible())
        {
            window_subscreen->hide();
        }
        else
        {
            window_subscreen->show();
        }
    };

    window_wrist->get_control_list().add(meter_mic);
    window_wrist->get_control_list().add(button_toggle_screen);
    window_wrist->show();
    easyvrui::run(U"vrc_wrist_hud");
    return 0;
}