#include "ui_test_host.h"
#include "easyvrui/core/ui_runtime.h"
#include "easyvrui/localization/language_pack.h"
#include <easyvrui.h>

#if defined(TUTORIAL_CAPTURE_desktop)
#include "desktop_window.h"
#elif defined(TUTORIAL_CAPTURE_designer)
#include "designer_window.h"
#elif defined(TUTORIAL_CAPTURE_file_manager)
#include "file_manager_window.h"
#elif defined(TUTORIAL_CAPTURE_task_manager)
#include "task_manager_window.h"
#elif defined(TUTORIAL_CAPTURE_demo)
#include "translator_window.h"
#elif defined(TUTORIAL_CAPTURE_keyboard)
#include "virtual_keyboard.h"
#elif defined(TUTORIAL_CAPTURE_pinyin) || defined(TUTORIAL_CAPTURE_japanese)
#include "candidate_window.h"
#elif defined(TUTORIAL_CAPTURE_dialog)
#include "easyvrui/dialog/internal/color_dialog_window.h"
#include "easyvrui/dialog/internal/file_open_dialog_window.h"
#include "easyvrui/dialog/internal/font_dialog_window.h"
#include "easyvrui/dialog/internal/messagebox_window.h"
#endif

#include <chrono>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>
#include <string_view>
#include <thread>
#include <type_traits>
#include <vector>

using namespace std;
using namespace easyvrui;
using nlohmann::json;

#if defined(TUTORIAL_CAPTURE_controls)
shared_ptr<window> create_window_demo();
shared_ptr<window> create_label_demo();
shared_ptr<window> create_button_demo();
shared_ptr<window> create_textbox_demo();
shared_ptr<window> create_checkbox_demo();
shared_ptr<window> create_radiobutton_demo();
shared_ptr<window> create_progressbar_demo();

#endif

class tutorial_capture
{
    private:
        static constexpr auto PUMP_INTERVAL = chrono::milliseconds(12);
        static constexpr auto SURFACE_TIMEOUT = chrono::seconds(8);
        static constexpr uint64_t TUTORIAL_SLIDER_VALUE = 64u;
        filesystem::path fixture;
        string locale;
        ui_test_host host;

        u32string translate(u32string_view zh, u32string_view en, u32string_view ja) const
        {
            return u32string(locale == "zh" ? zh : (locale == "ja" ? ja : en));
        }

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
                throw runtime_error("Surface did not present: " + filesystem::path(surface.get_name()).string());
            }
        }

        void show(const shared_ptr<window> &surface, const string &name)
        {
            host.attach_control(surface, name);
            host.execute({{"action", "show"}, {"name", name}});
            wait_for_surface(*surface);
        }

        void snapshot(const shared_ptr<window> &surface, const string &name)
        {
            pump();
            wait_for_surface(*surface);
            host.execute({{"action", "snapshot"}, {"window", name}, {"label", name}});
        }

        void capture_surface(const shared_ptr<window> &surface, const string &name)
        {
            show(surface, name);
            snapshot(surface, name);
            surface->close(true);
            pump();
        }

#if defined(TUTORIAL_CAPTURE_controls)
        template<typename control_type>
        shared_ptr<control_type> add_preview_control(window &surface, const u32string &name, const rectangle_t &rectangle)
        {
            auto item = make_shared<control_type>(name);
            item->set_rect(rectangle);
            surface.get_control_list().add(item);
            return item;
        }

        shared_ptr<window> create_preview_window(const string &name, uint64_t width, uint64_t height)
        {
            auto surface = make_shared<window>(U"window_preview");
            surface->set_title(u32string(name.begin(), name.end()));
            surface->set_size(width, height);
            return surface;
        }

        template<typename control_type>
        void capture_default_control(const string &name, const u32string &text)
        {
            auto surface = create_preview_window(name, 540u, 174u);
            auto item = add_preview_control<control_type>(*surface, U"control_preview", {36u, 82u, 468u, 52u});

            if constexpr(!is_same_v<control_type, progressbar>)
            {
                item->set_text(text);
            }

            capture_surface(surface, name + "_default");
        }

        template<typename control_type>
        shared_ptr<control_type> add_comparison_row(window &surface, uint64_t index, const u32string &caption, const u32string &text)
        {
            uint64_t top = 80u + (72u * index);
            u32string suffix(1u, U'0' + static_cast<char32_t>(index));
            auto title = add_preview_control<label>(surface, U"label_" + suffix, {22u, top, 254u, 48u});
            title->set_text(caption);
            auto item = add_preview_control<control_type>(surface, U"control_" + suffix, {290u, top, 370u, 50u});

            if constexpr(!is_same_v<control_type, progressbar>)
            {
                item->set_text(text);
            }

            return item;
        }

        void capture_window_comparison()
        {
            auto surface = create_preview_window("window", 540u, 178u);
            auto text = add_preview_control<label>(*surface, U"label_content", {30u, 91u, 480u, 46u});
            text->set_text(U"默认标题栏");
            capture_surface(surface, "window_default");
            surface = create_preview_window("window", 540u, 178u);
            surface->set_title_background_color(0x294f73ffu);
            surface->set_title_foreground_color(0xffd48affu);
            surface->set_title_font(font_t{U"Microsoft YaHei UI", 26u, true});
            text = add_preview_control<label>(*surface, U"label_content", {30u, 91u, 480u, 46u});
            text->set_text(U"自定义标题颜色和字体");
            capture_surface(surface, "window_custom_title");
            surface = create_preview_window("window", 540u, 178u);
            surface->set_show_close_button(false);
            text = add_preview_control<label>(*surface, U"label_content", {30u, 91u, 480u, 46u});
            text->set_text(U"隐藏标准关闭入口");
            capture_surface(surface, "window_no_close");
            surface = create_preview_window("window", 540u, 178u);
            surface->set_show_title_bar(false);
            text = add_preview_control<label>(*surface, U"label_content", {30u, 60u, 480u, 46u});
            text->set_text(U"隐藏标题栏");
            capture_surface(surface, "window_no_title");
        }

        void capture_label_comparison()
        {
            auto surface = create_preview_window("label", 700u, 380u);
            add_comparison_row<label>(*surface, 0u, U"默认", U"工作区连接");
            add_comparison_row<label>(*surface, 1u, U"font", U"工作区连接")->set_font(font_t{U"Microsoft YaHei UI", 28u, true});
            auto colored = add_comparison_row<label>(*surface, 2u, U"前景色与背景色", U"工作区连接");
            colored->set_foreground_color(0xa7efc9ffu);
            colored->set_background_color(0x173b38ffu);
            add_comparison_row<label>(*surface, 3u, U"enabled = false", U"工作区连接")->set_enabled(false);
            capture_surface(surface, "label_comparison");
        }

        void capture_button_comparison()
        {
            auto surface = create_preview_window("button", 700u, 380u);
            add_comparison_row<button>(*surface, 0u, U"默认", U"提交设置");
            auto colored = add_comparison_row<button>(*surface, 1u, U"字体与颜色", U"提交设置");
            colored->set_font(font_t{U"Microsoft YaHei UI", 24u, true});
            colored->set_background_color(0x244b70ffu);
            colored->set_foreground_color(0xe5f5ffffu);
            add_comparison_row<button>(*surface, 2u, U"enabled = false", U"提交设置")->set_enabled(false);
            auto focused = add_comparison_row<button>(*surface, 3u, U"focus()", U"提交设置");
            show(surface, "button_comparison");
            focused->focus();
            snapshot(surface, "button_comparison");
            surface->close(true);
            pump();
        }

        void capture_textbox_comparison()
        {
            auto surface = create_preview_window("textbox", 700u, 450u);
            add_comparison_row<textbox>(*surface, 0u, U"默认", U"工作区备注");
            auto read_only = add_comparison_row<textbox>(*surface, 1u, U"read_only = true", U"工作区备注");
            read_only->set_read_only(true);
            auto disabled = add_comparison_row<textbox>(*surface, 2u, U"enabled = false", U"工作区备注");
            disabled->set_enabled(false);
            auto multiline = add_comparison_row<textbox>(*surface, 3u, U"multiline = true", U"");
            multiline->set_multiline(true);
            multiline->set_vertical_scrollbar_visible(true);
            multiline->set_rect({290u, 296u, 370u, 114u});
            multiline->set_text(U"第一行：检查连接\n第二行：同步配置\n第三行：检查结果\n第四行：记录时间");
            capture_surface(surface, "textbox_comparison");
        }

        void capture_choice_comparison()
        {
            auto check = create_preview_window("checkbox", 700u, 380u);
            add_comparison_row<checkbox>(*check, 0u, U"默认", U"播放通知声音");
            add_comparison_row<checkbox>(*check, 1u, U"checked = true", U"播放通知声音")->set_checked(true);
            auto disabled = add_comparison_row<checkbox>(*check, 2u, U"enabled = false", U"播放通知声音");
            disabled->set_checked(true);
            disabled->set_enabled(false);
            auto colored = add_comparison_row<checkbox>(*check, 3u, U"字体与颜色", U"播放通知声音");
            colored->set_font(font_t{U"Microsoft YaHei UI", 24u, true});
            colored->set_foreground_color(0x9de1ffffu);
            colored->set_background_color(0x233748ffu);
            capture_surface(check, "checkbox_comparison");

            auto radio = create_preview_window("radiobutton", 700u, 380u);
            add_comparison_row<radiobutton>(*radio, 0u, U"默认", U"接收全部通知");
            add_comparison_row<radiobutton>(*radio, 1u, U"checked = true", U"仅接收重要通知")->set_checked(true);
            add_comparison_row<radiobutton>(*radio, 2u, U"enabled = false", U"暂不可选")->set_enabled(false);
            auto styled = add_comparison_row<radiobutton>(*radio, 3u, U"字体与颜色", U"暂停通知");
            styled->set_font(font_t{U"Microsoft YaHei UI", 23u, true});
            styled->set_foreground_color(0xf2c78affu);
            styled->set_background_color(0x38332affu);
            capture_surface(radio, "radiobutton_comparison");
        }

        void capture_progress_comparison()
        {
            auto surface = create_preview_window("progressbar", 700u, 380u);
            add_comparison_row<progressbar>(*surface, 0u, U"默认 0 / 100", U"");
            add_comparison_row<progressbar>(*surface, 1u, U"value = 42", U"")->set_value(42);
            auto bounded = add_comparison_row<progressbar>(*surface, 2u, U"范围 20–80，值 65", U"");
            bounded->set_maximum(80);
            bounded->set_minimum(20);
            bounded->set_value(65);
            auto disabled = add_comparison_row<progressbar>(*surface, 3u, U"禁用与自定义背景", U"");
            disabled->set_value(65);
            disabled->set_background_color(0x293744ffu);
            disabled->set_enabled(false);
            capture_surface(surface, "progressbar_comparison");
        }

        void capture_demo(const shared_ptr<window> &surface, const string &name, double left, double top, uint64_t click_count = 1u)
        {
            show(surface, name);

            for(uint64_t index = 0u;index < click_count;index++)
            {
                host.execute({{"action", "click"}, {"window", name}, {"left", left}, {"top", top}});
            }

            host.execute({{"action", "move"}, {"window", name}, {"left", 12.0}, {"top", 65.0}});
            snapshot(surface, name);
            surface->close(true);
            pump();
        }

        void capture_control_chapters()
        {
            capture_window_comparison();
            capture_default_control<label>("label", U"工作区连接");
            capture_default_control<button>("button", U"提交设置");
            capture_default_control<textbox>("textbox", U"工作区备注");
            capture_default_control<checkbox>("checkbox", U"播放通知声音");
            capture_default_control<radiobutton>("radiobutton", U"接收全部通知");
            capture_default_control<progressbar>("progressbar", U"");
            capture_label_comparison();
            capture_button_comparison();
            capture_textbox_comparison();
            capture_choice_comparison();
            capture_progress_comparison();
            capture_demo(create_window_demo(), "window_demo", 110.0, 184.0);
            capture_surface(create_label_demo(), "label_demo");
            capture_demo(create_button_demo(), "button_demo", 110.0, 180.0);
            capture_demo(create_textbox_demo(), "textbox_demo", 115.0, 348.0);
            capture_demo(create_checkbox_demo(), "checkbox_demo", 105.0, 105.0);
            capture_demo(create_radiobutton_demo(), "radiobutton_demo", 115.0, 110.0);
            capture_demo(create_progressbar_demo(), "progressbar_demo", 110.0, 226.0, 3u);
        }
#endif

#if defined(TUTORIAL_CAPTURE_file_manager) || defined(TUTORIAL_CAPTURE_dialog)
        void prepare_sample_places(listview &place)
        {
            auto &item_list = place.get_item_list();
            auto folder_icon = item_list.get_size() == 0u ? shared_ptr<const drawing_image>{} : item_list[0u]->get_icon();
            place.on_selection_changed.clear();
            item_list.clear();

            for(const auto &name : {translate(U"计算机", U"Computer", U"コンピューター"), translate(U"示例文件夹", U"Example folder", U"サンプルフォルダー"), translate(U"素材", U"Assets", U"素材"), translate(U"模板", U"Templates", U"テンプレート")})
            {
                auto item = make_shared<listview_item>(vector<u32string>{name});
                item->set_icon(folder_icon);
                item_list.add(move(item));
            }
        }
#endif

#if defined(TUTORIAL_CAPTURE_demo)
        void configure_demo(translator_window &surface)
        {
            surface.set_title(translate(U"EasyVRUI控件演示", U"EasyVRUI Control Demo", U"EasyVRUIコントロールデモ"));
            surface.label_caption->set_text(translate(U"窗口与交互控件", U"Windows and interactive controls", U"ウィンドウと操作コントロール"));
            surface.label_frame->set_text(translate(U"跟踪参考", U"Tracking reference", U"追従基準"));
            surface.select_reference_object(reference_object_t{reference_object_type_t::world});
            surface.textbox_text->set_text(translate(U"你好，VR", U"Hello, VR", U"こんにちは、VR"));
            surface.button_dialog->set_text(translate(U"打开设置", U"Open settings", U"設定を開く"));
            surface.button_duplicate->set_text(translate(U"新建窗口", U"New window", U"新規ウィンドウ"));
            surface.tabpage_text->set_text(translate(U"文本", U"Text", U"テキスト"));
            surface.tabpage_custom->set_text(translate(U"绘图", U"Drawing", U"描画"));
            surface.tabpage_scrolling->set_text(translate(U"多行", U"Multiline", U"複数行"));
            surface.tabpage_input->set_text(translate(U"输入", U"Inputs", U"入力"));
            surface.tabpage_gallery->set_text(translate(U"容器", U"Containers", U"コンテナー"));
            surface.tabpage_listview->set_text(translate(U"列表", U"ListView", U"リスト"));
            surface.tabpage_screen->set_text(translate(U"屏幕", U"Screen", U"画面"));
            surface.tabpage_grid->set_text(translate(U"表格", U"Grid", U"グリッド"));
            surface.tabpage_toolbar->set_text(translate(U"工具栏", U"Tools", U"ツール"));
            surface.checkbox_option->set_text(translate(U"启用选项", U"Enable option", U"オプションを有効化"));
            surface.radiobutton_first->set_text(translate(U"第一项", U"First choice", U"選択肢 1"));
            surface.radiobutton_second->set_text(translate(U"第二项", U"Second choice", U"選択肢 2"));
            surface.menuitem_file->set_text(translate(U"文件(&F)", U"&File", U"ファイル(&F)"));
            surface.menuitem_view->set_text(translate(U"视图(&V)", U"&View", U"表示(&V)"));
            surface.menuitem_tools->set_text(translate(U"工具(&T)", U"&Tools", U"ツール(&T)"));
            surface.listbox_entry->get_item_list().assign({translate(U"欢迎", U"Welcome", U"ようこそ"), translate(U"快捷短语", U"Quick phrases", U"定型文"), translate(U"翻译历史", U"History", U"履歴"), translate(U"最近窗口", U"Recent windows", U"最近のウィンドウ"), translate(U"书签", U"Bookmarks", U"ブックマーク"), translate(U"偏好设置", U"Preferences", U"環境設定"), translate(U"帮助", U"Help", U"ヘルプ")});
            surface.listbox_entry->set_selected_index(1);
            surface.checkbox_option->set_checked(true);
            surface.radiobutton_first->set_checked(true);
            surface.slider_value->set_value(TUTORIAL_SLIDER_VALUE);
            surface.progressbar_value->set_value(TUTORIAL_SLIDER_VALUE);
            surface.tabcontrol_local->set_selected_index(static_cast<int64_t>(surface.tabcontrol_local->get_page_list().get_index(*surface.tabpage_input)));
        }
#endif

#if defined(TUTORIAL_CAPTURE_pinyin) || defined(TUTORIAL_CAPTURE_japanese)
        void capture_candidate()
        {
            candidate_window_configuration_t configuration;
            input_context_t context;
#if defined(TUTORIAL_CAPTURE_japanese)
            configuration.title = U"EasyVRUI日本語";
            configuration.native_mode_text = U"かな";
            configuration.empty_preedit_text = U"ローマ字で入力";
            configuration.font_family = U"Yu Gothic UI";
            context.preedit = U"にほんご";
            context.candidate_list = {input_candidate_t{U"日本語", U""}, input_candidate_t{U"にほんご", U""}, input_candidate_t{U"ニホンゴ", U""}};
            const string IME_NAME = "EasyVRUI日本語";
            const string IME_LANGUAGE = "ja";
#else
            context.preedit = U"nihao";
            context.candidate_list = {input_candidate_t{U"你好", U""}, input_candidate_t{U"拟好", U""}, input_candidate_t{U"您好", U""}, input_candidate_t{U"你好呀", U""}};
            const string IME_NAME = "EasyVRUI拼音";
            const string IME_LANGUAGE = "zh";
#endif
            context.cursor = context.preedit.size();
            context.selected_candidate = 0u;
            context.highlight_candidate = true;
            context.is_last_page = false;

            auto candidate = make_shared<candidate_window>(configuration);
            candidate->set_auxiliary(false);
            candidate->set_context(context, false);
            capture_surface(candidate, "candidate");

            auto owner = make_shared<window>(U"tutorial_input");
            owner->set_title(translate(U"文本输入", U"Text Input", U"テキスト入力"));
            owner->set_size(710u, 164u);
            owner->set_tracking_mode_set({});
            auto field = make_shared<textbox>(U"textbox_example");
            const rectangle_t FIELD_RECTANGLE{34u, 80u, 642u, 52u};
            field->set_rect(FIELD_RECTANGLE);
            field->set_font(font_t{configuration.font_family, 24u});
            field->set_text(translate(U"你好，VR", U"Hello, VR", U"こんにちは、VR"));
            owner->get_control_list().add(field);
            show(owner, "input_box");
            host.execute({{"action", "click"}, {"window", "input_box"}, {"left", 170.0}, {"top", 106.0}});
            auto &runtime = ui_runtime::get_current();
            json state{{"message_type", "event"}, {"event_type", "input_ui_state"}, {"window", owner->get_id()}, {"physical", false}, {"rectangle", {{"left", FIELD_RECTANGLE.left}, {"top", FIELD_RECTANGLE.top}, {"width", FIELD_RECTANGLE.width}, {"height", FIELD_RECTANGLE.height}}}, {"provider_list", {{{"id", 2u}, {"role", "ime"}, {"name", IME_NAME}, {"language", IME_LANGUAGE}, {"state", "running"}, {"configured", true}, {"active", true}, {"process_id", 2u}, {"error", ""}}}}};
            runtime.process_message(state);
            const auto DEADLINE = chrono::steady_clock::now() + SURFACE_TIMEOUT;
            shared_ptr<window> bar;

            while(!bar && (chrono::steady_clock::now() < DEADLINE))
            {
                pump();

                for(uint64_t id : runtime.window_list)
                {
                    auto surface = runtime.get_window_by_id(id);

                    if(surface && (surface->get_name() == U"input_bar"))
                    {
                        bar = move(surface);
                        break;
                    }
                }
            }

            if(!bar)
            {
                throw runtime_error("The SDK input bar was not created after input focus");
            }

            host.attach_control(bar, "input_bar");
            snapshot(bar, "input_bar");
            host.execute({{"action", "move"}, {"window", "input_box"}, {"left", 31.0}, {"top", 74.0}});
            snapshot(owner, "input_box");
            owner->close(true);
            pump();
        }
#endif

    public:
        tutorial_capture(const filesystem::path &output, filesystem::path fixture_path, string language) :
            fixture(move(fixture_path)), locale(move(language)), host(output, true)
        {
        }

        void run(const filesystem::path &output)
        {
#if defined(TUTORIAL_CAPTURE_desktop)
            capture_surface(make_shared<desktop_window>(U"tutorial_desktop"), "desktop");
#elif defined(TUTORIAL_CAPTURE_designer)
            auto surface = make_shared<designer_window>(U"tutorial_designer");
            show(surface, "form_designer");
            auto document = surface->get_active_document();
            const auto ROOT = document->get_root().key;
            const auto LABEL = document->add_control(ROOT, U"label", U"label_tip");
            document->set_property(LABEL, U"rect", rectangle_t{48u, 104u, 438u, 38u});
            document->set_property(LABEL, U"text", translate(U"输入一条短消息", U"Enter a short message", U"短いメッセージを入力"));
            const auto FIELD = document->add_control(ROOT, U"textbox", U"textbox_msg");
            document->set_property(FIELD, U"rect", rectangle_t{48u, 152u, 438u, 44u});
            document->set_property(FIELD, U"text", translate(U"你好，VR", U"Hello, VR", U"こんにちは、VR"));
            const auto BUTTON = document->add_control(ROOT, U"button", U"button_send");
            document->set_property(BUTTON, U"rect", rectangle_t{48u, 224u, 140u, 46u});
            document->set_property(BUTTON, U"text", translate(U"发送", U"Send", U"送信"));
            surface->get_active_surface()->rebuild_preview();
            surface->get_active_surface()->set_selection_list({BUTTON});

            if(locale == "zh")
            {
                auto &workspace = *surface->splitter_workspace;
                auto &navigation = *surface->splitter_navigation;
                workspace.set_split_position(0.18);
                const auto &tool_list = surface->scrollpanel_toolbox->get_control_list();
                const auto &last_tool = tool_list[9u].get_rect();
                uint64_t toolbox_height = (surface->label_toolbox->get_rect().height + last_tool.top) + last_tool.height;
                navigation.set_split_position(static_cast<double>(toolbox_height) / static_cast<double>(navigation.get_rect().height));
            }

            snapshot(surface, "form_designer");
            auto &runtime = ui_runtime::get_current();
            auto toolbar = runtime.get_absolute_rect(*surface->toolbar_command);
            auto menu = runtime.get_absolute_rect(*surface->get_menu());
            json region_map{{"command", {toolbar.left, menu.top, toolbar.width, (toolbar.top + toolbar.height) - menu.top}}};

            for(const auto *control : runtime.get_descendant_list(*surface))
            {
                const auto &name = control->get_name();
                const char *key = (name == U"scrollpanel_toolbox") ? "toolbox" : ((name == U"tabcontrol_document") ? "canvas" : ((name == U"propertygrid_property") ? "property" : nullptr));

                if(key != nullptr)
                {
                    auto rectangle = runtime.get_absolute_rect(*control);
                    region_map[key] = {rectangle.left, rectangle.top, rectangle.width, rectangle.height};
                }
            }

            if(region_map.size() != 4u)
            {
                throw runtime_error("The designer did not expose all four annotation regions");
            }

            ofstream region_file(output / "designer_regions.json", ios::binary);
            region_file << region_map.dump(4);

            if(!region_file)
            {
                throw runtime_error("Could not write designer region coordinates");
            }

            if(locale == "zh")
            {
                surface->open_document(fixture.parent_path() / "quick_shout_window.easyvruifrm");
                auto lesson = surface->get_active_document();

                for(const auto &node : lesson->get_root().child_list)
                {
                    if(node.name == U"button_send")
                    {
                        surface->get_active_surface()->set_selection_list({node.key});
                        break;
                    }
                }

                pump();
                wait_for_surface(*surface);
                host.execute({{"action", "snapshot"}, {"window", "form_designer"}, {"label", "basics_form_design"}});
            }

#elif defined(TUTORIAL_CAPTURE_file_manager)
            auto surface = make_shared<file_manager_window>(U"tutorial_file_manager");
            show(surface, "file_manager");
            surface->textbox_path->set_text(fixture.u32string());
            surface->button_go->activate();
            const auto DEADLINE = chrono::steady_clock::now() + SURFACE_TIMEOUT;

            while((surface->listview_entry->get_item_list().get_size() < 4u) && (chrono::steady_clock::now() < DEADLINE))
            {
                pump();
                this_thread::sleep_for(PUMP_INTERVAL);
            }

            if(surface->listview_entry->get_item_list().get_size() < 4u)
            {
                throw runtime_error("File Manager did not populate the tutorial directory");
            }

            prepare_sample_places(*surface->listview_navigation);
            surface->set_title(translate(U"文件管理器 — 示例文件夹", U"File Manager — Example folder", U"ファイルマネージャー — サンプルフォルダー"));
            surface->textbox_path->set_text(U"Examples");
            snapshot(surface, "file_manager");
#elif defined(TUTORIAL_CAPTURE_task_manager)
            auto surface = make_shared<task_manager_window>(U"tutorial_task_manager");
            show(surface, "task_manager");
            surface->pump_snapshot();
            surface->tabcontrol_page->set_selected_index(1);
            auto &item_list = surface->listview_detail->get_item_list();
            item_list.clear();

            for(const auto &row : vector<vector<u32string>>{{translate(U"桌面", U"Desktop", U"デスクトップ"), U"0.2%", U"22 MB (0.1%)", U"0.1%", U"11", U"4204", U"1"}, {translate(U"窗体设计器", U"Form Designer", U"フォームデザイナー"), U"1.4%", U"84 MB (0.3%)", U"0.3%", U"12", U"5048", U"1"}, {translate(U"文件管理器", U"File Manager", U"ファイルマネージャー"), U"0.3%", U"38 MB (0.1%)", U"0.1%", U"13", U"5820", U"1"}, {translate(U"控件演示", U"Control Demo", U"コントロールデモ"), U"0.8%", U"46 MB (0.2%)", U"0.2%", U"14", U"7160", U"2"}})
            {
                auto item = make_shared<listview_item>();
                item->set_tag(row[4u]);
                item->get_cell_list().assign(row);
                item_list.add(move(item));
            }

            surface->listview_detail->set_selected_index(1);
            snapshot(surface, "task_manager");
#elif defined(TUTORIAL_CAPTURE_controls)
            capture_control_chapters();
#elif defined(TUTORIAL_CAPTURE_demo)
            auto surface = make_shared<translator_window>(U"tutorial_demo");
            configure_demo(*surface);
            capture_surface(surface, "demo_controls");
#elif defined(TUTORIAL_CAPTURE_keyboard)
            virtual_keyboard keyboard;
            auto &runtime = ui_runtime::get_current();

            for(uint64_t id = 1u;id < 64u;id++)
            {
                auto surface = runtime.get_window_by_id(id);

                if(surface && (surface->get_name() == U"__virtual_keyboard"))
                {
                    surface->set_auxiliary(false);
                    capture_surface(surface, "layout_keyboard");
                    return;
                }
            }

            throw runtime_error("The standard_104 window was not created");
#elif defined(TUTORIAL_CAPTURE_pinyin) || defined(TUTORIAL_CAPTURE_japanese)
            capture_candidate();
#elif defined(TUTORIAL_CAPTURE_dialog)
            auto message = make_shared<messagebox_window>(U"tutorial_messagebox");
            message->set_title(translate(U"保存窗体", U"Save Form", U"フォームの保存"));
            message->set_icon(messagebox_icon_t::question);
            message->set_message(translate(U"要保存对当前窗体所做的修改吗？", U"Save changes to the current form?", U"現在のフォームへの変更を保存しますか？"));
            message->set_button_set(messagebox_button_set_t::yes_no_cancel);
            message->set_default_button(dialog_result_t::yes);
            capture_surface(message, "dialog_messagebox");
            auto color = make_shared<color_dialog_window>(U"tutorial_color");
            color->set_color(0x5296e8ffu);

            if(locale == "zh")
            {
                color->get_control_list()[U"label_hue_caption"].set_rect({448u, 80u, 60u, 32u});
                color->get_control_list()[U"label_alpha_caption"].set_rect({508u, 80u, 64u, 32u});
            }

            capture_surface(color, "dialog_color");
            auto font = make_shared<font_dialog_window>(U"tutorial_font");
            font->set_font(font_t{translate(U"Microsoft YaHei UI", U"Segoe UI", U"Yu Gothic UI"), 24u});
            auto &family = dynamic_cast<listbox &>(font->get_control_list()[U"listbox_family"]);
            auto family_rectangle = family.get_rect();
            family_rectangle.height -= family_rectangle.height % family.get_row_height();
            family.set_rect(family_rectangle);
            capture_surface(font, "dialog_font");
            auto open = make_shared<file_open_dialog_window>(U"tutorial_file_open");
            open->set_filter_list({{translate(U"窗体设计文件", U"Form design files", U"フォーム設計ファイル"), {U"*.easyvruifrm"}}, {translate(U"所有文件", U"All files", U"すべてのファイル"), {U"*.*"}}});
            open->set_filter_index(1u);
            open->set_directory(fixture.u32string());
            open->set_filename(U"welcome.easyvruifrm");
            show(open, "dialog_file_open");
            const auto DEADLINE = chrono::steady_clock::now() + SURFACE_TIMEOUT;

            while(open->get_loading() && (chrono::steady_clock::now() < DEADLINE))
            {
                pump();
                this_thread::sleep_for(PUMP_INTERVAL);
            }

            if(open->get_loading())
            {
                throw runtime_error("The standard file dialog did not finish its directory scan");
            }

            auto &control_list = open->get_control_list();
            prepare_sample_places(dynamic_cast<listview &>(control_list[U"listview_place"]));
            dynamic_cast<textbox &>(control_list[U"textbox_directory"]).set_text(U"Examples");

            if(locale == "zh")
            {
                auto &column_list = dynamic_cast<listview &>(control_list[U"listview_entry"]).get_column_list();
                column_list[0u]->set_width(230u);
                column_list[1u]->set_width(258u);
                column_list[2u]->set_width(190u);
            }

            snapshot(open, "dialog_file_open");
#endif
        }
};

int32_t main(int32_t count, char **argument)
{
    try
    {
        if(count != 4)
        {
            throw invalid_argument("Usage: tutorial_capture_<role> <output-directory> <fixture-directory> <zh|en|ja>");
        }

        auto output = filesystem::u8path(argument[1]);
        tutorial_capture capture(output, filesystem::u8path(argument[2]), argument[3]);
        capture.run(output);
        return 0;
    }
    catch(const exception &error)
    {
        cerr << get_error_message(error) << '\n';
        return 1;
    }
}
