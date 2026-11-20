#include "ui_test_host.h"
#include "easyvrui/dialog/internal/messagebox_window.h"
#include "easyvrui/dialog/internal/inputbox_window.h"
#include "easyvrui/dialog/internal/file_save_dialog_window.h"
#include <easyvrui.h>
#include <array>
#include <chrono>
#include <cstdint>
#include <filesystem>
#include <functional>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>
#include <thread>
#include <vector>

using namespace std;
using namespace easyvrui;
using nlohmann::json;
shared_ptr<window> create_first_window();
void use_shout_window(const function<void(const shared_ptr<window> &)> &capture);

class capture_project_story
{
    private:
        class meter_view : public control
        {
            private:
                double level = 0.32;

            protected:
                void render(render_context &context) const override
                {
                    const auto AREA = context.get_rectangle(*this);
                    context.fill_rounded_rectangle(AREA, 8.0, 8.0, 0x182c40ffu);
                    const auto TRACK = render_rectangle_t{AREA.left + 12.0, AREA.top + 38.0, AREA.width - 24.0, 22.0};
                    context.fill_rounded_rectangle(TRACK, 5.0, 5.0, 0x30485dffu);
                    context.fill_rounded_rectangle({TRACK.left, TRACK.top, TRACK.width * level, TRACK.height}, 5.0, 5.0, 0x61d7a5ffu);
                    auto number = to_string(static_cast<uint32_t>(level * 100.0));
                    context.draw_text((U"MIC " + u32string(number.begin(), number.end())) + U"%", font_t{U"Segoe UI", 20u, true}, {TRACK.left, AREA.top + 7.0, TRACK.width, 30.0}, 0xe9f7ffffu);
                }

            public:
                explicit meter_view(const u32string &name) : control(name)
                {
                }

                void set_level(double value)
                {
                    level = value;
                    invalidate();
                }
        };

        ui_test_host host;
        filesystem::path fixture;

        void settle()
        {
            host.execute({{"action", "step"}});
        }

        void settle_surface(const window &surface, const string &name)
        {
            const auto DEADLINE = chrono::steady_clock::now() + chrono::seconds(8);

            do
            {
                settle();

                if(host.is_surface_ready(surface))
                {
                    return;
                }

                this_thread::sleep_for(chrono::milliseconds(12));
            }
            while(chrono::steady_clock::now() < DEADLINE);
            throw runtime_error("Tutorial surface did not present: " + name);
        }

        void show(const shared_ptr<window> &surface, const string &name)
        {
            host.attach_control(surface, name);
            host.execute({{"action", "show"}, {"name", name}});
            settle_surface(*surface, name);
        }

        void take(const shared_ptr<window> &surface, const string &name, const string &image_name)
        {
            settle_surface(*surface, image_name);
            host.execute({{"action", "snapshot"}, {"window", name}, {"label", image_name}});
        }

        void close(const shared_ptr<window> &surface)
        {
            surface->close(true);
            settle();
        }

        void click(const string &name, double left, double top)
        {
            host.execute({{"action", "click"}, {"window", name}, {"left", left}, {"top", top}});
        }

        void move_pointer(const string &name, double left, double top)
        {
            host.execute({{"action", "move"}, {"window", name}, {"left", left}, {"top", top}});
        }

        void capture(const shared_ptr<window> &surface, const string &name)
        {
            show(surface, name);
            take(surface, name, name);
            close(surface);
        }

        template <typename item_type>
        shared_ptr<item_type> add_item(container_control &owner, const u32string &name, const rectangle_t &rectangle)
        {
            auto item = make_shared<item_type>(name);
            item->set_rect(rectangle);
            owner.get_control_list().add(item);
            return item;
        }

        shared_ptr<label> add_label(container_control &owner, const u32string &name, const rectangle_t &rectangle, const u32string &text)
        {
            auto item = add_item<label>(owner, name, rectangle);
            item->set_text(text);
            return item;
        }

        shared_ptr<button> add_button(container_control &owner, const u32string &name, const rectangle_t &rectangle, const u32string &text)
        {
            auto item = add_item<button>(owner, name, rectangle);
            item->set_text(text);
            return item;
        }

        shared_ptr<window> create_window(const u32string &title, uint64_t width, uint64_t height)
        {
            auto surface = make_shared<window>(U"window_preview");
            surface->set_title(title);
            surface->set_size(width, height);
            return surface;
        }

        void capture_basics()
        {
            auto first = create_first_window();
            show(first, "first");
            take(first, "first", "basics_first_initial");
            click("first", 137.0, 174.0);
            auto &status = dynamic_cast<label &>(first->get_control_list()[U"label_status"]);

            if(status.get_text() != U"你好，VR世界！")
            {
                throw runtime_error("First window click did not update the label");
            }

            take(first, "first", "basics_first_clicked");
            close(first);

            use_shout_window([this](const shared_ptr<window> &surface)
            {
                show(surface, "shout");
                take(surface, "shout", "basics_form_initial");
                click("shout", 96.0, 140.0);
                host.execute({{"action", "type"}, {"text", "Ready for sync"}});
                auto &field = dynamic_cast<textbox &>(surface->get_control_list()[U"textbox_message"]);

                if(field.get_text() != U"Ready for sync")
                {
                    throw runtime_error("Exported form did not receive text");
                }

                auto &send = dynamic_cast<button &>(surface->get_control_list()[U"button_send"]);
                send.activate();
                auto &hint = dynamic_cast<label &>(surface->get_control_list()[U"label_hint"]);

                if(hint.get_text() != U"已发送：Ready for sync")
                {
                    throw runtime_error("Exported form click did not update the label");
                }

                take(surface, "shout", "basics_form_sent");
                close(surface);
            });
        }

        void capture_chatbox()
        {
            auto surface = create_window(U"VRChat快捷聊天", 850u, 490u);
            add_label(*surface, U"label_phrase", {34u, 80u, 245u, 35u}, U"常用短语");
            auto phrase = add_item<listbox>(*surface, U"list_phrase", {34u, 124u, 245u, 150u});
            phrase->get_item_list().assign({U"大家好！", U"我会在入口等候。", U"请再发一次链接。", U"我稍后回来。", U"谢谢，晚点见！"});
            add_label(*surface, U"label_edit", {302u, 80u, 507u, 35u}, U"消息预览");
            auto editor = add_item<textbox>(*surface, U"textbox_chat", {302u, 124u, 507u, 154u});
            editor->set_multiline(true);
            editor->set_max_length(144u);
            auto limit = add_item<progressbar>(*surface, U"progressbar_length", {302u, 290u, 507u, 20u});
            limit->set_maximum(144);
            auto count = add_label(*surface, U"label_count", {302u, 315u, 280u, 36u}, U"0 / 144");
            auto status = add_label(*surface, U"label_state", {34u, 419u, 775u, 41u}, U"离线演示 · 等待编辑");
            auto send = add_button(*surface, U"button_send", {302u, 360u, 200u, 43u}, U"发送模拟消息");
            add_button(*surface, U"button_clear", {523u, 360u, 192u, 43u}, U"清空气泡…");

            phrase->on_selection_changed += [editor](control_base &source, event_args_t &)
            {
                editor->set_text(static_cast<listbox &>(source).get_selected_item());
            };

            editor->on_text_changed += [limit, count](control_base &source, event_args_t &)
            {
                auto length = static_cast<textbox &>(source).get_text().size();
                limit->set_value(static_cast<int64_t>(length));
                auto value = to_string(length);
                count->set_text(u32string(value.begin(), value.end()) + U" / 144");
            };

            send->on_click += [status](control_base &source, event_args_t &)
            {
                static_cast<button &>(source).set_enabled(false);
                status->set_text(U"模拟数据报已提交 · 冷却期间暂停发送");
            };

            show(surface, "chatbox");
            move_pointer("chatbox", 28.0, 72.0);
            take(surface, "chatbox", "project_chatbox_idle");
            click("chatbox", 151.0, 170.0);
            editor->set_text(editor->get_text() + U"\n等大家到齐后，我们按名单依次进入。\n如果暂时无法回应，可以先在这里留言。\n我会核对集合地点，并在下一轮确认人数。");
            take(surface, "chatbox", "project_chatbox_preview");
            click("chatbox", 402.0, 382.0);

            if(send->get_enabled())
            {
                throw runtime_error("Chat cooldown did not disable the action");
            }

            take(surface, "chatbox", "project_chatbox_cooldown");
            close(surface);
            auto confirm = make_shared<messagebox_window>(U"confirm_clear");
            confirm->set_title(U"清空当前Chatbox");
            confirm->set_message(U"确定发送清空指令吗？本地草稿可以保留。");
            confirm->set_button_set(messagebox_button_set_t::yes_no);
            confirm->set_icon(messagebox_icon_t::question);
            capture(confirm, "project_chatbox_confirm");
        }

        shared_ptr<const drawing_image> create_gallery_image()
        {
            constexpr uint64_t WIDTH = 1600u;
            constexpr uint64_t HEIGHT = 900u;
            vector<uint8_t> pixel_buffer;
            pixel_buffer.reserve((WIDTH * HEIGHT) * 4u);

            for(uint64_t y = 0u;y < HEIGHT;y++)
            {
                for(uint64_t x = 0u;x < WIDTH;x++)
                {
                    const bool SUN = (((static_cast<double>(x) - 1170.0) * (static_cast<double>(x) - 1170.0)) + ((static_cast<double>(y) - 278.0) * (static_cast<double>(y) - 278.0))) < (110.0 * 110.0);
                    auto slope = uint64_t{420u} + ((x % 540u) / 3u);
                    auto ridge = uint64_t{540u} + (((x + 320u) % 670u) / 4u);

                    if(SUN)
                    {
                        pixel_buffer.insert(pixel_buffer.end(), {255u, 196u, 128u, 255u});
                    }
                    else if(y >= ridge)
                    {
                        pixel_buffer.insert(pixel_buffer.end(), {25u, 72u, 86u, 255u});
                    }
                    else if(y >= slope)
                    {
                        pixel_buffer.insert(pixel_buffer.end(), {57u, 92u, 118u, 255u});
                    }
                    else
                    {
                        pixel_buffer.insert(pixel_buffer.end(), {static_cast<uint8_t>(54u + (y / 5u)), static_cast<uint8_t>(98u + (y / 9u)), 161u, 255u});
                    }
                }
            }

            return make_shared<drawing_image>(WIDTH, HEIGHT, move(pixel_buffer));
        }

        void capture_gallery()
        {
            auto surface = create_window(U"房间记录与相册", 880u, 550u);
            auto tabs = add_item<tabcontrol>(*surface, U"tabcontrol_main", {34u, 82u, 810u, 393u});
            auto logs = make_shared<tabpage>(U"tabpage_log");
            logs->set_text(U"房间记录");
            auto photos = make_shared<tabpage>(U"tabpage_photo");
            photos->set_text(U"相册预览");
            tabs->get_page_list().add(logs);
            tabs->get_page_list().add(photos);
            auto filter = add_item<combobox>(*logs, U"combobox_filter", {15u, 15u, 295u, 42u});
            filter->get_item_list().assign({U"全部房间与玩家", U"观景台 / Mika", U"港口 / Ren"});
            filter->set_selected_index(0);
            auto rows = add_item<listview>(*logs, U"listview_log", {15u, 76u, 776u, 234u});
            rows->get_column_list().assign({make_shared<listview_column>(U"时间", 173u), make_shared<listview_column>(U"房间", 188u), make_shared<listview_column>(U"玩家", 189u), make_shared<listview_column>(U"事件", 139u)});
            auto status = add_label(*surface, U"label_state", {43u, 480u, 798u, 41u}, U"本地示例数据 · 已读取4条记录");

            auto refresh = [rows, status](int64_t selected)
            {
                const array<vector<u32string>, 4u> ROW_LIST{{{U"12:10:14", U"观景台", U"Mika", U"加入"}, {U"12:12:08", U"港口", U"Ren", U"加入"}, {U"12:15:30", U"观景台", U"Mika", U"离开"}, {U"12:18:43", U"港口", U"Ren", U"离开"}}};
                rows->get_item_list().clear();

                for(size_t index = 0u;index < ROW_LIST.size();index++)
                {
                    if((selected <= 0) || ((index % 2u) == static_cast<size_t>(selected - 1)))
                    {
                        rows->get_item_list().add(make_shared<listview_item>(ROW_LIST[index]));
                    }
                }

                status->set_text((selected <= 0) ? U"本地示例数据 · 已读取4条记录" : U"本地示例数据 · 筛选后2条记录");
            };

            refresh(0);

            filter->on_selection_changed += [refresh](control_base &source, event_args_t &)
            {
                refresh(static_cast<combobox &>(source).get_selected_index());
            };

            auto tree = add_item<treeview>(*photos, U"treeview_photo", {15u, 15u, 216u, 300u});
            auto month = make_shared<tree_node>(U"演示相册", true);
            auto file = make_shared<tree_node>(U"观景台日落.png");
            month->get_node_list().add(file);
            tree->get_node_list().add(month);
            auto photo = add_item<image>(*photos, U"image_photo", {255u, 15u, 533u, 252u});
            auto note = add_label(*photos, U"label_photo", {255u, 276u, 533u, 38u}, U"选择照片以预览");

            tree->on_selection_changed += [this, photo, note](control_base &, tree_node_event_args_t &event)
            {
                if(event.node && event.node->get_parent())
                {
                    photo->set_source(create_gallery_image());
                    note->set_text(U"观景台日落 · 1600×900 · 合成素材");
                }
            };

            show(surface, "gallery");
            take(surface, "gallery", "project_gallery_idle");
            filter->set_selected_index(1);
            take(surface, "gallery", "project_gallery_filtered");
            tabs->set_selected_index(1);
            status->set_text(U"相册 · 等比预览");
            tree->set_selected_node(file.get());
            take(surface, "gallery", "project_gallery_photo");
            close(surface);
            auto save = make_shared<file_save_dialog_window>(U"confirm_export");
            save->set_title(U"导出筛选后的房间记录");
            save->set_filter_list({{U"TSV表格", {U"*.tsv"}}});
            save->set_directory((fixture / "Assets").u32string());
            save->set_filename(U"room-log.tsv");
            show(save, "gallery_export");
            const auto DEADLINE = chrono::steady_clock::now() + chrono::seconds(8);

            while(save->get_loading() && (chrono::steady_clock::now() < DEADLINE))
            {
                settle();
                this_thread::sleep_for(chrono::milliseconds(12));
            }

            dynamic_cast<textbox &>(save->get_control_list()[U"textbox_directory"]).set_text(U"Assets");
            auto &places = dynamic_cast<listview &>(save->get_control_list()[U"listview_place"]).get_item_list();
            places.clear();
            places.add(make_shared<listview_item>(vector<u32string>{U"导出示例目录"}));
            take(save, "gallery_export", "project_gallery_export");
            close(save);
        }

        void capture_avatar()
        {
            auto surface = create_window(U"Avatar参数与预设", 875u, 529u);
            auto param = add_item<grid>(*surface, U"grid_param", {34u, 88u, 490u, 268u});
            param->set_column_list({grid_column_t{U"参数名", 185u, false}, grid_column_t{U"类型", 115u, false}, grid_column_t{U"当前值", 154u}});
            param->set_row_count(3u);
            param->set_cell_value(0u, 0u, u32string(U"EarFlop"));
            param->set_cell_value(0u, 1u, u32string(U"Float"));
            param->set_cell_value(0u, 2u, 0.50);
            param->set_cell_value(1u, 0u, u32string(U"TailWag"));
            param->set_cell_value(1u, 1u, u32string(U"Bool"));
            param->set_cell_value(1u, 2u, true);
            param->set_cell_value(2u, 0u, u32string(U"CoatToggle"));
            param->set_cell_value(2u, 1u, u32string(U"Int"));
            param->set_cell_value(2u, 2u, int64_t{2});
            auto enabled = add_item<checkbox>(*surface, U"checkbox_sim", {549u, 88u, 280u, 44u});
            enabled->set_text(U"实时更新 · 本地演示");
            add_label(*surface, U"label_float", {549u, 147u, 280u, 42u}, U"当前Float参数");
            auto level = add_item<slider>(*surface, U"slider_float", {549u, 193u, 280u, 43u});
            level->set_value(50);
            auto preset = add_item<combobox>(*surface, U"combobox_preset", {549u, 254u, 280u, 44u});
            preset->get_item_list().assign({U"自定义", U"演示预设"});
            preset->set_selected_index(0);
            add_button(*surface, U"button_save", {549u, 380u, 222u, 44u}, U"保存为预设…");
            auto status = add_label(*surface, U"label_state", {34u, 448u, 795u, 44u}, U"示例Avatar · 等待编辑");

            level->on_value_changed += [param, status](control_base &source, event_args_t &)
            {
                auto amount = static_cast<double>(static_cast<slider &>(source).get_value()) / 100.0;
                param->set_cell_value(0u, 2u, amount);
                status->set_text(U"已更新EarFlop · 演示通道");
            };

            show(surface, "avatar");
            take(surface, "avatar", "project_avatar_idle");
            click("avatar", 590.0, 109.0);
            param->set_selected_index(0);
            host.execute({{"action", "drag"}, {"window", "avatar"}, {"from", {689.0, 214.0}}, {"to", {769.0, 214.0}}});
            preset->set_dropped_down(true);
            take(surface, "avatar", "project_avatar_edit");
            close(surface);
            auto field = make_shared<inputbox_window>(U"preset_name");
            field->set_title(U"保存自定义预设");
            field->set_prompt(U"为当前参数快照输入名称");
            field->set_text(U"观景台调试预设");
            capture(field, "project_avatar_preset");
        }

        void capture_wrist()
        {
            host.execute({{"action", "pose"}, {"frame", "head"}, {"position", {0.0, 1.5, 0.0}}});
            host.execute({{"action", "pose"}, {"frame", "left"}, {"position", {-0.25, 1.2, -0.45}}});
            host.execute({{"action", "pose"}, {"frame", "body"}, {"position", {0.0, 1.5, 0.0}}});
            auto surface = create_window(U"腕部HUD", 410u, 286u);
            surface->set_startup_position(startup_position_t::none);
            surface->set_reference_object(reference_object_t{reference_object_type_t::left});
            surface->set_physical_scale(0.65);
            auto meter = add_item<meter_view>(*surface, U"meter_level", {33u, 83u, 344u, 76u});
            add_label(*surface, U"label_anchor", {33u, 171u, 344u, 37u}, U"left · 0.65倍 · 测试采样");
            add_button(*surface, U"button_screen", {33u, 219u, 225u, 40u}, U"显示桌面副屏");
            show(surface, "wrist");
            take(surface, "wrist", "project_wrist_compact");
            meter->set_level(0.78);
            take(surface, "wrist", "project_wrist_level");
            close(surface);
            auto companion = create_window(U"桌面副屏与电平", 850u, 522u);
            companion->set_startup_position(startup_position_t::none);
            companion->set_position({-0.4, 0.17, -1.1});
            companion->set_reference_object(reference_object_t{reference_object_type_t::body});
            companion->set_curvature(0.65);
            auto preview = add_item<screen>(*companion, U"screen_preview", {34u, 84u, 782u, 255u});
            preview->set_screen_id(10002u);
            add_label(*companion, U"label_preview", {72u, 172u, 659u, 69u}, U"无头WARP · 桌面画面占位");
            auto audio = add_item<meter_view>(*companion, U"meter_audio", {34u, 361u, 782u, 67u});
            audio->set_level(0.78);
            auto anchor = add_label(*companion, U"label_anchor", {34u, 449u, 782u, 40u}, U"body · 曲率0.65m⁻¹");
            show(companion, "companion");
            take(companion, "companion", "project_wrist_screen");
            companion->set_reference_object(reference_object_t{reference_object_type_t::world});
            companion->set_curvature(0.0);
            anchor->set_text(U"world · 曲率0.00m⁻¹ · 平面");
            take(companion, "companion", "project_wrist_anchor");
            close(companion);
        }

        void capture_kaomoji()
        {
            auto remote = create_window(U"远程会话配置", 786u, 366u);
            add_label(*remote, U"label_address", {34u, 91u, 290u, 39u}, U"Engine地址与端口");
            auto address = add_item<textbox>(*remote, U"textbox_host", {335u, 91u, 416u, 43u});
            address->set_text(U"render-host.example");
            auto port = add_item<numericupdown>(*remote, U"numeric_port", {335u, 149u, 196u, 43u});
            port->set_minimum(1.0);
            port->set_maximum(65535.0);
            port->set_value(18342.0);
            add_label(*remote, U"label_tls", {34u, 203u, 717u, 40u}, U"凭据与证书指纹 · 使用测试配置");
            auto connect = add_button(*remote, U"button_connect", {34u, 254u, 170u, 44u}, U"验证配置");
            auto state = add_label(*remote, U"label_state", {228u, 254u, 523u, 44u}, U"等待验证 · 本地状态演示");

            connect->on_click += [state](control_base &, event_args_t &)
            {
                state->set_text(U"测试状态：会话已连接");
            };

            show(remote, "remote");
            take(remote, "remote", "project_kaomoji_config");
            click("remote", 114.0, 274.0);
            take(remote, "remote", "project_kaomoji_connected");
            close(remote);
            auto surface = create_window(U"颜文字测试面板", 740u, 360u);
            auto tabs = add_item<tabcontrol>(*surface, U"tabcontrol_group", {34u, 87u, 672u, 168u});
            auto greeting = make_shared<tabpage>(U"tabpage_greeting");
            auto reaction = make_shared<tabpage>(U"tabpage_reaction");
            greeting->set_text(U"问候");
            reaction->set_text(U"回应");
            tabs->get_page_list().add(greeting);
            tabs->get_page_list().add(reaction);
            add_button(*greeting, U"button_hello", {18u, 15u, 223u, 51u}, U"(^_^)/");
            auto choice = add_button(*reaction, U"button_send", {18u, 15u, 223u, 51u}, U"(>_<)");
            add_button(*reaction, U"button_smile", {261u, 15u, 223u, 51u}, U"(^o^)");
            auto history = add_label(*surface, U"label_history", {34u, 274u, 672u, 46u}, U"最近使用 · 暂无");

            choice->on_click += [history](control_base &source, event_args_t &)
            {
                history->set_text(U"测试提交 · 最近使用：" + static_cast<button &>(source).get_text());
            };

            show(surface, "pad");
            tabs->set_selected_index(1);
            take(surface, "pad", "project_kaomoji_group");
            click("pad", 165.0, 163.0);
            take(surface, "pad", "project_kaomoji_history");
            close(surface);
        }

    public:
        capture_project_story(const filesystem::path &output, filesystem::path fixture_path) : host(output, true), fixture(move(fixture_path))
        {
        }

        void run()
        {
            capture_basics();
            capture_chatbox();
            capture_gallery();
            capture_avatar();
            capture_wrist();
            capture_kaomoji();
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

        capture_project_story capture{filesystem::u8path(argument[1]), filesystem::u8path(argument[2])};
        capture.run();
        return 0;
    }
    catch(const exception &error)
    {
        (cerr << get_error_message(error)) << '\n';
        return 1;
    }
}