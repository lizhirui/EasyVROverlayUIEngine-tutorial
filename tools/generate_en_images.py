from argparse import ArgumentParser
import json
from pathlib import Path
import re
import shutil
from tempfile import TemporaryDirectory
from PIL import ImageFont
import capture_ui_screenshots as capture
import generate_advanced_diagrams as advanced
import render_3d_mockups as spatial
ADVANCED_TEXT_MAP = {"坐标系与窗口上的刻度": "Coordinate systems and window units", "方向轴、左上角锚点与窗面中心": "Axes, top-left anchor, and surface center", "SteamVR右手跟踪坐标": "SteamVR right-handed tracking", "窗口逻辑像素": "Window logical pixels", "+X向右": "+X right", "+Y向上": "+Y up", "+Z朝向佩戴者": "+Z toward the user", "−Z朝向前方": "−Z forward", "左上角锚点 A": "Top-left anchor A", "left向右": "left → right", "top向下": "top → down", "窗面中心 C": "Surface center C", "示例宽高 640×360": "Example: 640 × 360", "逻辑像素到米   m = physical_scale / 1000": "Logical pixels to metres   m = physical_scale / 1000", "左上角系中的点为 (m·left, −m·top, 0)，负号来自竖直正方向相反。": "Top-left coordinates are (m·left, −m·top, 0). The Y axes point in opposite directions.", "万向节锁与轴角四元数": "Gimbal lock and axis–angle quaternions", "同一姿态可以有多组欧拉角，连续旋转可以直接用轴角计算": "Many Euler angles can represent the same pose. Axis–angle rotations compose directly.", "欧拉角 Rz·Ry·Rx": "Euler angles Rz·Ry·Rx", "单位四元数的轴角表示": "Unit quaternion as axis–angle", "初始 β = γ = 0°": "Initially β = γ = 0°", "中间角 β = 90°": "Middle angle β = 90°", "转轴相互独立": "Independent axes", "γ轴 +Z": "γ axis +Z", "α轴 −Z": "α axis −Z", "沿同一根直线": "Collinear axes", "β = 90°时，姿态只依赖 α − γ": "At β = 90°, only α − γ matters", "标量在前的数学记号": "Scalar-first notation", "旋转后的向量": "Rotated vector", "原向量": "Original vector", "向量在垂直于单位轴的平面内转 θ": "Rotate by θ in the plane normal to the axis", "代码字段顺序   quat_t{x, y, z, w}": "Code field order   quat_t{x, y, z, w}", "半角在乘积里出现两次，q · (0, p) · q^(-1)得到实际转角。": "The two half angles combine into the full angle in q · (0, p) · q^(-1).", "柱面窗口与激光反投影": "Cylindrical windows and laser projection", "横截面在窗面中心坐标系中表示，竖直轴 Y 垂直于图面": "This cross-section uses surface-centered coordinates. The vertical Y axis leaves the page.", "在 XZ 截面中求交": "Ray hit in the XZ plane", "弯曲与反算": "Curve and inverse map", "圆心": "Circle center", "窗面中心": "Surface center", "射线起点 o": "Ray origin o", "最近有效交点": "Nearest valid hit", "半径 R": "Radius R", "窗口弧面": "Window arc", "交点要在窗口弧段内": "Accept hits within the window arc", "弧角 φ 决定横向弧长": "Arc angle φ gives horizontal distance", "柱面截面   x² + (z − R)² = R²": "Cylinder cross-section   x² + (z − R)² = R²", "先把世界射线变到窗面中心系，求根后再把弧长和高度换回逻辑像素。": "Transform the ray to surface coordinates. Solve for the hit, then convert arc length and height to pixels.", "从控件到画面的渲染管线": "From controls to pixels", "SDK的请求确认、Engine的栅格化和SteamVR的呈现是三个时间点": "SDK acknowledgment, Engine rasterization, and SteamVR presentation happen at different times.", "控件与窗口版本": "Control and window versions", "事件使对象和父链失效": "Events invalidate the parent chain", "记录绘图节点": "Record draw nodes", "节点 ID 标识控件与段": "Node IDs encode control and segment", "提交 present 差量": "Submit a present delta", "等待响应后更新比较基准": "Advance the baseline on response", "校验并合并节点": "Validate and merge nodes", "按 order 淘汰旧节点": "Prune by order", "离屏绘制或复用": "Draw offscreen or reuse", "D3D11 纹理": "D3D11 texture", "成功重绘后更新代数": "Advance generation on redraw", "接收 Overlay 纹理": "Receive overlay texture", "空间位姿 / 大小 / 曲率": "Pose / size / curvature", "复用静态表面": "Reuse static surface", "跟踪与合成仍按帧更新": "Track and composite per frame", "显示于头显": "Display in the headset", "叠加窗口与激光": "Composite windows and lasers", "协议拒绝 → 批次隔离     图形绘制错误 → render_error": "Protocol rejection → isolate batch     Drawing failure → render_error", "节点差量减少传输和资源构造。窗面产生新图像时仍按完整顺序回放有效节点。": "Node deltas reduce traffic and resource creation. A redraw replays every active node in order.", "输入切换的串行排空": "Serial draining when input changes", "保持旧输入的去向，等待上游与下游明确完成，再启用新路径": "Keep the old input route until both components acknowledge their work. Then enable the new route.", "1  冻结旧路线": "1  Freeze old route", "保存旧窗口与组件": "Save window and providers", "新输入在队列等待": "Queue new input", "合成旧键释放": "Synthesize key releases", "2  等待旧layout": "2  Drain old layout", "发送 input_drain": "Send input_drain", "旧键送入旧IME": "Route keys to old IME", "收到该连接确认": "Receive its acknowledgment", "3  等待旧IME": "3  Drain old IME", "尾部文本只送旧窗": "Send final text to old window", "任务与待发计数归零": "Wait for jobs and sends", "4  提交变更": "4  Commit change", "改变窗口或模式": "Change window or mode", "发布新路由状态": "Publish routing state", "恢复队列处理": "Resume queued input", "组件不在旧路由中时跳过相应阶段，当前阶段超时或断线时吊销资格并继续。": "Skip a provider absent from the old route. On timeout or disconnect, revoke its send permission.", "确认匹配   正在排空 + 发送会话等于当前等待会话": "An acknowledgment must come from the session currently being drained.", "旧窗口失效时仍可清理旧路径，尾部正文不会改投给新窗口。": "If the old window becomes invalid, drain its route and keep any final text away from the new window.", "应用、接入层、原生SDK与Engine": "Applications, language APIs, the native SDK, and Engine", "前三层同在应用进程，服务进程统一处理窗面、空间输入与图形资源": "The first three layers run in the application. Engine owns window surfaces, spatial input, and graphics resources.", "应用进程   C++或Python程序": "Application process   C++ or Python program", "独立服务进程": "Separate service process", "独立应用": "Independent apps", "业务对象": "App logic", "数字与处理函数": "Data and handlers", "窗口与控件": "Windows and controls", "Desktop / 设计器": "Desktop / Designer", "输入组件": "Input providers", "语言接入层": "Language APIs", "C++公开头": "C++ public headers", "链接静态库或DLL": "Link a static library or DLL", "Python包": "Python package", "调用原生编译扩展": "Call the native extension", "语言适配": "Language binding", "属性 / 集合 / 回调": "Properties / containers / callbacks", "原生控件树": "Native control tree", "布局与本地焦点": "Layout and local focus", "UI运行时": "UI runtime", "记录节点并提交": "Record and submit nodes", "客户端连接": "Client connection", "发现、请求与事件": "Discovery, requests, events", "会话与窗面": "Sessions and surfaces", "验证归属与可用性": "Validate owner and state", "空间输入": "Spatial input", "拾取、捕获与路由": "Hit test, capture, route", "D3D与OpenVR": "D3D and OpenVR", "绘制纹理并送头显": "Draw textures for the headset", "跨进程边界   TCP/TLS传递请求、响应与事件": "Process boundary   TCP/TLS carries requests, responses, and events", "应用拥有控件与回调，Engine拥有窗面、GPU纹理和Overlay。": "Apps own controls and callbacks. Engine owns window surfaces, GPU textures, and overlays.", "原生SDK绑定与对象寿命": "Native SDK bindings and object lifetime", "属性与集合直接进入原生对象，事件回调按拥有者线程的顺序执行": "Language APIs access native objects. The owning UI thread runs event callbacks in order.", "语言入口": "Language interfaces", "C++接口": "C++ API", "公开头与配套二进制": "Public headers and binaries", "Python接口": "Python API", "属性与语言原生容器": "Properties and containers", "pybind11桥接": "pybind11 bridge", "进入回调时获取GIL": "Acquire the GIL for callbacks", "原生运行时": "Native runtime", "登记对象": "Register object", "ID索引可使用非拥有入口": "Non-owning ID index", "显示窗口": "Show window", "共享窗口在活动期持有": "Retain shared windows", "关闭窗面": "Close surface", "调用者仍可保有对象": "Caller may retain the object", "强类型事件": "Typed events", "事件信号": "Event signal", "复制回调名单并顺序执行": "Copy callbacks and call in order", "发送者与载荷": "Sender and event payload", "基类统一，字段按事件定义": "Common base, typed fields", "返回本次决定": "Return handler decision", "回写 cancel 或 handled": "Write back cancel or handled", "跨线程入口   投递回调后由界面所属线程执行": "Cross-thread calls   Post a callback for the owning UI thread", "设计器生成构造代码。业务实例持有生成窗体并绑定其公开控件。": "Form Designer generates construction code. The application owns the form and binds its public controls.", "TCP/TLS连接与消息队列": "TCP/TLS connection and message queues", "后台读取负责分流，界面线程只在明确的入口消费工作": "A background reader routes messages. The UI thread dispatches work at explicit pump points.", "1  建立连接": "1  Connect", "取得服务描述": "Discover service", "本机管道或远程参数": "Local pipe or remote arguments", "确认TLS公钥": "Check TLS public key", "比对DER公钥信息指纹": "Match DER public key fingerprint", "四步应用鉴权": "Four-step authentication", "挑战证明换取会话令牌": "Prove challenge, receive token", "2  后台reader分流": "2  Background reader", "同步响应槽": "Synchronous response slot", "响应必须匹配正等待的ID": "Match the waiting request ID", "异步响应队列": "Async response queue", "按接收序号排列": "Sort by receive sequence", "服务事件队列": "Server event queue", "使用同一接收序号源": "Share the receive sequence", "3  UI所属线程消费": "3  UI thread dispatch", "只等自身响应或失败": "Wait for own response or failure", "按两队列的队首序号合并": "Merge the two queue heads", "运行本地投递回调": "Run UI callbacks", "处理本轮截止值以前的工作": "Process work up to pump cutoff", "收包保序   先处理旧IME最后一次文本提交，再处理关闭完成": "Receive order   Deliver the old IME’s final text before hide completes", "同步请求只等回包。普通与模态循环都通过消息泵执行事件。": "A synchronous call waits for its own response. The application loop and modal loops both pump events.", "会话归属与同线程模态循环": "Session ownership and same-thread modal loops", "Engine维护窗面和当前窗口，SDK在应用线程上处理控件事件": "Engine owns surfaces and window selection. The SDK runs control events on the application thread.", "已鉴权连接": "Authenticated connection", "会话ID与会话令牌": "Session ID and token", "所属窗面": "Owned surfaces", "局部窗口号映射到全局表面": "Local ID maps to global surface", "当前应用窗口": "Current app window", "决定键盘送往哪个会话": "Select keyboard target session", "SDK调用栈": "SDK call stack", "主窗事件": "Main window event", "进入确认窗A，阻塞主窗": "Open A and block its owner", "A的事件": "Event in A", "进入确认窗B，阻塞A": "Open B and block A", "B的事件": "Event in B", "设置结果并结束B的循环": "Set result and stop B’s loop", "逐层返回": "Return one level at a time", "B返回结果": "B returns its result", "恢复A的交互资格": "Restore interaction in A", "A返回结果": "A returns its result", "恢复主窗的交互资格": "Restore main window interaction", "主窗回调继续": "Resume the original callback", "原调用栈继续运行": "Continue the original stack", "直接owner阻塞   各层共用一套UI队列与窗体状态": "Each modal loop blocks its direct owner and uses the same UI queues and window state.", "同步RPC静候对应响应，模态调用主动泵消息。渲染提交期间禁止进入模态。": "Sync RPC waits for a response. Modal calls pump events. Rendering and submission disallow modal waits.",}
STORY_TEXT_MAP = {"你好，VR世界！": "Hello, VR world!", "已发送：Ready for sync": "Sent: Ready for sync", "VRChat快捷聊天": "VRChat quick chat", "常用短语": "Common phrases", "大家好！": "Hello, everyone!", "我会在入口等候。": "I’ll wait at the entrance.", "请再发一次链接。": "Please resend the link.", "我稍后回来。": "I’ll be right back.", "谢谢，晚点见！": "Thanks, see you later!", "消息预览": "Message preview", "离线演示 · 等待编辑": "Offline demo · Ready to edit", "发送模拟消息": "Send test message", "清空气泡…": "Clear bubble…", "模拟数据报已提交 · 冷却期间暂停发送": "Test packet sent · Cooling down", "\\n等大家到齐后，我们按名单依次进入。\\n如果暂时无法回应，可以先在这里留言。\\n我会核对集合地点，并在下一轮确认人数。": "\\nWe’ll go in order when everyone arrives.\\nLeave a note if you can’t reply yet.\\nI’ll check the meeting point and count.", "清空当前Chatbox": "Clear current Chatbox", "确定发送清空指令吗？本地草稿可以保留。": "Send the clear command? Your local draft stays available.", "房间记录与相册": "Room logs and gallery", "房间记录": "Room logs", "相册预览": "Photo preview", "全部房间与玩家": "All rooms and players", "观景台 / Mika": "Lookout / Mika", "港口 / Ren": "Harbor / Ren", "时间": "Time", "房间": "Room", "玩家": "Player", "事件": "Event", "本地示例数据 · 已读取4条记录": "Local sample data · 4 records loaded", "观景台": "Lookout", "加入": "Joined", "港口": "Harbor", "离开": "Left", "本地示例数据 · 筛选后2条记录": "Local sample data · 2 matching records", "演示相册": "Sample gallery", "观景台日落.png": "lookout_sunset.png", "选择照片以预览": "Choose a photo to preview", "观景台日落 · 1600×900 · 合成素材": "Lookout sunset · 1600 × 900 · Generated image", "相册 · 等比预览": "Photo gallery · Aspect ratio preserved", "导出筛选后的房间记录": "Export filtered room logs", "TSV表格": "TSV table", "导出示例目录": "Export sample folder", "Avatar参数与预设": "Avatar parameters and presets", "参数名": "Parameter", "类型": "Type", "当前值": "Current value", "实时更新 · 本地演示": "Live updates · Local demo", "当前Float参数": "Current Float parameters", "自定义": "Custom", "演示预设": "Sample preset", "保存为预设…": "Save as preset…", "示例Avatar · 等待编辑": "Sample Avatar · Ready to edit", "已更新EarFlop · 演示通道": "EarFlop updated · Test channel", "保存自定义预设": "Save custom preset", "为当前参数快照输入名称": "Name the current parameter snapshot", "观景台调试预设": "Lookout test preset", "腕部HUD": "Wrist HUD", "left · 0.65倍 · 测试采样": "left · 0.65× · Test samples", "显示桌面副屏": "Show desktop preview", "桌面副屏与电平": "Desktop preview and level", "无头WARP · 桌面画面占位": "Headless WARP · Screen placeholder", "body · 曲率0.65m⁻¹": "body · Curvature 0.65 m⁻¹", "world · 曲率0.00m⁻¹ · 平面": "world · Curvature 0.00 m⁻¹ · Flat", "远程会话配置": "Remote session setup", "Engine地址与端口": "Engine address and port", "凭据与证书指纹 · 使用测试配置": "Credential and certificate fingerprint · Test configuration", "验证配置": "Validate setup", "等待验证 · 本地状态演示": "Waiting for validation · Local demo", "测试状态：会话已连接": "Test status: session connected", "颜文字测试面板": "Kaomoji test panel", "问候": "Greetings", "回应": "Replies", "最近使用 · 暂无": "Recent · Empty", "测试提交 · 最近使用：": "Test input · Recent: ", "我的第一个VR窗口": "My First VR Window", "点一下下面的按钮试试看！": "Click the button below to try it!", "点我打招呼": "Say hello", "已发送：": "Sent: ", "输入想说的话：": "Enter a message:", "发送": "Send", "把文本框里的内容发出去": "Send the text in the textbox", "静音快捷喊话条": "Quiet Quick-Message Bar",}
OUTPUT = capture.OUTPUT / "en"
WORKSPACE = capture.WORKSPACE
ENGLISH_BUILD = capture.WORK / "capture_en"
HAN = re.compile(r"[\u3400-\u9fff]")
STRING_LITERAL = re.compile(r'"((?:\\.|[^"\\\n])*)"')
WIDE_LITERAL = re.compile(r'std::u32string\{U"((?:\\.|[^"\\\n])*)", std::size_t\{\d+u\}\}')
ESCAPE = re.compile(r"\\(?:U([0-9A-Fa-f]{8})|u([0-9A-Fa-f]{4}))")
CAPTURE_ROLE_LIST = ("desktop", "designer", "file_manager", "task_manager", "demo", "keyboard", "dialog", "ime",)
STORY_SOURCE_LIST = ("tools/capture_project_story.cpp", "examples/basics/03_first_window/cpp/main.cpp", "examples/basics/04_form_designer/cpp/main.cpp", "examples/basics/04_form_designer/cpp/quick_shout_window.cpp",)
DESIGNER_SOURCE = "tools/capture_ui.cpp"
GUIDE_TEXT_MAP = {"默认标题栏": "Default title bar", "自定义标题颜色和字体": "Custom Title Color and Font", "隐藏标准关闭入口": "Hide Standard Close Entrance", "隐藏标题栏": "Hide Title Bar", "默认": "Default", "工作区连接": "Connect workspace", "前景色与背景色": "Text and fill", "提交设置": "Apply settings", "字体与颜色": "Font and Color", "工作区备注": "Workspace Notes", "第一行：检查连接\\n第二行：同步配置\\n第三行：检查结果\\n第四行：记录时间": "Check connection\\nSync settings\\nReview results\\nRecord time", "播放通知声音": "Play sound", "接收全部通知": "All notifications", "仅接收重要通知": "Receive Only Important Notifications", "暂不可选": "Unavailable", "暂停通知": "Pause alerts", "默认 0 / 100": "Default 0 / 100", "范围 20–80，值 65": "Range 20–80, Value 65", "禁用与自定义背景": "Disabled · Custom fill", "计算机": "Computer", "示例文件夹": "Example Folder", "素材": "Materials", "模板": "Templates", "EasyVRUI控件演示": "EasyVRUI Control Demonstration", "窗口与交互控件": "Windows and Interaction Controls", "ウィンドウと操作コントロール": "Windows and Operation Controls", "跟踪参考": "Tracking", "追従基準": "Tracking", "你好，VR": "Hello, VR", "打开设置": "Open Settings", "設定を開く": "Open Settings", "新建窗口": "New window", "新規ウィンドウ": "New Window", "文本": "Text", "绘图": "Drawing", "描画": "Drawing", "多行": "Multiple Lines", "複数行": "Multiple Lines", "输入": "Input", "入力": "Input", "容器": "Containers", "列表": "Lists", "屏幕": "Screen", "画面": "Display", "表格": "Tables", "工具栏": "Toolbar", "启用选项": "Enable Options", "オプションを有効化": "Activate Options", "第一项": "First Item", "選択肢 1": "Option 1", "第二项": "Second Item", "選択肢 2": "Option 2", "文件(&F)": "File (&F)", "视图(&V)": "&View", "表示(&V)": "&View", "工具(&T)": "Tool (&T)", "欢迎": "Welcome", "快捷短语": "Shortcuts", "定型文": "Phrases", "翻译历史": "History", "履歴": "History", "最近窗口": "Recent Window", "最近のウィンドウ": "Recent Windows", "书签": "Bookmarks", "偏好设置": "Preferences", "環境設定": "Settings", "帮助": "Help", "EasyVRUI日本語": "EasyVRUI Japanese", "ローマ字で入力": "Input in Roman Alphabet", "日本語": "Japanese", "你好": "Hello", "拟好": "Ready", "您好": "Good day", "你好呀": "Hello there", "EasyVRUI拼音": "EasyVRUI Pinyin", "文本输入": "Text input", "テキスト入力": "Text input", "输入一条短消息": "Enter a short message", "短いメッセージを入力": "Enter a short message", "发送": "Send", "送信": "Send", "文件管理器 — 示例文件夹": "File Manager — Example folder", "桌面": "Desktop", "窗体设计器": "Form Designer", "文件管理器": "File Manager", "控件演示": "Control demo", "保存窗体": "Save form", "フォームの保存": "Save the form", "要保存对当前窗体所做的修改吗？": "Save changes to this form?", "現在のフォームへの変更を保存しますか？": "Save changes to this form?", "窗体设计文件": "Form design file", "フォーム設計ファイル": "Form design file", "所有文件": "All files", "记录 ": "Record", "默认方向：horizontal": "Default direction: horizontal", "禁用 · 范围−20至20，当前为10": "Disabled · Range from -20 to 20, currently 10", "vertical · 当前为65": "Vertical · Currently 65", "默认值与显示精度": "Default value and display precision", "范围−2.00至2.00": "Range from -2.00 to 2.00", "步长0.25 · 1.00 → 1.25": "Step size 0.25 · 1.00 → 1.25", "同一数值 · 禁用": "Same value · Disabled", "每5分钟": "Every 5 minutes", "每15分钟": "Every 15 minutes", "每30分钟": "Every 30 minutes", "每45分钟": "Every 45 minutes", "默认行高30 · 列表顶部": "Default line height 30 · Top of list", "行高42 · 定位所选项": "Line height 42 · Position selected item", "读取配置": "Read settings", "检查目录": "Check directory", "建立连接": "Connect", "同步图像": "Sync image", "同步音频": "Sync audio", "同步模型": "Sync model", "核验校验和": "Verify checksum", "生成报告": "Generate report", "默认边框和背景": "Default border and background", "背景色与嵌套子控件": "Custom fill and nested control", "同步服务": "Sync service", "连接正常": "Connected", "滚动偏移0 · 内容超出视口": "Offset 0 · Content overflows", "滚动后 · 显示后续内容": "After scrolling · Later entries", "第一区": "Area 1", "第二区": "Area 2", "vertical · 左右分区": "Vertical · Left and right areas", "horizontal · 上下分区": "Horizontal · Up and down areas", "概览": "Overview", "概览内容": "Overview content", "历史": "History", "历史内容": "History content", "top · 默认选中第一页": "Top · Default selection for the first page", "left · 选中并重命名第二页": "Left · Select and rename the second page", "同步记录": "Sync log", "同步任务": "Sync tasks", "核验清单": "Checklist", "本地配置": "Local settings", "折叠 · 仅显示根节点": "Fold · Only display the root node", "展开 · 选中子节点": "Unfold · Select the child nodes", "任务": "Tasks", "状态": "Status", "完成": "Completed", "待处理": "Pending", "默认单选": "Single selection", "多选 · 自定义列宽和行高": "Multi-select · Custom sizes", "配置": "Configuration", "数值": "Value", "任务数": "Number of Tasks", "重试次数": "Retries", "整行选择 · 只读": "Whole Row Selection · Read-Only", "单元格选择 · 编辑中": "Cell Selection · Editing", "任务(&T)": "&Tasks", "刷新记录(&R)": "&Refresh", "显示已完成项(&S)": "&Show completed", "清除历史(&C)": "&Clear history", "按住Alt · 显示助记符": "Hold Alt · Show Mnemonic", "键盘导航 · 行高42、勾选与禁用": "Keyboard navigation · 42 px rows, checked and disabled items", "同步记录已刷新": "Sync log refreshed", "默认尺寸与间距": "Default Size and Spacing", "尺寸56 · 间距14 · 禁用右侧操作": "56 px buttons · 14 px gap · Last action disabled", "已请求预览": "Preview requested", "未获得画面": "No frame", "测试事件：采集源可用": "Test Event: Acquisition Source Available", "测试事件：采集源不可用": "Test Event: Acquisition Source Unavailable", "无头渲染占位": "Headless preview", "等待画面": "Waiting Image", "无头WARP采集区域": "Headless WARP Acquisition Area", "采集源可用": "Source available", "边框属于父级panel": "Border belongs to the parent panel", "替换前 · blank": "Before replacement · blank", "替换后 · label": "After replacement · label", "内容已加载": "Loaded", "命名同步报告": "Name report", "输入报告名称": "Report name", "同步检查报告": "Sync report", "保存同步报告": "Save report", "文本报告": "Text report", "同步速率": "Sync rate", "最近9次采样 · 归一化速率": "Last 9 samples · normalized rate", "空间定位配置": "Spatial settings", "五种参考对象 · 窗口空间属性": "Five references · Window spatial properties", "参考对象": "Reference", "跟踪目标": "Tracking targets", "固定的SteamVR跟踪空间": "Fixed SteamVR tracking space", "头显姿态": "Headset posture", "校准朝向与身体平移": "Calibrate orientation and body translation", "左手柄姿态": "Left controller pose", "右手柄姿态": "Right controller pose", "同步周期": "Sync interval", "选择一个同步周期": "Select a synchronization period", "当前周期：每5分钟": "Current period: every 5 minutes", "当前周期：": "Current interval: ", "编辑同步参数": "Edit sync settings", "参数": "Parameters", "值": "Values", "并行任务": "Parallel Tasks", "双击值所在单元格进行编辑": "Double-click a value to edit it", "参数修改已提交": "Parameter modifications have been submitted", "选择要查看的同步任务": "Select the synchronization task to view", "尚未选择任务": "No task selected", "清理临时文件": "Clear temp files", "写入报告": "Write the report", "选中任务：": "Selected task: ", "同步结果": "Sync results", "文件数": "Files", "请选择同步记录": "Please select synchronization records", "当前记录：": "Current record: ", "任务分类": "Task group", "检查报告": "View report", "请选择任务": "Select a task", "选中：": "Selected: ", "延迟安装内容": "Deferred content", "加载内容": "Load content", "素材预览": "Material preview", "切换等比填充": "Toggle fit", "工作区命令": "Workspace commands", "刷新记录": "Refresh Records", "等待刷新": "Wait for Refresh", "显示输出监视": "Display monitor", "等待显示器画面": "Wait for Monitor Screen", "采集源不可用": "Source unavailable", "预览操作": "Preview controls", "预览结果": "Preview Result", "单击蓝色操作项": "Click Blue Action Item", "连接分组": "Connect Group", "连接正常，可以开始同步": "Connection Normal, Synchronization Can Begin", "隐藏连接详情": "Hide details", "显示连接详情": "Show details", "同步日志": "Sync Log", "滚动查看同步步骤": "Scroll to View Sync Steps", "01 读取配置": "01 Read Configuration", "02 检查目录": "02 Check Directory", "03 建立连接": "03 Establish Connection", "04 同步图像": "04 Sync Images", "05 校验数据": "05 Verify Data", "06 生成报告": "06 Generate Report", "日志记录按时间排列": "Log Records Arranged by Time", "双区工作台": "Two-pane workspace", "任务队列": "Task Queue", "同步摘要": "Sync summary", "拖动分隔条调整布局": "Drag the divider bar to adjust the layout", "布局比例已更新": "Layout ratio has been updated", "同步工作台": "Sync dashboard", "同步服务已连接": "Synchronous service is connected", "最近一次同步已完成": "The last synchronization is complete", "已核验12份文件": "12 files have been verified", "通知偏好": "Notifications", "显示未读状态": "Show unread", "通知声音已关闭": "Notification sound is turned off", "通知声音已开启": "Notification sound is turned on", "校准增益": "Calibrate gain", "范围：0.00至2.00": "Range: 0.00 to 2.00", "当前增益低于基准": "Current gain is below the baseline", "当前增益达到或超过基准": "Gain at or above baseline", "同步进度": "Sync progress", "已同步2/8项": "2/8 items have been synchronized", "完成下一项": "Next item", "同步完成": "Sync complete", "已同步": "Synced ", "/8项": "/8 items", "通知模式": "Alert mode", "当前模式：仅接收重要通知": "Mode: Important only", "当前模式：": "Current mode: ", "监听音量": "Listening Volume", "音量较低": "Low Volume", "音量较高": "High Volume", "设置尚未提交": "Unsaved settings", "重新编辑": "Edit again", "设置已提交": "Settings saved", "连接状态": "Connection status", "已连接 · 测试服务": "Connected · Testing Service", "可以开始同步设置": "Synchronization Settings Can Start", "编辑备注": "Edit Notes", "备注（最多80个字符）": "Notes (Up to 80 Characters)", "请编辑或选择备注": "Please Edit or Select Notes", "全选备注": "Select All Notes", "第一行：检查连接\\n第二行：同步配置": "Check connection\\nSync settings", "备注已修改": "Notes Modified", "会话窗口": "Session Window", "当前窗口已显示": "Current Window Displayed", "切换标题栏配色": "Title bar color",}
GUIDE_SOURCE_MAP = {"controls": "capture_ui.cpp", "controls_second": "capture_layout_control.cpp", "controls_third": "capture_display_control.cpp",}

class english_diagram(advanced.diagram):
    def text(self, rectangle, message, size = 28, color = advanced.INK, bold = False, center = False):
        if HAN.search(message):
            message = ADVANCED_TEXT_MAP[message]

        left, top, right, bottom = rectangle
        font_path = str(advanced.FONT_DIRECTORY / ("msyhbd.ttc" if bold else "msyh.ttc"))

        while size >= 17:
            font = ImageFont.truetype(font_path, size)
            x0, y0, x1, y1 = self.draw.textbbox((0, 0), message, font = font)

            if (((x1 - x0) + 4) <= (right - left)) and (((y1 - y0) + 4) <= (bottom - top)):
                return super().text(rectangle, message, size, color, bold, center)

            size -= 1

        raise ValueError(f"English label does not fit: {message!r} in {rectangle}")

def render_diagram_list():
    diagram_type = advanced.diagram
    output = advanced.OUTPUT_DIRECTORY
    advanced.diagram = english_diagram
    advanced.OUTPUT_DIRECTORY = OUTPUT

    try:
        advanced.run()
    finally:
        advanced.OUTPUT_DIRECTORY = output
        advanced.diagram = diagram_type

def localize_source(source, text_map):
    def replace_wide(match):
        raw = match.group(1)
        decoded = ESCAPE.sub(lambda item: chr(int((item.group(1) or item.group(2)), 16)), raw)

        if decoded not in text_map:
            return match.group()

        value = text_map[decoded]
        return f"std::u32string{{U{json.dumps(value, ensure_ascii=False)}, std::size_t{{{len(value)}u}}}}"

    def replace_string(match):
        value = match.group(1)

        if HAN.search(value):
            escaped = re.sub(r'(?<!\\)"', r'\\"', text_map[value])
            return ('"' + escaped) + '"'

        return match.group()

    source = WIDE_LITERAL.sub(replace_wide, source)
    return STRING_LITERAL.sub(replace_string, source)

def prepare_localized_source(build_directory):
    fixture = build_directory / "english_source"
    fixture.mkdir(parents = True, exist_ok = True)
    source_map = {}

    for index, relative in enumerate(STORY_SOURCE_LIST):
        original = capture.SITE / relative
        localized = fixture / f"story_{index}_{original.name}"
        localized.write_text(localize_source(original.read_text(encoding = "utf-8"), STORY_TEXT_MAP), encoding = "utf-8")
        source_map[original] = localized

    original = capture.SITE / DESIGNER_SOURCE
    source = original.read_text(encoding = "utf-8")
    needle = 'if(locale == "zh")\n            {\n                surface->open_document(fixture.parent_path() / "quick_shout_window.easyvruifrm");'
    assert source.count(needle) == 1
    localized = fixture / "english_capture_ui.cpp"
    source = source.replace(needle, needle.replace('locale == "zh"', 'locale == "en"'))
    source = source.replace('capture_surface(make_shared<desktop_window>(U"tutorial_desktop"), "desktop");', 'auto surface = make_shared<desktop_window>(U"tutorial_desktop");\n            show(surface, "desktop");\n            surface->label_clock->set_text(U"2026-11-21 Saturday 03:31:07");\n            snapshot(surface, "desktop");',)
    bar_capture = 'host.attach_control(bar, "input_bar");'
    assert source.count(bar_capture) == 1
    bar_layout = 'auto &language = bar->get_control_list()[U"label_language"];\n            auto &ime = bar->get_control_list()[U"label_ime"];\n            auto &button = bar->get_control_list()[U"button_input_selector"];\n            constexpr uint64_t EXTRA_LABEL_WIDTH = 24u;\n            auto language_rectangle = language.get_rect();\n            auto ime_rectangle = ime.get_rect();\n            auto button_rectangle = button.get_rect();\n            language_rectangle.width += EXTRA_LABEL_WIDTH;\n            ime_rectangle.left += EXTRA_LABEL_WIDTH;\n            ime_rectangle.width += EXTRA_LABEL_WIDTH;\n            button_rectangle.left += EXTRA_LABEL_WIDTH * uint64_t{2u};\n            language.set_rect(language_rectangle);\n            ime.set_rect(ime_rectangle);\n            button.set_rect(button_rectangle);\n            auto bar_rectangle = bar->get_rect();\n            bar->set_size(bar_rectangle.width + (EXTRA_LABEL_WIDTH * uint64_t{2u}), bar_rectangle.height);\n            '
    source = source.replace(bar_capture, bar_layout + bar_capture)
    localized.write_text(source, encoding = "utf-8")
    return source_map, (original, localized)

def prepare_guide_source(build_directory):
    fixture = build_directory / "english_source"
    fixture.mkdir(parents = True, exist_ok = True)
    output = []
    example_directory = capture.SITE / "examples/guide/controls"
    example_map = {path.parents[1].name: path for path in example_directory.glob("*/*/cpp/main.cpp")}

    for role, filename in GUIDE_SOURCE_MAP.items():
        source_list = [(capture.SITE / "tools") / filename] + [example_map[name] for name in capture.CONTROL_CAPTURE_MAP[role]]
        source_map = {}

        for index, original in enumerate(source_list):
            localized = fixture / f"{role}_{index}_{original.name}"
            source = localize_source(original.read_text(encoding = "utf-8"), GUIDE_TEXT_MAP)

            if original.name == "capture_layout_control.cpp":
                fixed_click = 'click("tabcontrol_demo", 128.0, 102.0);\n            auto &tabs = dynamic_cast<tabcontrol &>(demo->get_control_list()[U"tabcontrol_workspace"]);'
                measured_click = 'auto &tabs = dynamic_cast<tabcontrol &>(demo->get_control_list()[U"tabcontrol_workspace"]);\n            const auto TAB = tabs.get_rect();\n            constexpr double TAB_MINIMUM_EXTENT = 48.0;\n            constexpr double TAB_PADDING_WIDTH = 24.0;\n            double first_width = max(TAB_MINIMUM_EXTENT, measure_text(tabs.get_page_list()[0u].get_text(), tabs.get_tab_font()) + TAB_PADDING_WIDTH);\n            double second_width = max(TAB_MINIMUM_EXTENT, measure_text(tabs.get_page_list()[1u].get_text(), tabs.get_tab_font()) + TAB_PADDING_WIDTH);\n            click("tabcontrol_demo", (static_cast<double>(TAB.left) + first_width) + (second_width * 0.5), static_cast<double>(TAB.top) + (static_cast<double>(tabs.get_tab_size()) * 0.5));'
                assert source.count(fixed_click) == 1
                source = source.replace(fixed_click, measured_click)

            if original.name == "capture_display_control.cpp":
                menu_note = 'note->set_text(U"Keyboard navigation · 42 px rows, checked and disabled items");'
                assert source.count(menu_note) == 1
                source = source.replace(menu_note, "note->set_rect({28u, 229u, 699u, 42u});\n            " + menu_note)

            if not localized.is_file() or (localized.read_text(encoding = "utf-8") != source):
                localized.write_text(source, encoding = "utf-8")

            source_map[original] = localized

        output.append((f"tutorial_capture_{role}", source_map.items()))

    return output

def prepare_capture_project(build_directory, guide):
    path = build_directory / "english_capture.cmake"
    line_list = [f'include("{(capture.SITE / "tools/capture_project.cmake").as_posix()}")', "function(configure_english_capture)",]

    if guide:
        target_source_list = prepare_guide_source(build_directory)
    else:
        source_map, designer = prepare_localized_source(build_directory)
        target_source_list = [("tutorial_capture_project_story", source_map.items())] + [(f"tutorial_capture_{role}", (designer,)) for role in ("designer", "desktop", "pinyin", "japanese")]

    for target, source_pair_list in target_source_list:
        line_list.append(f"    get_target_property(source_list {target} SOURCES)")

        for original, localized in source_pair_list:
            original_path = original.resolve().as_posix()
            localized_path = localized.resolve().as_posix()
            line_list.extend(["    set(updated_source_list)", "    foreach(source IN LISTS source_list)", "        cmake_path(NORMAL_PATH source OUTPUT_VARIABLE normalized_source)", f'        if(normalized_source STREQUAL "{original_path}")', f'            set(source "{localized_path}")', "        endif()", '        list(APPEND updated_source_list "${source}")', "    endforeach()", '    set(source_list "${updated_source_list}")', f'    target_include_directories({target} PRIVATE "{original.parent.resolve().as_posix()}")',])

        line_list.append(f'    set_property(TARGET {target} PROPERTY SOURCES "${{source_list}}")')

    line_list.extend(["endfunction()", "cmake_language(DEFER CALL configure_english_capture)"])
    path.write_text("\n".join(line_list), encoding = "utf-8")
    return path

def build_capture(build_directory, guide):
    build_directory.mkdir(parents = True, exist_ok = True)
    project = prepare_capture_project(build_directory, guide)
    tool_map = {"ime": ("pinyin", "japanese")}
    role_list = [item for role in CAPTURE_ROLE_LIST for item in tool_map.get(role, (role,))]
    capture.build_capture_targets(build_directory, project, GUIDE_SOURCE_MAP if guide else (*role_list, "project_story"))

def render_capture_list(build_directory, repository):
    with TemporaryDirectory(prefix = "stage_", dir = build_directory) as temporary:
        stage = Path(temporary)
        installation = stage / "installation"
        capture.stage_installation(installation, repository, CAPTURE_ROLE_LIST)
        fixture = stage / "Examples"
        capture.prepare_fixture(fixture)
        design = stage / "quick_shout_window.easyvruifrm"
        design.write_text(localize_source(design.read_text(encoding = "utf-8"), STORY_TEXT_MAP), encoding = "utf-8")
        image_list, part_list = capture.capture_locale(stage, installation, build_directory, "en", CAPTURE_ROLE_LIST)
        capture.run_capture(installation, build_directory, "project_story", stage / "en", fixture, stage / "profile_en", "en")
        image_list.extend((stage / "en") / f"{name}.png" for name in capture.STORY_IMAGE_LIST)
        image_list.append(stage / "en/basics_form_design.png")
        stage_images = stage / "images/en"
        stage_parts = stage / "parts/en"
        stage_images.mkdir(parents = True)
        stage_parts.mkdir(parents = True)

        for image in image_list:
            capture.check_image(image)
            shutil.copyfile(image, stage_images / image.name)

        for part in part_list:
            shutil.copyfile(part, stage_parts / part.name)

        spatial.render_locale("en", stage_images.parent, stage_parts.parent)

        for image in sorted(stage_images.glob("*.png")):
            width, height = capture.check_image(image)
            shutil.copyfile(image, OUTPUT / image.name)
            print(f"{image.name} {width}x{height}")

def render_guide_list(build_directory, repository):
    role_list = tuple(GUIDE_SOURCE_MAP)

    with TemporaryDirectory(prefix = "guide_", dir = build_directory) as temporary:
        stage = Path(temporary)
        installation = stage / "installation"
        fixture = stage / "Examples"
        profile = stage / "profile_en"
        (profile / "Roaming").mkdir(parents = True)
        (profile / "Local").mkdir()
        output = stage / "en"
        capture.stage_installation(installation, repository, role_list)
        capture.prepare_fixture(fixture)

        for role in role_list:
            capture.run_capture(installation, build_directory, role, output, fixture, profile, "en")

        capture.combine_window_comparison(output)
        capture.combine_menu_comparison(output)
        source = capture.SITE / "docs/guide"
        name_set = {name for page in source.rglob("*.md") for name in re.findall(r"/images/zh/([A-Za-z0-9_.-]+\.png)", page.read_text(encoding = "utf-8"))}

        for name in sorted(name_set):
            image = output / name

            if image.is_file():
                width, height = capture.check_image(image)
                shutil.copyfile(image, OUTPUT / name)
                print(f"{name} {width}x{height}")
            else:
                capture.check_image(OUTPUT / name)

def run():
    parser = ArgumentParser(description = "Capture current EasyVRUI windows with WARP and generate the English tutorial diagrams.")
    parser.add_argument("--repository", type = Path, default = WORKSPACE / "repo")
    parser.add_argument("--build-directory", type = Path, default = ENGLISH_BUILD)
    parser.add_argument("--diagrams-only", action = "store_true")
    parser.add_argument("--capture-only", action = "store_true")
    parser.add_argument("--reuse-binaries", action = "store_true")
    parser.add_argument("--guide", action = "store_true")
    option = parser.parse_args()
    OUTPUT.mkdir(parents = True, exist_ok = True)

    if not option.capture_only and not option.guide:
        render_diagram_list()

    if not option.diagrams_only:
        build_directory = option.build_directory.resolve()

        if not build_directory.is_relative_to(capture.SITE):
            raise ValueError("Choose a capture build directory inside the tutorial checkout.")

        if not option.reuse_binaries:
            build_capture(build_directory, option.guide)

        repository = option.repository.resolve()

        if option.guide:
            render_guide_list(build_directory, repository)
        else:
            render_capture_list(build_directory, repository)

if __name__ == "__main__":
    run()