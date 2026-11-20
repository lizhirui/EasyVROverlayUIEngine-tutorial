#include <easyvrui.h>
#include <memory>
#include <string>

using namespace std;

int main()
{
    auto window_main = make_shared<easyvrui::window>(U"window_main");
    window_main->set_title(U"头显环境调音台");
    window_main->set_rect(easyvrui::rectangle_t{0u, 0u, 560u, 420u});

    auto label_summary = make_shared<easyvrui::label>(U"label_summary");
    label_summary->set_rect(easyvrui::rectangle_t{24u, 56u, 512u, 36u});

    auto checkbox_mute = make_shared<easyvrui::checkbox>(U"checkbox_mute");
    checkbox_mute->set_rect(easyvrui::rectangle_t{24u, 104u, 220u, 36u});
    checkbox_mute->set_text(U"全局静音");

    auto checkbox_ducking = make_shared<easyvrui::checkbox>(U"checkbox_ducking");
    checkbox_ducking->set_rect(easyvrui::rectangle_t{260u, 104u, 276u, 36u});
    checkbox_ducking->set_text(U"说话时自动压低音乐");
    checkbox_ducking->set_checked(true);

    auto panel_scene = make_shared<easyvrui::panel>(U"panel_scene");
    panel_scene->set_rect(easyvrui::rectangle_t{24u, 156u, 220u, 140u});
    auto radio_party = make_shared<easyvrui::radiobutton>(U"radio_party");
    radio_party->set_rect(easyvrui::rectangle_t{12u, 12u, 196u, 32u});
    radio_party->set_text(U"聚会模式（全响）");
    radio_party->set_checked(true);
    auto radio_cinema = make_shared<easyvrui::radiobutton>(U"radio_cinema");
    radio_cinema->set_rect(easyvrui::rectangle_t{12u, 52u, 196u, 32u});
    radio_cinema->set_text(U"影院模式（重低音）");
    auto radio_sleep = make_shared<easyvrui::radiobutton>(U"radio_sleep");
    radio_sleep->set_rect(easyvrui::rectangle_t{12u, 92u, 196u, 32u});
    radio_sleep->set_text(U"睡眠模式（柔和）");
    panel_scene->get_control_list().add(radio_party);
    panel_scene->get_control_list().add(radio_cinema);
    panel_scene->get_control_list().add(radio_sleep);

    auto slider_master = make_shared<easyvrui::slider>(U"slider_master");
    slider_master->set_rect(easyvrui::rectangle_t{260u, 160u, 210u, 36u});
    slider_master->set_value(75);

    auto slider_bgm = make_shared<easyvrui::slider>(U"slider_bgm");
    slider_bgm->set_rect(easyvrui::rectangle_t{492u, 156u, 36u, 140u});
    slider_bgm->set_orientation(easyvrui::orientation_t::vertical);
    slider_bgm->set_value(60);

    auto numeric_gain = make_shared<easyvrui::numericupdown>(U"numeric_gain");
    numeric_gain->set_rect(easyvrui::rectangle_t{260u, 220u, 210u, 40u});
    numeric_gain->set_minimum(-12.0);
    numeric_gain->set_maximum(12.0);
    numeric_gain->set_step(0.5);
    numeric_gain->set_decimal_places(1u);
    numeric_gain->set_value(1.5);

    auto progressbar_level = make_shared<easyvrui::progressbar>(U"progressbar_level");
    progressbar_level->set_rect(easyvrui::rectangle_t{24u, 360u, 512u, 28u});

    window_main->get_control_list().add(label_summary);
    window_main->get_control_list().add(checkbox_mute);
    window_main->get_control_list().add(checkbox_ducking);
    window_main->get_control_list().add(panel_scene);
    window_main->get_control_list().add(slider_master);
    window_main->get_control_list().add(slider_bgm);
    window_main->get_control_list().add(numeric_gain);
    window_main->get_control_list().add(progressbar_level);

    auto refresh_mixer = [=]()
    {
        auto state = checkbox_mute->get_checked() ? u32string(U"已静音") : u32string(U"正常播放");
        auto duck = checkbox_ducking->get_checked() ? u32string(U"开启") : u32string(U"关闭");
        progressbar_level->set_value(checkbox_mute->get_checked() ? 0 : (slider_master->get_value() * slider_bgm->get_value()) / 100);
        label_summary->set_text(U"状态：" + state + U" | 自动压低：" + duck);
    };

    checkbox_mute->on_checked_changed += [=](easyvrui::control_base &, easyvrui::event_args_t &)
    {
        refresh_mixer();
    };
    checkbox_ducking->on_checked_changed += [=](easyvrui::control_base &, easyvrui::event_args_t &)
    {
        refresh_mixer();
    };
    slider_master->on_value_changed += [=](easyvrui::control_base &, easyvrui::event_args_t &)
    {
        refresh_mixer();
    };
    slider_bgm->on_value_changed += [=](easyvrui::control_base &, easyvrui::event_args_t &)
    {
        refresh_mixer();
    };
    numeric_gain->on_value_changed += [=](easyvrui::control_base &, easyvrui::event_args_t &)
    {
        refresh_mixer();
    };

    refresh_mixer();
    window_main->show();
    easyvrui::run(U"vr_mixer");
    return 0;
}