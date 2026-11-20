#include <winsock2.h>
#include <ws2tcpip.h>
#include <easyvrui.h>
#include <chrono>
#include <cstdint>
#include <memory>
#include <string>
#include <thread>
#include <vector>

using namespace std;

static string utf32_to_utf8(const u32string &text)
{
    string out;

    for(char32_t cp : text)
    {
        if(cp <= 0x7Fu)
        {
            out.push_back(static_cast<char>(cp));
        }
        else if(cp <= 0x7FFu)
        {
            out.push_back(static_cast<char>(0xC0u | (cp >> 6u)));
            out.push_back(static_cast<char>(0x80u | (cp & 0x3Fu)));
        }
        else if(cp <= 0xFFFFu)
        {
            out.push_back(static_cast<char>(0xE0u | (cp >> 12u)));
            out.push_back(static_cast<char>(0x80u | ((cp >> 6u) & 0x3Fu)));
            out.push_back(static_cast<char>(0x80u | (cp & 0x3Fu)));
        }
        else
        {
            out.push_back(static_cast<char>(0xF0u | (cp >> 18u)));
            out.push_back(static_cast<char>(0x80u | ((cp >> 12u) & 0x3Fu)));
            out.push_back(static_cast<char>(0x80u | ((cp >> 6u) & 0x3Fu)));
            out.push_back(static_cast<char>(0x80u | (cp & 0x3Fu)));
        }
    }

    return out;
}

static void append_osc_string(vector<uint8_t> &buffer, const string &text)
{
    buffer.insert(buffer.end(), text.begin(), text.end());
    buffer.push_back(0u);

    while((buffer.size() % 4u) != 0u)
    {
        buffer.push_back(0u);
    }
}

static bool send_vrc_chatbox(const u32string &text)
{
    vector<uint8_t> packet;
    append_osc_string(packet, "/chatbox/input");
    append_osc_string(packet, ",sTT");
    append_osc_string(packet, utf32_to_utf8(text));
    SOCKET sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);

    if(sock != INVALID_SOCKET)
    {
        sockaddr_in addr{};
        addr.sin_family = AF_INET;
        addr.sin_port = htons(9000u);
        inet_pton(AF_INET, "127.0.0.1", &addr.sin_addr);
        auto size = static_cast<int32_t>(packet.size());
        auto sent = sendto(sock, reinterpret_cast<const char *>(packet.data()), size, 0, reinterpret_cast<const sockaddr *>(&addr), static_cast<int32_t>(sizeof(addr)));
        closesocket(sock);
        return sent == size;
    }

    return false;
}

int main()
{
    WSADATA wsa{};
    WSAStartup(MAKEWORD(2, 2), &wsa);
    auto window_main = make_shared<easyvrui::window>(U"vrc_chatbox_window");
    window_main->set_title(U"VRChat 快捷聊天框 (OSC)");
    window_main->set_rect(easyvrui::rectangle_t{0u, 0u, 720u, 440u});
    auto listbox_phrases = make_shared<easyvrui::listbox>(U"listbox_phrases");
    listbox_phrases->set_rect(easyvrui::rectangle_t{20u, 64u, 240u, 310u});
    listbox_phrases->get_item_list().assign({U"你好呀！我是静音玩家~", U"我去喝口水马上回来 (AFK)", U"请问这首BGM叫什么名字？", U"大家晚安，下次再一起玩！", U"(｡･ω･｡)ﾉ♡ 贴贴！"});
    listbox_phrases->set_tooltip_text(U"点选常用短语快速填入输入框");
    auto textbox_chat = make_shared<easyvrui::textbox>(U"textbox_chat");
    textbox_chat->set_rect(easyvrui::rectangle_t{278u, 64u, 422u, 140u});
    textbox_chat->set_multiline(true);
    textbox_chat->set_max_length(144u);
    textbox_chat->set_vertical_scrollbar_visible(true);
    textbox_chat->set_tooltip_text(U"支持中文拼音/日语/英文输入，按Enter发送");
    auto progressbar_length = make_shared<easyvrui::progressbar>(U"progressbar_length");
    progressbar_length->set_rect(easyvrui::rectangle_t{278u, 214u, 422u, 22u});
    progressbar_length->set_minimum(0);
    progressbar_length->set_maximum(144);
    auto checkbox_live_osc = make_shared<easyvrui::checkbox>(U"checkbox_live_osc");
    checkbox_live_osc->set_rect(easyvrui::rectangle_t{278u, 248u, 250u, 36u});
    checkbox_live_osc->set_text(U"启用实时OSC (127.0.0.1:9000)");
    auto button_send = make_shared<easyvrui::button>(U"button_send");
    button_send->set_rect(easyvrui::rectangle_t{540u, 248u, 160u, 42u});
    button_send->set_text(U"发送 Chatbox");
    button_send->set_tooltip_text(U"发送到VRChat头顶聊天气泡");
    auto button_clear = make_shared<easyvrui::button>(U"button_clear");
    button_clear->set_rect(easyvrui::rectangle_t{278u, 300u, 160u, 40u});
    button_clear->set_text(U"清空气泡");
    auto label_status = make_shared<easyvrui::label>(U"label_status");
    label_status->set_rect(easyvrui::rectangle_t{20u, 390u, 680u, 32u});
    label_status->set_text(U"状态：离线模拟模式（勾选实时OSC即可连接VRChat）");
    auto submission_id = make_shared<uint64_t>(0u);

    auto dispatch_chatbox = [checkbox_live_osc, label_status, submission_id](const u32string &text)
    {
        (*submission_id)++;
        uint64_t submission = *submission_id;

        if(checkbox_live_osc->get_checked())
        {
            if(!send_vrc_chatbox(text))
            {
                label_status->set_text(U"OSC提交失败 · 草稿已保留");
                return false;
            }

            label_status->set_text(text.empty() ? U"已提交清空指令" : U"OSC数据报已提交");
        }
        else
        {
            label_status->set_text(text.empty() ? U"已模拟提交清空指令" : U"模拟消息已提交");
        }

        thread([label_status, submission_id, submission]()
        {
            this_thread::sleep_for(chrono::seconds(3));

            label_status->begin_invoke([label_status, submission_id, submission]()
            {
                if(!label_status->get_disposed() && ((*submission_id) == submission))
                {
                    label_status->set_text(U"状态：等待下一条消息...");
                }
            });
        })

        .detach();
        return true;
    };

    listbox_phrases->on_selection_changed += [listbox_phrases, textbox_chat](easyvrui::control_base &, easyvrui::event_args_t &)
    {
        if(listbox_phrases->get_selected_index() >= 0)
        {
            textbox_chat->set_text(listbox_phrases->get_selected_item());
            textbox_chat->focus();
        }
    };

    textbox_chat->on_text_changed += [textbox_chat, progressbar_length](easyvrui::control_base &, easyvrui::event_args_t &)
    {
        progressbar_length->set_value(static_cast<int64_t>(textbox_chat->get_text().size()));
    };

    textbox_chat->on_key_down += [textbox_chat, dispatch_chatbox](easyvrui::control_base &, easyvrui::key_event_args_t &event)
    {
        if(easyvrui::parse_keyboard_key(event.key) == easyvrui::keyboard_key_t::enter)
        {
            auto msg = textbox_chat->get_text();

            if(!msg.empty() && dispatch_chatbox(msg))
            {
                textbox_chat->set_text(U"");
            }

            event.handled = true;
        }
    };

    button_send->on_click += [textbox_chat, dispatch_chatbox](easyvrui::control_base &, easyvrui::event_args_t &)
    {
        auto msg = textbox_chat->get_text();

        if(!msg.empty() && dispatch_chatbox(msg))
        {
            textbox_chat->set_text(U"");
        }
    };

    button_clear->on_click += [dispatch_chatbox](easyvrui::control_base &, easyvrui::event_args_t &)
    {
        dispatch_chatbox(U"");
    };

    window_main->on_closing += [window_main, checkbox_live_osc](easyvrui::control_base &, easyvrui::cancel_event_args_t &event)
    {
        if(checkbox_live_osc->get_checked())
        {
            auto answer = easyvrui::messagebox(U"当前处于实时OSC模式，确定退出聊天框吗？", U"确认退出", easyvrui::messagebox_button_set_t::yes_no, easyvrui::messagebox_icon_t::question, easyvrui::dialog_result_t::no, window_main.get());

            if(answer != easyvrui::dialog_result_t::yes)
            {
                event.cancel = true;
            }
        }
    };

    auto &list = window_main->get_control_list();
    list.add(listbox_phrases);
    list.add(textbox_chat);
    list.add(progressbar_length);
    list.add(checkbox_live_osc);
    list.add(button_send);
    list.add(button_clear);
    list.add(label_status);
    window_main->show();
    easyvrui::run(U"vrc_chatbox");
    WSACleanup();
    return 0;
}