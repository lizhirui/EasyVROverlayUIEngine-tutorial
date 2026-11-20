#include "ui_test_host.h"
#include "easyvrui/core/ui_runtime.h"
#include "easyvrui/dialog/internal/file_save_dialog_window.h"
#include "easyvrui/dialog/internal/inputbox_window.h"
#include <easyvrui.h>
#include <array>
#include <chrono>
#include <cstdint>
#include <filesystem>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>
#include <string_view>
#include <thread>
#include <vector>

using namespace std;
using namespace easyvrui;
using nlohmann::json;
shared_ptr<window> create_treeview_demo();
shared_ptr<window> create_listview_demo();
shared_ptr<window> create_grid_demo();
shared_ptr<window> create_menubar_demo();
shared_ptr<window> create_toolbar_demo();
shared_ptr<window> create_image_demo();
shared_ptr<window> create_screen_demo();
shared_ptr<window> create_blank_demo();

class capture_display_control
{
    private:
        class signal_plot : public control
        {
            protected:
                void render(render_context &context) const override
                {
                    auto area = context.get_rectangle(*this);
                    context.fill_rounded_rectangle(area, 8.0, 8.0, 0x172c40ffu);
                    context.push_clip(area);
                    constexpr array<double, 9u> LEVEL_LIST{0.25, 0.40, 0.34, 0.66, 0.61, 0.82, 0.57, 0.70, 0.86};
                    constexpr double INSET = 24.0;
                    double left = area.left + INSET;
                    double top = area.top + INSET;
                    double width = area.width - (2.0 * INSET);
                    double height = area.height - (2.0 * INSET);
                    double step = width / static_cast<double>(LEVEL_LIST.size() - 1u);

                    for(size_t index = 0u;index <= 4u;index++)
                    {
                        double y = top + (height * (static_cast<double>(index) / 4.0));
                        context.draw_line(left, y, left + width, y, 0x42617dffu, 1.0);
                    }

                    for(size_t index = 1u;index < LEVEL_LIST.size();index++)
                    {
                        double x = left + (step * static_cast<double>(index));
                        double previous = top + (height * (1.0 - LEVEL_LIST[index - 1u]));
                        double current = top + (height * (1.0 - LEVEL_LIST[index]));
                        context.draw_line(x - step, previous, x, current, 0x7de8c0ffu, 4.0);
                        context.fill_circle(x, current, 4.0, 0x7de8c0ffu);
                    }

                    context.pop_clip();
                }

            public:
                explicit signal_plot(const u32string &name) : control(name)
                {
                }
        };

        static constexpr auto WAIT_LIMIT = chrono::seconds(8);
        static constexpr uint64_t UNAVAILABLE_SCREEN_ID = 10000u;
        static constexpr uint64_t FIXTURE_SCREEN_ID = 10001u;
        ui_test_host host;

        void settle()
        {
            host.execute({{"action", "step"}});
        }

        void show(const shared_ptr<window> &surface, const string &name)
        {
            host.attach_control(surface, name);
            host.execute({{"action", "show"}, {"name", name}});
            wait_for_surface(*surface);
        }

        void wait_for_surface(const window &surface)
        {
            const auto DEADLINE = chrono::steady_clock::now() + WAIT_LIMIT;

            while(!host.is_surface_ready(surface) && (chrono::steady_clock::now() < DEADLINE))
            {
                settle();
                this_thread::sleep_for(chrono::milliseconds(12));
            }

            if(!host.is_surface_ready(surface))
            {
                throw runtime_error("WARP surface did not present");
            }
        }

        void move_pointer(const string &name, double left, double top)
        {
            host.execute({{"action", "move"}, {"window", name}, {"left", left}, {"top", top}});
        }

        void click(const string &name, double left, double top)
        {
            host.execute({{"action", "click"}, {"window", name}, {"left", left}, {"top", top}});
        }

        void finish(const shared_ptr<window> &surface, const string &name)
        {
            settle();
            wait_for_surface(*surface);
            host.execute({{"action", "snapshot"}, {"window", name}, {"label", name}});
            surface->close(true);
            settle();
        }

        void capture(const shared_ptr<window> &surface, const string &name)
        {
            show(surface, name);
            move_pointer(name, 28.0, 72.0);
            finish(surface, name);
        }

        shared_ptr<window> create_surface(const u32string &title, uint64_t width = 760u, uint64_t height = 360u)
        {
            auto surface = make_shared<window>(U"window_preview");
            surface->set_title(title);
            surface->set_size(width, height);
            return surface;
        }

        template <typename item_type>
        shared_ptr<item_type> add_control(container_control &owner, const u32string &name, const rectangle_t &rectangle)
        {
            auto result = make_shared<item_type>(name);
            result->set_rect(rectangle);
            owner.get_control_list().add(result);
            return result;
        }

        shared_ptr<label> add_label(container_control &owner, const u32string &name, const rectangle_t &rectangle, const u32string &text)
        {
            auto item = add_control<label>(owner, name, rectangle);
            item->set_text(text);
            return item;
        }

        template <typename item_type>
        void capture_default(const string &name)
        {
            auto surface = create_surface(u32string(name.begin(), name.end()), 650u, 244u);
            add_control<item_type>(*surface, U"control_default", {40u, 88u, 570u, 112u});
            capture(surface, name + "_default");
        }

        shared_ptr<const drawing_image> create_pattern()
        {
            constexpr uint64_t WIDTH = 96u;
            constexpr uint64_t HEIGHT = 48u;
            constexpr array<uint8_t, 4u> BLUE{53u, 146u, 224u, 255u};
            constexpr array<uint8_t, 4u> GREEN{95u, 220u, 170u, 255u};
            constexpr array<uint8_t, 4u> AMBER{245u, 186u, 102u, 255u};
            vector<uint8_t> pixel_buffer;

            for(uint64_t y = 0u;y < HEIGHT;y++)
            {
                for(uint64_t x = 0u;x < WIDTH;x++)
                {
                    const auto &color = (x < 32u) ? BLUE : ((x < 64u) ? ((y < 24u) ? AMBER : BLUE) : GREEN);
                    pixel_buffer.insert(pixel_buffer.end(), color.begin(), color.end());
                }
            }

            return make_shared<drawing_image>(WIDTH, HEIGHT, move(pixel_buffer));
        }

        shared_ptr<tree_node> add_tree(treeview &view, bool expanded)
        {
            auto root = make_shared<tree_node>(U"同步任务", expanded);
            auto child = make_shared<tree_node>(U"核验清单");
            root->get_node_list().add(make_shared<tree_node>(U"同步图像"));
            root->get_node_list().add(child);
            view.get_node_list().add(root);
            view.get_node_list().add(make_shared<tree_node>(U"本地配置"));
            return child;
        }

        void capture_treeview()
        {
            capture_default<treeview>("treeview");
            auto surface = create_surface(U"treeview");
            add_label(*surface, U"label_collapsed", {36u, 83u, 320u, 42u}, U"折叠 · 仅显示根节点");
            add_label(*surface, U"label_expanded", {390u, 83u, 320u, 42u}, U"展开 · 选中子节点");
            auto first = add_control<treeview>(*surface, U"tree_first", {36u, 138u, 320u, 150u});
            auto second = add_control<treeview>(*surface, U"tree_second", {390u, 138u, 320u, 150u});
            add_tree(*first, false);
            auto selected = add_tree(*second, true);
            second->set_selected_node(selected.get());
            second->set_foreground_color(0xd0efe5ffu);
            capture(surface, "treeview_comparison");
            auto demo = create_treeview_demo();
            show(demo, "treeview_demo");
            click("treeview_demo", 172.0, 157.0);
            auto &tree = dynamic_cast<treeview &>(demo->get_control_list()[U"tree_task"]);

            if((tree.get_selected_node() == nullptr) || (tree.get_selected_node()->get_tag() != U"report"))
            {
                throw runtime_error("Treeview demo did not select the report");
            }

            finish(demo, "treeview_demo");
        }

        void add_list_table(listview &view)
        {
            view.get_column_list().assign({make_shared<listview_column>(U"任务", 146u), make_shared<listview_column>(U"状态", 115u)});
            view.get_item_list().assign({make_shared<listview_item>(vector<u32string>{U"同步图像", U"完成"}), make_shared<listview_item>(vector<u32string>{U"同步音频", U"待处理"}), make_shared<listview_item>(vector<u32string>{U"核验清单", U"完成"})});
        }

        void capture_listview()
        {
            capture_default<listview>("listview");
            auto surface = create_surface(U"listview");
            add_label(*surface, U"label_single", {36u, 83u, 320u, 42u}, U"默认单选");
            add_label(*surface, U"label_multi", {390u, 83u, 320u, 42u}, U"多选 · 自定义列宽和行高");
            auto first = add_control<listview>(*surface, U"list_single", {36u, 138u, 320u, 160u});
            auto second = add_control<listview>(*surface, U"list_multi", {390u, 138u, 320u, 160u});
            add_list_table(*first);
            add_list_table(*second);
            first->set_selected_index(1);
            second->get_column_list()[0u]->set_width(184u);
            second->set_row_height(42u);
            second->set_multi_select(true);
            second->select_item(0u);
            second->select_item(2u, false, true);
            capture(surface, "listview_comparison");
            auto demo = create_listview_demo();
            show(demo, "listview_demo");
            click("listview_demo", 100.0, 161.0);
            auto &view = dynamic_cast<listview &>(demo->get_control_list()[U"list_result"]);

            if(view.get_selected_index() != 1)
            {
                throw runtime_error("Listview demo did not select the second row");
            }

            finish(demo, "listview_demo");
        }

        void add_grid_table(grid &view)
        {
            view.set_column_list({grid_column_t{U"配置", 150u, false}, grid_column_t{U"数值", 130u, true}});
            view.set_row_count(2u);
            view.set_cell_value(0u, 0u, u32string(U"任务数"));
            view.set_cell_value(0u, 1u, int64_t{4});
            view.set_cell_value(1u, 0u, u32string(U"重试次数"));
            view.set_cell_value(1u, 1u, int64_t{2});
        }

        void capture_grid()
        {
            capture_default<grid>("grid");
            auto surface = create_surface(U"grid");
            add_label(*surface, U"label_row", {36u, 83u, 320u, 42u}, U"整行选择 · 只读");
            add_label(*surface, U"label_cell", {390u, 83u, 320u, 42u}, U"单元格选择 · 编辑中");
            auto first = add_control<grid>(*surface, U"grid_row", {36u, 138u, 320u, 155u});
            auto second = add_control<grid>(*surface, U"grid_cell", {390u, 138u, 320u, 155u});
            add_grid_table(*first);
            add_grid_table(*second);
            first->set_read_only(true);
            first->set_selection_mode(grid_selection_mode_t::row);
            first->set_selected_index(1);
            show(surface, "grid_comparison");

            if(!second->begin_edit(0u, 1u))
            {
                throw runtime_error("Grid comparison could not start editing");
            }

            second->set_edit_text(U"6");
            finish(surface, "grid_comparison");
            auto demo = create_grid_demo();
            show(demo, "grid_demo");
            auto &view = dynamic_cast<grid &>(demo->get_control_list()[U"grid_config"]);

            if(!view.begin_edit(0u, 1u) || !view.commit_edit(int64_t{6}))
            {
                throw runtime_error("Grid demo could not commit the edited value");
            }

            finish(demo, "grid_demo");
        }

        shared_ptr<menuitem> add_menu_item(menu_container &owner, const u32string &name, const u32string &text)
        {
            auto item = make_shared<menuitem>(name);
            item->set_text(text);
            owner.get_control_list().add(item);
            return item;
        }

        void send_menu_key(const window &surface, const string &event_type, const string &key, bool alt = false, bool alt_tap = false)
        {
            ui_runtime::get_current().process_message({{"message_type", "event"}, {"event_type", event_type}, {"window", surface.get_id()}, {"key", key}, {"alt", alt}, {"alt_tap", alt_tap}});
            settle();
        }

        void capture_menubar()
        {
            auto defaults = create_surface(U"menubar", 650u, 230u);
            auto default_bar = make_shared<menubar>(U"menu_default");
            add_menu_item(*default_bar, U"menu_task", U"任务(&T)");
            add_menu_item(*default_bar, U"menu_view", U"视图(&V)");
            defaults->set_menu(default_bar);
            capture(defaults, "menubar_default");
            auto surface = create_surface(U"menubar", 760u, 290u);
            auto bar = make_shared<menubar>(U"menu_main");
            bar->set_row_height(42u);
            bar->set_font(font_t{U"Microsoft YaHei UI", 20u});
            auto task = add_menu_item(*bar, U"menu_task", U"任务(&T)");
            add_menu_item(*bar, U"menu_view", U"视图(&V)");
            auto refresh = add_menu_item(*task, U"menu_refresh", U"刷新记录(&R)");
            refresh->set_shortcut(U"Ctrl+R");
            auto finished = add_menu_item(*task, U"menu_finished", U"显示已完成项(&S)");
            finished->set_checkable(true);
            finished->set_checked(true);
            auto clear = add_menu_item(*task, U"menu_clear", U"清除历史(&C)");
            clear->set_enabled(false);
            surface->set_menu(bar);
            auto note = add_label(*surface, U"label_state", {330u, 139u, 385u, 49u}, U"按住Alt · 显示助记符");
            show(surface, "menubar_comparison");
            click("menubar_comparison", 702.0, 254.0);
            send_menu_key(*surface, "key_down", "Alt", true);

            if(bar->get_is_open())
            {
                throw runtime_error("Holding Alt opened the menu before release");
            }

            host.execute({{"action", "snapshot"}, {"window", "menubar_comparison"}, {"label", "menubar_alt_held"}});
            send_menu_key(*surface, "key_up", "Alt", false, true);

            if(!bar->get_is_open())
            {
                throw runtime_error("Tapping Alt did not enter menu navigation");
            }

            send_menu_key(*surface, "key_down", "Down");
            send_menu_key(*surface, "key_up", "Down");
            note->set_text(U"键盘导航 · 行高42、勾选与禁用");

            if(!bar->get_is_submenu_open(*task))
            {
                throw runtime_error("Menubar comparison submenu did not open");
            }

            finish(surface, "menubar_comparison");
            auto demo = create_menubar_demo();
            show(demo, "menubar_demo");
            click("menubar_demo", 420.0, 180.0);
            send_menu_key(*demo, "key_down", "Alt", true);
            send_menu_key(*demo, "key_up", "Alt", false, true);
            send_menu_key(*demo, "key_down", "Down");
            send_menu_key(*demo, "key_up", "Down");
            send_menu_key(*demo, "key_down", "Enter");
            send_menu_key(*demo, "key_up", "Enter");
            auto &state = dynamic_cast<label &>(demo->get_control_list()[U"label_state"]);

            if(state.get_text() != U"同步记录已刷新")
            {
                throw runtime_error("Menubar demo did not activate the refresh command");
            }

            send_menu_key(*demo, "key_down", "Alt", true);
            finish(demo, "menubar_demo");
        }

        void add_tool_item(toolbar &bar, const shared_ptr<const drawing_image> &resource, bool disabled)
        {
            auto first = make_shared<toolbar_button>(U"button_first");
            first->set_icon(resource);
            bar.get_button_list().add(first);
            auto &separator = bar.get_button_list().add(U"separator_preview");
            separator.set_separator(true);
            auto second = make_shared<toolbar_button>(U"button_second");
            second->set_icon(resource);
            second->set_enabled(!disabled);
            bar.get_button_list().add(second);
        }

        void capture_toolbar()
        {
            auto defaults = create_surface(U"toolbar", 650u, 214u);
            auto first = add_control<toolbar>(*defaults, U"toolbar_default", {36u, 85u, 578u, 65u});
            const auto RESOURCE = create_pattern();
            add_tool_item(*first, RESOURCE, false);
            capture(defaults, "toolbar_default");
            auto surface = create_surface(U"toolbar", 760u, 350u);
            add_label(*surface, U"label_default", {36u, 74u, 608u, 40u}, U"默认尺寸与间距");
            auto standard = add_control<toolbar>(*surface, U"toolbar_standard", {36u, 119u, 674u, 59u});
            add_tool_item(*standard, RESOURCE, false);
            add_label(*surface, U"label_large", {36u, 191u, 608u, 41u}, U"尺寸56 · 间距14 · 禁用右侧操作");
            auto large = add_control<toolbar>(*surface, U"toolbar_large", {36u, 236u, 674u, 67u});
            large->set_tool_size(56u);
            large->set_spacing(14.0);
            add_tool_item(*large, RESOURCE, true);
            capture(surface, "toolbar_comparison");
            auto demo = create_toolbar_demo();
            show(demo, "toolbar_demo");
            click("toolbar_demo", 62.0, 112.0);
            auto &state = dynamic_cast<label &>(demo->get_control_list()[U"label_state"]);

            if(state.get_text() != U"已请求预览")
            {
                throw runtime_error("Toolbar demo did not activate the preview command");
            }

            move_pointer("toolbar_demo", 28.0, 72.0);
            finish(demo, "toolbar_demo");
        }

        void capture_image()
        {
            capture_default<image>("image");
            auto surface = create_surface(U"image", 840u, 294u);
            const auto SOURCE = create_pattern();
            const array<u32string, 4u> NAME_LIST{U"contain", U"cover", U"fill", U"none"};
            const array<image_stretch_mode_t, 4u> MODE_LIST{image_stretch_mode_t::contain, image_stretch_mode_t::cover, image_stretch_mode_t::fill, image_stretch_mode_t::none};

            for(uint64_t index = 0u;index < NAME_LIST.size();index++)
            {
                uint64_t left = 38u + (195u * index);
                add_label(*surface, U"label_" + NAME_LIST[index], {left, 85u, 176u, 38u}, NAME_LIST[index]);
                auto preview = add_control<image>(*surface, U"image_" + NAME_LIST[index], {left, 132u, 176u, 112u});
                preview->set_source(SOURCE);
                preview->set_stretch_mode(MODE_LIST[index]);
            }

            capture(surface, "image_comparison");
            auto demo = create_image_demo();
            show(demo, "image_demo");
            click("image_demo", 160.0, 299.0);
            auto &preview = dynamic_cast<image &>(demo->get_control_list()[U"image_preview"]);

            if(preview.get_stretch_mode() != image_stretch_mode_t::cover)
            {
                throw runtime_error("Image demo did not switch to cover");
            }

            finish(demo, "image_demo");
        }

        void set_screen_state(const window &owner, uint64_t id, bool available)
        {
            ui_runtime::get_current().process_message(json{{"message_type", "event"}, {"event_type", "screen_state"}, {"window", owner.get_id()}, {"screen_id", id}, {"available", available}});
        }

        void capture_screen()
        {
            auto defaults = create_surface(U"screen", 650u, 270u);
            auto preview = add_control<screen>(*defaults, U"screen_default", {36u, 84u, 578u, 110u});
            preview->set_screen_id(UNAVAILABLE_SCREEN_ID);
            add_label(*defaults, U"label_state", {36u, 208u, 578u, 32u}, U"未获得画面");
            capture(defaults, "screen_default");
            auto surface = create_surface(U"screen", 820u, 327u);
            add_label(*surface, U"label_left", {36u, 82u, 350u, 46u}, U"测试事件：采集源可用");
            add_label(*surface, U"label_right", {424u, 82u, 350u, 46u}, U"测试事件：采集源不可用");
            auto first = add_control<screen>(*surface, U"screen_ready", {36u, 136u, 350u, 142u});
            auto second = add_control<screen>(*surface, U"screen_missing", {424u, 136u, 350u, 106u});
            first->set_screen_id(FIXTURE_SCREEN_ID);
            first->set_background_color(0x193d36ffu);
            second->set_screen_id(UNAVAILABLE_SCREEN_ID);
            add_label(*surface, U"label_placeholder", {58u, 182u, 304u, 45u}, U"无头渲染占位");
            add_label(*surface, U"label_empty", {446u, 165u, 304u, 45u}, U"等待画面");
            show(surface, "screen_comparison");
            set_screen_state(*surface, FIXTURE_SCREEN_ID, true);
            set_screen_state(*surface, UNAVAILABLE_SCREEN_ID, false);

            if(!first->get_screen_available() || second->get_screen_available())
            {
                throw runtime_error("Screen fixture states did not reach their respective controls");
            }

            finish(surface, "screen_comparison");
            auto demo = create_screen_demo();
            auto &demo_screen = dynamic_cast<screen &>(demo->get_control_list()[U"screen_preview"]);
            demo_screen.set_screen_id(FIXTURE_SCREEN_ID);
            auto placeholder = add_label(*demo, U"label_placeholder", {72u, 135u, 536u, 60u}, U"无头WARP采集区域");
            placeholder->set_foreground_color(0x8bb6d8ffu);
            show(demo, "screen_demo");
            set_screen_state(*demo, FIXTURE_SCREEN_ID, true);
            auto &state = dynamic_cast<label &>(demo->get_control_list()[U"label_state"]);

            if(state.get_text() != U"采集源可用")
            {
                throw runtime_error("Screen demo did not receive the restored event");
            }

            finish(demo, "screen_demo");
        }

        void capture_blank()
        {
            auto defaults = create_surface(U"blank", 650u, 265u);
            auto panel_default = add_control<panel>(*defaults, U"panel_default", {36u, 84u, 578u, 90u});
            add_control<blank>(*panel_default, U"blank_item", {14u, 13u, 520u, 53u});
            add_label(*defaults, U"label_frame", {36u, 190u, 578u, 37u}, U"边框属于父级panel");
            capture(defaults, "blank_default");
            auto surface = create_surface(U"blank", 760u, 310u);
            add_label(*surface, U"label_before", {36u, 83u, 320u, 42u}, U"替换前 · blank");
            add_label(*surface, U"label_after", {390u, 83u, 320u, 42u}, U"替换后 · label");
            auto first = add_control<panel>(*surface, U"panel_before", {36u, 136u, 320u, 116u});
            auto second = add_control<panel>(*surface, U"panel_after", {390u, 136u, 320u, 116u});
            add_control<blank>(*first, U"blank_item", {14u, 22u, 290u, 59u});
            add_label(*second, U"label_content", {14u, 22u, 290u, 59u}, U"内容已加载");
            capture(surface, "blank_comparison");
            auto demo = create_blank_demo();
            show(demo, "blank_demo");
            click("blank_demo", 140.0, 262.0);
            auto &content = dynamic_cast<panel &>(demo->get_control_list()[U"panel_content"]);

            if(!content.get_control_list().contains(U"label_content"))
            {
                throw runtime_error("Blank demo did not replace the placeholder");
            }

            finish(demo, "blank_demo");
        }

        void capture_dialog(const filesystem::path &fixture)
        {
            auto field = make_shared<inputbox_window>(U"tutorial_inputbox");
            field->set_title(U"命名同步报告");
            field->set_prompt(U"输入报告名称");
            field->set_text(U"同步检查报告");
            field->set_max_length(48u);
            capture(field, "dialog_inputbox");
            auto save = make_shared<file_save_dialog_window>(U"tutorial_save");
            save->set_title(U"保存同步报告");
            save->set_filter_list({{U"文本报告", {U"*.txt"}}, {U"所有文件", {U"*.*"}}});
            save->set_filter_index(1u);
            save->set_default_extension(U"txt");
            save->set_directory(fixture.u32string());
            save->set_filename(U"report.txt");
            show(save, "dialog_file_save");
            const auto DEADLINE = chrono::steady_clock::now() + WAIT_LIMIT;

            while(save->get_loading() && (chrono::steady_clock::now() < DEADLINE))
            {
                settle();
                this_thread::sleep_for(chrono::milliseconds(12));
            }

            if(save->get_loading())
            {
                throw runtime_error("File save dialog directory scan timed out");
            }

            auto &collection = save->get_control_list();
            auto &column_list = dynamic_cast<listview &>(collection[U"listview_entry"]).get_column_list();
            column_list[0u]->set_width(230u);
            column_list[1u]->set_width(258u);
            column_list[2u]->set_width(190u);
            dynamic_cast<textbox &>(collection[U"textbox_directory"]).set_text(U"Examples");
            auto &places = dynamic_cast<listview &>(collection[U"listview_place"]).get_item_list();
            places.clear();
            places.add(make_shared<listview_item>(vector<u32string>{U"示例文件夹"}));
            move_pointer("dialog_file_save", 28.0, 70.0);
            finish(save, "dialog_file_save");
        }

        void capture_spatial()
        {
            auto plot = create_surface(U"同步速率", 710u, 335u);
            add_label(*plot, U"label_rate", {36u, 80u, 638u, 44u}, U"最近9次采样 · 归一化速率");
            add_control<signal_plot>(*plot, U"plot_rate", {36u, 137u, 638u, 150u});
            capture(plot, "spatial_custom_drawing");
            auto surface = create_surface(U"空间定位配置", 760u, 360u);
            add_label(*surface, U"label_anchor", {36u, 80u, 688u, 45u}, U"五种参考对象 · 窗口空间属性");
            auto list = add_control<listview>(*surface, U"list_anchor", {36u, 137u, 688u, 171u});
            list->set_row_height(27u);
            list->get_column_list().assign({make_shared<listview_column>(U"参考对象", 163u), make_shared<listview_column>(U"跟踪目标", 465u)});
            list->get_item_list().assign({make_shared<listview_item>(vector<u32string>{U"world", U"固定的SteamVR跟踪空间"}), make_shared<listview_item>(vector<u32string>{U"head", U"头显姿态"}), make_shared<listview_item>(vector<u32string>{U"body", U"校准朝向与身体平移"}), make_shared<listview_item>(vector<u32string>{U"left", U"左手柄姿态"}), make_shared<listview_item>(vector<u32string>{U"right", U"右手柄姿态"})});
            list->set_selected_index(2);
            capture(surface, "spatial_anchor_config");
        }

    public:
        explicit capture_display_control(const filesystem::path &output) : host(output, true)
        {
        }

        void run(const filesystem::path &fixture, bool menubar_only)
        {
            if(menubar_only)
            {
                capture_menubar();
                return;
            }

            capture_treeview();
            capture_listview();
            capture_grid();
            capture_menubar();
            capture_toolbar();
            capture_image();
            capture_screen();
            capture_blank();
            capture_dialog(fixture);
            capture_spatial();
        }
};

int main(int count, char **argument)
{
    try
    {
        bool menubar_only = (count == 5) && (string_view(argument[4]) == "--menubar-only");

        if((count != 4) && !menubar_only)
        {
            throw invalid_argument("Expected output directory, fixture directory, locale, and optional --menubar-only");
        }

        capture_display_control capture{filesystem::u8path(argument[1])};
        capture.run(filesystem::u8path(argument[2]), menubar_only);
        return 0;
    }
    catch(const exception &error)
    {
        (cerr << get_error_message(error)) << '\n';
        return 1;
    }
}