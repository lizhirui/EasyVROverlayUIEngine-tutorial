#include <algorithm>
#include <easyvrui.h>
#include <memory>

using namespace std;

class wrist_dial_control : public easyvrui::control
{
    public:
        explicit wrist_dial_control(const u32string &name) : easyvrui::control(name)
        {
        }

    protected:
        void render(easyvrui::render_context &context) const override
        {
            auto rc = context.get_rectangle(*this);
            double cx = rc.left + (rc.width * 0.5);
            double cy = rc.top + (rc.height * 0.5);
            double radius = min(rc.width, rc.height) * 0.44;
            uint32_t bg = context.is_hovered(*this) ? 0x1E3A5FFFu : 0x0F172AFFu;
            context.fill_circle(cx, cy, radius, bg);
            context.draw_circle(cx, cy, radius, 0x38BDF8FFu, 3.0);
            drawing_path pointer;
            pointer.move_to(cx, cy).line_to(cx, cy - (radius * 0.65));
            context.outline_path(pointer, 0xFACC15FFu, 3.0);
            context.draw_text(U"12:00", easyvrui::font_t{U"Segoe UI", 22u, true, false}, easyvrui::render_rectangle_t{rc.left, cy + 12.0, rc.width, 34.0}, 0xFFFFFFFFu, true);
        }
};

int main()
{
    auto window_main = make_shared<easyvrui::window>(U"window_main");
    window_main->set_rect(easyvrui::rectangle_t{0u, 0u, 220u, 220u});
    window_main->set_show_title_bar(false);
    window_main->set_startup_position(easyvrui::startup_position_t::none);
    window_main->set_reference_object(easyvrui::reference_object_t{easyvrui::reference_object_type_t::left});
    window_main->set_physical_scale(0.5);
    window_main->set_curvature(1.2);
    window_main->set_position(easyvrui::vec3_t{-0.05, 0.06, 0.08});
    window_main->set_rotation(easyvrui::vec3_t{-45.0, 20.0, 0.0});

    auto dial_watch = make_shared<wrist_dial_control>(U"dial_watch");
    dial_watch->set_rect(easyvrui::rectangle_t{0u, 0u, 220u, 220u});
    dial_watch->on_click += [=](easyvrui::control_base &, easyvrui::event_args_t &)
    {
        if(window_main->get_reference_object().type == easyvrui::reference_object_type_t::left)
        {
            window_main->reparent(easyvrui::reference_object_t{easyvrui::reference_object_type_t::world}, true);
        }
        else
        {
            window_main->set_reference_object(easyvrui::reference_object_t{easyvrui::reference_object_type_t::left});
            window_main->set_position(easyvrui::vec3_t{-0.05, 0.06, 0.08});
            window_main->set_rotation(easyvrui::vec3_t{-45.0, 20.0, 0.0});
        }
    };

    window_main->get_control_list().add(dial_watch);
    window_main->show();
    easyvrui::run(U"wrist_watch");
    return 0;
}