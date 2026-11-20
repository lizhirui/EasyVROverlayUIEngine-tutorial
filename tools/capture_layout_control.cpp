#include "ui_test_host.h"
#include "easyvrui/internal/control_access.h"
#include <easyvrui.h>
#include <array>
#include <chrono>
#include <cstdint>
#include <filesystem>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>
#include <thread>

using namespace std;
using namespace easyvrui;
using nlohmann::json;
shared_ptr<window> create_slider_demo();
shared_ptr<window> create_numericupdown_demo();
shared_ptr<window> create_combobox_demo();
shared_ptr<window> create_listbox_demo();
shared_ptr<window> create_panel_demo();
shared_ptr<window> create_scrollpanel_demo();
shared_ptr<window> create_splitter_demo();
shared_ptr<window> create_tabcontrol_demo();

class capture_layout_control
{
    private:
        static constexpr auto SURFACE_TIMEOUT = chrono::seconds(8);
        static constexpr auto PUMP_INTERVAL = chrono::milliseconds(12);
        static constexpr uint32_t BLUE_BACKGROUND = 0x263f57ffu;
        static constexpr uint32_t GREEN_BACKGROUND = 0x254a40ffu;
        ui_test_host host;

        void pump()
        {
            host.execute({{"action", "step"}});
        }

        void wait_for_surface(const window &surface)
        {
            const auto DEADLINE = chrono::steady_clock::now() + SURFACE_TIMEOUT;

            while(!host.is_surface_ready(surface) && (chrono::steady_clock::now() < DEADLINE))
            {
                pump();
                this_thread::sleep_for(PUMP_INTERVAL);
            }

            if(!host.is_surface_ready(surface))
            {
                throw runtime_error("Tutorial WARP surface did not present");
            }
        }

        void show(const shared_ptr<window> &surface, const string &name)
        {
            host.attach_control(surface, name);
            host.execute({{"action", "show"}, {"name", name}});
            wait_for_surface(*surface);
        }

        void finish(const shared_ptr<window> &surface, const string &name)
        {
            pump();
            wait_for_surface(*surface);
            host.execute({{"action", "snapshot"}, {"window", name}, {"label", name}});
            surface->close(true);
            pump();
        }

        void capture(const shared_ptr<window> &surface, const string &name)
        {
            show(surface, name);
            move_pointer(name, 28.0, 72.0);
            finish(surface, name);
        }

        void move_pointer(const string &name, double left, double top)
        {
            host.execute({{"action", "move"}, {"window", name}, {"left", left}, {"top", top}});
        }

        void click(const string &name, double left, double top)
        {
            host.execute({{"action", "click"}, {"window", name}, {"left", left}, {"top", top}});
        }

        void drag(const string &name, const array<double, 2u> &start, const array<double, 2u> &end)
        {
            host.execute({{"action", "drag"}, {"window", name}, {"from", start}, {"to", end}});
        }

        shared_ptr<window> create_surface(const u32string &title, uint64_t width, uint64_t height)
        {
            auto surface = make_shared<window>(U"window_preview");
            surface->set_title(title);
            surface->set_size(width, height);
            return surface;
        }

        template <typename control_type>
        shared_ptr<control_type> add_control(container_control &owner, const u32string &name, const rectangle_t &rectangle)
        {
            auto result = make_shared<control_type>(name);
            result->set_rect(rectangle);
            owner.get_control_list().add(result);
            return result;
        }

        shared_ptr<label> add_label(container_control &owner, const u32string &name, const rectangle_t &rectangle, const u32string &text)
        {
            auto result = add_control<label>(owner, name, rectangle);
            result->set_text(text);
            return result;
        }

        template <typename control_type>
        void capture_default(const string &name, const rectangle_t &rectangle, uint64_t height)
        {
            auto surface = create_surface(u32string(name.begin(), name.end()), 650u, height);
            add_control<control_type>(*surface, U"control_default", rectangle);
            capture(surface, name + "_default");
        }

        shared_ptr<tabpage> add_tabpage(tabcontrol &owner, const u32string &name, const u32string &title, const u32string &body)
        {
            auto page = make_shared<tabpage>(name);
            page->set_text(title);

            if(!body.empty())
            {
                add_label(*page, U"label_body", {14u, 12u, 228u, 42u}, body);
            }

            owner.get_page_list().add(page);
            return page;
        }

        void add_scroll_row(scrollpanel &owner)
        {
            for(uint64_t index = 0u;index < 6u;index++)
            {
                u32string number(1u, U'1' + static_cast<char32_t>(index));
                auto row = add_label(owner, U"label_" + number, {12u, 8u + (56u * index), 270u, 40u}, U"记录 " + number);
                row->set_background_color(((index % 2u) == 0u) ? BLUE_BACKGROUND : GREEN_BACKGROUND);
            }
        }

        void capture_slider()
        {
            capture_default<slider>("slider", {40u, 90u, 570u, 54u}, 187u);
            auto surface = create_surface(U"slider", 760u, 433u);
            add_label(*surface, U"label_horizontal", {36u, 77u, 340u, 38u}, U"默认方向：horizontal");
            auto horizontal = add_control<slider>(*surface, U"slider_horizontal", {36u, 125u, 440u, 52u});
            horizontal->set_value(65);
            add_label(*surface, U"label_disabled", {36u, 216u, 410u, 38u}, U"禁用 · 范围−20至20，当前为10");
            auto disabled = add_control<slider>(*surface, U"slider_disabled", {36u, 267u, 440u, 52u});
            disabled->set_minimum(-20);
            disabled->set_maximum(20);
            disabled->set_value(10);
            disabled->set_enabled(false);
            add_label(*surface, U"label_vertical", {500u, 77u, 224u, 38u}, U"vertical · 当前为65");
            auto vertical = add_control<slider>(*surface, U"slider_vertical", {582u, 132u, 54u, 252u});
            vertical->set_orientation(orientation_t::vertical);
            vertical->set_value(65);
            capture(surface, "slider_comparison");
            auto demo = create_slider_demo();
            show(demo, "slider_demo");
            drag("slider_demo", {255.0, 175.0}, {530.0, 175.0});
            auto &slider_level = dynamic_cast<slider &>(demo->get_control_list()[U"slider_level"]);

            if(slider_level.get_value() < 60)
            {
                throw runtime_error("Slider demo did not update after dragging");
            }

            finish(demo, "slider_demo");
        }

        void capture_numericupdown()
        {
            capture_default<numericupdown>("numericupdown", {40u, 90u, 360u, 54u}, 187u);
            auto surface = create_surface(U"numericupdown", 760u, 405u);
            const array<u32string, 4u> CAPTION_LIST{U"默认值与显示精度", U"范围−2.00至2.00", U"步长0.25 · 1.00 → 1.25", U"同一数值 · 禁用"};

            for(uint64_t index = 0u;index < CAPTION_LIST.size();index++)
            {
                u32string suffix(1u, U'0' + static_cast<char32_t>(index));
                uint64_t top = 80u + (72u * index);
                add_label(*surface, U"label_" + suffix, {36u, top, 312u, 46u}, CAPTION_LIST[index]);
                auto field = add_control<numericupdown>(*surface, U"number_" + suffix, {366u, top, 334u, 52u});

                if(index > 0u)
                {
                    field->set_minimum(-2.0);
                    field->set_maximum(2.0);
                    field->set_decimal_places(2u);
                    field->set_value((index == 1u) ? -2.0 : ((index == 2u) ? 1.0 : 1.25));
                }

                if(index >= 2u)
                {
                    field->set_step(0.25);
                }

                if(index == 3u)
                {
                    field->set_enabled(false);
                }
            }

            show(surface, "numericupdown_comparison");
            click("numericupdown_comparison", 686.0, 236.0);
            auto &example = dynamic_cast<numericupdown &>(surface->get_control_list()[U"number_2"]);

            if(example.get_value() != 1.25)
            {
                throw runtime_error("Numericupdown comparison did not apply one step");
            }

            move_pointer("numericupdown_comparison", 28.0, 72.0);
            finish(surface, "numericupdown_comparison");
            auto demo = create_numericupdown_demo();
            show(demo, "numericupdown_demo");
            click("numericupdown_demo", 342.0, 159.0);
            auto &number = dynamic_cast<numericupdown &>(demo->get_control_list()[U"numericupdown_gain"]);

            if(number.get_value() != 1.0)
            {
                throw runtime_error("Numericupdown demo did not step from 0.75 to 1.00");
            }

            finish(demo, "numericupdown_demo");
        }

        void capture_combobox()
        {
            capture_default<combobox>("combobox", {40u, 90u, 460u, 54u}, 187u);
            auto surface = create_surface(U"combobox", 760u, 450u);
            add_label(*surface, U"label_list", {36u, 83u, 256u, 46u}, U"dropdown_list");
            add_label(*surface, U"label_text", {36u, 155u, 256u, 46u}, U"dropdown");
            add_label(*surface, U"label_expanded", {36u, 227u, 256u, 46u}, U"dropped_down = true");
            auto fixed = add_control<combobox>(*surface, U"combobox_fixed", {310u, 83u, 390u, 52u});
            fixed->get_item_list().assign({U"每5分钟", U"每15分钟", U"每30分钟"});
            fixed->set_selected_index(0);
            auto editable = add_control<combobox>(*surface, U"combobox_editable", {310u, 155u, 390u, 52u});
            editable->set_dropdown_style(combobox_dropdown_style_t::dropdown);
            editable->get_item_list().assign({U"每5分钟", U"每15分钟", U"每30分钟"});
            editable->set_text(U"每45分钟");
            auto expanded = add_control<combobox>(*surface, U"combobox_expanded", {310u, 227u, 390u, 52u});
            expanded->get_item_list().assign({U"每5分钟", U"每15分钟", U"每30分钟"});
            expanded->set_selected_index(1);
            show(surface, "combobox_comparison");
            expanded->set_dropped_down(true);

            if(!expanded->get_dropped_down())
            {
                throw runtime_error("Combobox comparison did not open");
            }

            move_pointer("combobox_comparison", 450.0, 327.0);
            finish(surface, "combobox_comparison");
            auto demo = create_combobox_demo();
            show(demo, "combobox_demo");
            click("combobox_demo", 350.0, 152.0);
            click("combobox_demo", 118.0, 227.0);
            auto &choice = dynamic_cast<combobox &>(demo->get_control_list()[U"combobox_interval"]);

            if(choice.get_selected_index() != 1)
            {
                throw runtime_error("Combobox demo did not select the second item");
            }

            finish(demo, "combobox_demo");
        }

        void capture_listbox()
        {
            capture_default<listbox>("listbox", {40u, 90u, 570u, 118u}, 247u);
            auto surface = create_surface(U"listbox", 760u, 372u);
            add_label(*surface, U"label_top", {36u, 82u, 325u, 42u}, U"默认行高30 · 列表顶部");
            add_label(*surface, U"label_scroll", {396u, 82u, 325u, 42u}, U"行高42 · 定位所选项");
            auto top = add_control<listbox>(*surface, U"listbox_top", {36u, 134u, 325u, 150u});
            auto bottom = add_control<listbox>(*surface, U"listbox_bottom", {396u, 134u, 325u, 168u});
            const vector<u32string> ITEM_LIST{U"读取配置", U"检查目录", U"建立连接", U"同步图像", U"同步音频", U"同步模型", U"核验校验和", U"生成报告"};
            top->get_item_list().assign(ITEM_LIST);
            top->set_selected_index(1);
            bottom->set_row_height(42u);
            bottom->get_item_list().assign(ITEM_LIST);
            bottom->set_selected_index(7);
            capture(surface, "listbox_comparison");
            auto demo = create_listbox_demo();
            show(demo, "listbox_demo");
            click("listbox_demo", 170.0, 228.0);
            auto &choice = dynamic_cast<listbox &>(demo->get_control_list()[U"listbox_task"]);

            if(choice.get_selected_index() != 2)
            {
                throw runtime_error("Listbox demo did not select the third item");
            }

            finish(demo, "listbox_demo");
        }

        void capture_panel()
        {
            capture_default<panel>("panel", {40u, 90u, 570u, 118u}, 247u);
            auto surface = create_surface(U"panel", 760u, 366u);
            add_label(*surface, U"label_default", {36u, 82u, 325u, 44u}, U"默认边框和背景");
            add_label(*surface, U"label_nested", {396u, 82u, 325u, 44u}, U"背景色与嵌套子控件");
            auto plain = add_control<panel>(*surface, U"panel_plain", {36u, 138u, 325u, 164u});
            add_label(*plain, U"label_content", {14u, 12u, 280u, 42u}, U"同步服务");
            auto styled = add_control<panel>(*surface, U"panel_styled", {396u, 138u, 325u, 164u});
            styled->set_background_color(BLUE_BACKGROUND);
            add_label(*styled, U"label_content", {14u, 12u, 280u, 42u}, U"同步服务");
            auto detail = add_control<panel>(*styled, U"panel_detail", {14u, 70u, 296u, 70u});
            detail->set_background_color(GREEN_BACKGROUND);
            add_label(*detail, U"label_detail", {12u, 12u, 250u, 44u}, U"连接正常");
            capture(surface, "panel_comparison");
            auto demo = create_panel_demo();
            show(demo, "panel_demo");
            click("panel_demo", 125.0, 265.0);
            auto &outer = dynamic_cast<panel &>(demo->get_control_list()[U"panel_connection"]);
            auto &inner = outer.get_control_list()[U"panel_detail"];

            if(inner.get_visible())
            {
                throw runtime_error("Panel demo did not hide its details");
            }

            click("panel_demo", 125.0, 265.0);

            if(!inner.get_visible())
            {
                throw runtime_error("Panel demo did not restore its details");
            }

            move_pointer("panel_demo", 28.0, 72.0);
            finish(demo, "panel_demo");
        }

        void capture_scrollpanel()
        {
            capture_default<scrollpanel>("scrollpanel", {40u, 90u, 570u, 118u}, 247u);
            auto surface = create_surface(U"scrollpanel", 760u, 370u);
            add_label(*surface, U"label_top", {36u, 83u, 325u, 46u}, U"滚动偏移0 · 内容超出视口");
            add_label(*surface, U"label_offset", {396u, 83u, 325u, 46u}, U"滚动后 · 显示后续内容");
            auto first = add_control<scrollpanel>(*surface, U"scrollpanel_top", {36u, 143u, 325u, 176u});
            auto shifted = add_control<scrollpanel>(*surface, U"scrollpanel_offset", {396u, 143u, 325u, 176u});
            add_scroll_row(*first);
            add_scroll_row(*shifted);
            show(surface, "scrollpanel_comparison");
            control_access::set_vertical_scroll_offset(*shifted, uint64_t{112u});
            finish(surface, "scrollpanel_comparison");
            auto demo = create_scrollpanel_demo();
            show(demo, "scrollpanel_demo");
            auto &log = dynamic_cast<scrollpanel &>(demo->get_control_list()[U"scrollpanel_log"]);
            control_access::set_vertical_scroll_offset(log, uint64_t{120u});
            finish(demo, "scrollpanel_demo");
        }

        void add_split_pane(splitter &owner)
        {
            auto left = add_control<panel>(owner, U"panel_first", {});
            left->set_background_color(BLUE_BACKGROUND);
            add_label(*left, U"label_first", {10u, 12u, 112u, 36u}, U"第一区");
            auto right = add_control<panel>(owner, U"panel_second", {});
            right->set_background_color(GREEN_BACKGROUND);
            add_label(*right, U"label_second", {10u, 12u, 112u, 36u}, U"第二区");
        }

        void capture_splitter()
        {
            auto initial = create_surface(U"splitter", 650u, 300u);
            auto initial_splitter = add_control<splitter>(*initial, U"splitter_split", {40u, 90u, 570u, 168u});
            add_split_pane(*initial_splitter);
            capture(initial, "splitter_default");
            auto surface = create_surface(U"splitter", 810u, 383u);
            add_label(*surface, U"label_vertical", {36u, 80u, 354u, 44u}, U"vertical · 左右分区");
            add_label(*surface, U"label_horizontal", {420u, 80u, 354u, 44u}, U"horizontal · 上下分区");
            auto vertical = add_control<splitter>(*surface, U"splitter_vertical", {36u, 135u, 354u, 190u});
            auto horizontal = add_control<splitter>(*surface, U"splitter_horizontal", {420u, 135u, 354u, 190u});
            horizontal->set_orientation(orientation_t::horizontal);
            horizontal->set_split_position(0.38);
            add_split_pane(*vertical);
            add_split_pane(*horizontal);
            capture(surface, "splitter_comparison");
            auto demo = create_splitter_demo();
            show(demo, "splitter_demo");
            drag("splitter_demo", {296.0, 170.0}, {414.0, 170.0});
            auto &workspace = dynamic_cast<splitter &>(demo->get_control_list()[U"splitter_workspace"]);

            if(workspace.get_split_position() < 0.59)
            {
                throw runtime_error("Splitter demo divider did not move");
            }

            finish(demo, "splitter_demo");
        }

        void capture_tabcontrol()
        {
            auto initial = create_surface(U"tabcontrol", 650u, 282u);
            auto initial_tab = add_control<tabcontrol>(*initial, U"tabcontrol_initial", {40u, 85u, 570u, 153u});
            add_tabpage(*initial_tab, U"tabpage_overview", U"概览", U"概览内容");
            add_tabpage(*initial_tab, U"tabpage_history", U"历史", U"历史内容");
            capture(initial, "tabcontrol_default");
            auto surface = create_surface(U"tabcontrol", 860u, 386u);
            add_label(*surface, U"label_top", {36u, 80u, 380u, 44u}, U"top · 默认选中第一页");
            add_label(*surface, U"label_left", {444u, 80u, 380u, 44u}, U"left · 选中并重命名第二页");
            auto top = add_control<tabcontrol>(*surface, U"tabcontrol_top", {36u, 135u, 380u, 190u});
            auto left = add_control<tabcontrol>(*surface, U"tabcontrol_left", {444u, 135u, 380u, 190u});
            add_tabpage(*top, U"tabpage_overview", U"概览", U"概览内容");
            add_tabpage(*top, U"tabpage_history", U"历史", U"历史内容");
            add_tabpage(*left, U"tabpage_overview", U"概览", U"概览内容");
            auto second = add_tabpage(*left, U"tabpage_history", U"历史", U"历史内容");
            second->set_text(U"同步记录");
            left->set_tab_position(tab_position_t::left);
            left->set_tab_size(112u);
            left->set_selected_index(1);
            left->set_selected_tab_background_color(GREEN_BACKGROUND);
            capture(surface, "tabcontrol_comparison");
            auto demo = create_tabcontrol_demo();
            show(demo, "tabcontrol_demo");
            click("tabcontrol_demo", 128.0, 102.0);
            auto &tabs = dynamic_cast<tabcontrol &>(demo->get_control_list()[U"tabcontrol_workspace"]);

            if(tabs.get_selected_index() != 1)
            {
                throw runtime_error("Tabcontrol demo did not switch to the history page");
            }

            finish(demo, "tabcontrol_demo");
        }

    public:
        explicit capture_layout_control(const filesystem::path &output) : host(output, true)
        {
        }

        void run()
        {
            capture_slider();
            capture_numericupdown();
            capture_combobox();
            capture_listbox();
            capture_panel();
            capture_scrollpanel();
            capture_splitter();
            capture_tabcontrol();
        }
};

int main(int count, char **argument)
{
    try
    {
        if(count != 4)
        {
            throw invalid_argument("Expected output directory, fixture directory, and locale");
        }

        capture_layout_control capture{filesystem::u8path(argument[1])};
        capture.run();
        return 0;
    }
    catch(const exception &error)
    {
        (cerr << get_error_message(error)) << '\n';
        return 1;
    }
}