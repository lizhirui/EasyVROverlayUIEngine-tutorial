#include <easyvrui.h>
#include <cstdlib>
#include <array>
#include <chrono>
#include <codecvt>
#include <locale>
#include <optional>
#include <string_view>
#include <system_error>
#include <filesystem>
#include <fstream>
#include <memory>
#include <string>
#include <thread>
#include <vector>

using namespace std;

using log_row_t = array<u32string, 3u>;

filesystem::path get_profile_directory()
{
    wchar_t *buffer = nullptr;
    size_t count = 0u;
    if(_wdupenv_s(&buffer, &count, L"USERPROFILE") != 0)
    {
        return {};
    }

    unique_ptr<wchar_t, decltype(&free)> value(buffer, &free);
    return value ? filesystem::path(value.get()) : filesystem::path{};
}

u32string decode_log_text(const string &value)
{
    return wstring_convert<codecvt_utf8<char32_t>, char32_t>{}.from_bytes(value);
}

filesystem::path find_latest_log(const filesystem::path &folder)
{
    error_code error;
    filesystem::path latest;
    auto latest_time = filesystem::file_time_type::min();
    for(filesystem::directory_iterator entry(folder, error), end;!error && (entry != end);entry.increment(error))
    {
        if(!entry->path().filename().wstring().starts_with(L"output_log_") || (entry->path().extension() != L".txt"))
        {
            continue;
        }

        auto stamp = entry->last_write_time(error);
        if(!error && (stamp >= latest_time))
        {
            latest_time = stamp;
            latest = entry->path();
        }
        error.clear();
    }

    return latest;
}

optional<log_row_t> parse_log_row(const string &line)
{
    for(const auto &[token, action] : {pair{string_view{"OnPlayerJoined"}, u32string_view{U"Joined"}}, pair{string_view{"OnPlayerLeft"}, u32string_view{U"Left"}}})
    {
        auto position = line.find(token);
        if(position == string::npos)
        {
            continue;
        }

        auto name_start = line.find_first_not_of(" :\t", position + token.size());
        if(name_start == string::npos)
        {
            continue;
        }

        auto name_end = line.find_last_not_of(" \t\r");
        try
        {
            return log_row_t{decode_log_text(line.substr(0u, 19u)), u32string(action), decode_log_text(line.substr(name_start, (name_end - name_start) + 1u))};
        }
        catch(const range_error &)
        {
            return {};
        }
    }

    return {};
}

void populate_gallery(easyvrui::treeview &view, const filesystem::path &folder)
{
    error_code error;
    for(filesystem::directory_iterator month(folder, error), end;!error && (month != end);month.increment(error))
    {
        error_code month_error;
        if(!month->is_directory(month_error))
        {
            continue;
        }

        auto group = make_shared<easyvrui::tree_node>(month->path().filename().u32string());
        for(filesystem::directory_iterator photo(month->path(), month_error);!month_error && (photo != end);photo.increment(month_error))
        {
            if(photo->path().extension() == L".png")
            {
                group->get_node_list().add(make_shared<easyvrui::tree_node>(photo->path().filename().u32string(), false, photo->path().u32string()));
            }
        }

        if(group->get_node_list().get_size() != 0u)
        {
            view.get_node_list().add(move(group));
        }
    }
}

int main()
{
    auto window_main = make_shared<easyvrui::window>(U"window_main");
    window_main->set_title(U"VRChat 日志与相册管理器");
    window_main->set_rect(easyvrui::rectangle_t{0u, 0u, 820u, 520u});

    auto menubar_main = make_shared<easyvrui::menubar>(U"menubar_main");
    auto menuitem_file = make_shared<easyvrui::menuitem>(U"menuitem_file");
    menuitem_file->set_text(U"文件(&F)");
    auto menuitem_open_dir = make_shared<easyvrui::menuitem>(U"menuitem_open_dir");
    menuitem_open_dir->set_text(U"选择照片...");
    menuitem_open_dir->set_shortcut(U"Ctrl+O");
    menuitem_file->get_control_list().add(menuitem_open_dir);
    menubar_main->get_control_list().add(menuitem_file);

    auto tabcontrol_main = make_shared<easyvrui::tabcontrol>(U"tabcontrol_main");
    tabcontrol_main->set_rect(easyvrui::rectangle_t{16u, 86u, 788u, 418u});

    auto tabpage_logs = make_shared<easyvrui::tabpage>(U"tabpage_logs");
    tabpage_logs->set_text(U"房间进出日志");

    auto listview_logs = make_shared<easyvrui::listview>(U"listview_logs");
    listview_logs->set_rect(easyvrui::rectangle_t{12u, 60u, 744u, 296u});
    listview_logs->get_column_list().add(make_shared<easyvrui::listview_column>(U"时间", 140u));
    listview_logs->get_column_list().add(make_shared<easyvrui::listview_column>(U"动作", 110u));
    listview_logs->get_column_list().add(make_shared<easyvrui::listview_column>(U"玩家昵称", 470u));
    tabpage_logs->get_control_list().add(listview_logs);

    auto tabpage_gallery = make_shared<easyvrui::tabpage>(U"tabpage_gallery");
    tabpage_gallery->set_text(U"VRChat相册");

    auto treeview_months = make_shared<easyvrui::treeview>(U"treeview_months");
    treeview_months->set_rect(easyvrui::rectangle_t{12u, 16u, 230u, 340u});

    auto image_photo = make_shared<easyvrui::image>(U"image_photo");
    image_photo->set_rect(easyvrui::rectangle_t{254u, 16u, 502u, 296u});
    image_photo->set_stretch_mode(easyvrui::image_stretch_mode_t::contain);

    auto label_photo_note = make_shared<easyvrui::label>(U"label_photo_note");
    label_photo_note->set_rect(easyvrui::rectangle_t{254u, 322u, 502u, 32u});
    label_photo_note->set_text(U"通过 文件 -> 选择照片 加载图片");

    tabpage_gallery->get_control_list().add(treeview_months);
    tabpage_gallery->get_control_list().add(image_photo);
    tabpage_gallery->get_control_list().add(label_photo_note);

    tabcontrol_main->get_page_list().add(tabpage_logs);
    tabcontrol_main->get_page_list().add(tabpage_gallery);

    menuitem_open_dir->on_click += [window_main, image_photo, label_photo_note](easyvrui::control_base &, easyvrui::event_args_t &)
    {
        auto paths = easyvrui::file_open_dialog(U"选择图片", {}, U"", {{U"PNG图片", {U"*.png", U"*.jpg"}}}, 0u, false, U"", window_main.get());

        if(!paths.empty())
        {
            image_photo->set_source(drawing_image::load_file(paths[0u].u32string()));
            label_photo_note->set_text(U"正在预览：" + paths[0u].filename().u32string());
        }
    };

    auto filter = make_shared<easyvrui::combobox>(U"combobox_filter");
    filter->set_rect(easyvrui::rectangle_t{12u, 12u, 220u, 38u});
    filter->set_dropdown_style(easyvrui::combobox_dropdown_style_t::dropdown_list);
    filter->get_item_list().assign({U"全部事件", U"仅加入", U"仅离开"});
    filter->set_selected_index(0);
    tabpage_logs->get_control_list().add(filter);

    auto log_data = make_shared<vector<log_row_t>>();
    auto refresh_log = [listview_logs, observer = weak_ptr<easyvrui::combobox>(filter), log_data]()
    {
        auto filter = observer.lock();
        if(!filter)
        {
            return;
        }

        vector<shared_ptr<easyvrui::listview_item>> items;
        auto mode = filter->get_selected_index();
        for(const auto &row : *log_data)
        {
            if(((mode == 1) && (row[1u] != U"Joined")) || ((mode == 2) && (row[1u] != U"Left")))
            {
                continue;
            }

            items.push_back(make_shared<easyvrui::listview_item>(vector<u32string>(row.begin(), row.end())));
        }

        listview_logs->get_item_list().assign(move(items));
    };

    filter->on_selection_changed += [refresh_log](easyvrui::control_base &, easyvrui::event_args_t &)
    {
        refresh_log();
    };

    auto menuitem_export_log = make_shared<easyvrui::menuitem>(U"menuitem_export_log");
    menuitem_export_log->set_text(U"导出日志…");
    menuitem_export_log->set_shortcut(U"Ctrl+S");
    menuitem_file->get_control_list().add(menuitem_export_log);
    menuitem_export_log->on_click += [owner = weak_ptr<easyvrui::window>(window_main), log_data](easyvrui::control_base &, easyvrui::event_args_t &)
    {
        if(auto window = owner.lock())
        {
            auto path = easyvrui::file_save_dialog(U"导出日志…", {}, U"vrchat-events.tsv", {{U"TSV", {U"*.tsv"}}}, 0u, U"tsv", true, U"", window.get());
            if(path)
            {
                ofstream output(*path, ios::binary);
                wstring_convert<codecvt_utf8<char32_t>, char32_t> converter;
                for(const auto &row : *log_data)
                {
                    output << converter.to_bytes(row[0u]) << '\t' << converter.to_bytes(row[1u]) << '\t' << converter.to_bytes(row[2u]) << '\n';
                }
            }
        }
    };

    auto profile = get_profile_directory();
    if(!profile.empty())
    {
        populate_gallery(*treeview_months, profile / L"Pictures" / L"VRChat");
    }

    treeview_months->on_selection_changed += [image_photo, label_photo_note](easyvrui::control_base &, easyvrui::tree_node_event_args_t &event)
    {
        if((event.node == nullptr) || event.node->get_tag().empty())
        {
            return;
        }

        try
        {
            image_photo->set_source(drawing_image::load_file(event.node->get_tag()));
            label_photo_note->set_text(event.node->get_text());
        }
        catch(const exception &)
        {
            label_photo_note->set_text(U"无法读取所选图片");
        }
    };

    auto &list = window_main->get_control_list();
    window_main->set_menu(menubar_main);
    list.add(tabcontrol_main);

    window_main->show();

    const filesystem::path log_folder = profile.empty() ? filesystem::path{} : profile / L"AppData" / L"LocalLow" / L"VRChat" / L"VRChat";
    jthread watcher([owner = weak_ptr<easyvrui::window>(window_main), log_folder, log_data, refresh_log](stop_token stop)
    {
        filesystem::path active;
        ifstream stream;
        while(!stop.stop_requested())
        {
            auto latest = log_folder.empty() ? filesystem::path{} : find_latest_log(log_folder);
            if(latest != active)
            {
                active = latest;
                stream.close();
                stream.clear();
                if(!active.empty())
                {
                    stream.open(active, ios::binary);
                }
            }

            vector<log_row_t> added;
            if(stream.is_open())
            {
                stream.clear();
                string line;
                while(!stop.stop_requested())
                {
                    auto position = stream.tellg();
                    if(!getline(stream, line))
                    {
                        break;
                    }

                    if(stream.eof())
                    {
                        stream.clear();
                        stream.seekg(position);
                        break;
                    }

                    if(auto row = parse_log_row(line))
                    {
                        added.push_back(move(*row));
                    }
                }
            }

            if(!added.empty())
            {
                auto window = owner.lock();
                if(!window)
                {
                    return;
                }

                window->begin_invoke([log_data, refresh_log, added = move(added)]()
                {
                    log_data->insert(log_data->end(), added.begin(), added.end());
                    constexpr size_t MAXIMUM_LOG_ROW_COUNT = 100u;
                    if(log_data->size() > MAXIMUM_LOG_ROW_COUNT)
                    {
                        log_data->erase(log_data->begin(), log_data->end() - static_cast<ptrdiff_t>(MAXIMUM_LOG_ROW_COUNT));
                    }

                    refresh_log();
                });
            }

            this_thread::sleep_for(chrono::milliseconds(500));
        }
    });
    easyvrui::run(U"vrc_log_and_gallery");
    return 0;
}