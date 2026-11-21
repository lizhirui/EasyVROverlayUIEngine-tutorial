from argparse import ArgumentParser
from functools import lru_cache
from pathlib import Path
from tempfile import TemporaryDirectory
import os
import re
import shutil
from PIL import ImageFont
import capture_ui_screenshots as capture
import generate_advanced_diagrams as advanced
import render_3d_mockups as mockup
SITE = Path(__file__).resolve().parents[1]
DOCS = SITE / "docs"
WORK = DOCS / "ja/.ja_work"
OUTPUT = DOCS / "public/images/ja"
SECTION_LIST = ("basics", "projects", "advanced", "reference")
IMAGE_PATH = re.compile(r"/images/(?:zh|ja)/([^()\s]+\.png)")
FONT_DIRECTORY = Path(os.environ["WINDIR"]) / "Fonts"
DIAGRAM_LABEL_TEXT = "\n+X向右|+Xは右方向\n+Y向上|+Yは上方向\n+Z朝向佩戴者|+Zは装着者の方向\n1  冻结旧路线|1  旧経路を凍結\n1  建立连接|1  接続を確立\n2  后台reader分流|2  読み取りスレッドで振り分け\n2  等待旧layout|2  旧layoutの完了を待機\n3  UI所属线程消费|3  UIスレッドで処理\n3  等待旧IME|3  旧IMEの完了を待機\n4  提交变更|4  変更を確定\nA的事件|Aのイベント\nA返回结果|Aが結果を返す\nB的事件|Bのイベント\nB返回结果|Bが結果を返す\nC++公开头|C++公開ヘッダー\nC++接口|C++インターフェース\nD3D11 纹理|D3D11テクスチャ\nD3D与OpenVR|D3DとOpenVR\nDesktop / 设计器|Desktop / Form Designer\nEngine维护窗面和当前窗口，SDK在应用线程上处理控件事件|Engineがウィンドウ面と現在のウィンドウを管理し、SDKがアプリのスレッドでイベントを処理します\nID索引可使用非拥有入口|ID索引は非所有参照でも管理可能\nPython包|Pythonパッケージ\nPython接口|Pythonインターフェース\nSDK的请求确认、Engine的栅格化和SteamVR的呈现是三个时间点|SDKの応答確認、Engineのラスタライズ、SteamVRの表示は別のタイミングで行われます\nSDK调用栈|SDKの呼び出しスタック\nSteamVR右手跟踪坐标|SteamVRの右手系トラッキング座標\nTCP/TLS连接与消息队列|TCP/TLS接続とメッセージキュー\nUI运行时|UIランタイム\nleft向右|leftは右方向\npybind11桥接|pybind11ブリッジ\ntop向下|topは下方向\nα轴 −Z|αの軸 −Z\nβ = 90°时，姿态只依赖 α − γ|β = 90°では姿勢はα − γだけで決まります\nγ轴 +Z|γの軸 +Z\n−Z朝向前方|−Zは前方\n万向节锁与轴角四元数|ジンバルロックと軸角クォータニオン\n业务对象|アプリのオブジェクト\n中间角 β = 90°|中間の回転角 β = 90°\n主窗事件|メインウィンドウのイベント\n主窗回调继续|メインウィンドウのコールバックを再開\n事件使对象和父链失效|イベントがオブジェクトと親階層を無効化\n事件信号|イベントシグナル\n交点要在窗口弧段内|交点はウィンドウの円弧内\n从控件到画面的渲染管线|コントロールから画面までの描画パイプライン\n代码字段顺序   quat_t{x, y, z, w}|コード上のフィールド順   quat_t{x, y, z, w}\n任务与待发计数归零|タスクと送信待ちの件数がゼロ\n会话ID与会话令牌|セッションIDとセッショントークン\n会话与窗面|セッションとウィンドウ面\n会话归属与同线程模态循环|セッションの所有関係と同一スレッドのモーダルループ\n使用同一接收序号源|同じ受信連番を使う\n保存旧窗口与组件|旧ウィンドウとコンポーネントを記録\n保持旧输入的去向，等待上游与下游明确完成，再启用新路径|旧入力の宛先を保持し、上流と下流の処理完了を待って新しい経路に切り替えます\n先把世界射线变到窗面中心系，求根后再把弧长和高度换回逻辑像素。|ワールドのレイをウィンドウ面の中心座標系に変換し、解を求めて弧長と高さを論理ピクセルに戻します。\n公开头与配套二进制|公開ヘッダーと対応するバイナリ\n共享窗口在活动期持有|動作中のwindowを共有所有\n关闭窗面|ウィンドウ面を閉じる\n决定键盘送往哪个会话|キーボード入力の宛先セッションを決定\n初始 β = γ = 0°|初期状態 β = γ = 0°\n前三层同在应用进程，服务进程统一处理窗面、空间输入与图形资源|上の3層は同じアプリプロセス内にあり、サービスがウィンドウ面、空間入力、グラフィックスリソースを管理します\n半径 R|半径 R\n半角在乘积里出现两次，q · (0, p) · q^(-1)得到实际转角。|積の中で半角が2回現れ、q · (0, p) · q^(-1)が実際の回転を与えます。\n协议拒绝 → 批次隔离     图形绘制错误 → render_error|プロトコル拒否 → バッチを分離     描画エラー → render_error\n单位四元数的轴角表示|単位クォータニオンの軸角表現\n原向量|元のベクトル\n原生SDK绑定与对象寿命|ネイティブSDKのバインディングとオブジェクトの寿命\n原生控件树|ネイティブのコントロールツリー\n原生运行时|ネイティブランタイム\n原调用栈继续运行|元の呼び出しスタックで再開\n发布新路由状态|新経路の状態を通知\n发现、请求与事件|サービス検出・リクエスト・イベント\n发送 input_drain|input_drainを送信\n发送者与载荷|送信元とペイロード\n取得服务描述|サービス記述子を取得\n叠加窗口与激光|オーバーレイウィンドウとレーザー\n只等自身响应或失败|対応する応答か失敗を待機\n合成旧键释放|旧経路にキー解放を生成\n同一姿态可以有多组欧拉角，连续旋转可以直接用轴角计算|1つの姿勢を複数のオイラー角で表せます。連続回転は軸角から直接計算できます\n同步RPC静候对应响应，模态调用主动泵消息。渲染提交期间禁止进入模态。|同期RPCは応答を待機し、モーダル処理はメッセージを処理します。描画の送信中はモーダルに入れません。\n同步响应槽|同期応答スロット\n同步请求只等回包。普通与模态循环都通过消息泵执行事件。|同期リクエストは応答を待機します。通常・モーダルの両ループがメッセージポンプでイベントを実行します。\n后台读取负责分流，界面线程只在明确的入口消费工作|バックグラウンドの読み取り処理が振り分け、UIスレッドが所定の入口で実行します\n向量在垂直于单位轴的平面内转 θ|ベクトルが単位軸に垂直な平面でθだけ回転\n响应必须匹配正等待的ID|応答IDは待機中のIDと一致\n四步应用鉴权|アプリ認証の4ステップ\n回写 cancel 或 handled|cancelまたはhandledを書き戻す\n圆心|円の中心\n在 XZ 截面中求交|XZ断面で交点を求める\n坐标系与窗口上的刻度|座標系とウィンドウ上の目盛り\n基类统一，字段按事件定义|基底型を統一し、フィールドはイベント別に定義\n处理本轮截止值以前的工作|今回の境界番号までの処理を実行\n复制回调名单并顺序执行|コールバック一覧を複製して順に実行\n复用静态表面|静的なウィンドウ面を再利用\n客户端连接|クライアント接続\n射线起点 o|レイの始点 o\n尾部文本只送旧窗|末尾テキストは旧ウィンドウへ\n局部窗口号映射到全局表面|ローカルIDを全体のウィンドウ面に対応付け\n属性 / 集合 / 回调|属性 / 集合 / コールバック\n属性与语言原生容器|プロパティと言語の標準コンテナー\n属性与集合直接进入原生对象，事件回调按拥有者线程的顺序执行|プロパティとコレクションはネイティブオブジェクトに反映され、イベントは所有スレッドで順に実行されます\n左上角系中的点为 (m·left, −m·top, 0)，负号来自竖直正方向相反。|左上基準の点は (m·left, −m·top, 0) です。上下の正方向が逆なのでY成分に負号が付きます。\n左上角锚点 A|左上のアンカー A\n已鉴权连接|認証済み接続\n布局与本地焦点|レイアウトとローカルのフォーカス\n应用、接入层、原生SDK与Engine|アプリ・言語バインディング・ネイティブSDK・Engine\n应用拥有控件与回调，Engine拥有窗面、GPU纹理和Overlay。|アプリはコントロールとコールバックを、Engineはウィンドウ面、GPUテクスチャ、Overlayを所有します。\n应用进程   C++或Python程序|アプリプロセス   C++またはPythonプログラム\n异步响应队列|非同期応答キュー\n弧角 φ 决定横向弧长|弧の角度φから横方向の弧長を算出\n弯曲与反算|曲面化と逆変換\n强类型事件|型付きイベント\n当前应用窗口|現在のアプリウィンドウ\n恢复A的交互资格|Aの操作を再び有効にする\n恢复主窗的交互资格|メインウィンドウの操作を再び有効にする\n恢复队列处理|キューの処理を再開\n成功重绘后更新代数|再描画成功後に世代番号を更新\n所属窗面|所属するウィンドウ面\n拾取、捕获与路由|ヒット・捕捉・ルーティング\n按 order 淘汰旧节点|orderに従い古いノードを除外\n按两队列的队首序号合并|両キューの先頭の連番を比較して合流\n按接收序号排列|受信連番順に並べる\n挑战证明换取会话令牌|チャレンジの証明と引き換えにトークンを取得\n接收 Overlay 纹理|Overlayのテクスチャを受信\n控件与窗口版本|コントロールとウィンドウのバージョン\n提交 present 差量|presentの差分を送信\n收到该连接确认|該当する接続の完了通知を受信\n收包保序   先处理旧IME最后一次文本提交，再处理关闭完成|受信順を維持   旧IMEからの最後のテキスト入力を処理してから終了通知を処理\n改变窗口或模式|ウィンドウまたはモードを変更\n数字与处理函数|番号とハンドラー\n新输入在队列等待|新しい入力はキューで待機\n方向轴、左上角锚点与窗面中心|座標軸、左上アンカー、ウィンドウ面の中心\n旋转后的向量|回転後のベクトル\n旧窗口失效时仍可清理旧路径，尾部正文不会改投给新窗口。|旧ウィンドウが無効になっても旧経路は後処理できます。末尾のテキストは新ウィンドウへ転送しません。\n旧键送入旧IME|旧経路のキーを旧IMEへ送信\n显示于头显|ヘッドセットに表示\n显示窗口|ウィンドウを表示\n最近有效交点|最も近い有効な交点\n服务事件队列|サービスイベントキュー\n本机管道或远程参数|ローカルパイプまたはリモート接続パラメーター\n柱面截面   x² + (z − R)² = R²|円筒面の断面   x² + (z − R)² = R²\n柱面窗口与激光反投影|円筒ウィンドウとレーザーの逆投影\n标量在前的数学记号|スカラーを先頭に置く数学表記\n校验并合并节点|検証してノードをマージ\n横截面在窗面中心坐标系中表示，竖直轴 Y 垂直于图面|断面はウィンドウ面の中心座標系で示し、鉛直のY軸は図の面に垂直です\n欧拉角 Rz·Ry·Rx|オイラー角 Rz·Ry·Rx\n比对DER公钥信息指纹|DER公開鍵情報の指紋を照合\n沿同一根直线|同一直線上\n独立应用|独立アプリ\n独立服务进程|独立したサービスプロセス\n登记对象|オブジェクトを登録\n直接owner阻塞   各层共用一套UI队列与窗体状态|直接のownerをブロック   各階層でUIキューとウィンドウ状態を共有\n确认TLS公钥|TLS公開鍵を確認\n确认匹配   正在排空 + 发送会话等于当前等待会话|完了を照合   ドレイン中で、送信元が待機対象のセッションと一致\n示例宽高 640×360|サンプルの幅と高さ 640×360\n离屏绘制或复用|オフスクリーン描画または再利用\n空间位姿 / 大小 / 曲率|空間の位置・姿勢 / サイズ / 曲率\n空间输入|空間入力\n窗口与控件|ウィンドウとコントロール\n窗口弧面|曲面の円弧\n窗口逻辑像素|ウィンドウの論理ピクセル\n窗面中心|ウィンドウ面の中心\n窗面中心 C|ウィンドウ面の中心 C\n等待响应后更新比较基准|応答を待って比較基準を更新\n组件不在旧路由中时跳过相应阶段，当前阶段超时或断线时吊销资格并继续。|旧経路にないコンポーネントの段階はスキップし、待機がタイムアウトするか切断された場合は送信資格を取り消して続行します。\n绘制纹理并送头显|描画テクスチャをHMDへ送信\n节点 ID 标识控件与段|ノードIDでコントロールと区間を識別\n节点差量减少传输和资源构造。窗面产生新图像时仍按完整顺序回放有效节点。|ノード差分で転送とリソース生成を削減します。新しい画像の描画時は、有効な全ノードを順番どおりに再生します。\n记录绘图节点|描画ノードを記録\n记录节点并提交|ノードを記録して送信\n设置结果并结束B的循环|結果を設定してBのループを終了\n设计器生成构造代码。业务实例持有生成窗体并绑定其公开控件。|Form Designerが構築コードを生成し、アプリのインスタンスが生成フォームを保持して公開コントロールに処理を結び付けます。\n语言入口|言語別の入口\n语言接入层|言語バインディング\n语言适配|言語のアダプター\n调用原生编译扩展|ネイティブ拡張を呼び出す\n调用者仍可保有对象|呼び出し元で保持を継続可能\n跟踪与合成仍按帧更新|トラッキングと合成はフレームごとに更新\n跨线程入口   投递回调后由界面所属线程执行|スレッド間の入口   コールバックを投稿し、UIスレッドで実行\n跨进程边界   TCP/TLS传递请求、响应与事件|プロセス境界   TCP/TLSでリクエスト、応答、イベントを転送\n转轴相互独立|回転軸は互いに独立\n输入切换的串行排空|入力切り替えの順次ドレイン\n输入组件|入力コンポーネント\n运行本地投递回调|ローカルに投稿されたコールバックを実行\n返回本次决定|今回の判定を返す\n进入回调时获取GIL|コールバック開始時にGILを取得\n进入确认窗A，阻塞主窗|確認ウィンドウAを開き、メインをブロック\n进入确认窗B，阻塞A|確認ウィンドウBを開き、Aをブロック\n逐层返回|内側のループから順に戻る\n逻辑像素到米   m = physical_scale / 1000|論理ピクセルからメートルへ   m = physical_scale / 1000\n链接静态库或DLL|静的ライブラリまたはDLLをリンク\n验证归属与可用性|所有関係と操作可否を検証\n"
CAPTURE_LABEL_TEXT = "\nAvatar参数与预设|アバターパラメーターとプリセット\nEngine地址与端口|Engineのアドレスとポート\nTSV表格|TSVファイル\nVRChat快捷聊天|VRChatクイックチャット\n\\n等大家到齐后，我们按名单依次进入。\\n如果暂时无法回应，可以先在这里留言。\\n我会核对集合地点，并在下一轮确认人数。|\\n全員がそろったら、リストの順に入室しましょう。\\n返事が難しい方は、ここにメッセージをどうぞ。\\n次に集合場所と人数を確認します。\nbody · 曲率0.65m⁻¹|body · 曲率0.65m⁻¹\nleft · 0.65倍 · 测试采样|left · 0.65倍 · テストサンプル\nworld · 曲率0.00m⁻¹ · 平面|world · 曲率0.00m⁻¹ · 平面\n为当前参数快照输入名称|現在のパラメーターセットに名前を付けてください\n事件|イベント\n你好，VR世界！|こんにちは、VRの世界！\n保存为预设…|プリセットに保存…\n保存自定义预设|カスタムプリセットを保存\n全部房间与玩家|すべてのルームとプレイヤー\n凭据与证书指纹 · 使用测试配置|認証情報と証明書の指紋 · テスト設定\n加入|入室\n参数名|パラメーター名\n发送模拟消息|テスト送信\n回应|返信\n大家好！|皆さん、こんにちは！\n实时更新 · 本地演示|リアルタイム更新 · デモ\n导出示例目录|サンプル出力先\n导出筛选后的房间记录|絞り込んだログをエクスポート\n已发送：Ready for sync|送信済み：Ready for sync\n已发送：|送信済み：\n已更新EarFlop · 演示通道|EarFlopを更新済み · デモ用\n常用短语|定型文\n当前Float参数|現在のFloat値\n当前值|現在値\n我会在入口等候。|入口で待っています。\n我稍后回来。|少ししたら戻ります。\n房间|ルーム\n房间记录|ルームログ\n房间记录与相册|ルームログと写真\n无头WARP · 桌面画面占位|ヘッドレスWARP · デスクトップの表示領域\n时间|時刻\n显示桌面副屏|補助画面を表示\n最近使用 · 暂无|最近使った顔文字 · なし\n本地示例数据 · 已读取4条记录|ローカルサンプル · 4件のログを読み込み済み\n本地示例数据 · 筛选后2条记录|ローカルサンプル · 絞り込み結果2件\n桌面副屏与电平|補助画面とレベル表示\n模拟数据报已提交 · 冷却期间暂停发送|テスト送信済み · クールダウン中\n测试提交 · 最近使用：|テスト送信 · 最近の入力：\n测试状态：会话已连接|テスト状態：セッション接続済み\n消息预览|メッセージのプレビュー\n清空当前Chatbox|現在のChatboxを消去\n清空气泡…|吹き出しを消去…\n港口|港\n港口 / Ren|港 / Ren\n演示相册|サンプルアルバム\n演示预设|デモプリセット\n玩家|プレイヤー\n相册 · 等比预览|アルバム · 縦横比を維持\n相册预览|写真プレビュー\n确定发送清空指令吗？本地草稿可以保留。|消去コマンドを送信しますか？下書きは保持できます。\n示例Avatar · 等待编辑|サンプルアバター · 編集待ち\n离开|退室\n离线演示 · 等待编辑|オフラインデモ · 編集待ち\n等待验证 · 本地状态演示|検証待ち · 状態表示のデモ\n类型|種類\n腕部HUD|手首HUD\n自定义|カスタム\n观景台|展望台\n观景台 / Mika|展望台 / Mika\n观景台日落 · 1600×900 · 合成素材|展望台の夕景 · 1600×900 · 合成素材\n观景台日落.png|展望台の夕景.png\n观景台调试预设|展望台テスト用\n请再发一次链接。|リンクを再送してね。\n谢谢，晚点见！|ありがとう、また後で！\n远程会话配置|リモートセッション設定\n选择照片以预览|プレビューする写真を選択\n问候|あいさつ\n颜文字测试面板|顔文字テストパネル\n验证配置|設定を検証\n我的第一个VR窗口|初めてのVRウィンドウ\n点一下下面的按钮试试看！|下のボタンを押してみましょう。\n点我打招呼|あいさつ\n发送|送信\n把文本框里的内容发出去|入力したテキストを送信\n输入想说的话：|メッセージを入力：\n静音快捷喊话条|クイックメッセージ\n"
NATIVE_ROLE_LIST = ("desktop", "designer", "file_manager", "task_manager", "demo", "keyboard", "pinyin", "japanese", "project_story",)
GUIDE_WORK = SITE / ".work/ja-guide"
GUIDE_SOURCE_MAP = {"controls": "capture_ui.cpp", "controls_second": "capture_layout_control.cpp", "controls_third": "capture_display_control.cpp", "dialog": "capture_ui.cpp", "demo": "capture_ui.cpp",}
GUIDE_LABEL_TEXT = "\n默认标题栏|既定のタイトルバー\n自定义标题颜色和字体|タイトルの色と書体を変更\n隐藏标准关闭入口|閉じるボタンを非表示\n隐藏标题栏|タイトルバーを非表示\n默认|既定\n工作区连接|ワークスペースの接続\n前景色与背景色|前景色と背景色\n提交设置|設定の適用\n字体与颜色|フォントと色\n工作区备注|ワークスペースのメモ\n第一行：检查连接\\n第二行：同步配置\\n第三行：检查结果\\n第四行：记录时间|1行目：接続の確認\\n2行目：設定の同期\\n3行目：結果の確認\\n4行目：時刻の記録\n播放通知声音|通知音の再生\n接收全部通知|すべての通知\n仅接收重要通知|重要な通知のみ\n暂不可选|選択不可\n暂停通知|通知の一時停止\n默认 0 / 100|既定 0 / 100\n范围 20–80，值 65|範囲 20–80、値 65\n禁用与自定义背景|無効・背景色を変更\n计算机|コンピューター\n示例文件夹|サンプルフォルダー\n素材|マテリアル\n模板|テンプレート\nEasyVRUI控件演示|EasyVRUIコントロールデモ\n窗口与交互控件|ウィンドウとインタラクションコントロール\nウィンドウと操作コントロール|ウィンドウと操作コントロール\n跟踪参考|トラッキング\n追従基準|追従基準\n你好，VR|こんにちは、VR\n打开设置|設定を開く\n設定を開く|設定を開く\n新建窗口|新規ウィンドウ\n新規ウィンドウ|新規ウィンドウ\n文本|テキスト\n绘图|描画\n描画|描画\n多行|複数行\n複数行|複数行\n输入|入力\n入力|入力\n容器|コンテナ\n列表|リスト\n屏幕|画面\n画面|表示\n表格|テーブル\n工具栏|ツールバー\n启用选项|オプションの有効化\nオプションを有効化|オプションの有効化\n第一项|項目1\n選択肢 1|オプション1\n第二项|項目2\n選択肢 2|オプション2\n文件(&F)|ファイル(&F)\n视图(&V)|表示(&V)\n表示(&V)|表示(&V)\n工具(&T)|ツール(&T)\n欢迎|ようこそ\n快捷短语|クイックフレーズ\n定型文|定型文\n翻译历史|翻訳履歴\n履歴|履歴\n最近窗口|最近のウィンドウ\n最近のウィンドウ|最近のウィンドウ\n书签|ブックマーク\n偏好设置|環境設定\n環境設定|環境設定\n帮助|ヘルプ\nEasyVRUI日本語|EasyVRUI 日本語\nローマ字で入力|ローマ字入力\n日本語|日本語\n你好|こんにちは\n拟好|準備完了\n您好|こんにちは\n你好呀|こんにちは\nEasyVRUI拼音|EasyVRUI ピンイン\n文本输入|テキスト入力\nテキスト入力|テキスト入力\n输入一条短消息|短いメッセージを入力\n短いメッセージを入力|短いメッセージを入力\n发送|送信\n送信|送信\n文件管理器 — 示例文件夹|ファイルマネージャー — サンプルフォルダー\n桌面|デスクトップ\n窗体设计器|フォームデザイナー\n文件管理器|ファイルマネージャー\n控件演示|コントロールデモ\n保存窗体|フォームの保存\nフォームの保存|フォームの保存\n要保存对当前窗体所做的修改吗？|現在のフォームへの変更を保存しますか？\n現在のフォームへの変更を保存しますか？|現在のフォームへの変更を保存しますか？\n窗体设计文件|フォーム設計ファイル\nフォーム設計ファイル|フォーム設計ファイル\n所有文件|すべてのファイル\n记录 |レコード\n默认方向：horizontal|既定の方向：水平\n禁用 · 范围−20至20，当前为10|無効 · 範囲 -20～20、現在 10\nvertical · 当前为65|縦方向 · 現在65\n默认值与显示精度|既定値と表示精度\n范围−2.00至2.00|範囲 -2.00～2.00\n步长0.25 · 1.00 → 1.25|ステップ 0.25 · 1.00 → 1.25\n同一数值 · 禁用|同一の値 · 無効\n每5分钟|5分ごと\n每15分钟|15分ごと\n每30分钟|30分ごと\n每45分钟|45分ごと\n默认行高30 · 列表顶部|既定の行高 30 · リスト上部\n行高42 · 定位所选项|行高 42 · 選択項目の位置\n读取配置|設定の読み取り\n检查目录|ディレクトリの確認\n建立连接|接続の確立\n同步图像|画像の同期\n同步音频|音声の同期\n同步模型|モデルを同期\n核验校验和|チェックサムを検証\n生成报告|レポートを生成\n默认边框和背景|既定の枠線と背景\n背景色与嵌套子控件|背景色と子コントロール\n同步服务|同期サービス\n连接正常|接続正常\n滚动偏移0 · 内容超出视口|初期位置 · 下に項目あり\n滚动后 · 显示后续内容|スクロール後 · 続きの項目\n第一区|エリア 1\n第二区|エリア 2\nvertical · 左右分区|vertical · 左右分割\nhorizontal · 上下分区|horizontal · 上下分割\n概览|概要\n概览内容|概要コンテンツ\n历史|履歴\n历史内容|履歴内容\ntop · 默认选中第一页|top · 1ページ目を表示\nleft · 选中并重命名第二页|left · 2ページ目の名前を変更\n同步记录|同期ログ\n同步任务|同期タスク\n核验清单|チェックリスト\n本地配置|ローカル設定\n折叠 · 仅显示根节点|折りたたみ · ルートノードのみ表示\n展开 · 选中子节点|展開 · 子ノードを選択\n任务|タスク\n状态|状態\n完成|完了\n待处理|保留中\n默认单选|既定の単一選択\n多选 · 自定义列宽和行高|複数選択 · 列幅と行高を変更\n配置|設定\n数值|値\n任务数|タスク数\n重试次数|再試行回数\n整行选择 · 只读|行選択 · 読み取り専用\n单元格选择 · 编辑中|セル選択 · 編集中\n任务(&T)|タスク(&T)\n刷新记录(&R)|ログを更新(&R)\n显示已完成项(&S)|完了項目を表示(&S)\n清除历史(&C)|履歴を消去(&C)\n按住Alt · 显示助记符|Altを押す · 下線を表示\n键盘导航 · 行高42、勾选与禁用|キー操作 · 行高42、チェック、無効\n同步记录已刷新|同期ログを更新済み\n默认尺寸与间距|既定のサイズと間隔\n尺寸56 · 间距14 · 禁用右侧操作|サイズ56 · 間隔14 · 右端は無効\n已请求预览|プレビューを要求しました\n未获得画面|フレームを取得できません\n测试事件：采集源可用|テスト：取得元あり\n测试事件：采集源不可用|テスト：取得元なし\n无头渲染占位|ヘッドレスの仮表示\n等待画面|画面取得待ち\n无头WARP采集区域|ヘッドレスWARPの表示領域\n采集源可用|取得元あり\n边框属于父级panel|枠線は親のpanel\n替换前 · blank|置換前 · blank\n替换后 · label|置換後 · label\n内容已加载|読み込み済み\n命名同步报告|同期レポートの名前\n输入报告名称|レポート名を入力\n同步检查报告|同期チェックレポート\n保存同步报告|同期レポートを保存\n文本报告|テキストレポート\n同步速率|同期レート\n最近9次采样 · 归一化速率|直近9サンプル · 正規化レート\n空间定位配置|空間設定\n五种参考对象 · 窗口空间属性|5つの参照対象 · 空間プロパティ\n参考对象|参照対象\n跟踪目标|トラッキング対象\n固定的SteamVR跟踪空间|固定SteamVRトラッキングスペース\n头显姿态|ヘッドセットの姿勢\n校准朝向与身体平移|較正した向きと体の移動\n左手柄姿态|左コントローラーの姿勢\n右手柄姿态|右コントローラーの姿勢\n同步周期|同期間隔\n选择一个同步周期|同期間隔を選択\n当前周期：每5分钟|現在の間隔：5分ごと\n当前周期：|現在の間隔：\n编辑同步参数|同期パラメータの編集\n参数|パラメータ\n值|値\n并行任务|並列タスク\n双击值所在单元格进行编辑|値をダブルクリックして編集\n参数修改已提交|パラメーターを更新しました\n选择要查看的同步任务|同期タスクを選択\n尚未选择任务|タスクが選択されていません\n清理临时文件|一時ファイルを削除\n写入报告|レポートを書き出す\n选中任务：|選択したタスク：\n同步结果|同期結果\n文件数|ファイル数\n请选择同步记录|同期ログを選択\n当前记录：|現在の記録：\n任务分类|タスク分類\n检查报告|レポートを表示\n请选择任务|タスクを選択してください\n选中：|選択：\n延迟安装内容|後から追加する内容\n加载内容|内容を読み込む\n素材预览|素材プレビュー\n切换等比填充|フィット切替\n工作区命令|ワークスペースコマンド\n刷新记录|記録の更新\n等待刷新|更新待ち\n显示输出监视|出力モニターの表示\n等待显示器画面|モニター映像待ち\n采集源不可用|取得元なし\n预览操作|プレビュー操作\n预览结果|プレビュー結果\n单击蓝色操作项|青い操作項目をクリック\n连接分组|グループ接続\n连接正常，可以开始同步|接続済み。同期を開始できます\n隐藏连接详情|接続詳細を非表示\n显示连接详情|接続詳細を表示\n同步日志|同期ログ\n滚动查看同步步骤|同期手順へスクロール\n01 读取配置|01 設定の読み取り\n02 检查目录|02 ディレクトリの確認\n03 建立连接|03 接続の確立\n04 同步图像|04 画像の同期\n05 校验数据|05 データの検証\n06 生成报告|06 レポートの生成\n日志记录按时间排列|ログは時刻順\n双区工作台|2ペインワークスペース\n任务队列|タスクキュー\n同步摘要|同期サマリー\n拖动分隔条调整布局|仕切りをドラッグして調整\n布局比例已更新|レイアウト比率を更新しました\n同步工作台|同期ワークスペース\n同步服务已连接|同期サービスが接続済み\n最近一次同步已完成|前回の同期が完了\n已核验12份文件|12件のファイルを照合済み\n通知偏好|通知設定\n显示未读状态|未読状態を表示\n通知声音已关闭|通知音はオフです\n通知声音已开启|通知音はオンです\n校准增益|ゲイン調整\n范围：0.00至2.00|範囲：0.00～2.00\n当前增益低于基准|ゲインが基準未満\n当前增益达到或超过基准|ゲインが基準以上\n同步进度|同期進捗\n已同步2/8项|2/8項目を同期済み\n完成下一项|次の項目を完了\n同步完成|同期完了\n已同步|同期済み：\n/8项|/8項目\n通知模式|通知モード\n当前模式：仅接收重要通知|現在：重要な通知のみ\n当前模式：|現在のモード：\n监听音量|モニター音量\n音量较低|音量が低い\n音量较高|音量が高い\n设置尚未提交|設定が未保存です\n重新编辑|再編集\n设置已提交|設定が保存されました\n连接状态|接続状態\n已连接 · 测试服务|接続済み · テストサービス\n可以开始同步设置|設定の同期を開始できます\n编辑备注|メモを編集\n备注（最多80个字符）|メモ（最大80文字）\n请编辑或选择备注|メモを編集または選択\n全选备注|メモを全選択\n第一行：检查连接\\n第二行：同步配置|1行目：接続を確認\\n2行目：設定を同期\n备注已修改|メモを変更しました\n会话窗口|セッションウィンドウ\n当前窗口已显示|ウィンドウを表示中\n切换标题栏配色|タイトル色を切り替え\n"

def get_page_list():
    return [DOCS / "index.md", *(path for section in SECTION_LIST for path in sorted((DOCS / section).glob("*.md"))),]

def show_inventory():
    image_set = set()

    for page in get_page_list():
        relative = page.relative_to(DOCS)
        japanese = (DOCS / "ja") / relative
        image_list = IMAGE_PATH.findall(page.read_text(encoding = "utf-8"))
        image_set.update(image_list)
        japanese_size = japanese.stat().st_size if japanese.is_file() else 0
        print(f"{relative.as_posix()} {page.stat().st_size} {japanese_size} {' '.join(image_list)}")

    print(f"{len(image_set)} referenced PNGs")

def get_label_map(source):
    return dict(line.split("|", 1) for line in source.strip().splitlines())

@lru_cache
def get_font(size, bold):
    filename = "YuGothB.ttc" if bold else "YuGothM.ttc"
    return ImageFont.truetype(str(FONT_DIRECTORY / filename), size)

class japanese_diagram(advanced.diagram):
    label_map = get_label_map(DIAGRAM_LABEL_TEXT)
    han = re.compile(r"[\u3400-\u9fff]")

    def text(self, rectangle, message, size = 28, color = advanced.INK, bold = False, center = False):
        value = self.label_map[message] if self.han.search(message) else message
        left, top, right, bottom = rectangle
        rendered = value
        alignment = "center" if center else "left"

        for font_size in range(size, min(size, 17) - 1, -1):
            font = get_font(font_size, bold)
            x0, y0, x1, y1 = self.draw.textbbox((0, 0), value, font = font)
            width = x1 - x0
            height = y1 - y0

            if ((width + 4) <= (right - left)) and ((height + 4) <= (bottom - top)):
                break
        else:
            split_list = [index for index in range(1, len(value)) if (not (value[index - 1].isascii() and value[index - 1].isalnum() and value[index].isascii() and value[index].isalnum())) and (value[index] not in "。、）」・")]
            split_list.sort(key = lambda index: abs((2 * index) - len(value)))
            layout = None

            for font_size in range(size, min(size, 17) - 1, -1):
                font = get_font(font_size, bold)

                for index in split_list:
                    rendered = (value[: index].rstrip() + "\n") + value[index: ].lstrip()
                    x0, y0, x1, y1 = self.draw.multiline_textbbox((0, 0), rendered, font = font, spacing = 2, align = alignment)
                    width = x1 - x0
                    height = y1 - y0

                    if ((width + 4) <= (right - left)) and ((height + 4) <= (bottom - top)):
                        layout = rendered
                        break

                if layout:
                    break

            if not layout:
                raise ValueError(f"Label will not fit {rectangle}: {value}")

        x = (left + (((right - left) - width) // 2)) if center else (left + 2)
        y = top + (((bottom - top) - height) // 2)
        bounds = (x, y, x + width, y + height)

        if ((x < 16) or (y < 16) or (bounds[2] > (advanced.WIDTH - 16)) or (bounds[3] > (advanced.HEIGHT - 16))):
            raise ValueError(f"Outside diagram margins: {value}")

        for prior, box in self.text_rectangle_list:
            if ((bounds[0] < box[2]) and (box[0] < bounds[2])) and ((bounds[1] < box[3]) and (box[1] < bounds[3])):
                raise ValueError(f"Overlapping labels: {value} / {prior}")

        self.text_rectangle_list.append((value, bounds))
        self.draw.multiline_text((x - x0, y - y0), rendered, font = font, fill = color, spacing = 2, align = alignment)

def render_advanced(output):
    advanced.OUTPUT_DIRECTORY = output
    advanced.diagram = japanese_diagram
    advanced.run()

def localize_capture_source(source, label_map):
    def replace_literal(match):
        value = match[1]
        return ('"' + label_map.get(value, value)) + '"'

    def replace_encoded_literal(match):
        value = match[1].encode("ascii").decode("unicode_escape")
        target = label_map.get(value)

        if target is None:
            return match[0]

        literal = "".join(r"\U" + f"{ord(character):08x}" for character in target)
        return f'std::u32string{{U"{literal}", std::size_t{{{len(target)}u}}}}'

    text = re.sub(r'"((?:[^"\\]|\\.)*)"', replace_literal, source)
    return re.sub(r'std::u32string\{U"((?:\\U[0-9a-f]{8})+)", std::size_t\{\d+u\}\}', replace_encoded_literal, text)

def fit_application_layout(content):
    desktop = '            auto surface = make_shared<desktop_window>(U"tutorial_desktop");\n            show(surface, "desktop");\n            surface->label_clock->set_text(U"2026-11-21 (土) 03:28");\n\n            for(auto *item : surface->scrollpanel_app->get_control_list().get_item_list())\n            {\n                if(auto *tile = dynamic_cast<button *>(item))\n                {\n                    tile->set_font(font_t{U"Yu Gothic UI", 14u});\n                }\n            }\n\n            snapshot(surface, "desktop");'
    file_manager = '            show(surface, "file_manager");\n            constexpr uint64_t EXTRA_WIDTH = 30u;\n            auto computer = surface->button_computer->get_rect();\n            auto up = surface->button_up->get_rect();\n            auto path = surface->textbox_path->get_rect();\n            computer.width += EXTRA_WIDTH;\n            up.left += EXTRA_WIDTH;\n            path.left += EXTRA_WIDTH;\n            path.width -= EXTRA_WIDTH;\n            surface->button_computer->set_rect(computer);\n            surface->button_up->set_rect(up);\n            surface->textbox_path->set_rect(path);'
    task_manager = '            auto &column_list = surface->listview_detail->get_column_list();\n            column_list[4u]->set_width(125u);\n            column_list[6u]->set_width(149u);\n            snapshot(surface, "task_manager");'
    replacement_map = {'            capture_surface(make_shared<desktop_window>(U"tutorial_desktop"), "desktop");': desktop, '            show(surface, "file_manager");': file_manager, '            snapshot(surface, "task_manager");': task_manager, 'if(locale == "zh")\n            {\n                auto &workspace': 'if(locale == "ja")\n            {\n                auto &workspace', 'if(locale == "zh")\n            {\n                surface->open_document': 'if(locale == "ja")\n            {\n                surface->open_document',}

    for source, target in replacement_map.items():
        if content.count(source) != 1:
            raise RuntimeError(f"Expected one capture fixture anchor: {source}")

        content = content.replace(source, target, 1)

    return content

def prepare_capture_build(directory):
    tool_folder = SITE / "tools"
    basics = SITE / "examples/basics"
    lesson_folder = basics / "04_form_designer"
    label_map = get_label_map(CAPTURE_LABEL_TEXT)
    copy_map = {"ja_capture_ui.cpp": tool_folder / "capture_ui.cpp", "ja_project_story.cpp": tool_folder / "capture_project_story.cpp", "ja_first_window.cpp": basics / "03_first_window/cpp/main.cpp", "ja_shout_main.cpp": lesson_folder / "cpp/main.cpp", "ja_shout_window.cpp": lesson_folder / "cpp/quick_shout_window.cpp",}

    for filename, path in copy_map.items():
        content = path.read_text(encoding = "utf-8")

        if filename == "ja_capture_ui.cpp":
            content = fit_application_layout(content)
        else:
            content = localize_capture_source(content, label_map)

        (directory / filename).write_text(content, encoding = "utf-8", newline = "\n")

    extra = f'''include("{(tool_folder / "capture_project.cmake").as_posix()}")\nfunction(configure_ja_capture)\n    foreach(role IN ITEMS desktop designer file_manager task_manager)\n        set(target "tutorial_capture_${{role}}")\n        get_target_property(source_list "${{target}}" SOURCES)\n        list(REMOVE_ITEM source_list "{(tool_folder / "capture_ui.cpp").as_posix()}")\n        list(APPEND source_list "{(directory / "ja_capture_ui.cpp").as_posix()}")\n        set_property(TARGET "${{target}}" PROPERTY SOURCES "${{source_list}}")\n    endforeach()\n    set_property(TARGET tutorial_capture_project_story PROPERTY SOURCES "{(directory / "ja_project_story.cpp").as_posix()};{(directory / "ja_first_window.cpp").as_posix()};{(directory / "ja_shout_main.cpp").as_posix()};{(directory / "ja_shout_window.cpp").as_posix()}")\n    target_include_directories(tutorial_capture_project_story PRIVATE "{(lesson_folder / "cpp").as_posix()}")\nendfunction()\ncmake_language(DEFER CALL configure_ja_capture)\n'''
    project = directory / "capture_project.cmake"
    project.write_text(extra, encoding = "utf-8", newline = "\n")
    return project

def format_file_dialog_rows(collection):
    return f'            auto &entry_list = dynamic_cast<listview &>({collection}[U"listview_entry"]);\n\n            for(size_t index = 0u;index < entry_list.get_item_list().get_size();index++)\n            {{\n                auto &cells = entry_list.get_item_list()[index]->get_cell_list();\n                const auto &filename = cells[0u];\n                u32string kind = U"フォルダー";\n\n                if(filename.ends_with(U".txt"))\n                {{\n                    kind = U"テキスト文書";\n                }}\n                else if(filename.ends_with(U".json"))\n                {{\n                    kind = U"JSONファイル";\n                }}\n                else if(filename.ends_with(U".easyvruifrm"))\n                {{\n                    kind = U"フォーム設計";\n                }}\n\n                cells.set_cell(1u, U"2026/11/21 04:17");\n                cells.set_cell(2u, kind);\n            }}\n\n'

def fit_guide_layout(source, role):
    source = source.replace('U"Microsoft YaHei UI"', 'U"Yu Gothic UI"')

    if role == "controls_second":
        fixed_click = 'click("tabcontrol_demo", 128.0, 102.0);\n            auto &tabs = dynamic_cast<tabcontrol &>(demo->get_control_list()[U"tabcontrol_workspace"]);'
        measured_click = 'auto &tabs = dynamic_cast<tabcontrol &>(demo->get_control_list()[U"tabcontrol_workspace"]);\n            const auto TAB = tabs.get_rect();\n            constexpr double TAB_MINIMUM_EXTENT = 48.0;\n            constexpr double TAB_PADDING_WIDTH = 24.0;\n            double first_width = max(TAB_MINIMUM_EXTENT, measure_text(tabs.get_page_list()[0u].get_text(), tabs.get_tab_font()) + TAB_PADDING_WIDTH);\n            double second_width = max(TAB_MINIMUM_EXTENT, measure_text(tabs.get_page_list()[1u].get_text(), tabs.get_tab_font()) + TAB_PADDING_WIDTH);\n            click("tabcontrol_demo", (static_cast<double>(TAB.left) + first_width) + (second_width * 0.5), static_cast<double>(TAB.top) + (static_cast<double>(tabs.get_tab_size()) * 0.5));'

        if source.count(fixed_click) != 1:
            raise RuntimeError("Could not locate the tabcontrol action in the capture fixture.")

        source = source.replace(fixed_click, measured_click)

    if role == "controls_third":
        save_snapshot = '            finish(save, "dialog_file_save");'

        if save_snapshot not in source:
            raise RuntimeError("Could not locate the file-save dialog snapshot.")

        source = source.replace(save_snapshot, format_file_dialog_rows("collection") + save_snapshot)

    if role == "dialog":
        color_layout = 'if(locale == "zh")\n            {\n                color->get_control_list()'
        source = source.replace(color_layout, color_layout.replace('"zh"', '"ja"'), 1)
        source = source.replace('U"サンプルフォルダー"', 'U"サンプル"', 1)
        open_snapshot = '            snapshot(open, "dialog_file_open");'

        if open_snapshot not in source:
            raise RuntimeError("Could not locate the file-open dialog snapshot.")

        source = source.replace(open_snapshot, format_file_dialog_rows("control_list") + open_snapshot)

    if role == "demo":
        source = source.replace('U"オプションを有効化"', 'U"有効にする"', 1)

    return source

def prepare_guide_capture_build(directory):
    tool_folder = SITE / "tools"
    example_map = {path.parents[1].name: path for path in (SITE / "examples/guide/controls").glob("*/*/cpp/main.cpp")}
    label_map = get_label_map(GUIDE_LABEL_TEXT)
    cmake_list = [f'include("{(tool_folder / "capture_project.cmake").as_posix()}")', "function(configure_japanese_guide_capture)",]

    for role, filename in GUIDE_SOURCE_MAP.items():
        target = f"tutorial_capture_{role}"
        file_list = [tool_folder / filename, *(example_map[name] for name in capture.CONTROL_CAPTURE_MAP.get(role, ())),]
        cmake_list.append(f"    get_target_property(source_list {target} SOURCES)")

        for index, original in enumerate(file_list):
            original = original.resolve()
            source = original.read_text(encoding = "utf-8")

            if index == 0:
                source = fit_guide_layout(source, role)

            source = localize_capture_source(source, label_map)
            localized = directory / f"{role}_{index}_{original.name}"

            if (not localized.is_file()) or (localized.read_text(encoding = "utf-8") != source):
                localized.write_text(source, encoding = "utf-8", newline = "\n")

            cmake_list.extend(["    set(updated_source_list)", "    foreach(source IN LISTS source_list)", "        cmake_path(NORMAL_PATH source OUTPUT_VARIABLE normalized_source)", f'        if(normalized_source STREQUAL "{original.as_posix()}")', f'            set(source "{localized.as_posix()}")', "        endif()", '        list(APPEND updated_source_list "${source}")', "    endforeach()", '    set(source_list "${updated_source_list}")', f'    target_include_directories({target} PRIVATE "{original.parent.as_posix()}")',])

        cmake_list.append(f'    set_property(TARGET {target} PROPERTY SOURCES "${{source_list}}")')

    cmake_list.extend(["endfunction()", "cmake_language(DEFER CALL configure_japanese_guide_capture)"])
    project = directory / "capture_project.cmake"
    project.write_text("\n".join(cmake_list), encoding = "utf-8", newline = "\n")
    return project

def render_guide(output, repository, reuse_binaries):
    directory = GUIDE_WORK / "native"
    directory.mkdir(parents = True, exist_ok = True)
    role_list = tuple(GUIDE_SOURCE_MAP)

    if not reuse_binaries:
        capture.build_capture_targets(directory / "build", prepare_guide_capture_build(directory), role_list)

    with TemporaryDirectory(prefix = "guide_", dir = GUIDE_WORK) as name:
        stage = Path(name)
        installation = stage / "installation"
        profile = stage / "profile"
        fixture = stage / "Examples"
        images = stage / "images"
        capture.stage_installation(installation, repository, role_list)
        capture.prepare_fixture(fixture)
        (profile / "Roaming").mkdir(parents = True)
        (profile / "Local").mkdir()

        for role in role_list:
            capture.run_capture(installation, directory / "build", role, images, fixture, profile, "ja")

        capture.combine_window_comparison(images)
        capture.combine_menu_comparison(images)
        mockup.make_anchors("ja").convert("RGB").save(images / "vr_spatial_anchors.png")
        mockup.make_curvature("ja", images).convert("RGB").save(images / "vr_curvature_and_handles.png")
        name_set = {f"{control}_{state}.png" for control_list in capture.CONTROL_CAPTURE_MAP.values() for control in control_list for state in ("default", "comparison", "demo")}
        name_set.update(f"{name}.png" for name in (*capture.TOPIC_IMAGE_LIST, *capture.CAPTURE_MAP["dialog"], "demo_controls", "vr_spatial_anchors", "vr_curvature_and_handles",))

        for name in sorted(name_set):
            source = images / name
            width, height = capture.check_image(source)
            shutil.copyfile(source, output / name)
            print(f"{name} {width}x{height}")

def get_capture_asset_list():
    return ("desktop", "form_designer", "file_manager", "task_manager", "layout_keyboard", "ime_candidates", "basics_form_design", *capture.STORY_IMAGE_LIST, "vr_hero_workspace", "vr_curvature_and_handles", "vr_input_stack", "vr_designer_annotated",)

def render_capture(output, repository, reuse_binaries):
    WORK.mkdir(parents = True, exist_ok = True)
    native = WORK / "native"
    native.mkdir(exist_ok = True)

    if not reuse_binaries:
        capture.build_capture_targets(native / "build", prepare_capture_build(native), NATIVE_ROLE_LIST)

    with TemporaryDirectory(prefix = "capture_", dir = WORK) as name:
        stage = Path(name)
        installation = stage / "installation"
        profile = stage / "profile"
        asset_directory = stage / "assets"
        fixture = stage / "Examples"
        capture.stage_installation(installation, repository, NATIVE_ROLE_LIST)
        capture.prepare_fixture(fixture)
        form = stage / "quick_shout_window.easyvruifrm"
        form.write_text(localize_capture_source(form.read_text(encoding = "utf-8"), get_label_map(CAPTURE_LABEL_TEXT)), encoding = "utf-8", newline = "\n",)
        (profile / "Roaming").mkdir(parents = True)
        (profile / "Local").mkdir()

        for role in NATIVE_ROLE_LIST:
            destination = (asset_directory / role) if (role in ("pinyin", "japanese")) else asset_directory
            capture.run_capture(installation, native / "build", role, destination, fixture, profile, "ja")

        capture.combine_ime_preview(asset_directory)
        part_directory = asset_directory / "japanese"
        shutil.copyfile(asset_directory / "designer_regions.json", part_directory / "designer_regions.json")

        for key, image in (("vr_hero_workspace", mockup.make_hero("ja", asset_directory)), ("vr_curvature_and_handles", mockup.make_curvature("ja", asset_directory)), ("vr_input_stack", mockup.make_input("ja", asset_directory, part_directory)), ("vr_designer_annotated", mockup.make_designer("ja", asset_directory, part_directory)),):
            image.convert("RGB").save(asset_directory / f"{key}.png")

        for key in get_capture_asset_list():
            source = asset_directory / f"{key}.png"
            size = capture.check_image(source)
            shutil.copyfile(source, output / source.name)
            print(f"{source.name} {size[0]}x{size[1]}")

def run():
    parser = ArgumentParser(description = "Generate the Japanese tutorial diagrams and WARP captures.")
    parser.add_argument("--inventory", action = "store_true", help = "List the Japanese batch-one pages and their reference images.",)
    parser.add_argument("--advanced", action = "store_true", help = "Draw the nine localized advanced diagrams.",)
    parser.add_argument("--capture", action = "store_true", help = "Build and capture Japanese basic and project UI with WARP.",)
    parser.add_argument("--guide", action = "store_true", help = "Build and capture Japanese controls, dialogs, and related diagrams.",)
    parser.add_argument("--reuse-binaries", action = "store_true", help = "Use the Japanese WARP fixture binaries from a previous run.",)
    parser.add_argument("--output", type = Path, default = OUTPUT)
    parser.add_argument("--repository", type = Path, default = capture.WORKSPACE / "repo")
    option = parser.parse_args()
    output = option.output.resolve()

    if not any(output.is_relative_to(directory.resolve()) for directory in (OUTPUT, WORK, GUIDE_WORK)):
        parser.error("Output must stay inside the Japanese image or working directory.")

    if option.inventory:
        show_inventory()

    if option.advanced:
        output.mkdir(parents = True, exist_ok = True)
        render_advanced(output)

    if option.capture:
        output.mkdir(parents = True, exist_ok = True)
        render_capture(output, option.repository.resolve(), option.reuse_binaries)

    if option.guide:
        output.mkdir(parents = True, exist_ok = True)
        render_guide(output, option.repository.resolve(), option.reuse_binaries)

if __name__ == "__main__":
    run()