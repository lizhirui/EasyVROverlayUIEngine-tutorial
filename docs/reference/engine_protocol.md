# Engine接口参考

Engine的可执行文件为`easyvrui_engine.exe`。Engine负责VR跟踪、激光命中、窗口表面、图形资源和输入路由。SDK管理控件、记录绘图指令并分派应用事件。

## Windows服务托管

`bin/easyvrui_service.exe`作为`EasyVROverlayUIEngine`在Session 0运行。服务根据活动控制台会话和登录标识在当前用户的默认桌面启动Engine（登录用户具备管理员权限时使用关联的管理员令牌）以连接SteamVR，同时在该会话中以SYSTEM身份运行`easyvrui_screen_helper.exe`，用于抓屏和桌面输入。会话切换时服务停止两个受管进程，再为目标用户启动新实例。启动时清理同一安装目录、同一控制台会话内的旧实例。

停止或关闭服务时，Engine和抓屏代理通过登录会话限定的事件收到退出通知。服务等待正常退出，超时由同一个Job Object回收两个进程。Job Object同时负责服务异常终止后的进程清理，两个受管进程通过监督互斥锁检测父服务退出。托管模式从安装目录读取配置。管理员可在`bin/config.json`中配置固定远程凭据，缺省时Engine为本次运行生成凭据。

抓屏代理启动后创建D3D11设备，并在Engine请求画面期间检查当前输入桌面。桌面名称变化或Desktop Duplication返回`DXGI_ERROR_ACCESS_LOST`时，代理通过`OpenInputDesktop`和`SetThreadDesktop`切换抓屏线程，再重建显示器枚举和`IDXGIOutput1::DuplicateOutput`。帧写入带`D3D11_RESOURCE_MISC_SHARED_NTHANDLE`和keyed mutex的共享纹理，句柄复制到本次由服务启动的Engine进程。Engine将纹理复制到渲染设备后提交给`screen`控件。

Helper通过重叠I/O等待管道请求，同时监听停止信号和Engine进程退出。队列优先处理待发送的鼠标及键盘请求，并合并连续且属于同一显示器的鼠标移动。

Helper的Named Pipe DACL只允许SYSTEM和当前登录会话。连接建立后使用`GetNamedPipeClientProcessId`核对对端PID和进程创建时间，两者均须与服务本次启动的Engine身份一致。Helper支持显示器枚举、抓帧、释放纹理、`inject_pointer`和`inject_keyboard`。输入请求在活动输入桌面执行，输入内容仅用于当前转发，不记录。

在CMD中执行以下命令安装并查询服务。安装命令须显式指定本地磁盘上的绝对目录，路径支持中文和空格。省略目录时，脚本向标准错误输出用法并返回退出码2。安装程序通过Windows管理员确认取得服务操作权限。服务和Helper以SYSTEM身份运行，服务安装须使用管理员保护的目录。

```bat
install.bat "%ProgramFiles%\EasyVRUI"
"%ProgramFiles%\EasyVRUI\bin\easyvrui_service.exe" --status
```

服务安装成功时，安装脚本将系统环境变量`EASYVROVERLAYUIENGINE_HOME`设为规范化后的安装根目录，例如`D:\Tools\EasyVROverlayUIEngine`。工具可在新开的CMD窗口中使用`%EASYVROVERLAYUIENGINE_HOME%\bin`定位引擎。环境变量写入失败时，安装脚本报告错误并回滚安装。

在管理员CMD中执行启停和卸载。手动注册服务可在安装目录内执行`easyvrui_service.exe --install`后再启动。

```bat
"%ProgramFiles%\EasyVRUI\bin\easyvrui_service.exe" --stop
"%ProgramFiles%\EasyVRUI\bin\easyvrui_service.exe" --start
"%ProgramFiles%\EasyVRUI\bin\easyvrui_service.exe" --uninstall
```

`easyvrui_service.exe --uninstall`移除服务注册，并保留安装文件及`EASYVROVERLAYUIENGINE_HOME`。永久移除该安装目录时，可在Windows的系统环境变量设置中删除该变量。

`install.bat "D:\Tools\EasyVRUI" --no-service`在自定义目录生成可独立运行的便携安装（同时复制服务工具、Helper及File Manager卷查询程序），保留系统环境变量的现有配置，并使用Engine本进程Desktop Duplication；安装完成后可在CMD中直接运行`start "" "D:\Tools\EasyVRUI\bin\easyvrui_engine.exe"`手动启动。`easyvrui_service.exe --check-install-root "D:\Tools\EasyVRUI"`校验目录路径是否合法。服务安装模式下，Helper随当前输入桌面切换，处理画面捕获和已鉴权的键鼠请求。

SDK在调用进程所在机器读取[应用清单](/reference/application_manifest)并启动程序，入口为`launch_application()`。应用清单可声明`run_as_administrator`。普通权限的SDK启动器会对管理员请求返回权限不足错误，管理员启动器按请求继承管理员权限或使用普通令牌。Engine提供`application_list`查询会话和窗口，并通过`application_terminate`结束应用或请求关闭指定窗口。应用在握手中提供非空`name`。单实例由应用自身实现。

示例中尖括号包裹的字符串为占位符，接入时替换为实际配置及握手数据。

Engine提供以下通信和进程协调入口。

* IPv4/IPv6 TCP/TLS接口：监听`0.0.0.0:<port>`和`[::]:<port>`，承载主要数据流。按IPv4、IPv6顺序初始化监听，IPv6设置`v6_only=true`；两路监听均须初始化成功。
* Windows命名管道：`\\.\pipe\EasyVROverlayUIEngine.Bootstrap`，向本机SDK提供端口号、接入凭据和公钥指纹。
* Windows命名互斥体：`Local\EasyVROverlayUIEngine.Engine`，用于协调Engine单实例。

## IPv4/IPv6 TCP/TLS接口

### 连接与启动参数

#### Engine配置

端口和共享接入凭据保存在Engine可执行文件同目录的`config.json`中。默认端口为`49537`；接入凭据允许任意长度的非空字符串，仅在配置项不存在时生成随机初始值。下面是相关配置项示例，实际文件还可包含输入组件配置：

Engine配置片段：

```json
{
    "ipc_service_port": 49537,
    "access_credential": "<自行设置的共享接入凭据>"
}
```

#### 本机SDK连接

SDK默认通过本机命名管道发现Engine，取得实际端口、接入凭据、公钥指纹和PID，随后连接本机TCP/TLS服务。

SDK接收线程按消息类型分流。同步请求按`id`等待并领取自己的响应。异步响应和服务端事件进入独立队列，UI线程按收包顺序分派两队列中的消息，并处理投递到UI线程的回调。同步请求期间的事件和异步回调留待下一次UI分派。这一顺序使输入排空前到达的按键或文字提交先于关闭完成回调交给应用。

#### 远程SDK连接

远程连接参数传入使用SDK的应用进程，应用自身的参数直接追加到同一命令行。

* `--easyvrui-host`：远程主机名或IPv4/IPv6地址，必填；IPv6使用裸地址，例如`::1`。
* `--easyvrui-port`：十进制端口，省略时为`49537`；有效范围为`1`至`65535`。
* `--easyvrui-access-credential`：接入凭据，必填。
* `--easyvrui-public-key-fingerprint`：服务端公钥指纹，必填；应使用发现信息中的SHA-256十六进制字符串。

只支持`--name=value`格式，按第一个`=`分隔参数名和值，值保留原始内容；含空格的值使用CMD引号。一旦出现这四个参数中的任何一个，就按远程模式校验；host、凭据或指纹缺项，任何已出现参数重复、值为空，以及端口非十进制数字、为零或溢出，均报错。

C++和Python共用同一个原生库，由原生库读取Windows当前进程命令行。应用如果使用自己的`argparse`或其它参数解析器，应声明并接受这些参数，或保留未知参数交由SDK读取。

以下均为Windows CMD单行示例，指纹中的64个零仅为占位，连接时请替换为实际指纹：

```cmd
my_vr_app.exe --easyvrui-host=192.0.2.10 --easyvrui-port=49537 --easyvrui-access-credential="demo credential with spaces" --easyvrui-public-key-fingerprint=0000000000000000000000000000000000000000000000000000000000000000
```

```cmd
python my_vr_app.py --easyvrui-host=::1 --easyvrui-access-credential="demo credential with spaces" --easyvrui-public-key-fingerprint=0000000000000000000000000000000000000000000000000000000000000000
```

### TLS

TLS使用自签名ECC P-256证书，通过固定公钥指纹建立服务器信任。公钥指纹为证书SubjectPublicKeyInfo的DER编码经SHA-256计算得到的64个十六进制字符，由本机管道提供；远程SDK预先取得该值用于验证服务器。证书与持久私钥保存在当前Windows用户的证书和密钥存储中，启动时先比对私钥算法，对样本摘要签名并用证书导出的公钥验签以确认配对，同时校验有效期；合格资源继续复用，校验失败时重新生成配对密钥与证书。生成证书的有效期至9999年12月31日23:59:59；重新生成私钥后，远程SDK须取得并使用新的公钥指纹。

Schannel按系统配置协商TLS版本，Engine要求TLS 1.2或以上版本。TLS握手超时为5秒。完成TLS后进行应用层鉴权，下面的长度头与JSON均在TLS加密通道内传输。

### 应用层帧格式

#### 长度头与消息体

所有自定义应用层帧，包括鉴权前消息、鉴权后请求、响应、心跳和推送，以及本机命名管道发现消息，统一为：

```text
8字节小端uint64长度头 | UTF-8 JSON消息体
```

长度为JSON完成序列化后的UTF-8消息体字节数。消息体为使用无BOM UTF-8编码的完整JSON对象，帧长包含实际发送的格式空白。接收方先精确读取8字节长度头，再按长度精确读取消息体，以此划分协议消息边界。

下面的消息体采用LF换行且末尾无换行，共14个UTF-8字节：

```json
{
    "a": 1
}
```

对应的完整明文字节为：

```text
0E 00 00 00 00 00 00 00 7B 0A 20 20 20 20 22 61 22 3A 20 31 0A 7D
```

长度须为接收进程尺寸类型可表示的正整数。

#### JSON与二进制字段

业务消息使用JSON。图片像素等二进制字段使用标准RFC 4648 Base64连续字符串，采用`A-Z a-z 0-9 + /`字母表及必要的`=`填充。先编码二进制字段，再序列化整个JSON，最后计算帧长。空二进制序列编码为`""`。

Base64文本长度为`4 × ceil(原始字节数 / 3)`。

### 应用层鉴权

TLS完成后，应用层鉴权另有5秒总期限。下面四个JSON对象分别独立成帧，均使用8字节小端长度头。鉴权失败、超时或握手消息非法时，服务端关闭连接。

#### 客户端问候：`client_hello`

客户端声明协议版本、本次随机nonce、自己的PID和会话名称：

客户端 → Engine：

```json
{
    "message_type": "client_hello",
    "version": 1,
    "client_nonce": "0000000000000000000000000000000000000000000000000000000000000000",
    "process_id": 23456,
    "name": "demo"
}
```

`version`固定为整数`1`。标准SDK用32个随机字节生成`client_nonce`，再编码为十六进制字符串；当前服务端检查该字段为字符串。`process_id`是uint32 PID。Engine取得真实本机连接进程后，会校验申报PID一致；远程PID作为客户端申报信息记录。`name`是会话名称，必填且为非空UTF-8字符串，Engine按该名称在应用列表中显示会话，名称缺失或为空时握手失败并关闭连接。

#### 服务端挑战：`challenge`

Engine → 客户端：

```json
{
    "message_type": "challenge",
    "version": 1,
    "server_nonce": "1111111111111111111111111111111111111111111111111111111111111111"
}
```

`server_nonce`由32个随机字节生成，再编码为十六进制字符串。客户端必须检查版本。

#### 客户端证明：`authenticate`

`proof`为HMAC-SHA256的十六进制结果。key是接入凭据的UTF-8字节；data是下列字符串的UTF-8字节，行间使用LF连接，最后一行为`server_nonce`：

```text
easyvrui-ipc-auth-v1\n<client_nonce>\n<server_nonce>
```

等价计算方式为：

```text
proof = hex(HMAC-SHA256(access_credential, "easyvrui-ipc-auth-v1\n" + client_nonce + "\n" + server_nonce))
```

nonce、proof、session_token及公钥指纹的标准输出使用小写十六进制。nonce按消息中的实际文本参与计算；接入凭据使用原始UTF-8字节，字符串中的空格也参与HMAC。证明消息如下：

客户端 → Engine：

```json
{
    "message_type": "authenticate",
    "proof": "<上述HMAC结果的64个十六进制字符>"
}
```

#### 会话确认：`welcome`

Engine → 客户端：

```json
{
    "message_type": "welcome",
    "version": 1,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "process_id": 12345,
    "owner_process_id": 23456,
    "owner_created": 134000000000000000
}
```

`process_id`是Engine的PID；`owner_process_id`是连接所属应用的PID，来自已验证的本机进程身份或客户端申报。`owner_created`是已验证Windows进程的创建时间原始值，用于区分PID重用；无法验证时为`0`。

`session_token`由32个随机字节生成后转为十六进制字符串。每条已鉴权TCP连接拥有一个`session_id`和token，同一个PID可以建立多个独立会话。关闭后重连会创建新会话。

## 会话建立后的通信协议

### 公共字段

#### 请求公共结构

下面的`ping`是可以实际发送的完整公共请求示例，其它操作在此基础上更换`op`并添加专用字段：

请求：

```json
{
    "message_type": "request",
    "id": 1,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "op": "ping"
}
```

`message_type`固定为`request`，`id`为uint64请求序号，由客户端用于对应响应；SDK自动递增并填写。每条请求都必须带当前连接自己的`session_id`和`session_token`。窗口ID和组件ID分别标识相应资源。

JSON中uint32/uint64均使用非负整数字面量。uint32的取值范围为`0`至`2^32-1`，uint64的取值范围为`0`至`2^64-1`。自行接入的语言需使用能精确保留相应完整范围的整数解析方式。

字段名、操作名、事件名及枚举字符串按大小写精确匹配。同一JSON对象的字段名保持唯一。整数、布尔值、字符串和数组按各自的JSON类型校验；显式`null`仅用于接口标明可空的字段。可选字段省略时采用该接口定义的初始值或保留规则。

请求、窗口属性和绘图命令按已定义字段执行业务，额外字段忽略；事件扩展字段由SDK约定。`op`、`event_type`和绘图`type`的取值须属于对应接口的定义集合。

同一连接中尚未完成请求的`id`保持唯一。响应和事件可以交错，长操作异步完成；调用方按`id`接收对应结果。发生超时后，调用方结合操作状态决定重试，连接重建按新会话处理。

#### 成功响应公共结构

响应：

```json
{
    "message_type": "response",
    "id": 1,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "ok": true,
    "value":
    {
        "window_count": 0
    }
}
```

`id`回送对应请求序号，`ok`为`true`，`value`的类型由具体操作决定，可以为`null`、布尔值、整数、字符串、数组或对象。请求响应与事件可以交错，客户端通过`message_type`区分消息，以`id`对应响应，以`event_type`分发事件。

#### 失败响应公共结构

业务操作失败示例：

```json
{
    "message_type": "response",
    "id": 2,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "ok": false,
    "error":
    {
        "language_key": "unknown_object",
        "message": "<文件:行号:列号: error: 条件 [unknown_object] 本地化说明>",
        "argument_list": [],
        "diagnostic":
        {
            "file": "<源码文件>",
            "line": 1,
            "column": 1,
            "function": "<函数>",
            "condition": "<未满足的条件>"
        }
    }
}
```

`language_key`用于查找语言包，`argument_list`为格式参数，`diagnostic`保留源文件、行列、函数与条件。`message`为单行本地化诊断；实际内容、位置和错误键取决于失败原因。未知标准异常可能只能保留捕获边界位置。

后面每种操作给出成功响应；请求处理过程中抛出的业务异常统一采用此失败结构。通过`ok`判断操作是否成功，`value`中的`false`或`null`可能是正常结果。无效JSON、错误会话/token、鉴权失败、读写失败、超时等问题可能直接导致连接关闭。

### 心跳与存活检测

#### 客户端心跳

心跳使用独立的`message_type`，结构如下：

客户端 → Engine：

```json
{
    "message_type": "heartbeat",
    "session_id": 1,
    "session_token": "<会话令牌>"
}
```

#### 服务端心跳

Engine → 客户端：

```json
{
    "message_type": "heartbeat",
    "session_id": 1,
    "session_token": "<会话令牌>"
}
```

两端每秒独立发送心跳。收到完整消息都会刷新存活时间，正常业务消息同样有效；服务端验证收到的心跳所属会话后完成处理。

超过10秒仍未收到完整消息，在定时检查时断开；单次写入同样有10秒期限。存活检测以完整消息的接收时间为准，标准SDK自动管理心跳，`ping`用于普通业务查询。

### 窗口表面与绘图提交

#### 提交窗口和绘图节点：`present`

一次提交可包含多个窗口，每项通过本会话局部窗口ID标识目标，并携带本次更新的窗口属性和绘图节点。下面的`command_list`包含一条覆盖640 × 360逻辑区域的矩形填充指令，颜色为`0x202020FF`，对应JSON整数`538976511`。

`window_list`是本次更新集合，省略的窗口继续存在。窗口首次出现时创建，已存在时更新；Engine分配全局窗口ID。

请求：

```json
{
    "message_type": "request",
    "id": 10,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "op": "present",
    "window_list":
    [
        {
            "window": 100,
            "metadata":
            {
                "width": 640,
                "height": 360,
                "physical_scale": 1.0,
                "position":
                [
                    0.0,
                    0.0,
                    0.0
                ],
                "rotation":
                [
                    0.0,
                    0.0,
                    0.0
                ],
                "visible": true,
                "enabled": true,
                "auxiliary": false,
                "name": "main",
                "title": "Main",
                "reference": "world"
            },
            "order":
            [
                1
            ],
            "node_list":
            [
                {
                    "node": 1,
                    "command_list":
                    [
                        {
                            "type": "fill_rectangle",
                            "rectangle":
                            {
                                "left": 0.0,
                                "top": 0.0,
                                "width": 640.0,
                                "height": 360.0
                            },
                            "color": 538976511
                        }
                    ]
                }
            ]
        }
    ]
}
```

成功响应：

```json
{
    "message_type": "response",
    "id": 10,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "ok": true,
    "value": null
}
```

`metadata`的类型、初始值及提供规则见下表。`auxiliary`标记辅助表面，当前窗口从普通表面中选择。

窗口更新项的字段如下：

|字段|类型|提供规则|
|---|---|---|
|`window`|uint64|必填，本会话内的窗口局部ID|
|`metadata`|对象|首次创建必填，后续更新可省略|
|`node_list`|对象数组|可省略，默认为`[]`，仅列本次更新节点|
|`order`|uint64数组|可省略，保留已有顺序；提供时描述完整保留集合及绘制顺序|

`metadata`字段的初始值及类型如下，后续提交按字段合并：

|字段|类型|初始值或约束|
|---|---|---|
|`width`、`height`|uint64|首次创建必填，均大于零|
|`physical_scale`|有限数值|首次创建必填，大于零，表示逻辑像素物理尺寸的缩放倍数；1倍时每逻辑像素为0.001米|
|`curvature`|有限数值|默认为`0.0`，大于或等于零，单位为米的倒数；曲率与有效物理宽度之积小于`2π`|
|`position`、`rotation`|长度为3的有限数值数组|默认均为三个`0.0`，单位分别为米和度|
|`visible`、`enabled`|布尔值|均默认为`true`|
|`auxiliary`|布尔值|默认为`false`|
|`title`|字符串|默认为`""`，保存SDK窗口标题，与`name`一样作为Engine窗体状态的固定属性，支持增量更新|
|`name`|字符串|默认为`""`，保存SDK窗口名称|
|`reference`|字符串|普通表面使用SDK参考对象枚举的成员名称，默认`world`，取`world/body/head/left/right`。辅助表面由Engine维护有效参考姿态|
|`startup_position`|字符串|可选，取`none/center`，省略为`none`；描述首次普通表面的启动定位|
|`startup_owner`|uint64|可选，同session来源窗口的局部ID；省略或0优先使用当前选中普通表面，无有效来源时按头显居中|

`startup_position=center`在首次创建普通表面时执行一次自动定位。非零`startup_owner`严格使用同session的来源窗口；该窗口可已存在，也可在同批次提交，提交顺序任意，来源关系须无环。center要求有效头显姿态；无效的显式来源或循环关系采用失败响应，本批窗口在校验和定位成功后统一提交。

`startup_owner`省略或0时，Engine优先使用提交前当前选中的可见普通表面作为来源，可跨session，例如从旋转后的Desktop启动其它App。辅助表面、自身及世界姿态无效的表面退出候选；没有有效来源时按当前头显姿态在前方居中。

新窗口与来源窗口平面平行、中心对齐，沿头显所在一侧的法线前移；正面与背面分别选择相应方向。Engine结合全部会话中可见普通窗口的实际姿态，对投影重叠的近平行表面安排不同初始深度。来源仅决定首次定位，后续移动由新窗口自己的reference及position/rotation确定。

`none`保留提交的位姿，允许显式重合。SDK窗口默认center，首次present会携带提示；直接提交present省略提示时采用none。辅助表面沿用输入区自动定位规则。重复启动提示保持已确定的位置，后续位姿通过position和rotation更新。

成功响应value在本次没有首次center定位结果时为null；具有定位结果时为对象，window_list逐项返回窗口局部ID及当前reference下的最终position/rotation。position为米，rotation为三轴欧拉角度数。SDK在完成回调中同步对象属性与已提交缓存，保留等待响应期间发生的新属性修改。

首次center定位响应示例：

```json
{
    "message_type": "response",
    "id": 10,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "ok": true,
    "value":
    {
        "window_list":
        [
            {
                "window": 100,
                "position":
                [
                    -0.32,
                    0.18,
                    0.02
                ],
                "rotation":
                [
                    0.0,
                    0.0,
                    0.0
                ]
            }
        ]
    }
}
```

`name`和`title`均保存在Engine窗体状态中。应用列表返回的每个窗口包含`id`、`name`、`title`和`visible`；`title`随SDK窗口标题更新，任务管理器使用它显示窗口标题。应用窗口列表与计数仅统计普通表面，包含隐藏窗口和普通模态窗口。

`window_list`须为数组，`[]`表示空更新。窗口ID在所属会话内解析，节点ID在所属窗口内解析；关闭后重新创建的窗口使用独立资源生命周期。窗口实例存活期间保留其局部ID。

`node_list`是本次更新的绘图节点列表，省略等同`[]`；每项包含uint64类型的`node`和绘图命令对象数组`command_list`。每条命令通过字符串`type`标明用途，其余字段描述绘制参数。同一次提交中的窗口ID、同一窗口内的节点ID分别保持唯一。

`order`是窗口保留的全部绘图节点ID及其绘制顺序，每个ID须对应已缓存或本次提交的节点，数组元素保持唯一。Engine按数组从前到后的顺序绘制，后绘制的内容叠在前面。例如背景节点为10、按钮为20、文本框为30时，`order`依次包含`10`、`20`、`30`。`node_list`负责更新节点内容，`order`负责排列和保留节点。

#### 增量、节点删除与空内容

已有窗口采用增量更新：省略`metadata`或提供`metadata: {}`时沿用已有属性；提供字段时，仅更新明确提交的字段，其余字段保留当前值。默认值仅在首次创建时应用。表中已提交字段按各自规则校验，位置与旋转数组按完整字段替换。显式`false`、零及空字符串按相应字段规则处理。

`metadata`提供时须为对象。首次创建按初始默认值补齐属性，后续更新在已有状态上合并字段，再校验最终窗口状态。组件会话的表面由Engine统一标记`auxiliary=true`，沿用输入辅助定位规则；普通应用会话按各窗口的`auxiliary`属性创建表面。

`order`可以省略，此时沿用窗口原来的顺序；新窗口提交绘图节点时，需提供引用这些节点的`order`。`node_list`仅列本次变更的节点，窗口复用`order`中其余已缓存的节点。只更新绘图内容时省略`metadata`；只更新窗口属性时提交对应字段，省略`node_list`以复用绘图缓存。

服务端按最终`order`保留节点缓存并确定显示顺序。删除节点时，从新`order`中移除对应ID；`order: []`清空窗口全部节点。

`command_list: []`表示零条绘图指令，可以保留节点ID和绘制位置并清除其内容。下面清空节点1：

请求：

```json
{
    "message_type": "request",
    "id": 11,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "op": "present",
    "window_list":
    [
        {
            "window": 100,
            "node_list":
            [
                {
                    "node": 1,
                    "command_list": []
                }
            ]
        }
    ]
}
```

成功响应：

```json
{
    "message_type": "response",
    "id": 11,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "ok": true,
    "value": null
}
```

仅移动窗口时，`window_list`中的更新项可以写为：

```json
{
    "window": 100,
    "metadata":
    {
        "position":
        [
            0.1,
            0.0,
            0.0
        ]
    }
}
```

Engine先准备本次各窗口的数据，通过处理后再写入表面状态。`ok:true`表示运行时已接受更新，后续绘制或提交纹理时仍可能异步推送`render_error`。

#### 关闭窗口表面：`surface_close`

查找当前会话中的`window`，关闭时释放表面和激光捕获。目标为当前窗口时，关闭关联输入界面，按当前窗口规则恢复同一应用中因禁用而暂停的窗口；没有可恢复窗口时清空当前选择。引用该窗口的其它表面可能因参考对象失效而无法定位。查找失败时返回业务错误。

请求：

```json
{
    "message_type": "request",
    "id": 12,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "op": "surface_close",
    "window": 100
}
```

成功响应：

```json
{
    "message_type": "response",
    "id": 12,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "ok": true,
    "value": null
}
```

### 激光捕获

#### 捕获激光：`pointer_capture`

`hand`为`left`或`right`，`window`须为本会话已存在的窗口局部ID。当前手的扳机或侧握键有效按下并命中指定窗口时可捕获。按键进入等待释放状态时，松开后重新按下即可发起捕获。捕获后离开窗口边界仍可继续收到坐标，坐标可能超出逻辑矩形。

`lock_position`为可选布尔值，默认`false`。设为`true`时，可视激光端点每帧按窗口的当前尺寸、曲率和姿态投影。移动、旋转、物理缩放和曲率调节使用捕获时的绝对逻辑像素。投递给SDK的坐标和射线继续跟随实际手柄输入。捕获释放或失效时清除端点锁定。

`lock_anchor_x`和`lock_anchor_y`可分别指定水平和垂直轴的锁定锚点，取值为`min`、`center`或`max`。设置锚点时须将`lock_position`设为`true`。`min`为左边或上边，`center`为中心线，`max`为右边或下边。Engine保留捕获点到对应锚点的有符号像素偏移，按新尺寸求出位置并限制在有效窗体范围内。省略某一轴的锚点时，该轴使用捕获时的绝对逻辑坐标。SDK在拖拽外圈控制块改变逻辑尺寸时同时指定两轴锚点。

合法目标未满足捕获条件时返回`false`；手别非法、窗口不存在或属于其它会话时返回业务错误。

请求：

```json
{
    "message_type": "request",
    "id": 20,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "op": "pointer_capture",
    "lock_position": true,
    "lock_anchor_x": "max",
    "lock_anchor_y": "center",
    "hand": "right",
    "window": 100
}
```

成功响应：

```json
{
    "message_type": "response",
    "id": 20,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "ok": true,
    "value": null
}
```

捕获条件不满足时的成功响应：

```json
{
    "message_type": "response",
    "id": 20,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "ok": true,
    "value": false
}
```

#### 释放激光：`pointer_release`

`hand`取`left`或`right`。释放本会话拥有的该手捕获，合法手别没有本会话捕获时同样返回`null`；手别非法时返回业务错误。扳机与侧握键都松开时，Engine自动解除捕获；SDK根据发起交互的按键主动释放捕获，例如松开侧握键即结束窗口移动。窗口关闭、提交隐藏状态或清理所属会话时，Engine立即清除该窗口的捕获；对仍连接的SDK发送`event_type="pointer"`且`lost=true`的事件，由SDK取消当前交互。仍按住的扳机或侧握键须先松开，再接受新的按下交互。

请求：

```json
{
    "message_type": "request",
    "id": 21,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "op": "pointer_release",
    "hand": "right"
}
```

成功响应：

```json
{
    "message_type": "response",
    "id": 21,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "ok": true,
    "value": null
}
```

#### 操作显示器指针：`screen_pointer_input`

普通应用会话可用该请求操作自己已提交、可见且启用的窗口中所显示的Windows屏幕。`screen_id`为DXGI显示器编号，`x/y`为画面区域内的归一化坐标，范围为`0.0`至`1.0`。`action`取`move`、`down`、`up`或`scroll`。`scroll`使用有符号整数`steps`，`horizontal=true`表示水平滚轮。输入端按显示器的`DesktopCoordinates`映射到包含负坐标的虚拟桌面，再使用绝对虚拟桌面鼠标事件。独立Engine直接调用`SendInput`，服务托管时通过Helper的`inject_pointer`执行。

SDK只在`screen.accept_pointer=true`、控件可见、启用且捕获可用时转发指针。画面保持纵横比，指针命中区域为画面矩形。

服务托管时，指针和键盘请求进入同一队列，响应表示请求已入队。连续的同屏移动可合并为最新坐标，按下、释放、滚动和键盘事件按入队顺序处理。渲染使用已就绪的捕获帧，后台管道接收后续帧。

```json
{
    "message_type": "request",
    "id": 22,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "op": "screen_pointer_input",
    "window": 100,
    "screen_id": 0,
    "action": "move",
    "x": 0.5,
    "y": 0.5,
    "steps": 0,
    "horizontal": false
}
```

#### 操作桌面键盘：`screen_keyboard_input`

普通应用会话通过自己的当前窗口发送键盘请求。`window`为应用窗口编号，`screen_id`为显示器编号。`event_type`取`key_down`、`key_up`或`ime_submit`。按键请求使用`key`指定键名，也可使用`scan_code`指定扫描码，扩展扫描码使用`0xE0`高字节。按下请求可附带`shift`、`ctrl`、`alt`和`meta`布尔值。文本提交使用`text`，每次请求支持最多65536字节UTF-8。使用`action="release"`释放该窗口和显示器组合转发的全部按键。

SDK在允许键盘的`screen`获得焦点时按控件设置开启输入区，转发按键及IME提交文本。独立Engine在本地调用`SendInput`，服务托管时由Helper通过`inject_keyboard`执行。按键使用虚拟键或扫描码，文本使用UTF-16的Unicode键事件。Windows将键盘事件交给活动输入桌面上的前台应用，激光可通过`accept_pointer`操作桌面前台窗口。Helper切换桌面时先在原桌面释放持有的键，切换后重试尚未释放的键。显示器捕获资源由发现或捕获请求按需重建。

```json
{
    "message_type": "request",
    "id": 23,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "op": "screen_keyboard_input",
    "window": 100,
    "screen_id": 0,
    "event_type": "key_down",
    "key": "Enter"
}
```

### 当前窗口与键盘路由

Engine维护一个全局当前窗口，启动时为空。普通窗口隐藏或关闭后的再次显示由新的激光按下重新选中；Desktop通过Ctrl+Pause显示后由Engine选中。激光在可交互的普通窗口上按下时发起窗口选择，完成相关排空后将它设为当前窗口；悬停移动保持当前选择。Engine向原窗口SDK发送失焦事件，再向新窗口SDK发送获焦事件，随后投递触发选择的按下事件。

SDK的本地窗口激活与控件焦点维护应用状态。Engine通过激光选择、Desktop唤起、同一应用内的禁用接替与恢复以及失效清理维护当前窗口，输入事件中的`window`指定接收输入的目标窗口。

已选中的窗口保持可见但被禁用时，Engine暂停其选择资格并记录恢复顺序。完成旧输入路径清理后，若该会话仅有一个可交互的普通窗口，则将键盘交给该窗口，适用于SDK打开模态对话框的过程。对话框关闭、隐藏或失效后，原窗口重新启用时按逆序恢复，可用于嵌套对话框。恢复目标须保持可见、属于原会话且参考姿态有效；显式选择的有效窗口优先，选择其它应用窗口后清除原应用的恢复记录。普通窗口隐藏或关闭后的选择采用前述激光规则，Desktop采用快捷键唤起规则。

激光事件按当前命中或捕获的窗口路由。启用IME的输入区开启时，按键先经活动IME处理，最终文本以`ime_submit`提交给SDK。输入区关闭或IME关闭时，Engine将按键直接送至当前窗口所属SDK。SDK负责窗口内的控件焦点、按键分发、文字编辑、选区、字符限制和Tab导航。`tab_index`为SDK本地属性，默认`0`：非零项按升序优先，零值项按`top/left`排列；Shift+Tab反向，跳过隐藏、禁用及label等不可聚焦项。

启动时采用虚拟键盘模式，单独按下Pause切换实体模式。Ctrl+Pause和Ctrl+Alt+Pause是全局快捷键，在两种模式及没有当前窗口时均有效；Alt+Shift、Ctrl+Shift仅在实体模式且存在有效当前窗口时处理。退出实体模式时清除尚未派发的输入法切换请求。当前窗口失效时解除拦截，Pause选定的键盘模式保留；后续选中有效窗口时按该模式恢复路由。实体模式下，Engine按输入区开关选择直接送SDK或先送IME。按钮等非文本控件通过当前窗口SDK接收按键。

服务托管时，Helper通过独立的已认证管道向Engine同步键盘状态。切换输入桌面时清空瞬态键态，释放旧路由中仍按下的键。安全桌面上的Helper只登记Pause热键，向Engine发送模式切换请求。普通按键留在Windows活动桌面。

Ctrl+Alt+Pause执行全局Body中心和World偏移重置，在两种键盘模式及窗口已选中或未选中时均生效，并保留当前键盘模式。Windows将该组合报告为Ctrl+Alt+Break时采用相同处理。头显暂时失去跟踪时，请求保留到有效姿态恢复后执行。重置成功且头显姿态有效时，Engine在新的World原点显示朝向头显的红色十字提示15秒，再次重置刷新15秒计时。

实体键盘模式且存在有效当前窗口时，按下`PrintScreen`复制当前VR视角（捕获前收起已有截图提示并等待隐藏帧），按下`Alt+PrintScreen`复制当前选中普通窗口的D3D平面纹理图像；两种截图均以PNG与Windows位图格式写入剪贴板，并在写入成功后在视野中央显示约2秒的头显相对、输入穿透提示浮窗。

Ctrl+Pause切换配置中Desktop应用窗口的显示与隐藏。首次调用启动程序，后续调用复用仍在运行的进程和窗口；每次显示时在当前头显正前方定位一次，采用world参考对象，然后提升并选中窗口。显示期间窗口保持该世界姿态。Desktop通过普通SDK会话创建窗口，配置和生命周期见“Desktop应用”。

实体键盘模式且存在有效当前窗口时，Alt+Shift循环切换IME语言，并恢复目标语言上次使用的IME；Ctrl+Shift只在当前语言内循环切换IME。切换按组件选择与排空流程执行，layout独立选择，键盘模式保持当前值。

当前窗口切换时，Engine先完成原输入路径的事件排空，再关闭原输入区、输入条与IME/layout界面并切换当前窗口。窗口关闭、隐藏、禁用、转为辅助表面、参考姿态失效或所属会话断开时，立即清理其当前窗口资格与键盘拦截；可交互状态失效时取消相应激光捕获，并完成旧输入路径清理。控件间的焦点变化由SDK处理。

输入条、layout与IME的界面使用`auxiliary=true`的辅助表面。输入条由当前应用的SDK创建，layout与IME界面由组件SDK创建；点击时激光事件交给对应表面所属会话，当前应用窗口保持选中，键盘沿当前窗口的输入路径分发。

#### 输入状态转换

|操作|当前窗口|输入区|后续路由|
|---|---|---|---|
|激光选择另一个普通窗口|切换为新窗口|关闭旧输入区|先按关闭输入区的路径处理，新窗口SDK按需唤起|
|再次选择当前窗口|保持|保持|保持原路径|
|`show_input_ui`|保持关联窗口|开启，或更新输入区矩形及组件开关|按开关选择layout和IME，IME关闭时按键直接送窗口SDK|
|`hide_input_ui`|保持|排空后关闭|直接送窗口SDK|
|Pause切换键盘模式|保持|保留开启状态及矩形|按新模式选用layout或实体键盘来源|
|选择另一个layout或IME|保持|保留开启状态及矩形|排空旧组件后启用新组件|
|重复选择已活动组件|保持|保持|保持原路径|
|活动输入组件断线|保留有效当前窗口|保留关联矩形，进入恢复阶段|输入区开启时暂存新输入，组件恢复后重建路径|
|当前窗口关闭、隐藏、禁用或转为辅助表面|清理原选择，按接替与恢复规则确定新窗口|关闭|释放旧窗口的实体键盘拦截资格|
|同一应用内的禁用接替与恢复|切换为可接替或已重新启用的窗口|关闭旧输入区|新窗口SDK按需恢复控件焦点与输入界面|
|当前窗口参考姿态失效|清空|关闭|解除对应实体键盘拦截，取消失效捕获|

只有改变旧输入路径的操作执行排空。更新同一输入区的几何信息、重复选择当前窗口或已活动组件时保留原处理状态。同一窗口的`show_input_ui`仅变更矩形时直接更新位置，变更任一组件开关时串行排空旧路径再应用新配置。切换控件时，SDK在隐藏完成后唤起新输入区。重复点击同一文本框时，SDK根据输入区是否开启决定唤起界面。

### 输入条、IME与Layout界面

#### 唤起输入界面：`show_input_ui`

请求包含关联`window`、输入区`rectangle`和公共请求字段。可选布尔字段`enable_virtual_keyboard`和`enable_ime`分别控制虚拟键盘及IME，各自省略时取`true`。`rectangle`包含有限数值`left`、`top`、`width`、`height`，相对于关联窗口左上角，使用窗口逻辑单位，宽高大于零。Engine按关联窗口的尺寸与空间姿态定位输入界面。

请求会话须为普通应用角色，关联窗口须属于该会话，并且是Engine当前选中的、可见并启用的普通窗口。启用IME时，SDK创建独立输入条，显示当前语言、具体IME名称及“输入法切换”按钮。虚拟键盘模式下，已启用的输入条、可见的IME候选界面和活动layout从上到下依次排列在输入区下方。

实体键盘模式下，输入条的右上角贴合当前窗口的右下角，随窗口移动、旋转和缩放。IME候选界面在光标行的输入区下方居中。对于曲面窗口，辅助界面沿各自锚点的切平面放置。

`enable_ime=true`要求当前应用选中的IME可用。虚拟键盘模式下，`enable_virtual_keyboard=true`要求活动layout可用。组件暂未就绪时返回业务失败，调用方可查询组件状态并在就绪后重试。成功响应表示输入区关联已建立、相应状态已推送，具体界面由组件异步绘制。

输入区按指定开关启用组件。IME关闭时，实体键盘和活动layout的按键直接投递给当前窗口。文本、选区、可编辑性及字符限制由SDK维护。同一窗口切换到新的文本输入目标时，SDK先请求结束原输入区，保留旧控件为输入目标并处理其收尾事件；隐藏完成后再切换本地控件焦点，为新目标唤起输入区。

请求：

```json
{
    "message_type": "request",
    "id": 30,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "op": "show_input_ui",
    "window": 100,
    "enable_virtual_keyboard": true,
    "enable_ime": false,
    "rectangle":
    {
        "left": 24.0,
        "top": 124.0,
        "width": 590.0,
        "height": 42.0
    }
}
```

成功响应：

```json
{
    "message_type": "response",
    "id": 30,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "ok": true,
    "value": null
}
```

#### 关闭输入界面：`hide_input_ui`

输入区已关闭时直接成功返回。输入区开启时，关联窗口所属会话或当前活动输入组件可以请求关闭。完成排空、清除输入区关联并推送关闭状态后返回成功，后续按键由Engine直接送给当前窗口SDK，当前窗口保持选中。应用SDK与组件SDK收到状态后分别收起输入条和各自界面。

请求：

```json
{
    "message_type": "request",
    "id": 31,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "op": "hide_input_ui"
}
```

成功响应：

```json
{
    "message_type": "response",
    "id": 31,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "ok": true,
    "value": null
}
```

激光切换当前窗口时，Engine自动关闭原输入界面。新窗口的SDK按需唤起自己的输入界面。同一输入区移动或调整尺寸时，SDK重复调用`show_input_ui`更新矩形；切换输入控件时，先等待`hide_input_ui`排空完成，再为新控件调用`show_input_ui`。

### Layout与IME组件

#### 注册输入组件：`input_provider_register`

layout、IME都是普通独立应用，通过自己的已鉴权会话注册。`role`必填且只能为`layout`或`ime`；`name`可省略，动态组件会获得生成名称；`default_provider`可省略，默认`false`。IME可附带字符串`language`，省略时为`en`；layout省略该字段。常用语言代码为`zh`、`en`、`ja`，分别表示中文、英文、日文，也接受其它非空语言代码。

会话初始为普通应用角色。注册成功后固定为layout或IME角色，直至连接关闭；同角色重复注册沿用已有组件身份，改为其它角色返回业务错误。注册前须关闭本会话全部普通表面及关联输入区，存在此类资源时注册返回业务错误并保持原角色。组件会话仅创建辅助表面，输入区由普通应用会话开启。配置启动的组件通过已验证的进程身份匹配已有记录。`default_provider=true`表示优先沿用已有活动组件；注册时该角色暂无活动组件、当前组件被明确选中，或`default_provider=false`时，新组件可成为活动组件。涉及替换时先完成旧路径排空；注册成功表示会话登记完成，活动选择通过组件列表确认。

请求：

```json
{
    "message_type": "request",
    "id": 40,
    "session_id": 2,
    "session_token": "<layout会话令牌>",
    "op": "input_provider_register",
    "role": "layout",
    "name": "standard_104",
    "default_provider": true
}
```

成功响应：

```json
{
    "message_type": "response",
    "id": 40,
    "session_id": 2,
    "session_token": "<layout会话令牌>",
    "ok": true,
    "value": null
}
```

#### IME注册示例

请求：

```json
{
    "message_type": "request",
    "id": 41,
    "session_id": 3,
    "session_token": "<IME会话令牌>",
    "op": "input_provider_register",
    "role": "ime",
    "name": "EasyVRUI English",
    "language": "en",
    "default_provider": true
}
```

成功响应：

```json
{
    "message_type": "response",
    "id": 41,
    "session_id": 3,
    "session_token": "<IME会话令牌>",
    "ok": true,
    "value": null
}
```

#### 查询输入组件：`input_provider_list`

返回全局组件列表。每项`id`标识组件，`state`为`stopped`、`starting`或`running`。`configured`表示来自持久配置，`active`表示该角色当前被选中。IME项包含`language`语言代码，layout项省略该字段。`name`为组件显示名称，来自持久配置或动态注册，内置英文、中文和日文IME分别为`EasyVRUI English`、`EasyVRUI拼音`和`EasyVRUI日本語`；输入条分别显示语言类别与具体IME名称。`process_id`为已关联的本机进程PID，缺省为`0`；`error`是失败说明字符串，正常为空。配置条目ID在本轮Engine运行期间保持稳定，动态条目退出后移除。SDK按实际返回的当前组件ID发起后续操作。

请求：

```json
{
    "message_type": "request",
    "id": 42,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "op": "input_provider_list"
}
```

成功响应：

```json
{
    "message_type": "response",
    "id": 42,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "ok": true,
    "value":
    [
        {
            "id": 1,
            "name": "standard_104",
            "role": "layout",
            "state": "running",
            "configured": true,
            "active": true,
            "process_id": 23457,
            "error": ""
        },
        {
            "id": 2,
            "name": "EasyVRUI English",
            "role": "ime",
            "language": "en",
            "state": "running",
            "configured": true,
            "active": true,
            "process_id": 23458,
            "error": ""
        },
        {
            "id": 3,
            "name": "custom_layout",
            "role": "layout",
            "state": "running",
            "configured": false,
            "active": false,
            "process_id": 23459,
            "error": ""
        }
    ]
}
```

#### 启动输入组件：`input_provider_start`

按已有`provider_id`启动配置程序，组件已启动时也可成功返回。`true`表示已接受请求或启动流程已开始，注册完成后列表状态变为`running`。未知ID、启动失败等使用公共失败响应。

请求：

```json
{
    "message_type": "request",
    "id": 43,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "op": "input_provider_start",
    "provider_id": 1
}
```

成功响应：

```json
{
    "message_type": "response",
    "id": 43,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "ok": true,
    "value": true
}
```

#### 选择输入组件：`input_provider_select`

选择相应角色的全局活动组件。目标已运行时按排空流程切换；尚未启动时先尝试启动，待完成注册和旧路径排空后切换，等待期间保持原活动组件。调用方通过`input_provider_list`查询目标`state="running"`且`active=true`，确认切换完成，也可消费收到的组件列表快照。目标启动或注册失败时，列表记录错误并保留原活动组件。layout与IME各自有一个全局活动项。

IME按`language`分组，选择某个IME同时确定当前输入语言。Alt+Shift循环切换语言并恢复各语言上次使用的IME，Ctrl+Shift循环切换当前语言内的IME；具体组件选择仍使用已有的`input_provider_select`流程。SDK输入方式对话框分别显示独立layout列表、语言列表及按语言过滤的IME列表，各语言的暂选在点击“确定”后应用，取消时丢弃。常用语言显示本地化名称，其它代码可直接显示。

点击输入条上的“输入法切换”按钮后，SDK先排空并收起输入条、IME和layout，再打开内置输入方式选择对话框。对话框沿用关联窗口的逻辑像素到米的缩放比例，在关联窗口附近居中定位，然后固定于world参考对象。关联窗口后续移动或旋转时，对话框保持已确定的世界姿态；关闭后返回原输入控件并按输入区状态恢复输入界面。应用自定义对话框采用SDK对话框规则及应用指定的参考关系；输入条、IME与layout表面采用`auxiliary=true`，由Engine自动跟随输入区。

成功响应表示选择请求已受理。每个角色按受理顺序维护选择队列，后续目标即使先完成注册，也等待同角色前面的选择完成或失败。等待启动期间保留原输入路径，其它窗口操作仍按输入事件队列处理。调用方会话断开时取消其尚未完成的选择。

显式选择优先于组件注册引发的未提交自动接管。选择当前活动项可以取消这类自动接管；已经发出的排空请求仍完成收尾，活动组件保持原选择。多个显式选择继续按各自角色的队列顺序处理。

请求：

```json
{
    "message_type": "request",
    "id": 44,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "op": "input_provider_select",
    "provider_id": 2
}
```

成功响应：

```json
{
    "message_type": "response",
    "id": 44,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "ok": true,
    "value": true
}
```

#### 发送输入事件：`input_provider_send`

输入区开启时，活动layout与IME通过此操作提交事件。Engine检查发送者角色、当前窗口、输入区及排空阶段，再按固定路线转发。

请求先通过当前连接的`session_id/session_token`校验。组件角色来自Engine保存的注册记录，事件目的端由当前路由确定：

|发送者|允许事件|目的端|
|---|---|---|
|当前活动layout|`key_down`、`key_up`|活动IME，或在IME关闭时送至当前窗口所属session|
|当前活动IME|`key_down`、`key_up`、`ime_submit`|当前窗口所属session|

Engine通过事件排空握手串行化输入路径切换。排空期间固定原窗口及session作为旧事件目的端，完成后启用新的路由。

正常输入按当前活动组件和窗口校验；排空期间按被冻结的旧窗口、组件连接和阶段校验。窗口已关闭或隐藏时，旧路径仍可完成排空确认；结果仅在原目标仍有效时投递，资源已失效时结束该旧目标的投递。

* layout发送`key_down/key_up`给活动IME，IME关闭时由Engine直接投递给当前窗口。新的按下事件来自可见的虚拟键盘；按键释放用于结束当前输入路径中此前的按下状态。
* IME消费自己使用的按键，转发其余`key_down/key_up`给当前窗口SDK。IME负责配对维护按下与释放状态。
* IME使用`ime_submit`提交最终文本，`text`为JSON字符串；Engine将文本转发给当前窗口所属session，再由SDK应用到本地输入控件。

`key_down/key_up`须提供字符串`key`，可选`text`为字符串，`shift/ctrl/alt/meta`为布尔值，省略时为`false`；`ime_submit`须提供字符串`text`。Engine按注册角色校验允许的事件类型，并生成`message_type`、`session_id/session_token`、目标`window`等路由字段。

`key`表示按键身份，字母使用小写`a`至`z`，数字使用`0`至`9`。功能键使用`Backspace`、`Tab`、`Enter`、`Escape`、`Space`、`Left`、`Right`、`Up`、`Down`、`Home`、`End`、`PageUp`、`PageDown`、`Insert`、`Delete`、`Shift`、`Ctrl`、`Alt`、`Meta`、`CapsLock`、`NumLock`、`ScrollLock`、`Pause`、`PrintScreen`及`F1`至`F24`。实体键盘其它按键使用`vk_`加Windows虚拟键码的十进制数字。左右同类修饰键使用相同名称，`meta`表示Win键状态。

`text`保存布局转换后的字符，包含大小写、标点及所选键盘布局的转换结果；同一个`key`可以产生不同的`text`。组件通过`text`提供可打印字符，IME据此提交最终文本。自动重复使用连续`key_down`，一次真实释放以`key_up`结束按住状态。IME决定消费或转发整个按住状态，并为已转发的按下配对释放。

提交的`event`对象使用`event_type`及对应参数。Engine根据已注册角色确定目的端，转发时统一封装为`message_type="event"`。

layout发送按键：

```json
{
    "message_type": "request",
    "id": 45,
    "session_id": 2,
    "session_token": "<layout会话令牌>",
    "op": "input_provider_send",
    "event":
    {
        "event_type": "key_down",
        "key": "a",
        "text": "a",
        "shift": false,
        "ctrl": false,
        "alt": false,
        "meta": false
    }
}
```

成功响应：

```json
{
    "message_type": "response",
    "id": 45,
    "session_id": 2,
    "session_token": "<layout会话令牌>",
    "ok": true,
    "value": null
}
```

#### IME提交文本事件：`ime_submit`

IME将最终提交的文本放入`event.event_type="ime_submit"`的事件。输入法的预编辑文本、候选项、选词操作和候选窗口由IME应用维护。候选窗口使用普通辅助表面及标准绘图、激光事件接口实现。

内置中日文候选窗口展示组合文本、候选项与输入模式。实体键盘模式下，活动IME有组合文本或候选项时显示候选窗口，上屏或清空组合后自动收起。虚拟键盘模式下，活动IME的候选窗口始终显示。中文原生模式按钮显示“拼音”，日文原生模式按钮显示“かな”，临时英文输入模式显示“ABC”。语言类别与具体IME身份由输入条显示，英文直通IME由输入条展示状态。

请求：

```json
{
    "message_type": "request",
    "id": 46,
    "session_id": 3,
    "session_token": "<IME会话令牌>",
    "op": "input_provider_send",
    "event":
    {
        "event_type": "ime_submit",
        "text": "hello"
    }
}
```

成功响应：

```json
{
    "message_type": "response",
    "id": 46,
    "session_id": 3,
    "session_token": "<IME会话令牌>",
    "ok": true,
    "value": null
}
```

#### IME转发按键

例如Tab由应用SDK处理，IME直接转发该按键事件：

```json
{
    "message_type": "request",
    "id": 47,
    "session_id": 3,
    "session_token": "<IME会话令牌>",
    "op": "input_provider_send",
    "event":
    {
        "event_type": "key_down",
        "key": "Tab",
        "shift": false,
        "ctrl": false,
        "alt": false,
        "meta": false
    }
}
```

成功响应：

```json
{
    "message_type": "response",
    "id": 47,
    "session_id": 3,
    "session_token": "<IME会话令牌>",
    "ok": true,
    "value": null
}
```

文字输入通过`ime_submit`交给SDK；转发的按键用于快捷键、导航等按键处理。IME维护自己的组合和候选状态，SDK维护应用文本与选区。

#### 按键路由

|输入区状态|键盘模式|路由|
|---|---|---|
|关闭|实体键盘拦截开启|实体键盘 → Engine → 当前窗口SDK|
|开启|虚拟键盘|layout → Engine → IME → Engine → 当前窗口SDK|
|开启|实体键盘|实体键盘 → Engine → IME → Engine → 当前窗口SDK|

输入区关闭时，按键由Engine直接推送到当前窗口所属session；该路径按Pause控制实体键盘拦截。输入区开启时，IME决定消费按键、转发按键或提交文本。应用SDK按窗口内的控件焦点分发收到的事件。

Engine负责窗口级路由、输入区矩形、键盘模式、组件会话和事件转发。IME负责输入算法、组合缓冲、候选窗口及选词交互。切换窗口或关闭输入区时，先完成layout与IME的事件排空，再清理原按键状态并启用新的路径。

#### 输入路径切换与事件排空

隐藏输入界面、切换当前窗口、改变键盘模式或替换输入组件时，Engine按以下顺序完成旧路径的排空。同一时刻串行处理一次输入路径切换。

1. 暂停向旧路径投递新按键，将切换期间的新输入暂存到内部队列。排空Engine已进入旧路径的事件，固定旧窗口及session作为这些事件的目的端。
2. 向旧layout发送`input_drain`。layout暂停产生新按键，处理完已有操作，将待发事件及配对的释放事件按连接顺序发出，然后提交`input_provider_drained`。
3. Engine收到layout确认后，先将此前的layout事件全部转入旧IME连接的发送队列，再向旧IME发送`input_drain`。
4. IME处理完排队按键及其已经启动的异步任务，发送已产生的按键、文本提交和释放事件，清理临时输入状态，然后提交`input_provider_drained`。
5. Engine按序转发IME的旧结果。收到IME确认时，此前结果已经排入原窗口连接的发送队列，随后完成本次输入路径切换，并推送新的状态。
6. 恢复按键投递，将暂存的新输入交给新的路径。

仅参与旧路径的组件需要排空。每条组件连接同时只处理一个排空请求，确认按连接身份与当前排空阶段匹配，组件对每个请求恰好提交一次确认。当前没有待确认阶段或确认连接不匹配时返回业务错误。确认消息通过连接身份匹配，组件负责避免将前次确认重复发送到后续排空阶段。layout确认后停止旧layout事件的发送资格；IME确认后结束旧IME事件的发送资格。组件在收到新激活状态后开始处理新输入。

所有旧事件及其确认按同一连接的FIFO顺序发送。排空确认表示组件已经结束本次全部异步工作，并将其全部结果排入确认之前的发送队列。Engine按串行事件队列处理消息，并按连接顺序推送应用事件。

排空采用异步握手，Engine与SDK继续处理消息和心跳。发起隐藏操作的组件同样需要处理排空请求，SDK通过异步等待保持该通路可运行。排空等待覆盖旧输入数据任务，管理操作的等待由控制流程处理。输入处理回调先完成本次数据输出，再将隐藏或组件选择操作调度到控制队列。隐藏请求在排空完成、输入区关联清除及关闭状态推送后返回成功。

SDK将隐藏请求的完成通知作为本地处理屏障：先按连接顺序执行此前旧输入事件的框架分发及文本编辑，再通知业务代码该请求完成。等待采用异步方式，保持输入分发可运行；完成后才修改本地输入控件并开启新输入区。

每个组件排空请求发出后，确认期限为10秒，心跳检测独立进行。超时或断线时，关闭旧连接、撤销发送资格并清理队列，再按组件故障策略继续切换。排空结果绑定旧窗口身份，目标已失效时清理旧路径及相关资源。

窗口选择、显示或关闭输入区、模式切换和组件替换按Engine事件队列顺序执行；排空确认、心跳及旧路径完成消息继续处理。触发窗口切换的按下及后续同手事件暂存，在新窗口获焦后按顺序投递。切换期间的新按键按其在队列中的位置交给对应的新路径，连续切换依次完成。

组件故障导致输入等待恢复时，Engine继续处理恢复所需的组件注册与启动，使新连接能够建立输入路径。已排队的窗口选择、输入区变化和模式切换保持与输入事件的先后顺序；恢复后，先前输入仍沿其对应路径投递，再执行后续切换。

窗口SDK按连接内顺序先接收旧结果，再处理失焦、获焦及新路由事件。

旧路径中已投递的按住状态在排空期间通过释放事件结束。仍被实体按住的按键等待真实释放后，再向新路径接受下一次按下；自动重复属于原按住状态。SDK在窗口失焦时清理本地按键状态，避免将旧按下对应的释放解释为新窗口的操作。

#### 确认事件排空：`input_provider_drained`

Engine仅接受当前等待确认的那条组件连接提交此操作。组件先将全部旧事件排入发送队列，再按顺序发送确认。请求只包含公共字段：

```json
{
    "message_type": "request",
    "id": 48,
    "session_id": 2,
    "session_token": "<layout会话令牌>",
    "op": "input_provider_drained"
}
```

成功响应：

```json
{
    "message_type": "response",
    "id": 48,
    "session_id": 2,
    "session_token": "<layout会话令牌>",
    "ok": true,
    "value": null
}
```

### 剪贴板、全局设置与跟踪中心

#### 读取剪贴板：`clipboard_get`

读取Engine所在Windows会话的系统剪贴板文本。文本格式或底层接口不可用时返回`null`，可读取的空文本返回`""`。

请求：

```json
{
    "message_type": "request",
    "id": 50,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "op": "clipboard_get"
}
```

成功响应：

```json
{
    "message_type": "response",
    "id": 50,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "ok": true,
    "value": "hello"
}
```

无可读取文本时：

```json
{
    "message_type": "response",
    "id": 50,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "ok": true,
    "value": null
}
```

#### 写入剪贴板：`clipboard_set`

`text`为UTF-8 JSON字符串，写入Engine所在Windows会话的剪贴板。包含U+0000的文本返回`value:false`，剪贴板保持原内容。底层操作失败时，成功响应中的`value`为`false`；业务异常采用`ok:false`响应。

请求：

```json
{
    "message_type": "request",
    "id": 51,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "op": "clipboard_set",
    "text": "hello"
}
```

成功响应：

```json
{
    "message_type": "response",
    "id": 51,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "ok": true,
    "value": true
}
```

#### 读取全局设置：`settings_get`

`name`接受`laser_position_offset`与`laser_rotation_offset`。前者为控制器局部空间位置偏移，单位米；后者为三轴欧拉角偏移，单位度。

请求：

```json
{
    "message_type": "request",
    "id": 52,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "op": "settings_get",
    "name": "laser_position_offset"
}
```

成功响应：

```json
{
    "message_type": "response",
    "id": 52,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "ok": true,
    "value":
    [
        0.0,
        0.0,
        0.0
    ]
}
```

#### 修改全局设置：`settings_set`

`value`必须是三个有限数值。返回设置后的值，作用于整个Engine的运行时激光配置；两种偏移的初始值均为零，表示设计基准姿态。

请求：

```json
{
    "message_type": "request",
    "id": 53,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "op": "settings_set",
    "name": "laser_rotation_offset",
    "value":
    [
        0.0,
        0.0,
        0.0
    ]
}
```

成功响应：

```json
{
    "message_type": "response",
    "id": 53,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "ok": true,
    "value":
    [
        0.0,
        0.0,
        0.0
    ]
}
```

#### 重置body跟踪中心：`body_reset`

以当前头显位置和完整四元数记录新的body参考中心与朝向；之后body跟踪经颈部枢轴补偿的XYZ平移，保持该参考朝向。校准瞬间body中心位于头显位置，转头产生的枢轴位移依据名义颈部模型补偿，行走或空间平移继续传递给body。当前头显姿态不可用时返回`false`。此请求重置全局body参考系并发布跟踪更新；Ctrl+Alt+Pause同时重置body中心和World偏移。

请求：

```json
{
    "message_type": "request",
    "id": 54,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "op": "body_reset"
}
```

成功响应：

```json
{
    "message_type": "response",
    "id": 54,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "ok": true,
    "value": true
}
```

#### 查询本会话窗口数：`ping`

返回当前连接会话拥有的窗口数，包括隐藏窗口及辅助表面，缺省为零。此操作用于业务查询，自动心跳按前述规则独立发送。

请求：

```json
{
    "message_type": "request",
    "id": 55,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "op": "ping"
}
```

成功响应：

```json
{
    "message_type": "response",
    "id": 55,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "ok": true,
    "value":
    {
        "window_count": 1
    }
}
```

#### 查询应用列表：`application_list`

由已验证的本机会话发起，仅填写公共请求字段。返回的`value`是引擎本机已验证应用的快照数组，每项包含`session_id/process_id/name/memory_bytes/cpu_percent/gpu_percent/window_list`。`name`是会话注册时上报的会话名称。`memory_bytes`是常驻内存字节数，`cpu_percent`与`gpu_percent`是采样窗口内的占用百分比。`window_list`是该会话拥有的窗口数组，每项包含`id/name/title/visible`，其中`id`是全局窗口ID。列表包含Desktop及仍在运行的普通本机应用。引擎根据已验证的本机进程身份查询进程指标。

请求：

```json
{
    "message_type": "request",
    "id": 57,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "op": "application_list"
}
```

成功响应：

```json
{
    "message_type": "response",
    "id": 57,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "ok": true,
    "value":
    [
        {
            "session_id": 2,
            "process_id": 23457,
            "name": "demo_cpp",
            "memory_bytes": 52428800,
            "cpu_percent": 3.5,
            "gpu_percent": 1.2,
            "window_list":
            [
                {
                    "id": 100,
                    "name": "translator_01",
                    "title": "Translator 01",
                    "visible": true
                }
            ]
        }
    ]
}
```

#### 结束应用或关闭窗口：`application_terminate`

由已验证的本机会话发起。`session_id`为调用方会话，`target_session_id`为目标普通应用会话，Desktop使用独立的生命周期。省略`window`时，Engine结束目标应用进程。提供`window`时，使用应用列表返回的全局窗口ID。Engine核对窗口归属后发送`window_close`事件，由目标SDK处理窗口关闭。

关闭窗口请求：

```json
{
    "message_type": "request",
    "id": 56,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "op": "application_terminate",
    "target_session_id": 2,
    "window": 100
}
```

结束整个应用时省略`window`。成功响应的`value`是布尔值：`true`表示结束进程成功，或窗口关闭事件已送达目标会话；`false`表示目标无效或窗口归属不符。窗口是否最终关闭取决于目标SDK的`on_closing`处理结果，可通过后续应用列表确认。

### Engine主动推送

所有事件统一使用`message_type="event"`，通过`event_type`区分具体类型，并包含接收连接的`session_id/session_token`。事件与响应共用帧流，心跳结构见前述章节。

|event_type|用途|
|---|---|
|`pointer`|激光命中、移动与按压状态|
|`tracking`|空间跟踪状态|
|`input_drain`|要求输入组件排空事件|
|`input_ui_state`|输入界面及路由状态|
|`key_down`、`key_up`|按键按下与释放|
|`ime_submit`|IME提交最终文本|
|`focus_in`、`focus_out`|窗口获焦与失焦|
|`window_visibility`|要求SDK设置指定窗口的可见性|
|`window_close`|要求SDK按正常关闭流程关闭指定窗口|
|`render_error`|异步绘图错误|
|`screen_state`|屏幕捕获可用性、尺寸及帧率|
|`global_pointer_down`|手柄按键按下边沿，广播给已鉴权会话|
|`global_pointer_up`|手柄按键释放边沿，广播给已鉴权会话|

连续移动和跟踪快照可以在尚未发送的同一合并区间内替换为最新值。按下、释放、目标丢失、窗口焦点变化、窗口可见性要求、排空通知及排空确认构成顺序边界；边界两侧的事件各自保持所属区间。按键和文本提交按入队顺序投递。

#### 激光消息：`pointer`

发送给当前命中或捕获窗口的所属会话。`left/top`是窗口逻辑坐标；`origin/direction/rotation`是世界射线及手柄激光姿态。`world_position/world_rotation`在窗口世界姿态可解析时附带，表示窗口几何中心姿态，其中旋转使用四元数。

命中检测使用窗面的完整逻辑矩形，透明像素也参与命中。未捕获时，Engine在可见且姿态有效的窗面中选择最近的交点，距离相同时选择后创建的窗口。激光止于该交点，最近窗面启用且符合手别限制时才接收指针交互。捕获后按捕获规则继续投递。可交互窗口的边缘外扩64逻辑像素只用于延续激光显示，实际窗面交点优先。

示例窗口左上角的世界坐标为`(0, 1.6, -1)`，每逻辑单位对应0.001米。`left=120`、`top=80`的世界交点为`(0.12, 1.52, -1)`，与示例射线相交。

`hand`取`left`或`right`，`window`为接收会话的窗口局部ID。有效更新包含`left/top`、`trigger/grip`、`joystick`、`primary/secondary`、三维`origin/direction`及四元数`rotation`；`origin`使用米，`direction`为方向向量。`world_position/world_rotation`成对提供。

`trigger`表示扳机，`grip`表示侧握键，`true`表示按下，`false`表示松开。SDK使用扳机操作控件，使用侧握键抓取窗口并调整三维位置与旋转。`primary`对应左手X或右手A，`secondary`对应左手Y或右手B，同样使用布尔状态。`joystick.x/y`为0～255整数，中立值为128；X从左到右递增，Y从下到上递增。`joystick.pressed`表示摇杆垂直按压。缺少对应硬件或绑定时，按钮状态为`false`，摇杆坐标为128。

Engine分别跟踪两只手的激光命中和捕获。指向窗口、且未按下扳机或侧握键时，摇杆Y轴越过18%死区后产生垂直滚轮步数。推杆幅度越大，步频越高。`pointer.scroll`携带本次步数，负数向上、正数向下、零表示本次没有滚动。`screen`将步数换算为Windows滚轮方向。

窗口收到的逻辑坐标使用速度自适应滤波。支持模拟扳机的手柄在轻触阈值处记录稳定落点，按下时将合适的落点用于点击。按下后移动未超过12逻辑像素时保持按下点。悬停时，3D光束使用SteamVR的`/pose/tip`实时射线；姿态不可用时，光束过渡到带位置和旋转校准的手柄跟踪射线。按下冻结和锁定捕获期间，光束指向锁定点。

SteamVR按命中或捕获状态为左右手分别提交交互动作集优先级，两手互相独立：处于有效命中或捕获的手使用Overlay全局高优先级，退出交互后回到普通优先级；姿态动作集保持普通优先级。命中或捕获到有效目标交点时，Engine在交点处沿曲面切平面显示随头显距离自适应限幅的命中圆点；边缘外扩仅用于维持光束预提示。

命中或捕获更新：

```json
{
    "message_type": "event",
    "event_type": "pointer",
    "session_id": 1,
    "session_token": "<会话令牌>",
    "window": 100,
    "hand": "right",
    "left": 120.0,
    "top": 80.0,
    "trigger": true,
    "grip": false,
    "joystick":
    {
        "x": 128,
        "y": 128,
        "pressed": false
    },
    "primary": false,
    "secondary": false,
    "origin":
    [
        0.12,
        1.52,
        0.0
    ],
    "direction":
    [
        0.0,
        0.0,
        -1.0
    ],
    "rotation":
    [
        0.0,
        0.0,
        0.0,
        1.0
    ],
    "world_position":
    [
        0.32,
        1.42,
        -1.0
    ],
    "world_rotation":
    [
        0.0,
        0.0,
        0.0,
        1.0
    ]
}
```

离开或丢失跟踪：

```json
{
    "message_type": "event",
    "event_type": "pointer",
    "session_id": 1,
    "session_token": "<会话令牌>",
    "window": 100,
    "hand": "right",
    "lost": true
}
```

`lost:true`表示目标丢失，此时坐标和控制器状态为可选字段。扳机、侧握键、摇杆按压、面键的按下与释放、滚轮步数以及离开消息保序，普通连续移动和摇杆坐标更新可合并为最新值。

#### 跟踪消息：`tracking`

发送给拥有可见窗口的会话，窗口首次可见或重新可见时发送完整快照，之后在状态变化时发布。`frame_map`和`reference_map`均为该次完整快照；SDK整体替换相应缓存，移除已省略的窗口项。队列可合并尚未发送的旧跟踪快照。`world_origin`是Engine world原点姿态；`frame_map`包含head、left、right、body，失去跟踪的项目为`null`。`reference_map`列出本会话当前可见窗口，键是窗口局部ID的十进制字符串，值为参考对象的世界姿态；窗口自身的position/rotation作为相对偏移另行应用。可见窗口的参考姿态不可解析时值为`null`；隐藏或关闭的窗口项从快照中移除。

推送：

```json
{
    "message_type": "event",
    "event_type": "tracking",
    "session_id": 1,
    "session_token": "<会话令牌>",
    "world_origin":
    {
        "position":
        [
            0.0,
            1.6,
            -1.0
        ],
        "rotation":
        [
            0.0,
            0.0,
            0.0,
            1.0
        ]
    },
    "frame_map":
    {
        "head":
        {
            "position":
            [
                0.0,
                1.6,
                0.0
            ],
            "rotation":
            [
                0.0,
                0.0,
                0.0,
                1.0
            ]
        },
        "left": null,
        "right":
        {
            "position":
            [
                0.12,
                1.52,
                0.0
            ],
            "rotation":
            [
                0.0,
                0.0,
                0.0,
                1.0
            ]
        },
        "body":
        {
            "position":
            [
                0.0,
                1.6,
                0.0
            ],
            "rotation":
            [
                0.0,
                0.0,
                0.0,
                1.0
            ]
        }
    },
    "reference_map":
    {
        "100":
        {
            "position":
            [
                0.0,
                1.6,
                -1.0
            ],
            "rotation":
            [
                0.0,
                0.0,
                0.0,
                1.0
            ]
        }
    }
}
```

#### 组件排空事件：`input_drain`

Engine按旧layout、旧IME的顺序向参与切换的组件发送此消息。组件根据自己的连接身份处理请求，并在全部旧事件及异步工作完成后提交`input_provider_drained`。

Engine → layout：

```json
{
    "message_type": "event",
    "event_type": "input_drain",
    "session_id": 2,
    "session_token": "<layout会话令牌>"
}
```

Engine收到layout排空确认并转发完其已有事件后，向IME发送：

```json
{
    "message_type": "event",
    "event_type": "input_drain",
    "session_id": 3,
    "session_token": "<IME会话令牌>"
}
```

#### 输入界面状态：`input_ui_state`

发送给已注册输入组件及相关普通应用SDK。当前窗口、界面显示或键盘模式变化时，通知活动layout、IME和关联应用；组件列表变化时通知已注册组件及当前应用，可附带`provider_list`完整快照。该字段结构与`input_provider_list`查询结果一致，省略时沿用原列表，显式`[]`表示空列表。应用SDK据此显示输入条中的当前语言和具体IME名称。

`active`表示组件实际参与当前输入路径：组件须处于被选中、对应开关开启、输入区开启且当前窗口有效的状态。layout还须处于虚拟键盘模式。具体候选窗口的显示与内容由IME控制。`rectangle`在组件参与该路径时保存窗口局部输入矩形，其余情况为`null`。输入条及组件表面由Engine按辅助表面规则定位。

`input_ui_state`中的`active`描述组件是否参与当前输入路径；`provider_list`各项的`active`描述该角色被选中的组件。实体模式下，被选中的layout在组件列表中仍为`active=true`，其输入状态为`active=false`、`rectangle=null`。

输入界面显示时：

```json
{
    "message_type": "event",
    "event_type": "input_ui_state",
    "session_id": 2,
    "session_token": "<layout会话令牌>",
    "physical": false,
    "active": true,
    "rectangle":
    {
        "left": 24.0,
        "top": 124.0,
        "width": 590.0,
        "height": 42.0
    },
    "provider_list":
    [
        {
            "id": 1,
            "name": "standard_104",
            "role": "layout",
            "state": "running",
            "configured": true,
            "active": true,
            "process_id": 23457,
            "error": ""
        },
        {
            "id": 2,
            "name": "EasyVRUI English",
            "role": "ime",
            "language": "en",
            "state": "running",
            "configured": true,
            "active": true,
            "process_id": 23458,
            "error": ""
        },
        {
            "id": 3,
            "name": "custom_layout",
            "role": "layout",
            "state": "running",
            "configured": false,
            "active": false,
            "process_id": 23459,
            "error": ""
        }
    ]
}
```

输入区关闭、当前窗口失效或组件被替换时，Engine向原组件发送以下状态。

```json
{
    "message_type": "event",
    "event_type": "input_ui_state",
    "session_id": 2,
    "session_token": "<layout会话令牌>",
    "physical": false,
    "active": false,
    "rectangle": null
}
```

Engine在事件排空完成并切换输入路径后，向相关组件和窗口SDK推送新的路由状态，再恢复按键投递。

组件会话接收包含`active`的组件状态；普通应用会话接收包含`window`的窗口路由状态。两种会话角色互斥，各自的`rectangle`按所属状态解释。

应用SDK在当前窗口的路由状态变化时接收同类消息，字段为`window`、`physical`及`rectangle`，可附带`provider_list`，据此更新本地输入路由和输入条。有效当前窗口及非空`rectangle`表示输入区已开启。开启时消息包含`enable_virtual_keyboard`和`enable_ime`。两种键盘模式均在`enable_ime=true`时显示输入条。输入区关闭、关闭IME或切换当前应用时，输入条收起，停止定位和交互。

实体模式下，向当前应用发送输入区及组件列表：

```json
{
    "message_type": "event",
    "event_type": "input_ui_state",
    "session_id": 1,
    "session_token": "<会话令牌>",
    "window": 100,
    "physical": true,
    "enable_virtual_keyboard": true,
    "enable_ime": true,
    "rectangle":
    {
        "left": 24.0,
        "top": 124.0,
        "width": 590.0,
        "height": 42.0
    },
    "provider_list":
    [
        {
            "id": 1,
            "name": "standard_104",
            "role": "layout",
            "state": "running",
            "configured": true,
            "active": true,
            "process_id": 23457,
            "error": ""
        },
        {
            "id": 2,
            "name": "EasyVRUI English",
            "role": "ime",
            "language": "en",
            "state": "running",
            "configured": true,
            "active": true,
            "process_id": 23458,
            "error": ""
        }
    ]
}
```

关闭输入区后：

```json
{
    "message_type": "event",
    "event_type": "input_ui_state",
    "session_id": 1,
    "session_token": "<会话令牌>",
    "window": 100,
    "physical": true,
    "rectangle": null
}
```

#### 按键、文本提交与窗口焦点事件

输入区开启且启用IME时，Engine先将layout或实体键盘的按键发给IME，再将IME转发的按键或`ime_submit`文本发给当前窗口SDK。IME关闭或输入区关闭时，Engine直接投递按键。发给应用SDK的事件包含该会话局部`window`，按连接内顺序交给对应窗口。

Engine在独立按下再松开`Alt`的释放事件上设置`alt_tap=true`。组合键和排空释放按普通事件处理。输入组件自动转发时保留该字段。SDK在按住`Alt`或菜单键盘导航期间显示助记符下划线，收到有效的独立`Alt`释放后切换菜单导航。指针操作、焦点切换及输入状态变化会取消待定的菜单激活，因此`Alt+Shift`切换输入语言时保留原编辑焦点。

输入区关闭，Engine → 当前窗口SDK：

```json
{
    "message_type": "event",
    "event_type": "key_down",
    "session_id": 1,
    "session_token": "<会话令牌>",
    "window": 100,
    "key": "Tab",
    "shift": false,
    "ctrl": false,
    "alt": false,
    "meta": false
}
```

输入区开启，实体按键按下，Engine → IME：

```json
{
    "message_type": "event",
    "event_type": "key_down",
    "session_id": 3,
    "session_token": "<IME会话令牌>",
    "key": "a",
    "text": "a",
    "shift": false,
    "ctrl": false,
    "alt": false,
    "meta": false
}
```

按键释放，Engine → IME：

```json
{
    "message_type": "event",
    "event_type": "key_up",
    "session_id": 3,
    "session_token": "<IME会话令牌>",
    "key": "a",
    "shift": false,
    "ctrl": false,
    "alt": false,
    "meta": false
}
```

IME转发未消费的按键，Engine → 当前窗口SDK：

```json
{
    "message_type": "event",
    "event_type": "key_down",
    "session_id": 1,
    "session_token": "<会话令牌>",
    "window": 100,
    "key": "Tab",
    "shift": false,
    "ctrl": false,
    "alt": false,
    "meta": false
}
```

IME提交最终文本，Engine → 当前窗口SDK：

```json
{
    "message_type": "event",
    "event_type": "ime_submit",
    "session_id": 1,
    "session_token": "<会话令牌>",
    "window": 100,
    "text": "hello"
}
```

当前窗口失焦，Engine → 原窗口SDK：

```json
{
    "message_type": "event",
    "event_type": "focus_out",
    "session_id": 1,
    "session_token": "<会话令牌>",
    "window": 100
}
```

当前窗口获焦，Engine → 新窗口SDK：

```json
{
    "message_type": "event",
    "event_type": "focus_in",
    "session_id": 1,
    "session_token": "<会话令牌>",
    "window": 101
}
```

`focus_out/focus_in`由Engine直接发给对应窗口SDK。失焦通知携带原窗口，获焦通知携带新窗口。SDK据此管理窗口状态，再处理本地控件焦点。

`key_down/key_up`用于按键分发，可选`text`携带原始字符。启用IME时，使用`ime_submit.text`向SDK提交最终文字，SDK按本地选区与字符约束应用文本。

接收方根据目标`window`和已同步的输入区状态分发按键。`ime_submit`须来自当前活动IME，并符合已开启输入区及当前排空阶段的发送规则。

#### 窗口可见性：`window_visibility`

Engine向窗口所属SDK会话发送该事件，要求设置指定窗口的可见性。`window`为接收会话内的uint64窗口局部ID，指向已创建且实例仍存活的窗口；`visible`为必填布尔值，`true`表示显示，`false`表示隐藏。

SDK按局部ID查找窗口并调用`set_visible(visible)`，按该方法的既定规则更新本地状态和显示、隐藏事件，再通过正常`present`提交窗口的`visible`元数据。已隐藏窗口同样接收并处理该事件，`visible=true`使其重新显示。Engine接收提交后按普通窗口规则更新表面、激光捕获及输入路由。

Engine → 窗口SDK，显示窗口：

```json
{
    "message_type": "event",
    "event_type": "window_visibility",
    "session_id": 1,
    "session_token": "<会话令牌>",
    "window": 100,
    "visible": true
}
```

Engine → 窗口SDK，隐藏同一窗口：

```json
{
    "message_type": "event",
    "event_type": "window_visibility",
    "session_id": 1,
    "session_token": "<会话令牌>",
    "window": 100,
    "visible": false
}
```

Desktop通过该事件切换现有窗口的显示与隐藏，显示时的定位及选择规则见“Desktop应用”。

#### 请求正常关闭窗口：`window_close`

Engine向目标窗口所属SDK发送该事件。`window`是目标会话内的局部窗口ID。SDK调用正常关闭流程，触发`on_closing`；处理函数可取消关闭。关闭成功后SDK提交`surface_close`，Engine释放对应表面。

```json
{
    "message_type": "event",
    "event_type": "window_close",
    "session_id": 2,
    "session_token": "<目标会话令牌>",
    "window": 7
}
```

#### 异步绘制错误：`render_error`

发送给出错表面所属会话，错误字段直接放在推送顶层，结构如下：

推送：

```json
{
    "message_type": "event",
    "event_type": "render_error",
    "session_id": 1,
    "session_token": "<会话令牌>",
    "window": 100,
    "language_key": "unknown_object",
    "message": "<文件:行号:列号: error: 条件 [unknown_object] 本地化说明>",
    "argument_list": [],
    "diagnostic":
    {
        "file": "<源码文件>",
        "line": 1,
        "column": 1,
        "function": "<函数>",
        "condition": "<未满足的条件>"
    }
}
```

成功接收`present`后仍可能出现异步图形错误，通过该推送报告。可重试的纹理提交或GPU恢复由引擎处理。

#### 全局手柄按键：`global_pointer_down`与`global_pointer_up`

Engine分别跟踪左右手的按键边沿。事件随按键变化广播到所有已鉴权会话，并由连接写入各自的`session_id`与`session_token`，窗口可见性、焦点及激光落点均可独立变化。SDK将其转换为`global_pointer_event_args_t`，并触发会话内所有未关闭、未释放窗口（包含隐藏窗口）的`on_global_pointer_down`或`on_global_pointer_up`事件。

`hand`为`left`或`right`，`button`为`trigger`、`grip`、`joystick`、`primary`或`secondary`。`joystick`表示摇杆按压，`timestamp_ms`是采样时的Unix毫秒时间戳。

```json
{
    "message_type": "event",
    "event_type": "global_pointer_down",
    "session_id": 1,
    "session_token": "<会话令牌>",
    "hand": "left",
    "button": "trigger",
    "timestamp_ms": 1795564800123
}
```

```json
{
    "message_type": "event",
    "event_type": "global_pointer_up",
    "session_id": 1,
    "session_token": "<会话令牌>",
    "hand": "left",
    "button": "trigger",
    "timestamp_ms": 1795564800250
}
```

#### 屏幕内容状态：`screen_state`

窗口开始引用显示器、订阅节点变化、像素尺寸变化或可用性状态变化时，Engine向窗口所属会话发送此事件。`window`是接收会话内的局部窗口ID，`screen_id`是`screen`控件申报的显示器序号。`width`和`height`是捕获纹理的像素尺寸。`available=true`表示当前捕获内容可用。显示器断开、捕获访问丢失或图形设备故障时，`available`为`false`。SDK据此更新窗口内绑定相同`screen_id`的控件状态并计算等比显示区域。便携模式下屏幕像素由Engine本进程捕获，服务托管模式下由Helper捕获并经共享纹理交给Engine绘制，均由Engine发送本事件（EasyVRScreen工具栏展示的双FPS即取自这两个字段）。

`capture_frame_rate`和`render_frame_rate`是以FPS为单位的浮点数。前者统计该显示器在最近1秒内产生新捕获画面的次数，后者统计该窗口在最近1秒内成功提交可见SteamVR纹理的帧数。同一窗口的一帧即使提交了多个面也只计一次。Engine每0.5秒采样一次，任一帧率较上次推送变化至少0.1 FPS时发送事件。静止画面的捕获帧率随采样窗口归零。窗口持续没有新提交时，渲染帧率随采样窗口归零。窗口退出渲染范围或捕获不可用时，两项均归零。

```json
{
    "message_type": "event",
    "event_type": "screen_state",
    "session_id": 1,
    "session_token": "<会话令牌>",
    "window": 3,
    "screen_id": 0,
    "available": true,
    "width": 1920,
    "height": 1080,
    "capture_frame_rate": 60.0,
    "render_frame_rate": 59.0
}
```

### 空间参考对象与坐标

`present.metadata`表达SDK提交的表面空间属性。窗口局部左上角是定位基准，二维绘图与激光坐标从左上角向右、向下递增。

#### 位置、角度与方向

`position`为相对参考对象的`[x,y,z]`，单位米。VR世界采用右手坐标：X向右、Y向上，默认朝前为负Z。窗口逻辑坐标的top向下，因此转换到窗口三维局部空间时对应负Y。

`metadata.rotation`和`laser_rotation_offset`是`[x,y,z]`三轴欧拉角，单位度；当前转换组合为`qz × qy × qx`，作用于向量时先X再Y再Z。SDK用它提供可编辑角度属性。

跟踪消息中pose的`rotation`、激光`rotation`和`world_rotation`使用包含`x`、`y`、`z`、`w`四个分量的四元数数组，单位四元数`(0, 0, 0, 1)`表示无旋转。`direction`是三维射线方向向量。各字段按所属消息规定的编码解释。

`physical_scale`是缩放倍数。固定基准为1000逻辑像素对应1米，实际宽度为`width × physical_scale / 1000`，实际高度为`height × physical_scale / 1000`。相同倍率下，相同逻辑尺寸的控件具有相同物理尺寸。SDK将客户区和周围的控制框、标题栏、菜单栏合成为一个完整表面，再将其逻辑宽高写入`width`和`height`。绘图命令、输入区和激光命中坐标均以完整表面的左上角为原点。Engine的Overlay变换以几何中心定位，窗口metadata以表面左上角定位，转换时需计入半宽、半高偏移。

#### reference取值

普通表面的`reference`使用以下五种值：

* `world`：相对Engine的`world_origin`固定。初次建立的原点以头显位置为基准沿站立坐标负Z方向偏移，旋转为单位四元数。零位置、零旋转将窗口左上角置于该原点。Ctrl+Alt+Pause按当前头显姿态重置World偏移。
* `head`：跟随头显位置和旋转。
* `left`：跟随左手柄位置和旋转，使用右手激光交互。
* `right`：跟随右手柄位置和旋转，使用左手激光交互。
* `body`：以头显姿态估算颈部枢轴，补偿转头产生的轻微位移并跟随XYZ平移；参考旋转保持为初次建立或最近重置时的完整头显旋转。`body_reset`或Ctrl+Alt+Pause重新校准中心。

初次校准保存头显相对World的固定基准`B=world_origin⁻¹×head_initial`。Ctrl+Alt+Pause按`world_origin_new=head_current×B⁻¹`重置World，统一映射已有World窗口的整体布局，窗口局部位置与旋转保持原值。同一头显姿态下重复重置得到相同结果。

`world`、`head`和`body`可由双手激光交互。手柄或头显跟踪失效时，相应参考姿态为`null`，Engine清理该表面的输入资格与捕获；有效跟踪恢复后重新定位。

World采用SteamVR站立参考系，游戏中的角色移动由游戏自身维护。窗口相对Engine的World原点保持位置。

#### 辅助输入表面定位

输入条、IME和layout使用`auxiliary=true`的辅助表面。Engine根据当前窗口、输入矩形和组件角色计算参考姿态，并通过`tracking.reference_map`反馈给SDK。辅助表面可省略`reference`，其定位由Engine维护。

layout和IME会话创建的表面自动采用辅助定位。普通应用的辅助表面（输入条）在其为当前应用、输入区开启、启用IME且关联窗口有效时定位；输入组件表面要求组件实际参与当前输入路径，layout还要求虚拟键盘模式。`visible`决定是否显示，`enabled=true`时参与激光交互。输入路径收起、关联窗口失效或当前应用切换后，定位失效并释放捕获。

输入区的米制换算比例为`s = 关联窗口.physical_scale / 1000`。辅助表面的有效物理宽度为`W = 表面.width × s`，物理高度为`H = 表面.height × s`。其创建请求仍须提供大于零的`physical_scale`，有效显示比例跟随关联窗口。

虚拟键盘模式下，参与堆叠的可见辅助表面均相对输入区横向居中，顺序为当前应用的输入条、活动IME表面、活动layout表面（同一组按Engine窗口ID递增）。其辅助参考原点相对关联窗口左上角的偏移为`((rectangle.left + rectangle.width × 0.5) × s - W × 0.5, -((rectangle.top + rectangle.height) × s + ΣH), depth)`，再通过关联窗口姿态转换到世界空间；`ΣH`为排在当前表面之前的可见表面高度之和。

实体键盘模式下，当前应用的输入条以关联窗口右下角为锚点，右上角贴合该锚点（整宽向左展开、深度偏移为0）；活动IME表面仍以输入区下方为锚点独立堆叠并横向居中、保留`depth`偏移。曲面窗口下，两类辅助表面均沿各自锚点的切平面定向。

输入区矩形、关联窗口倍率、辅助表面宽高或前序表面状态变化时，Engine实时重算位置与有效物理尺寸。`position`和`rotation`作为自动参考姿态上的附加偏移；零值采用默认贴合位置。

`depth`为朝用户侧的2mm偏移。Engine将头显位置变换到关联窗口局部空间，局部Z小于0时取`-0.002`米，其余情况取`0.002`米；头显姿态不可用时取`0.002`米。辅助表面沿用关联窗口的激光手别限制。

#### 曲率

`curvature`为水平圆柱曲率，单位为米的倒数，默认`0.0`表示平面。非零曲率的圆柱半径为`1 / curvature`，窗口展开弧长为`width × physical_scale / 1000`，水平弯曲角为该弧长乘以曲率。

Engine接收有限且大于或等于零的曲率，并要求水平弯曲角小于`2π`。SDK的手柄调节入口采用160°的交互上限。`position`和`rotation`仍以窗口左上角为基准，Engine对显示和激光求交使用相同曲面几何。

空间运算的结果须能用有限浮点数表示。姿态组合或尺寸换算超出可表示范围时，跟踪快照使用`null`，并按参考姿态失效规则清理交互。

SDK中的移动、旋转、缩放、曲率、标题栏与跟踪模式选择，通过更新表面元数据及绘图节点实现。

### 绘图命令对象

SDK在本地批量记录绘图指令，提交时将每个节点的指令放入`command_list`数组。Engine按数组顺序解析、缓存并执行命令。每项为JSON对象，以字符串`type`选择命令类型，其余字段保存该命令的参数。一次节点更新替换该节点的整份命令列表；`[]`表示空列表。

#### 参数类型与校验

* 坐标、尺寸、半径、描边宽度、旋转和透明度使用有限JSON数值，Engine按double处理；坐标与几何尺寸使用窗口逻辑单位。
* `rectangle`为对象，包含`left`、`top`、`width`、`height`，宽高均大于或等于零。
* `ellipse`为对象，包含`center_x`、`center_y`、`radius_x`、`radius_y`，半径均大于或等于零。SDK的圆接口使用相等的X/Y半径生成椭圆命令。
* `color`为uint32无符号整数，位布局为`0xRRGGBBAA`，即24位RGB与8位alpha；JSON数值采用十进制形式。
* `font`为对象，包含系统字体名称`family`、uint64类型且大于零的`size`，以及布尔值`bold`、`italic`。`family`须为非空、无NUL的字符串。
* `text`为JSON字符串；`center`、`clockwise`、`large_arc`等开关使用JSON布尔值。
* `thickness`大于零，圆角半径大于或等于零，`opacity`取值为`[0,1]`。

下表列出的字段均须提供。Engine检查命令类型、字段类型、数值范围及组合约束；未知命令或非法参数通过业务失败响应报告。

#### 命令类型

|type|参数字段|用途|
|---|---|---|
|`fill_rectangle`|`rectangle`、`color`|填充矩形|
|`outline_rectangle`|`rectangle`、`color`、`thickness`|矩形描边|
|`draw_line`|`x1`、`y1`、`x2`、`y2`、`color`、`thickness`|绘制直线|
|`draw_text`|`rectangle`、`text`、`font`、`color`、`center`|在矩形区域绘制文字|
|`draw_rich_text`|`rectangle`、`font`、`foreground_color`、`multiline`、`horizontal_alignment`、`vertical_alignment`、`rich_text_list`|在同一文字布局中绘制带独立样式的片段|
|`push_clip`|`rectangle`|压入矩形裁剪区域|
|`pop_clip`|仅`type`|弹出当前裁剪区域|
|`fill_ellipse`|`ellipse`、`color`|填充椭圆或圆|
|`outline_ellipse`|`ellipse`、`color`、`thickness`|椭圆或圆描边|
|`fill_rounded_rectangle`|`rectangle`、`radius_x`、`radius_y`、`color`|填充圆角矩形|
|`outline_rounded_rectangle`|`rectangle`、`radius_x`、`radius_y`、`color`、`thickness`|圆角矩形描边|
|`draw_image`|`rectangle`、`image_width`、`image_height`、`pixel_data`、`opacity`|绘制RGBA像素图片|
|`draw_screen`|`rectangle`、`screen_id`，可选`accept_pointer`|绘制Engine宿主机的实时显示器内容|
|`fill_path`|`path`、`color`|填充路径|
|`outline_path`|`path`、`color`、`thickness`|路径描边|

每个节点独立维护裁剪栈。`push_clip`影响后续命令，嵌套裁剪取交集；`pop_clip`执行时须有待恢复的裁剪层，命令列表结束时裁剪栈须平衡。

`font.size`使用窗口逻辑单位。`draw_text.center=true`表示水平居中，`false`表示起始边对齐；垂直方向均居中。文字按显式换行符分行，关闭自动折行，最终裁剪在`rectangle`区域内。

#### 文字命令示例

```json
{
    "type": "draw_text",
    "rectangle":
    {
        "left": 24.0,
        "top": 24.0,
        "width": 240.0,
        "height": 40.0
    },
    "text": "Hello VR",
    "font":
    {
        "family": "Segoe UI",
        "size": 24,
        "bold": false,
        "italic": false
    },
    "color": 4294967295,
    "center": true
}
```

#### 富文本命令

`font`的`underline`和`strikethrough`为可选布尔值，默认`false`，适用于`draw_text`和`draw_rich_text`。

`rich_text_list`按显示顺序保存片段。每段的`text`为字符串，`foreground_color`和`background_color`为可选RGBA整数。省略时分别使用命令的`foreground_color`和透明背景。片段的`font`对象可覆盖`family`、`size`、`bold`、`italic`、`underline`和`strikethrough`。省略的字段继承命令的字体。字体族须非空且不含NUL，字号须大于0。

各段在同一个DirectWrite布局中排版，样式按转换后的UTF-16范围应用。片段背景按行绘制。`multiline`开启时支持显式换行及按矩形宽度自动折行。`horizontal_alignment`接受`left`、`center`和`right`，作用于每一行。`vertical_alignment`接受`top`、`center`和`bottom`，作用于整块文字。绘制结果裁剪在`rectangle`内。

```json
{
    "type": "draw_rich_text",
    "rectangle":
    {
        "left": 24.0,
        "top": 24.0,
        "width": 240.0,
        "height": 60.0
    },
    "font":
    {
        "family": "Segoe UI",
        "size": 18,
        "bold": false,
        "italic": false
    },
    "foreground_color": 4294967295,
    "multiline": true,
    "horizontal_alignment": "left",
    "vertical_alignment": "top",
    "rich_text_list":
    [
        {
            "text": "状态 ",
            "font": {}
        },
        {
            "text": "就绪",
            "foreground_color": 2162478079,
            "font":
            {
                "bold": true,
                "underline": true
            }
        }
    ]
}
```

#### 图片命令

`image_width/image_height`为大于零的uint64像素尺寸。`pixel_data`为原始RGBA像素字节的标准Base64字符串；像素从左上角开始，按从左到右、从上到下的行顺序紧密排列，每像素依次为R/G/B/A四个字节；RGB保存原始通道值，Engine在图形接口边界执行alpha预乘转换。解码后的字节数须等于`image_width × image_height × 4`，尺寸乘法须能被接收进程的内存尺寸类型表示。`rectangle`指定目标绘制区域，`opacity`控制整体透明度。

下面绘制一张1 × 1像素的红色图片：

```json
{
    "type": "draw_image",
    "rectangle":
    {
        "left": 24.0,
        "top": 80.0,
        "width": 32.0,
        "height": 32.0
    },
    "image_width": 1,
    "image_height": 1,
    "pixel_data": "/wAA/w==",
    "opacity": 1.0
}
```

#### 屏幕命令

`draw_screen`在指定逻辑矩形内绘制Engine宿主机的显示器内容。`screen_id`为宿主机DXGI显示器枚举的0起始序号。Engine在GPU上绘制显示器内容，并按显示器方向处理桌面与光标。

DXGI提供独立光标时，Helper单独传输可见性、虚拟桌面热点位置及形状信息。Engine按形状修订号缓存RGBA数据并在绘制时合成光标。启用`accept_pointer`时，激光命中屏幕画面或在该画面上开始拖拽后，Engine使用当前渲染帧的激光落点对齐光标热点。其他情况下，独立光标按系统位置和可见性绘制。`accept_pointer`省略时为`false`。驱动把光标写入桌面帧时，Engine显示驱动提供的画面。

显示矩形决定窗口内的显示大小：等尺寸绘制采用线性采样，缩放绘制采用高质量三次插值（`D2D1_INTERPOLATION_MODE_HIGH_QUALITY_CUBIC`）。普通窗口重绘完成后，Engine将内容复制到带完整Mipmap链的提交纹理并生成Mipmap，再提交给SteamVR Overlay以提升远距离清晰度。要按原始像素显示1920×1080的画面，可使用同样逻辑宽高的矩形，并保持窗口的`physical_scale`。显示器内容变化由Engine更新，窗口继续使用已提交的绘图节点。采集可用性通过`screen_state`反馈。

```json
{
    "type": "draw_screen",
    "rectangle":
    {
        "left": 0.0,
        "top": 0.0,
        "width": 1920.0,
        "height": 1080.0
    },
    "screen_id": 0
}
```

#### 路径命令

`path`为对象，包含字符串`fill_rule`和数组`segment_list`。`fill_rule`取`even_odd`或`non_zero`，分别表示奇偶填充规则与非零环绕填充规则。每段为JSON对象，使用字符串`type`选择段类型：

|type|参数字段|用途|
|---|---|---|
|`move`|`x`、`y`|在指定点建立图形|
|`line`|`x`、`y`|连接到指定终点|
|`quadratic`|`control_x`、`control_y`、`x`、`y`|二次贝塞尔曲线|
|`cubic`|`control_x1`、`control_y1`、`control_x2`、`control_y2`、`x`、`y`|三次贝塞尔曲线|
|`arc`|`x`、`y`、`radius_x`、`radius_y`、`rotation`、`clockwise`、`large_arc`|椭圆弧|
|`close`|仅`type`|闭合当前图形|

各坐标为有限数值，弧半径大于或等于零，弧旋转单位为度。路径先通过`move`建立图形，再添加其它段；`close`后通过新的`move`建立后续图形。数组顺序就是路径段顺序，空数组表示空路径。

下面填充一个三角形：

```json
{
    "type": "fill_path",
    "path":
    {
        "fill_rule": "non_zero",
        "segment_list":
        [
            {
                "type": "move",
                "x": 20.0,
                "y": 20.0
            },
            {
                "type": "line",
                "x": 80.0,
                "y": 20.0
            },
            {
                "type": "line",
                "x": 50.0,
                "y": 70.0
            },
            {
                "type": "close"
            }
        ]
    },
    "color": 4294967295
}
```

## Windows命名管道

### 发现接口

管道名为`\\.\pipe\EasyVROverlayUIEngine.Bootstrap`，用于本机发现，支持多个客户端并行读取。每个连接使用独立管道实例，服务端在连接建立后主动发送一次发现消息：

Engine → 本机SDK：

```json
{
    "version": 1,
    "port": 49537,
    "access_credential": "<接入凭据>",
    "public_key_fingerprint": "<公钥指纹>",
    "process_id": 12345
}
```

发现消息使用8字节小端uint64长度头，消息体为UTF-8 JSON，长度为消息体字节数。`version`为`1`，`port`为实际TCP端口，`process_id`为Engine PID。客户端随后完成TCP/TLS鉴权，取得session ID/token。

### 生命周期与访问边界

连接建立后的处理期限约为5秒。管道可并行处理多个客户端，发送发现信息后等待客户端断开或期限到期，再关闭连接。

管道通过`PIPE_REJECT_REMOTE_CLIENTS`限制为本机访问，使用Windows默认安全描述符。能读取管道的本机进程可以取得接入凭据及公钥指纹。TCP监听地址按前述配置独立设置。

窗口操作、输入组件注册、剪贴板、设置等业务统一通过TCP/TLS完成。

## Windows命名互斥体

### 单实例协调

互斥体名为`Local\EasyVROverlayUIEngine.Engine`，用于Windows当前登录会话内的单实例协调。不同登录会话使用各自的Local命名空间，固定TCP端口等资源仍可能跨会话冲突。

互斥体使用Windows默认安全属性。

## 生命周期与审计边界

### SteamVR连接、断开与恢复

Engine启动后立即初始化IPC并可先于SteamVR接受应用连接。探测SteamVR时，Engine要求当前Windows会话内同一安装目录的`vrserver.exe`与`vrmonitor.exe`均处于运行状态，且命名空间及对应服务端、合成器IPC管道均可连接，然后以`VRApplication_Background`后台类型初始化OpenVR（不会主动拉起SteamVR）。

Engine以`vrserver.exe`的进程标识和创建时间识别SteamVR实例。进程退出、帧同步调用失败或OpenVR连接失效时，Engine释放旧Overlay、手柄输入和OpenVR连接，暂停VR跟踪，并继续提供IPC服务和维护现有应用、Desktop、layout及IME会话。断开期间提交的窗口状态仍由Engine保存。

收到`VREvent_Quit`或检测到服务端退出时，Engine先确认退出并释放旧OpenVR连接，记录旧实例身份以避免重连退出中的进程，待新的SteamVR实例就绪后重新初始化OpenVR。恢复时重新加载动作清单，按需切换图形适配器，从当前窗口状态重建可见Overlay并恢复纹理、可见性、位姿、曲率以及激光追踪。关闭SteamVR后可重新启动SteamVR以恢复显示。

### 会话与进程归属

#### 普通应用

每条已鉴权TCP连接是独立会话，窗口局部ID在该会话内隔离。同一应用PID可以建立多个会话；关闭连接时，清理该会话的窗口、输入归属、捕获及注册资源。

Engine对本机回环连接尽力查询真实进程：IPv4使用`GetExtendedTcpTable(AF_INET)`，IPv6使用`GetExtendedTcpTable(AF_INET6)`，匹配客户端反向端点，IPv6还处理相关scope与映射地址。取得进程句柄后，使用PID与创建时间区分进程，发现其退出会关闭关联连接并清理资源。

进程身份查询适用于loopback连接。查询成功并能打开进程时，Engine绑定进程身份并监视退出；其余连接通过socket关闭及心跳超时清理资源。

SDK重连后重新建立会话并提交窗口。已成功执行的业务操作保留执行结果；发生超时时，请求可能处于已执行但响应尚未收到的状态。

会话断开时，取消该会话尚未执行的窗口、输入区及组件切换请求，并清理其待发送结果和事件队列。断开前已执行的操作按原执行结果处理；旧会话排队任务在执行前再次校验窗口及会话生命周期。

SDK建立新会话后重建窗口和绘图缓存，当前窗口与输入界面从初始状态开始，用户重新选中窗口后再按需唤起。输入组件使用新session重新注册；配置条目按合法进程身份匹配，动态组件获得新的运行时ID。

#### 持久与动态输入组件

配置中的组件启动后进入`starting`，须在10秒内连接、鉴权并注册，才进入`running`；启动失败、提前退出、注册超时则回到`stopped`并记录错误。配置示例：

config.json中相关配置片段：

```json
{
    "provider_list":
    [
        {
            "name": "standard_104",
            "role": "layout",
            "executable": "easyvrui_layout.exe",
            "argument_list": []
        },
        {
            "name": "EasyVRUI English",
            "role": "ime",
            "language": "en",
            "executable": "easyvrui_ime_english.exe",
            "argument_list": []
        },
        {
            "name": "EasyVRUI拼音",
            "role": "ime",
            "language": "zh",
            "executable": "easyvrui_ime_chinese_pinyin.exe",
            "argument_list": []
        },
        {
            "name": "EasyVRUI日本語",
            "role": "ime",
            "language": "ja",
            "executable": "easyvrui_ime_japanese.exe",
            "argument_list": []
        }
    ]
}
```

每项配置的`name`、`role`和`executable`必填且为字符串，名称和可执行路径须为非空；layout名称保持唯一，IME名称在同一语言内保持唯一。`role`取`layout`或`ime`，`argument_list`为字符串数组，省略时为`[]`。IME的`language`为非空字符串，默认`en`，常用代码为`zh/en/ja`；layout省略该字段。可执行文件相对路径以config.json所在目录为基准。省略`provider_list`时创建standard_104布局、EasyVRUI English、EasyVRUI拼音和EasyVRUI日本語四项默认配置；显式`provider_list: []`表示空配置列表。

`desktop`对象和`provider_list`每项支持布尔字段`run_as_administrator`。在已有对象中省略该字段时按`false`处理。首次生成的Desktop配置为`true`，layout和IME使用普通权限。普通权限Engine按管理员配置启动本机子进程时使用Windows提权确认，SDK应用启动使用其独立的权限规则。

Engine启动时加载配置列表并尝试启动全部配置程序。列表ID在每次运行时分配；配置组件退出后保留条目并切换为未启动状态，引擎仍运行时可再次调用start/select。

启动后动态注册的非配置组件标记为`configured=false`，断线或退出后移除条目。Engine管理自己启动并拥有的子进程生命周期，对外部SDK应用监视退出并清理所属资源。

某个角色具有配置条目或成功注册过组件后，该角色成为本轮Engine运行期间的必需角色。活动组件失效时，先尝试选用同角色已运行的候选，再等待正在启动的候选，或启动本轮尚未失败的配置候选。必需角色的候选全部耗尽时，报告错误并退出引擎。动态组件退出并移除条目后，该角色的必需状态仍保留。空配置启动且从未注册过组件的角色可以保持缺席。引擎仍运行时，人工重试可通过组件start/select发起。

输入区开启时，故障恢复作为串行输入路径切换：先撤销失效连接的资格，排空其余旧参与组件，保留有效当前窗口与输入矩形，并暂存此后的新输入。替代组件就绪后发送新的状态并恢复投递。旧路径中已经成功提交的文本保留，未完成的旧处理随失效路径清理。

输入区关闭时，窗口直达SDK的路径继续运行，组件管理独立执行恢复。调用方通过最新组件列表查询运行及活动状态；普通应用可主动调用`input_provider_list`，已收到完整列表快照时整体更新本地组件列表。

#### Desktop应用

`config.json`根对象中的`desktop`指定由Ctrl+Pause唤起的普通应用：

```json
{
    "desktop":
    {
        "executable": "easyvrui_desktop.exe",
        "argument_list": []
    }
}
```

省略`desktop`时生成上面的默认配置。`executable`为非空路径字符串，相对路径以配置文件所在目录为基准；`argument_list`为字符串数组，省略时为`[]`。

Engine首次响应Ctrl+Pause时启动配置程序；后续按下在Desktop窗口的显示与隐藏之间切换，复用仍在运行的进程及窗口实例。程序退出后，下次调用可重新启动。默认Desktop通过SDK创建采用world参考对象的应用列表窗口，显示应用图标、日期时间和网络状态，其窗口、事件和会话采用普通应用规则。Engine退出时关闭自己启动并拥有的Desktop子进程。

每次显示时，以当前有效头显姿态在正前方定位一次，然后保持该world姿态。再次唤出时重新以当时的头显姿态定位。Desktop与内置输入方式选择对话框默认采用world参考对象；输入条、IME与layout按辅助表面规则定位，应用自定义对话框按SDK及应用配置确定参考关系。

Engine通过`window_visibility`要求SDK显示或隐藏Desktop窗口。SDK调用窗口`set_visible()`并正常`present`；显示更新被Engine接收、窗口可交互后，Engine将其置于前景并选中。隐藏更新按当前窗口规则释放相应输入路由与捕获，Desktop进程和窗口实例保留供下一次显示。

唤起时用10秒期限等待Desktop会话及普通、启用的窗口元数据，已隐藏窗口也可作为目标。窗口元数据已到达、但头显姿态暂时缺失时，显示请求保留到跟踪恢复；此阶段保持已启动状态，姿态有效后再完成定位、显示与窗口选择。

### 权限与资源约束

#### 会话与资源隔离

* TLS公钥指纹验证服务器身份，HMAC通过共享接入凭据验证客户端的接入资格。
* 会话token必须与当前连接匹配，资源操作按所属会话执行。
* 普通窗口操作按本会话局部ID查找。跨会话输入界面定位由Engine根据当前应用、输入矩形和活动组件解析。
* provider输入要求发送者为当前活动组件、存在有效当前窗口及输入区，并符合当前排空阶段；layout新的按下事件还要求虚拟模式且该组件实际参与输入路径。layout按其界面交互产生按键，具体表面的显示状态由组件维护。`ime_submit`由活动IME提交最终文本。

#### 会话操作权限

客户端凭共享接入凭据完成鉴权。同一接入凭据用于本机和远程客户端。

* 本机和远程客户端均可读写宿主剪贴板、修改全局激光偏移、重置body中心，以及查询、启动和选择输入组件。
* 本机和远程客户端均可注册输入组件。`default_provider=false`的注册可能接管当前角色。
* 当前窗口所属的普通应用会话可以凭窗口和输入区矩形唤起输入界面，创建`auxiliary=true`的输入条，并维护窗口内的控件焦点与编辑规则。辅助定位在输入区开启且关联窗口有效时生效。layout/IME会话创建的表面自动采用辅助定位，接收组件输入与激光事件。可聚焦的应用控件可以接收键盘。
* `input_provider_send.event`由Engine校验对象类型、事件类型、注册角色、按键字段及排空阶段；SDK和输入组件按自身约定处理扩展字段。

* 连续tracking和普通pointer更新采用合并策略；其它响应和事件保留各自的发送规则。
* 输入组件候选耗尽等故障可导致Engine退出，影响全局可用性。

### 其它系统接口

Engine调用Windows键盘hook/热键、剪贴板、进程与TLS接口，以及SteamVR/OpenVR和Direct3D/Direct2D/DirectWrite。

keyboard模块与Engine同进程，通过内部队列及共享状态通信。layout与IME是独立普通应用，通过TCP/TLS协议注册和通信。配置文件、语言包和TLS密钥由对应本机模块管理。
