#include <easyvrui.h>
#include <memory>
#include <vector>

using namespace std;

int main()
{
    auto window_main = make_shared<easyvrui::window>(U"window_main");
    window_main->set_title(U"VR 迷你看图与副屏切换窗");
    window_main->set_rect(easyvrui::rectangle_t{0u, 0u, 760u, 480u});

    auto menubar_main = make_shared<easyvrui::menubar>(U"menubar_main");
    auto menu_view = make_shared<easyvrui::menuitem>(U"menu_view");
    menu_view->set_text(U"视图(&V)");
    auto menu_toggle_screen = make_shared<easyvrui::menuitem>(U"menu_toggle_screen");
    menu_toggle_screen->set_text(U"显示实时副屏(&S)");
    menu_toggle_screen->set_shortcut(U"Ctrl+M");
    menu_toggle_screen->set_checkable(true);
    menu_toggle_screen->set_checked(true);
    menu_view->get_control_list().add(menu_toggle_screen);
    menubar_main->get_control_list().add(menu_view);
    window_main->set_menu(menubar_main);

    auto make_swatch = [](uint8_t r, uint8_t g, uint8_t b)
    {
        return make_shared<drawing_image>(1u, 1u, vector<uint8_t>{r, g, b, 255u});
    };

    auto toolbar_main = make_shared<easyvrui::toolbar>(U"toolbar_main");
    toolbar_main->set_rect(easyvrui::rectangle_t{20u, 88u, 720u, 40u});
    toolbar_main->set_tool_size(36u);
    toolbar_main->set_spacing(8.0);
    auto &btn_fit = toolbar_main->get_button_list().add(U"btn_fit");
    btn_fit.set_icon(make_swatch(80u, 200u, 160u));
    btn_fit.set_tooltip_text(U"切换图片缩放模式");
    auto &btn_sep = toolbar_main->get_button_list().add(U"btn_sep");
    btn_sep.set_separator(true);
    auto &btn_next_screen = toolbar_main->get_button_list().add(U"btn_next_screen");
    btn_next_screen.set_icon(make_swatch(240u, 170u, 70u));
    btn_next_screen.set_tooltip_text(U"切换显示器编号（0 / 1）");

    vector<uint8_t> pixels;
    pixels.reserve(64u * 64u * 4u);
    for(size_t row = 0u;row < 64u;row++)
    {
        for(size_t col = 0u;col < 64u;col++)
        {
            bool is_blue = (((row / 8u) + (col / 8u)) % 2u) == 0u;
            pixels.push_back(is_blue ? 60u : 32u);
            pixels.push_back(is_blue ? 160u : 48u);
            pixels.push_back(is_blue ? 235u : 72u);
            pixels.push_back(255u);
        }
    }

    auto image_preview = make_shared<easyvrui::image>(U"image_preview");
    image_preview->set_rect(easyvrui::rectangle_t{20u, 136u, 350u, 290u});
    image_preview->set_source(make_shared<drawing_image>(64u, 64u, pixels));
    image_preview->set_stretch_mode(easyvrui::image_stretch_mode_t::contain);

    auto screen_monitor = make_shared<easyvrui::screen>(U"screen_monitor");
    screen_monitor->set_rect(easyvrui::rectangle_t{390u, 136u, 350u, 290u});
    screen_monitor->set_screen_id(0u);

    auto label_status = make_shared<easyvrui::label>(U"label_status");
    label_status->set_rect(easyvrui::rectangle_t{20u, 438u, 720u, 32u});
    label_status->set_text(U"当前模式：image=contain");

    btn_fit.on_click += [=](easyvrui::control_base &, easyvrui::event_args_t &)
    {
        auto next_mode = (image_preview->get_stretch_mode() == easyvrui::image_stretch_mode_t::contain) ? easyvrui::image_stretch_mode_t::fill : easyvrui::image_stretch_mode_t::contain;
        image_preview->set_stretch_mode(next_mode);
        label_status->set_text(next_mode == easyvrui::image_stretch_mode_t::fill ? U"拉伸模式：fill" : U"拉伸模式：contain");
    };
    btn_next_screen.on_click += [=](easyvrui::control_base &, easyvrui::event_args_t &)
    {
        uint64_t next_id = (screen_monitor->get_screen_id() == 0u) ? 1u : 0u;
        screen_monitor->set_screen_id(next_id);
        label_status->set_text(next_id == 0u ? U"当前显示器 #0" : U"当前显示器 #1");
    };
    menu_toggle_screen->on_click += [=](easyvrui::control_base &, easyvrui::event_args_t &)
    {
        bool next_checked = !menu_toggle_screen->get_checked();
        menu_toggle_screen->set_checked(next_checked);
        screen_monitor->set_visible(next_checked);
    };

    window_main->get_control_list().add(toolbar_main);
    window_main->get_control_list().add(image_preview);
    window_main->get_control_list().add(screen_monitor);
    window_main->get_control_list().add(label_status);
    window_main->show();
    easyvrui::run(U"media_viewer");
    return 0;
}