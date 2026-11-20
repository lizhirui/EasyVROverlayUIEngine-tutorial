from pathlib import Path
import math
import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
WIDTH = 1760
HEIGHT = 960
BACKGROUND = "#edf2f8"
CARD = "#ffffff"
INK = "#142842"
MUTED = "#526580"
RULE = "#d5dfeb"
BLUE = "#2553a6"
TEAL = "#08786e"
ORANGE = "#9b4226"
BLUE_WASH = "#e9f0fc"
TEAL_WASH = "#e2f5f0"
ORANGE_WASH = "#f9eae4"
FONT_DIRECTORY = Path(os.environ["WINDIR"]) / "Fonts"
OUTPUT_DIRECTORY = Path(__file__).resolve().parents[1] / "docs/public/images/zh"

class diagram:
    def __init__(self, title, subtitle):
        self.image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
        self.draw = ImageDraw.Draw(self.image)
        self.text_rectangle_list = []
        self.draw.rounded_rectangle((72, 50, 82, 121), radius = 5, fill = BLUE)
        self.text((104, 48, 1688, 127), title, 51, bold = True)
        self.text((105, 129, 1688, 170), subtitle, 27, color = MUTED)

    def text(self, rectangle, message, size = 28, color = INK, bold = False, center = False):
        left, top, right, bottom = rectangle
        font = ImageFont.truetype(str(FONT_DIRECTORY / ("msyhbd.ttc" if bold else "msyh.ttc")), size)
        x0, y0, x1, y1 = self.draw.textbbox((0, 0), message, font = font)
        width = x1 - x0
        height = y1 - y0
        assert (width + 4) <= (right - left), (message, rectangle, width)
        assert (height + 4) <= (bottom - top), (message, rectangle, height)
        x = (left + (((right - left) - width) // 2)) if center else (left + 2)
        y = top + (((bottom - top) - height) // 2)
        bounds = (x, y, x + width, y + height)
        assert (x >= 16) and (y >= 16) and (bounds[2] <= (WIDTH - 16)) and (bounds[3] <= (HEIGHT - 16)), (message)

        for before, box in self.text_rectangle_list:
            assert not ((bounds[0] < box[2]) and (box[0] < bounds[2]) and (bounds[1] < box[3]) and (box[1] < bounds[3])), (message, before)

        self.text_rectangle_list.append((message, bounds))
        self.draw.text((x - x0, y - y0), message, font = font, fill = color)

    def panel(self, rectangle, title):
        left, top, right, bottom = rectangle
        self.draw.rounded_rectangle(rectangle, radius = 26, fill = CARD, outline = RULE, width = 2)
        self.text((left + 30, top + 24, right - 30, top + 84), title, 33, bold = True)
        self.draw.line((left + 30, top + 99, right - 30, top + 99), fill = RULE, width = 2)

    def line(self, start, end, color = RULE, width = 3):
        self.draw.line((start, end), fill = color, width = width)

    def arrow(self, start, end, color = BLUE, width = 5):
        x0, y0 = start
        x1, y1 = end
        angle = math.atan2(y1 - y0, x1 - x0)
        self.line(start, end, color, width)
        length = 17
        self.draw.polygon((end, (x1 - (length * math.cos(angle - 0.43)), y1 - (length * math.sin(angle - 0.43))), (x1 - (length * math.cos(angle + 0.43)), y1 - (length * math.sin(angle + 0.43))),), fill = color,)

    def dot(self, center, color = BLUE, radius = 7):
        x, y = center
        self.draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill = color)

    def note(self, first, second):
        self.draw.rounded_rectangle((72, 843, 1688, 924), radius = 18, fill = "#e3eafa")
        self.text((101, 850, 1658, 885), first, 26, bold = True)
        self.text((102, 886, 1658, 916), second, 22, color = MUTED)

    def save(self, name):
        destination = OUTPUT_DIRECTORY / (name + ".png")
        self.image.save(destination, pnginfo = None, optimize = True)
        print(f"{name}.png {WIDTH}x{HEIGHT} verified_labels={len(self.text_rectangle_list)}")

def draw_coordinates():
    sheet = diagram("坐标系与窗口上的刻度", "方向轴、左上角锚点与窗面中心")
    sheet.panel((72, 198, 858, 819), "SteamVR右手跟踪坐标")
    sheet.panel((902, 198, 1688, 819), "窗口逻辑像素")
    origin = (391, 520)
    sheet.arrow(origin, (715, 520), BLUE)
    sheet.arrow(origin, (391, 337), TEAL)
    sheet.arrow(origin, (244, 648), ORANGE)
    sheet.arrow(origin, (537, 393), MUTED)
    sheet.dot(origin, INK)
    sheet.text((726, 495, 826, 546), "+X向右", 25, BLUE)
    sheet.text((214, 319, 379, 371), "+Y向上", 28, TEAL)
    sheet.text((111, 654, 444, 712), "+Z朝向佩戴者", 28, ORANGE)
    sheet.text((557, 369, 820, 423), "−Z朝向前方", 28, MUTED)
    sheet.text((211, 747, 737, 791), "+X × +Y = +Z", 33, bold = True, center = True)
    sheet.draw.rounded_rectangle((1040, 382, 1536, 661), radius = 11, fill = BLUE_WASH, outline = "#7d9ac9", width = 3)
    sheet.arrow((1040, 382), (1601, 382), BLUE)
    sheet.arrow((1040, 382), (1040, 713), TEAL)
    sheet.line((1288, 396), (1288, 647), "#aabbd5")
    sheet.line((1054, 522), (1522, 522), "#aabbd5")
    sheet.dot((1040, 382), INK)
    sheet.dot((1288, 522), TEAL)
    sheet.dot((1133, 444), ORANGE)
    sheet.text((1009, 318, 1290, 365), "左上角锚点 A", 27, bold = True)
    sheet.text((1437, 324, 1656, 367), "left向右", 25, BLUE)
    sheet.text((938, 718, 1157, 763), "top向下", 25, TEAL)
    sheet.line((1147, 444), (1304, 444), ORANGE, 2)
    sheet.text((1315, 418, 1524, 469), "P = (120, 80)", 25, ORANGE)
    sheet.text((1307, 529, 1518, 576), "窗面中心 C", 25, TEAL)
    sheet.text((1184, 716, 1649, 767), "示例宽高 640×360", 27, color = MUTED)
    sheet.note("逻辑像素到米   m = physical_scale / 1000", "左上角系中的点为 (m·left, −m·top, 0)，负号来自竖直正方向相反。",)
    sheet.save("advanced_coord_systems")

def draw_gimbal():
    sheet = diagram("万向节锁与轴角四元数", "同一姿态可以有多组欧拉角，连续旋转可以直接用轴角计算")
    sheet.panel((72, 198, 858, 819), "欧拉角 Rz·Ry·Rx")
    sheet.panel((902, 198, 1688, 819), "单位四元数的轴角表示")
    sheet.text((106, 328, 454, 385), "初始 β = γ = 0°", 27, bold = True, center = True)
    sheet.text((470, 328, 824, 385), "中间角 β = 90°", 27, bold = True, center = True)
    sheet.line((465, 326), (465, 695))
    sheet.arrow((241, 555), (241, 421), BLUE)
    sheet.arrow((241, 555), (394, 555), TEAL)
    sheet.dot((241, 555), INK)
    sheet.text((145, 423, 225, 472), "+Z", 25, BLUE)
    sheet.text((346, 570, 440, 614), "+X", 25, TEAL)
    sheet.text((116, 650, 433, 696), "转轴相互独立", 25, center = True)
    sheet.arrow((627, 538), (627, 414), BLUE)
    sheet.arrow((627, 538), (627, 661), TEAL)
    sheet.dot((627, 538), INK)
    sheet.text((645, 414, 811, 465), "γ轴 +Z", 25, BLUE)
    sheet.text((646, 608, 811, 657), "α轴 −Z", 25, TEAL)
    sheet.text((486, 681, 829, 729), "沿同一根直线", 25, center = True)
    sheet.text((112, 746, 824, 795), "β = 90°时，姿态只依赖 α − γ", 27, bold = True, center = True)
    sheet.text((958, 328, 1633, 381), "标量在前的数学记号", 26, MUTED, center = True)
    sheet.text((955, 394, 1638, 458), "q = (cos(θ/2), û·sin(θ/2))", 35, BLUE, bold = True, center = True)
    sheet.arrow((1124, 710), (1516, 710), BLUE, 5)
    sheet.arrow((1124, 710), (1349, 550), TEAL, 5)
    sheet.dot((1124, 710), INK)
    sheet.draw.arc((925, 511, 1323, 909), start = 326, end = 359, fill = ORANGE, width = 5)
    sheet.text((1361, 538, 1619, 594), "旋转后的向量", 26, TEAL)
    sheet.text((1401, 716, 1642, 766), "原向量", 26, BLUE)
    sheet.text((1335, 628, 1432, 679), "θ", 27, ORANGE)
    sheet.text((990, 772, 1619, 813), "向量在垂直于单位轴的平面内转 θ", 25, center = True)
    sheet.note("代码字段顺序   quat_t{x, y, z, w}", "半角在乘积里出现两次，q · (0, p) · q^(-1)得到实际转角。")
    sheet.save("advanced_gimbal_lock_quaternion")

def draw_cylinder():
    sheet = diagram("柱面窗口与激光反投影", "横截面在窗面中心坐标系中表示，竖直轴 Y 垂直于图面")
    sheet.panel((72, 198, 1085, 819), "在 XZ 截面中求交")
    sheet.panel((1129, 198, 1688, 819), "弯曲与反算")
    center = (559, 399)
    origin = (559, 718)
    radius = origin[1] - center[1]

    def curve(angle):
        return (origin[0] + (radius * math.sin(angle)), origin[1] - (radius * (1.0 - math.cos(angle))))

    sheet.arrow(origin, (933, 718), MUTED, 3)
    sheet.arrow(origin, (559, 334), MUTED, 3)
    outline = [curve((index - 40) * 0.022) for index in range(81)]
    sheet.draw.line(outline, fill = BLUE, width = 8)
    hit = curve(0.46)
    sheet.line(center, hit, "#98735e", 3)
    sheet.dot(center, ORANGE)
    sheet.dot(origin, BLUE)
    ray = (hit[0], 464)
    sheet.arrow(ray, hit, TEAL, 5)
    sheet.dot(ray, TEAL)
    sheet.dot(hit, ORANGE, 9)
    sheet.text((380, 352, 538, 398), "圆心", 28, ORANGE)
    sheet.text((578, 310, 682, 359), "+Z", 24, MUTED)
    sheet.text((944, 691, 1058, 740), "+X", 24, MUTED)
    sheet.text((390, 738, 647, 787), "窗面中心", 27, BLUE)
    sheet.text((723, 439, 1034, 488), "射线起点 o", 27, TEAL)
    sheet.line((709, 685), (791, 685), ORANGE, 2)
    sheet.line((791, 685), (822, 652), ORANGE, 2)
    sheet.text((824, 620, 1059, 667), "最近有效交点", 27, ORANGE)
    sheet.text((224, 471, 463, 522), "半径 R", 30, color = MUTED)
    sheet.text((152, 583, 360, 629), "窗口弧面", 27, BLUE)
    sheet.line((291, 630), (353, 667), BLUE)
    sheet.text((1164, 341, 1650, 394), "R = 1 / κ", 33, BLUE, bold = True)
    sheet.text((1164, 421, 1650, 476), "Θ = κ·W", 33, BLUE, bold = True)
    sheet.text((1164, 499, 1650, 551), "交点要在窗口弧段内", 26, color = MUTED)
    sheet.text((1164, 569, 1650, 621), "弧角 φ 决定横向弧长", 26, color = MUTED)
    sheet.text((1164, 650, 1650, 708), "u = φ / κ", 32, TEAL, bold = True)
    sheet.text((1164, 733, 1650, 788), "left = (u/W + 1/2)·w", 28, TEAL)
    sheet.note("柱面截面   x² + (z − R)² = R²", "先把世界射线变到窗面中心系，求根后再把弧长和高度换回逻辑像素。")
    sheet.save("advanced_cylinder_raycast")

def draw_render_pipeline():
    sheet = diagram("从控件到画面的渲染管线", "SDK的请求确认、Engine的栅格化和SteamVR的呈现是三个时间点")
    panel_list = (((72, 198, 560, 807), "SDK", BLUE, BLUE_WASH, (("控件与窗口版本", "事件使对象和父链失效"), ("记录绘图节点", "节点 ID 标识控件与段"), ("提交 present 差量", "等待响应后更新比较基准"),),), ((636, 198, 1124, 807), "Engine", TEAL, TEAL_WASH, (("校验并合并节点", "按 order 淘汰旧节点"), ("离屏绘制或复用", "Direct2D / DirectWrite"), ("D3D11 纹理", "成功重绘后更新代数"),),), ((1200, 198, 1688, 807), "SteamVR", ORANGE, ORANGE_WASH, (("接收 Overlay 纹理", "空间位姿 / 大小 / 曲率"), ("复用静态表面", "跟踪与合成仍按帧更新"), ("显示于头显", "叠加窗口与激光"),),),)

    for rectangle, title, color, wash, entry_list in panel_list:
        left, _, right, _ = rectangle
        sheet.panel(rectangle, title)

        for index, (heading, detail) in enumerate(entry_list):
            top = 325 + (index * 154)
            sheet.draw.rounded_rectangle((left + 26, top, right - 26, top + 121), radius = 16, fill = wash)
            sheet.text((left + 47, top + 15, right - 47, top + 59), heading, 28, color, True)
            sheet.text((left + 47, top + 63, right - 47, top + 107), detail, 23, MUTED)

            if index < 2:
                center = (left + right) // 2
                sheet.arrow((center, top + 126), (center, top + 149), color, 3)

    sheet.line((545, 691), (593, 691), BLUE, 4)
    sheet.line((593, 691), (593, 382), BLUE, 4)
    sheet.arrow((593, 382), (628, 382), BLUE, 4)
    sheet.line((1108, 691), (1156, 691), TEAL, 4)
    sheet.line((1156, 691), (1156, 382), TEAL, 4)
    sheet.arrow((1156, 382), (1191, 382), TEAL, 4)
    sheet.note("协议拒绝 → 批次隔离     图形绘制错误 → render_error", "节点差量减少传输和资源构造。窗面产生新图像时仍按完整顺序回放有效节点。",)
    sheet.save("advanced_render_pipeline")

def draw_drain_state():
    sheet = diagram("输入切换的串行排空", "保持旧输入的去向，等待上游与下游明确完成，再启用新路径")
    data = (("1  冻结旧路线", "保存旧窗口与组件", "新输入在队列等待", "合成旧键释放", BLUE, BLUE_WASH), ("2  等待旧layout", "发送 input_drain", "旧键送入旧IME", "收到该连接确认", TEAL, TEAL_WASH), ("3  等待旧IME", "发送 input_drain", "尾部文本只送旧窗", "任务与待发计数归零", ORANGE, ORANGE_WASH), ("4  提交变更", "改变窗口或模式", "发布新路由状态", "恢复队列处理", BLUE, BLUE_WASH),)

    for index, (title, first, second, third, color, wash) in enumerate(data):
        left = 72 + (index * 411)
        right = left + 383
        sheet.panel((left, 198, right, 712), title)
        sheet.draw.rounded_rectangle((left + 23, 324, right - 23, 665), radius = 19, fill = wash)
        sheet.text((left + 28, 349, right - 28, 408), first, 24, color, True, True)
        sheet.line((left + 39, 440), (right - 39, 440), RULE, 2)
        sheet.text((left + 28, 452, right - 28, 516), second, 24, MUTED, False, True)
        sheet.line((left + 39, 550), (right - 39, 550), RULE, 2)
        sheet.text((left + 28, 562, right - 28, 629), third, 24, MUTED, False, True)

        if index < 3:
            sheet.arrow((right + 4, 465), (right + 24, 465), color, 3)

    sheet.draw.rounded_rectangle((72, 742, 1688, 817), radius = 18, fill = CARD, outline = RULE, width = 2)
    sheet.text((101, 753, 1658, 806), "组件不在旧路由中时跳过相应阶段，当前阶段超时或断线时吊销资格并继续。", 26, color = MUTED,)
    sheet.note("确认匹配   正在排空 + 发送会话等于当前等待会话", "旧窗口失效时仍可清理旧路径，尾部正文不会改投给新窗口。",)
    sheet.save("advanced_input_drain_fsm")

def draw_flow_panel(sheet, rectangle, title, color, wash, entry_list, arrow_index_set = (0, 1)):
    left, _, right, _ = rectangle
    sheet.panel(rectangle, title)

    for index, (heading, detail) in enumerate(entry_list):
        top = 328 + (index * 151)
        sheet.draw.rounded_rectangle((left + 22, top, right - 22, top + 112), radius = 16, fill = wash)
        sheet.text((left + 34, top + 12, right - 34, top + 53), heading, 27, color, True, True)
        sheet.text((left + 34, top + 57, right - 34, top + 100), detail, 22, MUTED, False, True)

        if index in arrow_index_set:
            center = (left + right) // 2
            sheet.arrow((center, top + 118), (center, top + 145), color, 4)

def draw_architecture():
    sheet = diagram("应用、接入层、原生SDK与Engine", "前三层同在应用进程，服务进程统一处理窗面、空间输入与图形资源")
    sheet.draw.rounded_rectangle((72, 204, 1266, 807), radius = 25, fill = BLUE_WASH)
    sheet.draw.rounded_rectangle((1312, 204, 1688, 807), radius = 25, fill = TEAL_WASH)
    sheet.text((100, 216, 1240, 268), "应用进程   C++或Python程序", 30, BLUE, True)
    sheet.text((1333, 216, 1666, 268), "独立服务进程", 30, TEAL, True)
    entry_list = (("独立应用", BLUE, BLUE_WASH, (("业务对象", "数字与处理函数"), ("窗口与控件", "Desktop / 设计器"), ("输入组件", "layout / IME"),),), ("语言接入层", BLUE, BLUE_WASH, (("C++公开头", "链接静态库或DLL"), ("Python包", "调用原生编译扩展"), ("语言适配", "属性 / 集合 / 回调"),),), ("engine_interface", ORANGE, ORANGE_WASH, (("原生控件树", "布局与本地焦点"), ("UI运行时", "记录节点并提交"), ("客户端连接", "发现、请求与事件"),),), ("Engine", TEAL, TEAL_WASH, (("会话与窗面", "验证归属与可用性"), ("空间输入", "拾取、捕获与路由"), ("D3D与OpenVR", "绘制纹理并送头显"),),),)
    left_list = (91, 488, 885, 1325)

    for left, (title, color, wash, cell_list) in zip(left_list, entry_list):
        right = left + 350
        sheet.panel((left, 276, right, 785), title)

        for index, (heading, detail) in enumerate(cell_list):
            top = 397 + (index * 119)
            sheet.draw.rounded_rectangle((left + 17, top, right - 17, top + 102), radius = 14, fill = wash)
            sheet.text((left + 27, top + 7, right - 27, top + 48), heading, 26, color, True, True)
            sheet.text((left + 27, top + 49, right - 27, top + 92), detail, 22, MUTED, False, True)

    sheet.arrow((445, 566), (482, 566), BLUE)
    sheet.arrow((841, 566), (879, 566), BLUE)
    sheet.arrow((1243, 548), (1318, 548), ORANGE)
    sheet.arrow((1318, 581), (1243, 581), TEAL)
    sheet.note("跨进程边界   TCP/TLS传递请求、响应与事件", "应用拥有控件与回调，Engine拥有窗面、GPU纹理和Overlay。")
    sheet.save("advanced_architecture_layers")

def draw_sdk_lifecycle():
    sheet = diagram("原生SDK绑定与对象寿命", "属性与集合直接进入原生对象，事件回调按拥有者线程的顺序执行")
    draw_flow_panel(sheet, (72, 198, 560, 810), "语言入口", BLUE, BLUE_WASH, (("C++接口", "公开头与配套二进制"), ("Python接口", "属性与语言原生容器"), ("pybind11桥接", "进入回调时获取GIL"),), arrow_index_set = (1,),)
    draw_flow_panel(sheet, (636, 198, 1124, 810), "原生运行时", TEAL, TEAL_WASH, (("登记对象", "ID索引可使用非拥有入口"), ("显示窗口", "共享窗口在活动期持有"), ("关闭窗面", "调用者仍可保有对象"),),)
    draw_flow_panel(sheet, (1200, 198, 1688, 810), "强类型事件", ORANGE, ORANGE_WASH, (("事件信号", "复制回调名单并顺序执行"), ("发送者与载荷", "基类统一，字段按事件定义"), ("返回本次决定", "回写 cancel 或 handled"),),)
    sheet.line((566, 384), (597, 384), BLUE, 3)
    sheet.line((597, 384), (597, 686), BLUE, 3)
    sheet.line((566, 686), (597, 686), BLUE, 3)
    sheet.arrow((597, 535), (629, 535), BLUE, 3)
    sheet.arrow((1130, 535), (1193, 535), ORANGE)
    sheet.note("跨线程入口   投递回调后由界面所属线程执行", "设计器生成构造代码。业务实例持有生成窗体并绑定其公开控件。",)
    sheet.save("advanced_sdk_binding_lifecycle")

def draw_tls_queues():
    sheet = diagram("TCP/TLS连接与消息队列", "后台读取负责分流，界面线程只在明确的入口消费工作")
    draw_flow_panel(sheet, (72, 198, 560, 810), "1  建立连接", BLUE, BLUE_WASH, (("取得服务描述", "本机管道或远程参数"), ("确认TLS公钥", "比对DER公钥信息指纹"), ("四步应用鉴权", "挑战证明换取会话令牌"),),)
    draw_flow_panel(sheet, (636, 198, 1124, 810), "2  后台reader分流", TEAL, TEAL_WASH, (("同步响应槽", "响应必须匹配正等待的ID"), ("异步响应队列", "按接收序号排列"), ("服务事件队列", "使用同一接收序号源"),), arrow_index_set = (),)
    draw_flow_panel(sheet, (1200, 198, 1688, 810), "3  UI所属线程消费", ORANGE, ORANGE_WASH, (("request()", "只等自身响应或失败"), ("pump_message_list()", "按两队列的队首序号合并"), ("运行本地投递回调", "处理本轮截止值以前的工作"),), arrow_index_set = (1,),)
    sheet.arrow((566, 535), (629, 535), BLUE)
    sheet.arrow((1130, 384), (1193, 384), TEAL)
    sheet.line((1130, 686), (1161, 686), TEAL, 3)
    sheet.line((1161, 686), (1161, 535), TEAL, 3)
    sheet.line((1130, 535), (1161, 535), TEAL, 3)
    sheet.arrow((1161, 535), (1193, 535), TEAL, 3)
    sheet.note("收包保序   先处理旧IME最后一次文本提交，再处理关闭完成", "同步请求只等回包。普通与模态循环都通过消息泵执行事件。",)
    sheet.save("advanced_tls_ipc_queues")

def draw_session_modal():
    sheet = diagram("会话归属与同线程模态循环", "Engine维护窗面和当前窗口，SDK在应用线程上处理控件事件")
    draw_flow_panel(sheet, (72, 198, 560, 810), "Engine", BLUE, BLUE_WASH, (("已鉴权连接", "会话ID与会话令牌"), ("所属窗面", "局部窗口号映射到全局表面"), ("当前应用窗口", "决定键盘送往哪个会话"),),)
    draw_flow_panel(sheet, (636, 198, 1124, 810), "SDK调用栈", TEAL, TEAL_WASH, (("主窗事件", "进入确认窗A，阻塞主窗"), ("A的事件", "进入确认窗B，阻塞A"), ("B的事件", "设置结果并结束B的循环"),),)
    draw_flow_panel(sheet, (1200, 198, 1688, 810), "逐层返回", ORANGE, ORANGE_WASH, (("B返回结果", "恢复A的交互资格"), ("A返回结果", "恢复主窗的交互资格"), ("主窗回调继续", "原调用栈继续运行"),),)
    sheet.arrow((566, 535), (629, 535), BLUE)
    sheet.line((1130, 686), (1161, 686), TEAL, 4)
    sheet.line((1161, 686), (1161, 384), TEAL, 4)
    sheet.arrow((1161, 384), (1193, 384), TEAL, 4)
    sheet.note("直接owner阻塞   各层共用一套UI队列与窗体状态", "同步RPC静候对应响应，模态调用主动泵消息。渲染提交期间禁止进入模态。",)
    sheet.save("advanced_session_modal_loop")

def draw_advanced_architecture_batch():
    draw_architecture()
    draw_sdk_lifecycle()
    draw_tls_queues()
    draw_session_modal()

def run():
    draw_coordinates()
    draw_gimbal()
    draw_cylinder()
    draw_render_pipeline()
    draw_drain_state()
    draw_advanced_architecture_batch()

if __name__ == "__main__":
    run()