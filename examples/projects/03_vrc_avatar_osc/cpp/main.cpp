#include <winsock2.h>
#include <ws2tcpip.h>
#include <easyvrui.h>
#include <json.hpp>
#include <bit>
#include <charconv>
#include <cmath>
#include <codecvt>
#include <cstdlib>
#include <filesystem>
#include <fstream>
#include <format>
#include <locale>
#include <optional>
#include <memory>
#include <string>
#include <vector>

using namespace std;

using avatar_row_t = vector<u32string>;

string encode_utf8(const u32string &value)
{
    return wstring_convert<codecvt_utf8<char32_t>, char32_t>{}.to_bytes(value);
}

u32string decode_utf8(const string &value)
{
    return wstring_convert<codecvt_utf8<char32_t>, char32_t>{}.from_bytes(value);
}

filesystem::path get_avatar_profile()
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

vector<avatar_row_t> load_avatar_rows()
{
    auto profile = get_avatar_profile();
    if(!profile.empty())
    {
        auto root = profile / L"AppData" / L"LocalLow" / L"VRChat" / L"VRChat" / L"OSC";
        error_code error;
        for(filesystem::recursive_directory_iterator item(root, filesystem::directory_options::skip_permission_denied, error), end;!error && (item != end);item.increment(error))
        {
            if((item->path().extension() != L".json") || (item->path().parent_path().filename() != L"Avatars"))
            {
                continue;
            }

            try
            {
                ifstream input(item->path());
                auto configuration = nlohmann::json::parse(input);
                vector<avatar_row_t> rows;
                for(const auto &parameter : configuration.at("parameters"))
                {
                    if(parameter.contains("input"))
                    {
                        rows.push_back({decode_utf8(parameter.at("name").get<string>()), decode_utf8(parameter.at("input").value("type", string("Float"))), U"0"});
                    }
                }

                if(!rows.empty())
                {
                    return rows;
                }
            }
            catch(const exception &)
            {
            }
        }
    }

    return {{U"EarFlop", U"Float", U"0.5"}, {U"TailWag", U"Bool", U"1"}, {U"CoatToggle", U"Int", U"2"}};
}

void append_osc_string(vector<uint8_t> &packet, const string &text)
{
    packet.insert(packet.end(), text.begin(), text.end());
    packet.push_back(0u);
    constexpr size_t OSC_WORD_SIZE = 4u;
    while((packet.size() % OSC_WORD_SIZE) != 0u)
    {
        packet.push_back(0u);
    }
}

optional<vector<uint8_t>> encode_avatar_packet(const avatar_row_t &row, const u32string &value)
{
    string name = encode_utf8(row[0u]);
    if(name.empty() || (name.find('\0') != string::npos))
    {
        return {};
    }

    string text = encode_utf8(value);
    vector<uint8_t> packet;
    append_osc_string(packet, "/avatar/parameters/" + name);

    if(row[1u] == U"Bool")
    {
        if((text != "0") && (text != "1") && (text != "true") && (text != "false"))
        {
            return {};
        }

        append_osc_string(packet, (text == "1") || (text == "true") ? ",T" : ",F");
        return packet;
    }

    uint32_t payload = 0u;
    if(row[1u] == U"Int")
    {
        int32_t number = 0;
        auto [end, error] = from_chars(text.data(), text.data() + text.size(), number);
        if((error != errc{}) || (end != (text.data() + text.size())))
        {
            return {};
        }

        append_osc_string(packet, ",i");
        payload = static_cast<uint32_t>(number);
    }
    else
    {
        float number = 0.0f;
        auto [end, error] = from_chars(text.data(), text.data() + text.size(), number);
        if((error != errc{}) || (end != (text.data() + text.size())) || !isfinite(number))
        {
            return {};
        }

        append_osc_string(packet, ",f");
        payload = bit_cast<uint32_t>(number);
    }

    for(uint32_t shift : {24u, 16u, 8u, 0u})
    {
        packet.push_back(static_cast<uint8_t>(payload >> shift));
    }

    return packet;
}

bool send_avatar_packet(const vector<uint8_t> &packet)
{
    constexpr uint16_t VRCHAT_OSC_PORT = 9000u;
    WSADATA state{};
    if(WSAStartup(MAKEWORD(2u, 2u), &state) != 0)
    {
        return false;
    }

    SOCKET connection = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if(connection == INVALID_SOCKET)
    {
        WSACleanup();
        return false;
    }

    sockaddr_in target{};
    target.sin_family = AF_INET;
    target.sin_port = htons(VRCHAT_OSC_PORT);
    target.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    int32_t size = static_cast<int32_t>(packet.size());
    int32_t sent = sendto(connection, reinterpret_cast<const char *>(packet.data()), size, 0, reinterpret_cast<const sockaddr *>(&target), static_cast<int32_t>(sizeof(target)));
    closesocket(connection);
    WSACleanup();
    return sent == size;
}

bool save_avatar_preset(const u32string &name, const vector<avatar_row_t> &rows)
{
    auto profile = get_avatar_profile();
    if(name.empty() || profile.empty())
    {
        return false;
    }

    auto folder = profile / L"easyvrui" / L"tutorial";
    error_code error;
    filesystem::create_directories(folder, error);
    if(error)
    {
        return false;
    }

    nlohmann::json values = nlohmann::json::object();
    for(const auto &row : rows)
    {
        values[encode_utf8(row[0u])] = encode_utf8(row[2u]);
    }

    ofstream output(folder / L"avatar_presets.jsonl", ios::binary | ios::app);
    output << nlohmann::json{{"name", encode_utf8(name)}, {"values", move(values)}}.dump() << '\n';
    return output.good();
}

class preset_dialog : public easyvrui::window
{
    public:
        shared_ptr<easyvrui::textbox> textbox_name;

        preset_dialog() : easyvrui::window(U"preset_dialog")
        {
            set_title(U"新建参数预设");
            set_rect(easyvrui::rectangle_t{0u, 0u, 380u, 210u});

            auto label_name = make_shared<easyvrui::label>(U"label_name");
            label_name->set_rect(easyvrui::rectangle_t{24u, 68u, 110u, 36u});
            label_name->set_text(U"预设名称：");

            textbox_name = make_shared<easyvrui::textbox>(U"textbox_name");
            textbox_name->set_rect(easyvrui::rectangle_t{140u, 68u, 210u, 36u});
            textbox_name->set_text(U"可爱日常模式");

            auto button_ok = make_shared<easyvrui::button>(U"button_ok");
            button_ok->set_rect(easyvrui::rectangle_t{80u, 134u, 100u, 40u});
            button_ok->set_text(U"保存");
            button_ok->on_click += [this](easyvrui::control_base &, easyvrui::event_args_t &)
            {
                set_dialog_result(easyvrui::dialog_result_t::ok);
            };

            auto button_cancel = make_shared<easyvrui::button>(U"button_cancel");
            button_cancel->set_rect(easyvrui::rectangle_t{200u, 134u, 100u, 40u});
            button_cancel->set_text(U"取消");
            button_cancel->on_click += [this](easyvrui::control_base &, easyvrui::event_args_t &)
            {
                set_dialog_result(easyvrui::dialog_result_t::cancel);
            };

            auto &list = get_control_list();
            list.add(label_name);
            list.add(textbox_name);
            list.add(button_ok);
            list.add(button_cancel);
        }
};

int main()
{
    auto window_main = make_shared<easyvrui::window>(U"window_main");
    window_main->set_title(U"Avatar OSC 调试与预设面板");
    window_main->set_rect(easyvrui::rectangle_t{0u, 0u, 740u, 480u});

    auto param_rows = make_shared<vector<avatar_row_t>>(load_avatar_rows());

    auto grid_params = make_shared<easyvrui::grid>(U"grid_params");
    grid_params->set_rect(easyvrui::rectangle_t{20u, 64u, 460u, 290u});
    grid_params->set_column_list({
        easyvrui::grid_column_t{U"参数名", 200u, false},
        easyvrui::grid_column_t{U"类型", 100u, false},
        easyvrui::grid_column_t{U"当前值", 140u}
    });

    grid_params->set_data_provider(
        param_rows->size(),
        [param_rows](uint64_t r, uint64_t c) -> easyvrui::grid_value_t
        {
            return (*param_rows)[static_cast<size_t>(r)][static_cast<size_t>(c)];
        },
        [param_rows](uint64_t r, uint64_t c, const easyvrui::grid_value_t &v, u32string &) -> bool
        {
            auto &row = (*param_rows)[static_cast<size_t>(r)];
            auto value = easyvrui::grid::get_value_text(v);
            if((c != 2u) || !encode_avatar_packet(row, value))
            {
                return false;
            }

            row[2u] = move(value);
            return true;
        });

    auto button_preset = make_shared<easyvrui::button>(U"button_preset");
    button_preset->set_rect(easyvrui::rectangle_t{500u, 232u, 210u, 42u});
    button_preset->set_text(U"保存为预设...");

    auto label_status = make_shared<easyvrui::label>(U"label_status");
    label_status->set_rect(easyvrui::rectangle_t{20u, 376u, 700u, 36u});
    label_status->set_text(U"双击表格数值列，或点击保存预设");

    auto checkbox_live = make_shared<easyvrui::checkbox>(U"checkbox_live");
    checkbox_live->set_rect(easyvrui::rectangle_t{500u, 68u, 220u, 36u});
    checkbox_live->set_text(U"实时发送OSC (9000)");
    const auto publish_value = [param_rows, checkbox_live, label_status](uint64_t row)
    {
        if(row >= param_rows->size())
        {
            return;
        }

        auto &entry = (*param_rows)[static_cast<size_t>(row)];
        auto packet = encode_avatar_packet(entry, entry[2u]);
        if(checkbox_live->get_checked() && packet)
        {
            label_status->set_text(send_avatar_packet(*packet) ? (U"OSC: " + entry[0u]) : U"OSC发送失败");
        }
    };

    grid_params->on_edit_committed += [publish_value](easyvrui::control_base &, easyvrui::grid_cell_event_args_t &event)
    {
        publish_value(event.row);
    };

    auto slider_float = make_shared<easyvrui::slider>(U"slider_float");
    slider_float->set_rect(easyvrui::rectangle_t{500u, 120u, 210u, 36u});
    slider_float->set_minimum(0);
    slider_float->set_maximum(100);
    slider_float->set_value(50);
    auto numeric_step = make_shared<easyvrui::numericupdown>(U"numeric_step");
    numeric_step->set_rect(easyvrui::rectangle_t{500u, 174u, 210u, 38u});
    numeric_step->set_minimum(0.0);
    numeric_step->set_maximum(1.0);
    numeric_step->set_step(0.05);
    numeric_step->set_decimal_places(2u);
    numeric_step->set_value(0.5);

    slider_float->on_value_changed += [numeric_step](easyvrui::control_base &source, easyvrui::event_args_t &)
    {
        numeric_step->set_value(static_cast<double>(static_cast<easyvrui::slider &>(source).get_value()) / 100.0);
    };

    numeric_step->on_value_changed += [observer = weak_ptr<easyvrui::grid>(grid_params), param_rows, publish_value](easyvrui::control_base &source, easyvrui::event_args_t &)
    {
        auto grid = observer.lock();
        if(!grid || (grid->get_selected_index() < 0))
        {
            return;
        }

        auto index = static_cast<size_t>(grid->get_selected_index());
        auto &row = (*param_rows)[index];
        if(row[1u] != U"Float")
        {
            return;
        }

        auto value = static_cast<easyvrui::numericupdown &>(source).get_value();
        row[2u] = decode_utf8(format("{:.2f}", value));
        grid->refresh_data();
        publish_value(static_cast<uint64_t>(index));
    };

    auto button_theme = make_shared<easyvrui::button>(U"button_theme");
    button_theme->set_rect(easyvrui::rectangle_t{500u, 288u, 210u, 42u});
    button_theme->set_text(U"切换背景色");
    button_theme->on_click += [owner = weak_ptr<easyvrui::window>(window_main)](easyvrui::control_base &, easyvrui::event_args_t &)
    {
        if(auto window = owner.lock())
        {
            auto color = easyvrui::color_dialog(window->get_background_color(), U"选择面板背景色", 0x0d1624ffu, window.get());
            if(color)
            {
                window->set_background_color(*color);
            }
        }
    };

    button_preset->on_click += [window_main, label_status, param_rows](easyvrui::control_base &, easyvrui::event_args_t &)
    {
        auto dlg = make_shared<preset_dialog>();

        if(dlg->show_dialog(*window_main) == easyvrui::dialog_result_t::ok)
        {
            auto name = dlg->textbox_name->get_text();
            label_status->set_text(save_avatar_preset(name, *param_rows) ? (U"已保存预设：" + dlg->textbox_name->get_text()) : U"无法保存预设");
        }
    };

    auto &list = window_main->get_control_list();
    list.add(grid_params);
    list.add(button_preset);
    list.add(checkbox_live);
    list.add(slider_float);
    list.add(numeric_step);
    list.add(button_theme);
    list.add(label_status);

    window_main->show();
    easyvrui::run(U"vrc_avatar_osc");
    return 0;
}