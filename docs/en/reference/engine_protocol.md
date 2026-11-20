# Engine Protocol Reference

The installed Engine executable file is `bin/easyvrui_engine.exe`. Engine is responsible for VR tracking, laser hit detection, window surfaces, graphics resources, and input routing. The SDK manages controls, records drawing commands, and dispatches application events.

The SDK reads the application list on the machine where the calling process is located and starts the program, with the entry point being `launch_application()`. Engine provides `application_list` and `application_terminate` for management sessions. The application provides a non-empty `name` in the handshake, and coordinates the single instance on its own.

The strings enclosed in angle brackets in the examples are placeholders, which should be replaced with actual configurations and handshake data during integration.

Engine provides the following communication and process coordination entries.

* IPv4/IPv6   TCP/TLS interface: Monitors `0.0.0.0:<port>` and `[::]:<port>`, carrying the main data streams. Initialize monitoring in order of IPv4 and IPv6, with IPv6 setting `v6_only=true`; both monitoring channels must be initialized successfully.
* Windows named pipe: `\\.\pipe\EasyVROverlayUIEngine.Bootstrap`, provides the local SDK with port number, access credentials, and public key fingerprint.
* Windows named mutex: `Local\EasyVROverlayUIEngine.Engine`, used to coordinate the single instance of Engine.

## IPv4/IPv6   TCP/TLS interface

### Connection and startup parameters

#### Engine configuration

Ports and shared access credentials are stored in `config.json` in the same directory as the Engine executable file, with the installation path being `bin/config.json`. The default port is `49537`. Access credentials are non-empty strings; if missing, they are initialized with random values. Below are examples of related configuration items; the actual file may also include input component configurations.

Engine configuration segments:

```json
{
    "ipc_service_port": 49537,
    "access_credential": "<自行设置的共享接入凭据>"
}
```

#### Local SDK connection

The SDK discovers the Engine through the local named pipe by default, obtaining the actual port, access credentials, public key fingerprint, and PID, and then connects to the local TCP/TLS service.

#### Remote SDK connection

Remote connection parameters are passed to the application process using the SDK, with the application's own parameters added directly to the same command line.

* `--easyvrui-host`: Remote hostname or IPv4/IPv6 address, required; IPv6 uses raw addresses, such as `::1`.
* `--easyvrui-port`: Decimal port, `49537` if omitted; valid range is from `1` to `65535`.
* `--easyvrui-access-credential`: Access credentials, required.
* `--easyvrui-public-key-fingerprint`: Server public key fingerprint, required; should use the SHA-256 hexadecimal string from the discovery information.

Only the `--name=value` format is supported. Separate parameter names and values with a `=`; values containing spaces use CMD quotes. If any of these four parameters appear, it will be verified in the remote mode. Errors occur if host, credentials, or fingerprint are missing, if any parameter appears repeatedly, if the value is empty, or if the port is not a decimal number, zero, or overflows.

C++ and Python share the same native library, which reads the current Windows process command line. If the application uses its own `argparse` or other parameter parsers, it should declare and accept these parameters, or leave unknown parameters for the SDK to read.

The following are all Windows CMD single-line examples. The 64 zeros in the fingerprint are placeholders; replace them with the actual fingerprint during connection.

```cmd
my_vr_app.exe --easyvrui-host=192.0.2.10 --easyvrui-port=49537 --easyvrui-access-credential="demo credential with spaces" --easyvrui-public-key-fingerprint=0000000000000000000000000000000000000000000000000000000000000000
```

```cmd
python my_vr_app.py --easyvrui-host=::1 --easyvrui-access-credential="demo credential with spaces" --easyvrui-public-key-fingerprint=0000000000000000000000000000000000000000000000000000000000000000
```

### TLS

TLS uses a self-signed ECC P-256 certificate to establish server trust through a fixed public key fingerprint. The public key fingerprint is a 64 hexadecimal characters derived from the DER encoding of the certificate's SubjectPublicKeyInfo, calculated using SHA-256, and provided by the local pipeline. The remote SDK retrieves this value in advance for server verification. The certificate and persistent private key are stored in the current Windows user's certificate and key store. During startup, the authentication algorithm, certificate validity, and key pairing are verified, and valid resources are reused. The certificate's validity period expires on December 31, 9999, at 23:59:59. After generating a new private key, the remote SDK uses the new public key fingerprint.

Schannel negotiates the TLS version based on system configuration, with the Engine requiring TLS 1.2 or higher. The TLS handshake timeout is 5 seconds. After completing TLS, application-layer authentication is performed, and both the length header and JSON are transmitted over the TLS encrypted channel.

### Application-layer frame format

#### Length header and message body

All custom application-layer frames, including authentication-before messages, authentication-after requests, responses, heartbeats, and push messages, as well as local named pipe discovery messages, are uniformly defined as follows:

```text
8-byte little-endian uint64 length | UTF-8 JSON payload
```

The number of UTF-8 bytes in the message body after JSON serialization. The message body is a complete JSON object encoded in UTF-8 without BOM, with the frame length including the actual format whitespace sent. The receiver first reads the exact 8-byte length header, then reads the message body precisely according to the length, thereby defining the boundaries of protocol messages.

The following message body uses LF line breaks without a trailing line break, consisting of 14 UTF-8 bytes:

```json
{
    "a": 1
}
```

The corresponding complete plaintext segment is:

```text
0E 00 00 00 00 00 00 00 7B 0A 20 20 20 20 22 61 22 3A 20 31 0A 7D
```

The length must be a positive integer representable by the size type of the receiving process.

#### JSON and binary fields

Business messages use JSON. Binary fields such as image pixels are encoded using standard RFC 4648 Base64 continuous strings, using the `A-Z a-z 0-9 + /` alphabet and the necessary `=` padding. First, the binary fields are encoded, then the entire JSON is serialized, and finally the frame length is calculated. An empty binary sequence is encoded as `""`.

The length of Base64 text is `4 × ceil(原始字节数 / 3)`.

### Application-layer authentication

After TLS is completed, there is an additional 5-second total timeout for application-layer authentication. The following four JSON objects are framed independently, all using an 8-byte little-endian length header. If authentication fails, times out, or the handshake message is invalid, the server closes the connection.

#### Client greeting: `client_hello`

The client declares the protocol version, the current random nonce, its PID, and session name:

Client → Engine:

```json
{
    "message_type": "client_hello",
    "version": 1,
    "client_nonce": "0000000000000000000000000000000000000000000000000000000000000000",
    "process_id": 23456,
    "name": "demo"
}
```

`version` is fixed as an integer `1`. Standard SDKs generate `client_nonce` using 32 random bytes and then encode it as a hexadecimal string; the current server checks this field as a string. `process_id` is a uint32 PID. After obtaining the actual local connection process, the Engine will verify that the declared PID is consistent; the remote PID is recorded as the client's declared information. `name` is the session name, which must be a non-empty UTF-8 string. The Engine displays the session in the application list by this name. If the name is missing or empty, the handshake fails, and the connection is closed.

#### Server challenge: `challenge`

Engine → Client:

```json
{
    "message_type": "challenge",
    "version": 1,
    "server_nonce": "1111111111111111111111111111111111111111111111111111111111111111"
}
```

`server_nonce` is generated from 32 random bytes and then encoded as a hexadecimal string. The client must check the version.

#### Client proof: `authenticate`

`proof` is the hexadecimal result of HMAC-SHA256. The key is the UTF-8 bytes of the access credentials; the data is the UTF-8 bytes of the following strings, connected by LF between lines, with the last line being `server_nonce`:

```text
easyvrui-ipc-auth-v1\n<client_nonce>\n<server_nonce>
```

The equivalent calculation method is:

```text
proof = hex(HMAC-SHA256(access_credential, "easyvrui-ipc-auth-v1\n" + client_nonce + "\n" + server_nonce))
```

The standard output for nonce, proof, session_token, and public key fingerprints uses lowercase hexadecimal. Nonce is calculated based on the actual text in the message; access credentials use the original UTF-8 bytes, and spaces in the string are also included in the HMAC. The proof message is as follows:

Client → Engine:

```json
{
    "message_type": "authenticate",
    "proof": "<上述HMAC结果的64个十六进制字符>"
}
```

#### Session confirmation: `welcome`

Engine → Client:

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

`process_id` is the PID of the Engine; `owner_process_id` is the PID of the application it connects to, derived from the verified local process identity or client declaration. `owner_created` is the original creation time of the verified Windows process, used to distinguish PID reuse; if not verified, it is `0`.

`session_token` is generated from 32 random bytes and then converted into a hexadecimal string. Each authenticated TCP connection has a `session_id` and token; the same PID can establish multiple independent sessions. A reconnection after closing will create a new session.

## Communication protocol after session establishment

### Common fields

#### Request structure

The following `ping` is a complete public request example that can be actually sent. Other operations replace `op` with specific fields:

Request:

```json
{
    "message_type": "request",
    "id": 1,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "op": "ping"
}
```

`message_type` is fixed as `request`, and `id` is the uint64 request sequence number, used by the client for corresponding responses; the SDK automatically increments and fills in. Each request must include the current connection's `session_id` and `session_token`. The window ID and component ID identify the respective resources.

In JSON, all uint32/uint64 values are non-negative integers. The range for uint32 is from `0` to `2^32-1`, and for uint64, it is from `0` to `2^64-1`. Languages that require integration must use integer parsing methods that can accurately retain the entire range.

Field names, operation names, event names, and enumeration strings must match exactly in case and case insensitive. Field names in the same JSON object must remain unique. Integers, boolean values, strings, and arrays are validated according to their respective JSON types; explicit `null` is only used for fields indicated as optional in the interface. When optional fields are omitted, the initial values or retention rules defined by the interface are used.

Requests, window properties, and drawing commands operate according to the defined fields, with additional fields ignored; event extension fields are defined by the SDK. The values of `op`, `event_type`, and drawing `type` must belong to the defined sets of corresponding interfaces.

`id` in the same connection that has not been completed remains unique. Responses and events can be interleaved; long operations are completed asynchronously; the caller receives corresponding results based on `id`. After a timeout occurs, the caller decides whether to retry based on the operation status, and the connection is re-established as a new session.

#### Successful response structure

Response:

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

`id` echoes the corresponding request sequence number, `ok` is `true`, and the type of `value` is determined by the specific operation, which can be `null`, boolean value, integer, string, array, or object. Request responses and events can be interleaved; the client distinguishes messages through `message_type`, responds with `id`, and distributes events with `event_type`.

#### Failed response structure

Example of failed business operation:

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

`language_key` is used to find language packs, `argument_list` is the format parameter, `diagnostic` retains the source file, rows, functions, and conditions. `message` is for single-line localization diagnostics; the actual content, location, and error keys depend on the cause of the failure. Unknown standard exceptions may only retain the captured boundary position.

Each operation is given a successful response; business exceptions thrown during request processing use this failed structure. Whether an operation is successful is determined by `ok`; `false` or `null` in `value` may be normal results. Invalid JSON, incorrect session/token, authentication failure, read/write failure, timeout, and other issues may directly lead to connection closure.

### Heartbeat and Survival Detection

#### Client Heartbeat

Heartbeat uses an independent `message_type`, with the structure as follows:

Client → Engine:

```json
{
    "message_type": "heartbeat",
    "session_id": 1,
    "session_token": "<会话令牌>"
}
```

#### Server Heartbeat

Engine → Client:

```json
{
    "message_type": "heartbeat",
    "session_id": 1,
    "session_token": "<会话令牌>"
}
```

Heartbeats are independently sent every second on both ends. The survival time is refreshed upon receiving complete messages, and normal business messages are also valid; the server processes the messages after verifying the session to which they belong.

If no complete message is received after 10 seconds, disconnection occurs during scheduled checks; a single write also has a 10-second duration. Survival detection is based on the time of receipt of complete messages. The standard SDK automatically manages heartbeats, and `ping` is used for ordinary business queries.

### Window Surface and Drawing Submission

#### Submission window and drawing node: `present`

A single submission can include multiple windows. Each is identified by the local window ID of this session and carries the window attributes and drawing node of this update. The following `command_list` contains a rectangular filling command covering a 640 × 360 logical area, with color `0x202020FF`, corresponding to the JSON integer `538976511`.

`window_list` is the set of this update. Omitted windows continue to exist. Windows are created when they first appear and updated when they exist; Engine assigns global window IDs.

Request:

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

Successful Response:

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

The type, initial value, and rules for `metadata` are shown in the table below. `auxiliary` marks auxiliary surfaces; the current window is selected from ordinary surfaces.

The fields of window update items are as follows:

|Field|Type|Rules|
|---|---|---|
|`window`|uint64|Required, local ID of windows within this session|
|`metadata`|Object|Required for first creation, can be omitted for subsequent updates|
|`node_list`|Object array|Can be omitted, default is `[]`, only listing nodes for this update|
|`order`|uint64 array|Can be omitted, retaining the existing order; when provided, describe the complete set and drawing order|

The initial value and type of the `metadata` field are as follows, with subsequent submissions merging by field:

|Field|Type|Initial value or constraint|
|---|---|---|
|`width`、`height`|uint64|Required for first creation, all must be greater than zero|
|`physical_scale`|Finite value|Required for the first creation, greater than zero, indicating the scaling factor of logical pixel to physical size; when it is 1, each logical pixel is 0.001 meters.|
|`curvature`|Finite value|Default is `0.0`, greater than or equal to zero, in meters' reciprocal; the product of curvature and effective physical width must be less than `2π`.|
|`position`、`rotation`|An array of finite values with a length of 3.|All default to `[0.0,0.0,0.0]`, with units being meters and degrees respectively.|
|`visible`、`enabled`|Boolean value.|All default to `true`.|
|`auxiliary`|Boolean value.|Default to `false`.|
|`title`|String.|By default, it is set to `""`, which stores the SDK window title. It serves as a fixed attribute for the Engine form state, similar to `name`, and supports incremental updates.|
|`name`|String.|Default to `""`, used to save the SDK window name.|
|`reference`|String.|For ordinary surfaces, the default value is `world`, but it is set to `world/body/head/left/right`; auxiliary surfaces are maintained by the Engine with valid reference poses.|
|`startup_position`|String.|Optional, default is `none/center`; can be omitted to `none`; describes the initial positioning of the first ordinary surface.|
|`startup_owner`|uint64|Optional, local ID of the source window in the same session; if omitted or 0, the currently selected ordinary surface is used preferentially. If there is no valid source, it centers on the headset.|

`startup_position=center` is automatically positioned once when the first ordinary surface is created. Non-zero `startup_owner` strictly uses the source window in the same session; this window can exist or be in the same batch submission, with the submission order being arbitrary, and the source relationship must be acyclic. center requires an effective headset pose; invalid explicit sources or cyclic relationships result in a failure response. This batch of windows is submitted uniformly after successful verification and positioning.

When `startup_owner` is omitted or 0, Engine preferentially uses the currently selected visible ordinary surface before submission as the source, which can cross sessions, such as starting other apps from the rotated Desktop. Auxiliary surfaces, self, and world poses are not valid for exiting candidates; if there is no valid source, it centers in front according to the current headset pose.

The new window is parallel to the plane of the source window and centered on it, moving forward along the normal of the side where the headset is located; the front and back are selected in the corresponding directions. Engine combines the actual poses of visible ordinary windows across all sessions to arrange different initial depths for nearly parallel surfaces with overlapping projections. The source only determines the first positioning; subsequent movements are determined by the new window's reference and position/rotation.

`none` retains the submitted pose, allowing explicit overlap. The SDK window defaults to center, with a prompt for the first present; when present is directly submitted without a prompt, none is used. Auxiliary surfaces follow the automatic positioning rules of the input area. Repeated startup prompts maintain the determined position, with subsequent poses updated through position and rotation.

The successful response value is null if there is no first center positioning result this time; if there is a positioning result, it is an object, with window_list returning the local ID of the window and the final position/rotation under the current reference. Position is in meters, and rotation is in three-axis Euler angles. The SDK synchronizes object properties with the submitted cache during the completion callback, retaining any new property changes that occur during the waiting period for response.

Example of the first center positioning response:

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

Both `name` and `title` are stored in the Engine form state. Each window returned by the application list includes `id`, `name`, `title`, and `visible`; `title` is updated with the SDK window title, and the task manager uses it to display window titles. The application window list and count only count ordinary surfaces, including hidden windows and ordinary modal windows.

`window_list` must be an array, and `[]` indicates an empty update. Window IDs are parsed within the session, and node IDs are parsed within the window; windows recreated after closing use independent resource lifecycles. Window instances retain their local ID during their existence.

`node_list` is the list of drawing nodes updated this time, which is omitted for `[]`; each item contains a `node` of type uint64 and an array of drawing command objects `command_list`. Each command is identified by the string `type`, and the remaining fields describe the drawing parameters. The window IDs and node IDs within the same window remain unique in each submission.

`order` contains all the drawing node IDs retained by the window and their drawing order. Each ID must correspond to a cached or submitted node, and the array elements are unique. The Engine draws in the order of the array, with later drawings overlapping the earlier ones. For example, if the background node is 10, the button is 20, and the text box is 30, then `order` would be `[10,20,30]`. `node_list` is responsible for updating node content, while `order` is responsible for arranging and retaining nodes.

#### Incremental updates, node deletion, and empty content

Existing windows are updated incrementally: When `metadata` is omitted or `metadata: {}` is provided, the existing properties are retained; when fields are provided, only the explicitly submitted fields are updated, and the remaining fields remain at their current values. Default values apply only during the first creation. Fields submitted in the table are verified according to their respective rules, and the position and rotation arrays are replaced with complete fields. Explicit `false`, zero, and empty strings are processed according to the corresponding field rules.

When `metadata` is provided, it must represent an object. Attributes are filled in according to the initial default values during the first creation, and fields are merged based on the existing state during subsequent updates, then the final window state is verified. The surface of the component session is uniformly marked with `auxiliary=true` by the Engine, following the input-assisted positioning rules; ordinary application sessions create surfaces based on the `auxiliary` attributes of each window.

`order` can be omitted, in which case the original window order is used; when new windows submit drawing nodes, `order` must be provided to reference these nodes. `node_list` only lists the nodes changed this time, and the window reuses the other cached nodes in `order`. `metadata` is omitted when only drawing content is updated; when only window attributes are updated, the corresponding fields are submitted, and `node_list` is omitted to reuse the drawing cache.

The server retains the node cache according to the final `order` and determines the display order. When a node is deleted, the corresponding ID is removed from the new `order`; `order: []` clears all nodes in the window.

`command_list: []` represents zero drawing commands. Node IDs and drawing positions can be retained, and the content can be cleared. Below, node 1 is cleared:

Request:

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

Successful Response:

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

When only the window is moved, the update items in `window_list` can be written as:

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

The Engine prepares the data for each window this time and writes it into the surface state after processing. `ok:true` indicates that updates have been accepted during runtime, and `render_error` may still be pushed asynchronously during subsequent drawing or texture submission.

#### Closing the window surface: `surface_close`

Search for the current `window` in the session, and release the surface and laser capture when closing. When targeting the current window, close the associated input interface, and restore the windows paused due to disabling according to the current window rules; if there are no recoverable windows, clear the current selection. Other surfaces referencing this window may fail to locate due to the reference object becoming invalid. Return a business error if the search fails.

Request:

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

Successful Response:

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

### Laser capture

#### Capturing the laser: `pointer_capture`

`hand` is either `left` or `right`, and `window` must be the local ID of the existing window in this session. Capturing is possible when the current trigger or side grip key is pressed and hits the specified window. When the key enters a waiting-release state, releasing it and pressing it again can initiate capturing. After leaving the window boundary, coordinates can still be received, and the coordinates may exceed the logical rectangle.

`lock_position` is an optional boolean value, defaulting to `false`. When set to `true`, the visible laser endpoint is fixed at the window's logical coordinates at the time of capture, and it repositions with the window's current size, curvature, and pose per frame; the coordinates and rays for SDK delivery are still updated based on actual controller input. The same locking rules apply for SDK for window movement, rotation, zooming, and curvature adjustment. Ordinary controls retain the default values when dragged. Endpoint locking is cleared simultaneously when capturing is released or invalidated.

When the legal target does not meet the capture conditions, return `false`; when the trigger is illegal, the window does not exist, or it belongs to another session, return a business error.

Request:

```json
{
    "message_type": "request",
    "id": 20,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "op": "pointer_capture",
    "lock_position": false,
    "hand": "right",
    "window": 100
}
```

Successful Response:

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

Successful responses when capture conditions are not met:

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

#### Release the laser: `pointer_release`

Take `hand` from `left` or `right`. Release the capture of this trigger if there is no capture in this session; otherwise, return `null`. Return a business error when the trigger is illegal. When the trigger and side grip keys are both released, the Engine automatically releases the capture; the SDK actively releases the capture based on the key used to initiate interaction, such as releasing the side grip key to end window movement. When the window closes, becomes hidden, or the session is cleared, the Engine immediately removes the capture of the window; for SDKs still connected, send `event_type="pointer"` and `lost=true` events, and the SDK cancels the current interaction. The trigger or side grip key must be released before accepting a new interaction.

Request:

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

Successful Response:

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

### Current window and keyboard routing

The Engine maintains a global current window, which is empty at startup. When a regular window is hidden or closed and then displayed again, it is selected by pressing the laser; the Desktop is selected by Ctrl+Pause. When the laser is pressed on a interactive regular window, window selection is initiated, and after completing the related emptying, it is set as the current window; hovering keeps the current selection. The Engine sends a loss of focus event to the original window SDK, then a gain of focus event to the new window SDK, and subsequently delivers the press event that triggered the selection.

The SDK's local window activation and control focus maintenance apply state. The Engine maintains the current window through laser selection, Desktop invocation, replacement and restoration of disabled controls within the same application, and cleanup of invalid controls. The `window` in input events specifies the target window to receive input.

When a selected window remains visible but is disabled, the Engine pauses its selection eligibility and records the restoration order. After clearing the old input path, if the session has only one interactive regular window, the keyboard is assigned to that window, suitable for the process where the SDK opens a modal dialog box. After the dialog box closes, hides, or becomes invalid, the original window is re-enabled in reverse order, useful for nested dialog boxes. The restoration target must be visible, belong to the original session, and have a valid reference pose; explicitly selected valid windows take precedence, and the restoration record of the original application is cleared after selecting other application windows. Selection after a regular window is hidden or closed follows the aforementioned laser rules, while the Desktop follows the shortcut key invocation rules.

Laser events are routed based on the currently hit or captured window. When the input area is closed, the Engine directly sends the key to the SDK belonging to the current window; when the input area is open, the key is first processed by the active IME, and the text is ultimately submitted to the SDK as `ime_submit`. The SDK is responsible for control focus within the window, key distribution, text editing, selection, character limits, and Tab navigation. `tab_index` is the SDK's local property, with the default being `0`: non-zero items take precedence in ascending order, and zero values are arranged as `top/left`; Shift+Tab reverses the order, skipping hidden, disabled, and label items that cannot be focused.

At startup, the virtual keyboard mode is used, and pressing Pause separately switches to the physical mode. Ctrl+Pause and Ctrl+Alt+Pause are global shortcuts that are effective in both modes and when there is no current window; Alt+Shift and Ctrl+Shift are only processed when in physical mode and there is a valid current window. When exiting the physical mode, any pending input method switch requests are cleared. When the current window becomes invalid, interception is removed, and the Pause selected keyboard mode is retained; subsequent selection of a valid window restores routing to that mode. In physical mode, the Engine sends input directly to the SDK based on the input area switch or first to the IME. Non-text controls such as buttons receive keys through the current window SDK.

Ctrl+Alt+Pause performs a global reset of the Body center and World offset, effective in both keyboard modes and when the window is selected or not, and retains the current keyboard mode. Windows report this combination as Ctrl+Alt+Break, and the same handling is applied. When the headset temporarily loses tracking, the request is reserved until the valid pose is restored before execution.

Ctrl+Pause switches the display and hiding of the Desktop application window during configuration. When the program is called for the first time, it reuses the running process and window for subsequent calls. Each time it is displayed, it positions itself in front of the current display device, using the world reference object, then raises and selects the window. The window maintains this world pose during display. The Desktop creates windows through regular SDK sessions; see “Desktop Application” for configuration and lifecycle details.

When in entity keyboard mode and there is a valid current window, Alt+Shift cycles through IME languages and restores the last used IME for the target language. Ctrl+Shift cycles only within the current language. The switching is performed according to component selection and emptying processes, with layout selection being independent. The keyboard mode remains unchanged.

When switching between windows, the Engine first empties the events of the original input path, then closes the original input area, input bar, and IME/layout interface, and switches to the current window. When the window is closed, hidden, disabled, converted to a secondary surface, its reference pose becomes invalid, or the session is disconnected, its current window status and keyboard interception are immediately cleared. When the interactive state becomes invalid, the corresponding laser capture is canceled, and the old input path is cleared. Focus changes between controls are handled by the SDK.

The input bar, layout, and IME interfaces use `auxiliary=true`’s secondary surface. The input bar is created by the current application’s SDK, while the layout and IME interfaces are created by the component SDK. When clicked, laser events are assigned to the corresponding surface’s session. The current application window remains selected, and the keyboard distributes along the input path of the current window.

#### Input state transitions

|Action|Current window|Input area|Subsequent routing|
|---|---|---|---|
|Laser selects another regular window|Switch to the new window|Close the old input area|First process according to the path to close the input area, then the new window SDK is invoked as needed|
|Select the current window again|Keep|Keep|Keep the original path|
|`show_input_ui`|Keep the associated window|Turn on, or update the rectangle of the already turned on input area|Pass through the active IME|
|`hide_input_ui`|Keep|Close after emptying|Directly send to the window SDK|
|Pause switches the keyboard mode|Keep|Maintain the turned-on state and rectangle|Select the layout or entity keyboard source according to the new mode|
|Select another layout or IME|Keep|Maintain the turned-on state and rectangle|After emptying old components, new components are enabled.|
|Re-select the active component.|Keep|Keep|Keep the original path|
|The active input component loses connection.|Keep the valid current window.|Retain the associated rectangle and enter the recovery phase.|Temporarily save the new input when the input area is open; rebuild the path after the component is restored.|
|The current window closes, hides, disables, or becomes a secondary surface.|Clean up the original selection and determine the new window according to replacement and recovery rules.|Close|Release the old window’s entity keyboard interception rights.|
|Disable replacement and recovery within the same application.|Switch to a window that can be replaced or has been re-enabled.|Close the old input area|The new window SDK restores control focus and input interface as needed.|
|The current window’s reference pose becomes invalid.|Clear.|Close|Remove the corresponding entity keyboard interception and release the effect capture.|

Only operations that change the old input path result in emptying. Update the geometric information of the same input area; retain the original processing state when re-selecting the current window or active component. Repeat `show_input_ui` to update the geometric information of the existing input area; when switching controls, the SDK uses the order of hiding first and then resuming. When clicking the same text box repeatedly, the SDK decides whether to evoke the interface based on whether the input area is open.

### Input bar, IME, and Layout interface.

#### Evoke the input interface: `show_input_ui`.

The request only includes the associated `window` and input area `rectangle`, as well as common request fields. `rectangle` contains limited values `left`, `top`, `width`, `height`. Relative to the upper-left corner of the associated window, use window logical units with width and height greater than zero. The Engine positions the input interface according to the size and spatial pose of the associated window.

The request session must be for a regular application role. The associated window must belong to that session and be a regular window that is currently selected, visible, and enabled by the Engine. The SDK creates an independent long-bar auxiliary window below the input area, displaying the current language, specific IME name, and “Input Method Switch” button. The input bar is displayed in both virtual and physical keyboard modes; in virtual mode, the active layout is also displayed. IME provides candidate interfaces according to its own functions, and English direct IME can remain empty. The interface is arranged from top to bottom as the input area, input bar, IME candidate interface, and layout.

The evocation requires the active IME to be available; in virtual mode, the active layout must also be available. If the component is not ready, a business failure is returned. The caller can query the component status and retry after it is ready. A successful response indicates that the association with the input area has been established and the corresponding status has been pushed. The specific interface is drawn asynchronously by the component.

When evoking, the input area is opened, and the IME processing path is enabled; when the same opened input area is evoked repeatedly, the rectangle is updated. Text, selection, editability, and character limits are maintained by the SDK. When the same window switches to a new text input target, the SDK first requests to end the original input area, retains the old control as the input target, and processes its closing events; after hiding is completed, the local control focus is switched to evoke the input area for the new target.

Request:

```json
{
    "message_type": "request",
    "id": 30,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "op": "show_input_ui",
    "window": 100,
    "rectangle":
    {
        "left": 24.0,
        "top": 124.0,
        "width": 590.0,
        "height": 42.0
    }
}
```

Successful Response:

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

#### Close the input interface: `hide_input_ui`.

When the input area is closed, a successful return is directly given. When the input area is opened, the session to which the associated window belongs or the currently active input component can request closure. After completing emptying, clearing the input area association, and pushing the closure status, a successful return is given. Subsequent keys are directly sent by the Engine to the current window SDK, and the current window remains selected. After receiving the status, the application SDK and component SDK close their respective input bars and interfaces.

Request:

```json
{
    "message_type": "request",
    "id": 31,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "op": "hide_input_ui"
}
```

Successful Response:

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

When the laser switches between windows, the Engine automatically closes the original input interface. The new window’s SDK then activates its own input interface as needed. When the input area is moved or resized, the SDK repeatedly calls `show_input_ui` to update the rectangle. When switching between input controls, it waits until `hide_input_ui` is emptied before calling `show_input_ui` for the new control.

### Layout and IME components

#### Registering input components: `input_provider_register`

Layout and IME are ordinary independent applications that register through their authenticated sessions. `role` is required and can only be `layout` or `ime`; `name` can be omitted, and dynamic components will receive a generated name; `default_provider` can be omitted, with the default being `false`. IME can include the string `language`, which is `en` if omitted; this field is omitted for layout. Common language codes are `zh`, `en`, and `ja`, representing Chinese, English, and Japanese respectively, and other non-empty language codes are also accepted.

Sessions start as ordinary application roles. After successful registration, they are fixed as layout or IME roles until the connection is closed; repeated registration for the same role uses the existing component identity, and returning to other roles results in a business error. Before registration, all ordinary surfaces and associated input areas of the session must be closed. If such resources exist, a business error is returned upon registration, and the original role is maintained. Component sessions only create auxiliary surfaces, and input areas are opened by ordinary application sessions. Configured startup components are matched with existing records through verified process identities. `default_provider=true` indicates priority use of existing active components; if there are no active components for this role during registration, the current component is explicitly selected, or when it is `default_provider=false`, a new component can become the active component. When replacement is involved, the old path must be emptied first; successful registration indicates that the session has been registered, and the active selection is confirmed through the component list.

Request:

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

Successful Response:

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

#### Example of IME registration

Request:

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

Successful Response:

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

#### Querying input components: `input_provider_list`

Returning the global component list. Each item is identified by `id`, with `state` being `stopped`, `starting`, or `running`. `configured` indicates persistence configuration, and `active` indicates that the role is currently selected. IME items include the language code `language`, and this field is omitted for layout. `name` is the component display name, either from persistence configuration or dynamic registration, with built-in English, Chinese, and Japanese IMEs being `EasyVRUI English`, `EasyVRUI拼音`, and `EasyVRUI日本語` respectively; the input bar displays the language category and specific IME name. `process_id` is the associated local process PID, defaulting to `0`; `error` is the failure description string, which is empty normally. Configuration entry IDs remain stable during the current Engine run, and are removed after dynamic entries exit. The SDK initiates subsequent operations based on the actual returned current component ID.

Request:

```json
{
    "message_type": "request",
    "id": 42,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "op": "input_provider_list"
}
```

Successful Response:

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

#### Starting the input component: `input_provider_start`

Start the program with the existing `provider_id`, and it can also successfully return when the component is already started. `true` indicates that the request has been accepted or the startup process has begun. After registration, the list status changes to `running`. Unknown IDs, startup failures, etc., use a common failure response.

Request:

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

Successful Response:

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

#### Selecting the input component: `input_provider_select`

Choosing the global active component of the corresponding role. If the target is already running, switch according to the emptying process; if it is not running, try to start first. After registration and old path emptying are completed, switch, and maintain the original active component during the waiting period. The caller queries the target `state="running"` and `active=true` through `input_provider_list` to confirm the switch is complete, and can also consume the received component list snapshot. If the target fails to start or register, the list records the error and retains the original active component. Layout and IME each have a global active item.

The IME is grouped by `language`. Select an IME to determine the current input language at the same time. Alt+Shift cyclically switches languages and restores the IMEs used in each language before. Ctrl+Shift cyclically switches the IMEs within the current language; the selection of specific components still follows the existing `input_provider_select` process. The SDK input method dialog box displays an independent layout list, a language list, and an IME list filtered by language. The temporary selection of each language is applied after clicking "OK", and discarded when canceled. Common languages are displayed with localized names, while other codes can be displayed directly.

After clicking the "Input Method Switch" button on the input bar, the SDK first empties and hides the input bar, IME, and layout, then opens the built-in input method selection dialog box. The dialog box follows the logical pixel-to-meter scaling ratio of the associated window, is centered near the associated window, and then fixed to the world reference object. When the associated window moves or rotates later, the dialog box maintains the determined world pose; after closing, it returns to the original input control and restores the input interface according to the input area status. The custom dialog box applies the SDK dialog box rules and the specified reference relationships; the surface of the input bar, IME, and layout uses `auxiliary=true`, which is automatically followed by the Engine.

A successful response indicates that the selection request has been accepted. Each role maintains a selection queue in the order of acceptance. Even if a subsequent target is registered first, it waits for the selection before or after the same role to complete or fail. The original input path is retained during the waiting start period, and other window operations are still processed according to the input event queue. When the caller's session is disconnected, any unfinished selections are canceled.

Explicit selection takes precedence over unsubmitted automatic takeovers triggered by component registration. Selecting the current active item can cancel such automatic takeovers; the already issued emptying requests are still completed, and the active component remains selected. Multiple explicit selections are processed according to the queue order of each role.

Request:

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

Successful Response:

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

#### Send input event: `input_provider_send`

When the input area is opened, the active layout and IME submit events through this operation. The Engine checks the sender role, current window, input area, and emptying stage, and then forwards the event according to a fixed route.

The request first passes through the current connected `session_id/session_token` for verification. The component role comes from the registration records saved by the Engine, and the event destination is determined by the current route:

|Sender|Allowed event|Destination|
|---|---|---|
|Current active layout|`key_down`、`key_up`|Current active IME|
|Current active IME|`key_down`、`key_up`、`ime_submit`|Session to which the current window belongs|

The Engine serializes input path switching through event emptying handshaking. During emptying, the original window and session are fixed as the old event destination, and after completion, the new route is enabled.

Normal input is verified according to the current active component and window; during emptying, it is verified according to the frozen old window, component connection, and stage. When the window is closed or hidden, the old path can still complete emptying confirmation; the result is only delivered when the original target is still valid, and the delivery of the old target ends when the resources are invalid.

* The layout sends `key_down/key_up` to the active IME. The new press event comes from the visible virtual keyboard; the release of the key is used to end the previous press state in the current input path.
* The IME consumes the keys it uses, and forwards the remaining `key_down/key_up` to the current window SDK. The IME is responsible for maintaining the pressed and released states.
* The IME uses `ime_submit` to submit the final text, where `text` is a JSON string; the Engine forwards the text to the session to which the current window belongs, and then the SDK applies it to the local input control.

`key_down/key_up` must provide the string `key`. Optionally, `text` is a string, `shift/ctrl/alt/meta` is a boolean value, and if omitted, it is `false`. `ime_submit` must provide the string `text`. The Engine verifies the allowed event types according to the registered roles and generates routing fields such as `message_type`, `session_id/session_token`, and target `window`.

`key` represents key identities. Letters are in lowercase from `a` to `z`, and numbers from `0` to `9`. Function keys use `Backspace`, `Tab`, `Enter`, `Escape`, `Space`, `Left`, `Right`, `Up`, `Down`, `Home`, `End`, `PageUp`, `PageDown`, `Insert`, `Delete`, `Shift`, `Ctrl`, `Alt`, `Meta`, `CapsLock`, `NumLock`, `ScrollLock`, `Pause`, `PrintScreen`, and `F1` to `F24`. Other keys on the physical keyboard use the decimal number of the Windows virtual keycode, `vk_`. Left and right modifier keys have the same name, with `meta` indicating the Win key state.

`text` stores the characters after layout conversion, including case, punctuation, and the results of the selected keyboard layout. The same `key` can produce different `text` values. Components provide printable characters through `text`, and IME submits the final text based on this. Continuous `key_down` is automatically reused, with a real release ending at the held state of `key_up`. IME decides whether to consume or forward the entire held state, and pairs the forwarded presses for release.

The submitted `event` object uses `event_type` and corresponding parameters. The Engine determines the destination based on registered roles, encapsulating it uniformly as `message_type="event"` during forwarding.

Layout sends keys:

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

Successful Response:

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

#### IME submits text events: `ime_submit`

IME places the final submitted text in `event.event_type="ime_submit"`. The pre-edited text, candidate options, word selection operations, and candidate windows are maintained by the IME application. The candidate window uses standard auxiliary surfaces and standard drawing and laser event interfaces.

The built-in Pinyin and Japanese IME candidate windows display combined text, candidate options, and input modes. The candidate windows always use their respective Chinese or Japanese interfaces, with native mode buttons showing “Pinyin” and “Kana” respectively, and temporary English input mode showing “ABC”. The EasyVRUI English direct button is displayed with English labels on the input bar. The control text on the input bar uses the SDK interface language.

Request:

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

Successful Response:

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

#### IME forwards keys

For example, Tab is processed by the application SDK, and IME directly forwards the key event:

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

Successful Response:

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

Text input is sent to the SDK through `ime_submit`; forwarded keys are used for shortcut keys, navigation, and other key processing. IME maintains its own combination and candidate states, while the SDK maintains the application text and selection.

#### Key routing

|Input area status|Keyboard mode|Routing|
|---|---|---|
|Close|Physical keyboard interception enabled|Physical keyboard → Engine → Current window SDK|
|Open|Virtual keyboard|Layout → Engine → IME → Engine → Current window SDK|
|Open|Physical keyboard|Physical keyboard → Engine → IME → Engine → Current window SDK|

When the input area is closed, keys are directly pushed by the Engine to the session belonging to the current window; this path controls the physical keyboard interception with Pause. When the input area is open, IME decides whether to consume the key, forward the key, or submit the text. The application SDK distributes received events to the controls within the window.

The Engine is responsible for window-level routing, input area layout, keyboard mode, component sessions, and event forwarding. IME is in charge of input algorithms, combined buffer, candidate windows, and word selection interactions. When switching windows or closing the input area, the Engine first completes the event emptying of the layout and IME, then clears the previous key states and activates the new path.

#### Input path switching and event emptying

When the input interface is hidden, the current window is switched, keyboard mode is changed, or input components are replaced, the Engine empties the old path in the following order. Each input path switch is processed serially at the same time.

1. New key presses are paused from being delivered to the old path, and new inputs during the switching period are temporarily stored in an internal queue. Events that have already entered the old path are emptied, and the old window and session are fixed as the destination for these events.
2. `input_drain` is sent to the old layout. The layout pauses to generate new key presses. After processing existing operations, pending events and paired release events are sent in the order of connection, and then `input_provider_drained` is submitted.
3. After the Engine receives confirmation from the layout, all previous layout events are transferred to the sending queue of the old IME connection, and then `input_drain` is sent to the old IME.
4. IME processes the queued key presses and their already started asynchronous tasks, sends generated key, text submission, and release events, clears temporary input states, and then submits `input_provider_drained`.
5. The Engine forwards the old results of IME in sequence. When confirmation from IME is received, the previous results have already been placed in the sending queue of the original window connection. Then, this input path switch is completed, and the new state is pushed.
6. Key delivery is resumed, and the temporarily stored new input is handed over to the new path.

Only components involved in the old path need to be emptied. Each component connection processes only one emptying request at a time. The confirmation matches the connection identity with the current emptying stage. Components confirm each request exactly once. A business error is returned when there is no pending confirmation stage or the confirmation connection does not match. Confirmation messages are matched by connection identity, and components ensure that previous confirmations are not sent repeatedly to subsequent emptying stages. After layout confirmation, the sending qualification for old layout events is stopped; after IME confirmation, the sending qualification for old IME events ends. Components start processing new inputs after receiving the new activated state.

All old events and their confirmations are sent in the FIFO order of the same connection. Emptying confirmation indicates that the component has completed all asynchronous work for this time and placed all its results in the sending queue before confirmation. The Engine processes messages in the serial event queue and pushes application events in connection order.

Emptying uses asynchronous handshaking. The Engine and SDK continue to process messages and heartbeats. Components that initiate hiding operations also need to process emptying requests. The SDK keeps this path running by waiting asynchronously. Emptying waits covers old input data tasks, and the waiting of operations is handled by the control flow. The input processing callback first completes this data output, then schedules the hiding or component selection operation to the control queue. The hiding request returns success after emptying is completed, the input area association is cleared, and the status is closed.

The SDK uses the completion of the hiding request as a local processing barrier: first, it executes the framework distribution and text editing of previous old input events in connection order, then notifies the business code that the request is completed. It waits asynchronously to keep input distribution running; only after completion does it modify the local input control and activate the new input area.

After each component emptying request is sent, the confirmation period is 10 seconds, and heartbeat detection is conducted independently. When the timeout or connection breaks, the old connection is closed, the sending qualification is revoked, and the queue is cleared. Then, switching continues according to the component failure strategy. The emptying result is bound to the old window identity. When the target is invalid, the old path and related resources are cleared.

Window selection, display, or closing of the input area, mode switching, and component replacement are executed in the order of the Engine event queue; emptying confirmation, heartbeats, and completion messages of the old path continue to be processed. Presses that trigger window switching and subsequent related events are temporarily stored. After the new window gets focus, they are sent in sequence. New key presses during the switching period are handed over to the corresponding new path according to their position in the queue, and continuous switching is completed in sequence.

When component failure causes input waiting to be restored, the Engine continues to process component registration and startup required for restoration, enabling new connections to establish input paths. Queued window selection, input area changes, and mode switching remain in the order of input events; after restoration, previous inputs are still delivered along their corresponding paths, and subsequent switching is executed.

The window SDK first receives old results in the order within the connection, then processes loss of focus, focus acquisition, and new routing events.

The held state that has been delivered in the old path ends through a release event during emptying. The keys still held by the entity wait for actual release before accepting the next press to the new path; the original held state is automatically repeated. The SDK clears the local key state when the window is out of focus to avoid interpreting the release corresponding to the old press as a new window operation.

#### Confirmation event emptying: `input_provider_drained`

The Engine only accepts the component connection that is currently waiting for confirmation to submit this operation. The component first queues all old events in the send queue and then sends the confirmation in order. The request only includes common fields:

```json
{
    "message_type": "request",
    "id": 48,
    "session_id": 2,
    "session_token": "<layout会话令牌>",
    "op": "input_provider_drained"
}
```

Successful Response:

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

### Clipboard, global settings, and tracking center

#### Read clipboard: `clipboard_get`

Read the system clipboard text of the Windows session where the Engine is located. If the text format or underlying interface is unavailable, return `null`; if the text is empty and readable, return `""`.

Request:

```json
{
    "message_type": "request",
    "id": 50,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "op": "clipboard_get"
}
```

Successful Response:

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

When no text can be read:

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

#### Write to clipboard: `clipboard_set`

`text` is a UTF-8 JSON string, which is written to the clipboard of the Windows session where the Engine is located. Text containing U+0000 returns `value:false`, and the clipboard retains the original content. If the underlying operation fails, `value` in the successful response becomes `false`; for business exceptions, `ok:false` is used for response.

Request:

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

Successful Response:

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

#### Read global settings: `settings_get`

`name` accepts `laser_position_offset` and `laser_rotation_offset`. The former is the local spatial position offset of the controller, in meters; the latter is the three-axis Euler angle offset, in degrees.

Request:

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

Successful Response:

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

#### Modify global settings: `settings_set`

`value` must be three finite values. The returned value applies to the runtime laser configuration of the entire Engine; the initial values for both offsets are zero, indicating the design reference pose.

Request:

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

Successful Response:

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

#### Reset the body tracking center: `body_reset`

Use the current headset position and complete quaternions to record the new body reference center and orientation; thereafter, the body tracking compensates for XYZ translation with the neck pivot, maintaining this reference orientation. At the moment of calibration, the body center is located at the headset position, and the pivot displacement caused by turning is compensated based on the nominal neck model. Walking or spatial translation continues to be transmitted to the body. If the current headset pose is unavailable, return `false`. This request resets the global body reference system and publishes tracking updates; Ctrl+Alt+Pause simultaneously resets the body center and World offset.

Request:

```json
{
    "message_type": "request",
    "id": 54,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "op": "body_reset"
}
```

Successful Response:

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

#### Query the number of windows in this session: `ping`

Return the number of windows owned by the current connection session, including hidden windows and auxiliary surfaces, defaulting to zero. This operation is used for business queries, and automatic heartbeats are sent independently according to the aforementioned rules.

Request:

```json
{
    "message_type": "request",
    "id": 55,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "op": "ping"
}
```

Successful Response:

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

#### Query the application list: `application_list`

Initiated by the verified local session, only common request fields are filled. The returned `value` is an array of snapshots of the engine's verified applications, with each item containing `session_id/process_id/name/memory_bytes/cpu_percent/gpu_percent/window_list`. `name` is the session name reported during session registration. `memory_bytes` is the number of bytes in memory, and `cpu_percent` and `gpu_percent` are the percentages of occupancy within the sampling window. `window_list` is the array of windows owned by this session, with each item containing `id/name/title/visible`, where `id` is the global window ID. The list includes Desktop and running normal local applications. The engine queries process metrics based on the verified local process identity.

Request:

```json
{
    "message_type": "request",
    "id": 57,
    "session_id": 1,
    "session_token": "<会话令牌>",
    "op": "application_list"
}
```

Successful Response:

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

#### End the application or close the window: `application_terminate`

Initiated by the verified local session. `session_id` is the caller session, `target_session_id` is the target normal application session, and Desktop has its own independent lifecycle. When `window` is omitted, the Engine ends the target application process. When `window` is provided, the global window ID returned from the application list is used. After the Engine verifies the window ownership, it sends a `window_close` event, which is processed by the target SDK to close the window.

Window close request:

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

When the entire application ends, omit `window`. A successfully responded `value` is a boolean value: `true` indicates that the process was successfully ended, or the window closing event was delivered to the target session; `false` indicates that the target is invalid or the window ownership does not match. Whether the window is ultimately closed depends on the `on_closing` processing result of the target SDK, which can be confirmed through the subsequent application list.

### Engine actively pushes

The Engine can actively push 13 types of events listed in the table. Each event uses `message_type="event"`, with the type indicated by `event_type`, and includes the receiving connections as `session_id` and `session_token`. Events and responses share the frame stream. The SDK assigns server events and asynchronous request completion notifications in the order of receipt, and the implementation of the connection queue is described in [, IPC, TLS, and connection queue](/en/advanced/03_ipc_tls_protocol).

|event_type|Purpose|
|---|---|
|`pointer`|Laser hit, movement, and press status|
|`tracking`|Space tracking status|
|`input_drain`|Request for component emptying events|
|`input_ui_state`|Input interface and routing status|
|`key_down`、`key_up`|Key press and release|
|`ime_submit`|IME submits final text|
|`focus_in`、`focus_out`|Window focus gain and loss|
|`window_visibility`|Request the SDK to set the visibility of a specified window|
|`window_close`|Request the target SDK to handle the specified window according to the normal closing process|
|`render_error`|Asynchronous drawing error|
|`screen_state`|Changes in screen content availability|

Continuous movement and tracking snapshots can be replaced with the latest values within the same merged interval before being sent. Pressing, releasing, target loss, window focus changes, window visibility requests, emptying notifications, and emptying confirmations constitute the order boundaries; events on both sides of the boundaries remain within their respective intervals. Key presses and text submissions are delivered in the order they are queued.

#### Laser message: `pointer`

Sent to the session belonging to the currently hit or captured window. `left/top` is the window's logical coordinates; `origin/direction/rotation` is the world ray and the laser pose of the handle. `world_position/world_rotation` is attached when the window's world pose is parseable, indicating the window's geometric center pose, where rotation uses quaternions.

Hit detection uses the complete logical rectangle of the window, with transparent pixels also participating in hits. When not captured, the Engine selects the nearest intersection point from the visible and valid pose windows, and if the distance is the same, the created window is chosen. The laser stops at this intersection point, and only when the nearest window is enabled and meets the hand restrictions will pointer interactions be accepted. After capture, delivery continues according to the capture rules. The edge of the interactive window expands outward by 64 logical pixels only for continuing laser display; the actual window intersection point is prioritized.

The world position of the upper left corner of the example window is `[0,1.6,-1]`, with each logical unit corresponding to 0.001 meters. `left=120` and `top=80` have their world intersections at `[0.12,1.52,-1]`, intersecting with the example ray.

`hand` takes `left` or `right`, and `window` is the local ID of the window receiving the session. Valid updates include `left/top`, `trigger/grip`, `joystick`, `primary/secondary`, three-dimensional `origin/direction`, and quaternion `rotation`; `origin` uses meters, and `direction` is the direction vector. `world_position/world_rotation` is provided in pairs.

`trigger` represents the trigger, `grip` represents the side grip key, `true` represents pressing, and `false` represents releasing. The SDK uses the trigger to operate the control, the side grip key to capture the window, and to adjust the three-dimensional position and rotation. `primary` corresponds to left hand X or right hand A, `secondary` corresponds to left hand Y or right hand B, also using boolean states. `joystick.x/y` is an integer from 0 to 255, with a neutral value of 128; X increases from left to right, Y increases from bottom to top. `joystick.pressed` represents the vertical pressing of the joystick. When the corresponding hardware is missing or not bound, the button state is `false`, and the joystick coordinates are 128.

Hit or capture updates:

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

Leaving or losing tracking:

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

`lost:true` indicates that the target is lost. In this case, the coordinates and controller state are optional fields. The pressing of the trigger, side grip key, joystick, pressing and releasing of face keys, and leaving messages are ordered. Normal continuous movements and joystick coordinate updates can be combined into the latest values.

#### Tracking message: `tracking`

It is sent to sessions with visible windows. A complete snapshot is sent when the window becomes visible for the first time or becomes visible again. After that, updates are published whenever the state changes. `frame_map` and `reference_map` represent both complete snapshots for that session. The SDK replaces the corresponding caches and removes the windows that are no longer visible. The queue can combine the old tracking snapshots that haven’t been sent yet. `world_origin` represents the origin position in the Engine world. `frame_map` includes information about the head, left, right, and body. The items that are no longer tracked are represented by `null`. `reference_map` lists the currently visible windows in this session. The key is a decimal string representing the local ID of the window, with the value being the world position of the reference object. The position/rotation of the window itself is applied as a relative offset. If the reference position of the visible window cannot be determined, the value is `null`. Windows that are hidden or turned off are removed from the snapshot.

Push:

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

#### Component emptying event: `input_drain`

The Engine sends this message to components involved in the switch in the order of the old layout and old IME. Components process the request based on their connection identity and submit `input_provider_drained` after all old events and asynchronous work are completed.

Engine → layout：

```json
{
    "message_type": "event",
    "event_type": "input_drain",
    "session_id": 2,
    "session_token": "<layout会话令牌>"
}
```

After the Engine receives confirmation of layout emptying and forwards its existing events, it sends to IME:

```json
{
    "message_type": "event",
    "event_type": "input_drain",
    "session_id": 3,
    "session_token": "<IME会话令牌>"
}
```

#### Input interface status: `input_ui_state`

Sent to registered input components and related ordinary application SDKs. When the current window, interface display, or keyboard mode changes, notify the active layout, IME, and associated applications; when the component list changes, notify registered components and the current application, and can be accompanied by a complete snapshot of `provider_list`. The structure of this field is consistent with the `input_provider_list` query result. If omitted, the original list is used. Explicit `[]` indicates an empty list. The application SDK displays the current language and specific IME name in the input bar accordingly.

`active` indicates that the component actually participates in the current input path: IME must be selected, the input area is open, and the current window is valid; the layout must also be in virtual keyboard mode and have an active IME. The display and content of specific candidate windows are controlled by IME. `rectangle` saves the local input rectangle of the window when the component participates in this path; in other cases, it is `null`. The input bar and component surface are positioned by the Engine according to auxiliary surface rules.

`active` in `input_ui_state` describes whether the component participates in the current input path; `active` for each item of `provider_list` describes the component that has been selected for the role. In entity mode, the selected layout is still `active=true` in the component list, and its input status is `active=false`, `rectangle=null`.

When the input interface is displayed:

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

When the input area is closed, the current window is invalid, or the component is replaced, the Engine sends the following status to the original component.

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

After the event emptying is completed and the input path is switched, the Engine pushes the new routing status to related components and window SDKs, then resumes key delivery.

The component session receives the component status including `active`; the ordinary application session receives the window routing status including `window`. The two session roles are mutually exclusive, and their respective `rectangle` are interpreted according to their states.

The application SDK receives similar messages when the routing status of the current window changes. The fields are `window`, `physical`, and `rectangle`, and can be accompanied by `provider_list`. This updates the local input routing and input bar accordingly. The ordinary application determines that the input area is open based on the valid current window and non-empty `rectangle`; at this time, the input bar is displayed in both keyboard modes. When the input area is closed or the current application switches, the input bar is retracted, its auxiliary reference pose is invalid, and the interaction ends.

In entity mode, send the input area and component list to the current application:

```json
{
    "message_type": "event",
    "event_type": "input_ui_state",
    "session_id": 1,
    "session_token": "<会话令牌>",
    "window": 100,
    "physical": true,
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

After closing the input area:

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

#### Key, text submission, and window focus events

When the input area is closed, the Engine directly sends key presses to the SDK belonging to the current window. When the input area is open, the Engine first sends key presses from the layout or physical keyboard to the IME, and then forwards the keys or text `ime_submit` to the current window's SDK. Events sent to the application SDK include the local `window` of that session, which are assigned to the corresponding window in the order of connection.

`Alt` When the button is pressed and released independently, the Engine supplements `alt_tap=true` on this release event. Release events generated by key combinations and clearing are processed as standard key releases. When input components automatically forward key presses, this field is retained. The SDK displays mnemonic underlines when `Alt` is held down or during menu keyboard navigation, and switches menu navigation on qualifying release events. Pointer operations, focus changes, and input state changes can cancel the pending activation state; `Alt+Shift` When switching input languages, the original edit control retains focus.

Input area closed, Engine → Current window SDK:

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

Input area open, physical key pressed, Engine → IME:

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

Key released, Engine → IME:

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

IME forwards unconsumed key presses, Engine → Current window SDK:

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

IME submits the final text, Engine → Current window SDK:

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

Current window loses focus, Engine → Original window SDK:

```json
{
    "message_type": "event",
    "event_type": "focus_out",
    "session_id": 1,
    "session_token": "<会话令牌>",
    "window": 100
}
```

Current window gains focus, Engine → New window SDK:

```json
{
    "message_type": "event",
    "event_type": "focus_in",
    "session_id": 1,
    "session_token": "<会话令牌>",
    "window": 101
}
```

`focus_out/focus_in` is directly sent by the Engine to the corresponding window SDK. The loss of focus notification carries the original window, while the gain of focus notification carries the new window. The SDK manages window status based on this and then processes the focus of local controls.

`key_down/key_up` is used for key distribution, and the original character information can be provided to the IME through the optional `text`. When the input area is open, text is submitted to the SDK in one go by `ime_submit.text`, and the SDK applies the text according to local selection and character constraints.

The recipient distributes key presses based on the target `window` and the synchronized input area status. `ime_submit` must come from the current active IME and comply with the sending rules for the open input area and the current emptying phase.

#### Window visibility: `window_visibility`

The Engine sends this event to the SDK session of the window, requesting to set the visibility of the specified window. `window` is the local ID of the uint64 window within the receiving session, pointing to a created window whose instance is still alive; `visible` is a required boolean value, `true` indicates display, and `false` indicates hide.

The SDK searches for the window by local ID and calls `set_visible(visible)`, updating the local status and display/hide events according to the rules of this method, and then submits the `visible` metadata of the window through the normal `present`. Hidden windows also receive and process this event, and `visible=true` makes them reappear. After receiving the submission, the Engine updates the surface, laser capture, and input routing according to normal window rules.

Engine → Window SDK, display the window:

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

Engine → Window SDK, hide the same window:

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

The Desktop switches the display and hide of existing windows through this event. The positioning and selection rules for display are described in “Desktop Application”.

#### Request to normally close the window: `window_close`

The Engine sends this event to the SDK belonging to the target window. `window` is the local window ID within the target session. The SDK calls the normal closing process, triggering `on_closing`; the processing function can cancel the closing. After successful closing, the SDK submits `surface_close`, and the Engine releases the corresponding surface.

```json
{
    "message_type": "event",
    "event_type": "window_close",
    "session_id": 2,
    "session_token": "<目标会话令牌>",
    "window": 7
}
```

#### Asynchronous drawing error: `render_error`

Send the session to which the error surface belongs, with the error field placed directly at the top of the push, with the structure as follows:

Push:

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

Asynchronous graphics errors may still occur after successfully receiving `present`, and are reported through this push. Engine handles retryable texture submissions or GPU restorations.

#### Screen content status: `screen_state`

Sends to the session to which the window belongs when the monitor referenced by the window is sampled for the first time, when the monitor source changes, or when the availability status changes. `window` is the local window ID within the receiving session, and `screen_id` is the monitor serial number declared by the `screen` control. `available=true` indicates that the currently collected content is available, while `false` indicates that it is not available, possibly due to a disconnected monitor, lost access to the collection, or a graphics device failure. The SDK updates the status of the control bound to the same `screen_id` within the window accordingly; screen pixels are collected and rendered locally by the Engine.

```json
{
    "message_type": "event",
    "event_type": "screen_state",
    "session_id": 1,
    "session_token": "<会话令牌>",
    "window": 3,
    "screen_id": 0,
    "available": false
}
```

### Spatial reference objects and coordinates

`present.metadata` represents the surface space attributes submitted by the SDK. The local upper-left corner of the window serves as the positioning reference, with two-dimensional drawing and laser coordinates increasing from the upper-left corner to the right and down.

#### Position, angle, and direction

`position` is relative to the reference object `[x,y,z]`, measured in meters. The VR world uses right-handed coordinates: X to the right, Y upward, with a default negative Z facing forward. The window's logical coordinates have top down orientation, so when converted to the window's three-dimensional local space, it corresponds to negative Y.

`metadata.rotation` and `laser_rotation_offset` are the three-axis Euler angles of `[x,y,z]`, measured in degrees; the current conversion combination is `qz × qy × qx`, which acts on vectors by X first, then Y, then Z. The SDK uses it to provide editable angle properties.

In tracking messages, the `rotation` of pose, laser `rotation`, and `world_rotation` use `[x,y,z,w]` quaternions, with `[0,0,0,1]` representing no rotation. `direction` is the three-dimensional ray direction vector. Each field is interpreted according to the encoding specified in the corresponding message.

`physical_scale` is the scaling factor. The fixed reference is 1000 logical pixels corresponding to 1 meter, with the actual width being `width × physical_scale / 1000` and the actual height being `height × physical_scale / 1000`. At the same scale, controls of the same logical size have the same physical size. The Engine's Overlay transformation locates based on the geometric center, and window metadata is located at the upper-left corner. Half-width and half-height offsets must be considered during conversion.

#### Reference value

For ordinary surfaces, `reference` uses the following five values:

* `world`: Fixed relative to `world_origin` of the Engine. The origin for initial establishment is offset by a negative Z direction along the standing coordinates based on the headset position, with rotation using quaternions. A zero position and zero rotation place the upper-left corner of the window at this origin. Ctrl+Alt+Pause resets the World offset based on the current headset pose.
* `head`: Follows the headset position and rotation.
* `left`: Follows the left-hand controller position and rotation, using right-handed laser interaction.
* `right`: Follows the right-hand controller position and rotation, using left-handed laser interaction.
* `body`: Estimates the neck pivot based on the headset pose, compensates for slight displacement caused by turning the head, and follows XYZ translation; the reference rotation remains the full headset rotation at initial establishment or most recent reset. `body_reset` or Ctrl+Alt+Pause recalibrate the center.

The initial calibration saves the fixed reference `B=world_origin⁻¹×head_initial` of the headset relative to the World. Ctrl+Alt+Pause resets the World using `world_origin_new=head_current×B⁻¹`, unifying the overall layout of existing World windows, while the local position and rotation of the window remain unchanged. Repeating the reset with the same headset pose yields the same result.

`world`, `head`, and `body` can be used for dual-handed laser interaction. When the controller or headset tracking fails, the corresponding reference pose is `null`, and the Engine clears the input eligibility and capture of that surface; it is repositioned after effective tracking is restored.

The World uses SteamVR standing reference frames, and character movement in the game is maintained by the game itself. The window's position relative to the Engine's World origin remains unchanged.

#### Auxiliary input for surface positioning

Input bars, IMEs, and layouts use the auxiliary surface `auxiliary=true`. The Engine calculates the reference pose based on the current window, input rectangle, and component role, and feeds it back to the SDK via `tracking.reference_map`. The auxiliary surface `reference` may be omitted; its positioning is maintained by the Engine.

The surface created for the layout and IME session automatically uses auxiliary positioning. The auxiliary surface of a regular application is positioned when it is activated for the current application, input area, and the associated window is valid. The input component surface requires the component to actually participate in the current input path, and the layout also requires the virtual keyboard mode. `visible` determines whether to display it, and when `enabled=true`, it participates in laser interaction. When the input path is collapsed, the associated window becomes invalid, or the current application is switched, the positioning is invalidated and the capture is released.

The metric conversion ratio for the input area is `s = 关联窗口.physical_scale / 1000`. The effective physical width of the auxiliary surface is `W = 表面.width × s`, and the physical height is `H = 表面.height × s`. The creation request still requires a value greater than zero, `physical_scale`, and the effective display ratio follows the associated window.

The offset of the auxiliary reference origin relative to the upper left corner of the associated window is `[(rectangle.left + (rectangle.width × 0.5)) × s - (W × 0.5), -((rectangle.top + rectangle.height) × s + ΣH), depth]`, which is then converted to world space through the pose of the associated window.

The surfaces involved in stacking must be visible and active auxiliary surfaces. First, arrange the input bar of the current application, then the active IME surface, and finally the layout surface in virtual mode; the same group is ordered by the Engine window ID. `ΣH` is the sum of the effective surface heights before the current surface. When a certain interface of the current surface is hidden, its height is zero, and subsequent interfaces are closely attached to the previous visible surface.

Each auxiliary surface is centered horizontally relative to the input area. When the rectangle of the input area, the magnification of the associated window, the width and height of the auxiliary surface, or the state of the previous surfaces change, the Engine recalculates the position and effective physical dimensions in real time. `position` and `rotation` serve as additional offsets on the automatic reference pose; a zero value uses the default fitting position.

`depth` is an offset of 2mm towards the user side. The Engine transforms the headset position to the local space of the associated window, taking `-0.002` meters when the local Z is less than 0, and `0.002` meters in other cases; when the headset pose is not available, it takes `0.002` meters. The auxiliary surface follows the laser hand restriction of the associated window.

#### Curvature

`curvature` represents the horizontal cylindrical curvature, with units being the reciprocal of meters. By default, `0.0` represents a plane. The radius of a cylindrical surface with non-zero curvature is `1 / curvature`, the arc length of the window expansion is `width × physical_scale / 1000`, and the horizontal bending angle is the arc length multiplied by the curvature.

The Engine receives a limited and non-negative curvature, requiring the horizontal bending angle to be less than `2π`. The SDK's handle adjustment entry uses a maximum interaction of 160°. `position` and `rotation` still use the upper left corner of the window as the reference, and the Engine uses the same surface geometry for display and laser intersection.

The results of spatial calculations must be representable with a finite floating-point number. When the pose combination or size conversion exceeds the representable range, the tracking snapshot uses `null`, and the interaction is cleared according to the reference pose invalidation rules.

Movement, rotation, scaling, curvature, title bar, and tracking mode selection in the SDK are achieved by updating surface metadata and drawing nodes.

### Drawing command objects

The SDK locally records drawing commands in batches. When submitting, each node's command is placed in the `command_list` array. The Engine parses, caches, and executes the commands in order. Each item is a JSON object, with the command type selected as a string `type`, and the other fields store the parameters of that command. A single node update replaces the entire command list for that node; `[]` represents an empty list.

#### Parameter types and validation

* Coordinates, dimensions, radius, stroke width, rotation, and transparency use finite JSON values, and the Engine processes them as doubles; coordinates and geometric dimensions use window logical units.
* `rectangle` is an object containing `left`, `top`, `width`, `height`, with both width and height greater than or equal to zero.
* `ellipse` is an object containing `center_x`, `center_y`, `radius_x`, and `radius_y`, all with a radius greater than or equal to zero. The SDK's circular interface uses an equal radius of X/Y to generate elliptical commands.
* `color` is a uint32 unsigned integer, with a bit layout of `0xRRGGBBAA`, which is 24 bits for RGB and 8 bits for alpha; JSON values are in decimal form.
* `font` is an object containing the system font name `family`, a uint64 value greater than zero `size`, and boolean values `bold` and `italic`. `family` must be a non-null string not containing NULs.
* `text` is a JSON string; switches such as `center`, `clockwise`, and `large_arc` use JSON boolean values.
* `thickness` is greater than zero, with a rounded corner radius greater than or equal to zero, and `opacity` is set to `[0,1]`.

All fields listed in the table must be provided. Engine checks the command type, field type, value range, and combination constraints; unknown commands or illegal parameters are reported through a business failure response.

#### Command type

|type|Parameter field|Purpose|
|---|---|---|
|`fill_rectangle`|`rectangle`、`color`|Fill rectangle|
|`outline_rectangle`|`rectangle`、`color`、`thickness`|Outline rectangle|
|`draw_line`|`x1`、`y1`、`x2`、`y2`、`color`、`thickness`|Draw line|
|`draw_text`|`rectangle`、`text`、`font`、`color`、`center`|Draw text within a rectangle|
|`push_clip`|`rectangle`|Push into the rectangle clipping area|
|`pop_clip`|Only `type`|Populate the current clipping area|
|`fill_ellipse`|`ellipse`、`color`|Fill an ellipse or circle|
|`outline_ellipse`|`ellipse`、`color`、`thickness`|Outline an ellipse or circle|
|`fill_rounded_rectangle`|`rectangle`、`radius_x`、`radius_y`、`color`|Fill a rounded rectangle|
|`outline_rounded_rectangle`|`rectangle`、`radius_x`、`radius_y`、`color`、`thickness`|Outline a rounded rectangle|
|`draw_image`|`rectangle`、`image_width`、`image_height`、`pixel_data`、`opacity`|Draw an RGBA pixel image|
|`draw_screen`|`rectangle`、`screen_id`|Draw the real-time display content of the Engine host|
|`fill_path`|`path`、`color`|Fill a path|
|`outline_path`|`path`、`color`、`thickness`|Outline a path|

Each node independently maintains a clipping stack. `push_clip` affects subsequent commands, with nested clippings taking intersection; `pop_clip` must have a restored clipping layer during execution, and the clipping stack must be balanced at the end of the command list.

`font.size` uses window-based logical units. `draw_text.center=true` indicates horizontal centering, while `false` indicates alignment with the starting edge. Everything is centered vertically. The text is separated into lines using explicit line breaks. Automatic line breaking is disabled. The final cropping occurs within the `rectangle` area.

#### Example of text commands

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

#### Image commands

`image_width/image_height` is a uint64 pixel size greater than zero. `pixel_data` is the standard Base64 string of the original RGBA pixel bytes; pixels are arranged tightly from the top left corner, in a left-to-right, top-to-bottom row order, with each pixel consisting of four bytes of R/G/B/A; RGB preserves the original channel values, and the Engine performs alpha pre-multiplication conversion at the graphics interface boundaries. The number of decoded bytes must equal `image_width × image_height × 4`, and the size multiplication must be representable by the memory size type of the receiving process. `rectangle` specifies the target drawing area, and `opacity` controls the overall transparency.

Below, a 1 × 1 pixel red image is drawn:

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

#### Screen commands

`draw_screen` draws the content of the Engine host's display within the specified logical rectangle. `screen_id` is the 0-based index of the host DXGI display enumeration; the SDK selects this display, and the Engine captures native resolution images, synthesizes Windows mouse movements, and draws on the GPU.

The display rectangle determines the display size within the window. To display a 1920×1080 image at original pixels, a rectangle with the same logical width and height can be used, maintaining `physical_scale` for the window. Display content changes are updated by the Engine, and the window continues to use the submitted drawing nodes. Availability of capture is fed back through `screen_state`.

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

#### Path commands

`path` is the object, containing the string `fill_rule` and the array `segment_list`. `fill_rule` takes either `even_odd` or `non_zero`, representing odd and even filling rules, respectively. Each segment is a JSON object, and the segment type is selected using the string `type`:

|type|Parameter field|Purpose|
|---|---|---|
|`move`|`x`、`y`|Create a graphic at the specified point|
|`line`|`x`、`y`|Connect to the specified endpoint|
|`quadratic`|`control_x`、`control_y`、`x`、`y`|Quadratic Bézier curve|
|`cubic`|`control_x1`、`control_y1`、`control_x2`、`control_y2`、`x`、`y`|Cubic Bézier curve|
|`arc`|`x`、`y`、`radius_x`、`radius_y`、`rotation`、`clockwise`、`large_arc`|Elliptical arc|
|`close`|Only `type`|Close the current graphic|

Each coordinate is a finite value, the arc radius is greater than or equal to zero, and the arc rotation is in degrees. The path first creates a graphic through `move`, then adds other segments; `close` then creates subsequent graphics with the new `move`. The array order is the path segment order; an empty array indicates an empty path.

Below, a triangle is filled:

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

## Windows named pipes

### Discovery interface

The pipe name is `\\.\pipe\EasyVROverlayUIEngine.Bootstrap`, used for local discovery, supporting multiple clients reading concurrently. Each connection uses an independent pipe instance, and the server actively sends a discovery message after the connection is established:

Engine → Local SDK:

```json
{
    "version": 1,
    "port": 49537,
    "access_credential": "<接入凭据>",
    "public_key_fingerprint": "<公钥指纹>",
    "process_id": 12345
}
```

The discovery message has an 8-byte little-endian uint64 length header, and the message body is UTF-8 JSON, with the length being the number of bytes in the message body. `version` is `1`, `port` is the actual TCP port, and `process_id` is the Engine PID. The client then completes TCP/TLS authentication to obtain the session ID/token.

### Life cycle and access boundaries

The processing period after the connection is established is approximately 5 seconds. The pipeline can handle multiple clients concurrently. After sending discovery information, it waits for the client to disconnect or the period to expire before closing the connection.

The pipeline is limited to local access using `PIPE_REJECT_REMOTE_CLIENTS` and employs Windows default security descriptors. Local processes that can read the pipeline can obtain access credentials and public key fingerprints. The TCP listening address is set independently according to the aforementioned configuration.

Window operations, component registration, clipboard, settings, and other services are all completed through TCP/TLS.

## Windows Name Mutex

### Single-instance coordination

The name of the mutex is `Local\EasyVROverlayUIEngine.Engine`, used for single-instance coordination within the current Windows login session. Different login sessions use their respective Local namespaces, and resources such as fixed TCP ports may still conflict across sessions.

The mutex uses Windows default security attributes.

## Lifecycle and Audit Boundaries

### SteamVR disconnection and recovery

The Engine identifies SteamVR instances using `vrserver.exe`'s PID and creation time. When handling `VREvent_Quit`, it first confirms exit and then releases the OpenVR connection. When a process exits, frame synchronization calls fail, or the OpenVR connection becomes invalid, the Engine releases the old Overlay and pauses VR tracking, continuing to provide IPC services while retaining application and input component sessions and submitted window states.

After the old instance completely exits and the new instance starts, the Engine reinitializes OpenVR, loads action lists, switches graphics adapters as needed, and restores Overlay, textures, visibility, pose, curvature, and laser tracking based on the current window state.

### Session and Process Attribution

#### Regular Applications

Each authenticated TCP connection is an independent session, with local window IDs isolated within that session. The same application PID can establish multiple sessions; when a connection is closed, resources such as windows, input attribution, capture, and registration are cleaned up for that session.

The Engine tries to query the real process for local loopback connections: IPv4 uses `GetExtendedTcpTable(AF_INET)`, IPv6 uses `GetExtendedTcpTable(AF_INET6)`, matching the client's reverse endpoint, and IPv6 also handles related scopes and mapping addresses. After obtaining the process handle, the Engine distinguishes processes using PID and creation time, closing associated connections and cleaning up resources when a process exits.

Process identity queries apply to loopback connections. When the query is successful and the process can be opened, the Engine binds the process identity and monitors exit; other connections are cleaned up through socket closure and heartbeat timeout.

After SDK reconnection, a new session is established and windows are submitted. Successfully executed business operations retain their results; if a timeout occurs, the request may be in a state where it has been executed but the response has not yet been received.

When a session disconnects, unexecuted window, input area, and component switching requests for that session are canceled, and their pending results and event queues are cleaned up. Operations that were executed before disconnection are processed according to the original results; old session queue tasks recheck the window and session lifecycle before execution.

After the SDK establishes a new session, the window and drawing cache are rebuilt. The current window and input interface start from the initial state, and the user can evoke them again as needed after reselecting the window. Input components reregister using the new session; configuration entries match the legitimate process identity, and dynamic components obtain a new runtime ID.

#### Persistent and Dynamic Input Components

Components in the configuration enter `starting` after startup and must connect, authenticate, and register within 10 seconds to enter `running`; if startup fails, exits prematurely, or registration times out, they return to `stopped` and an error is recorded. Configuration example:

The following is a snippet of input component configuration in `bin/config.json` after installation. The executable path is relative to the `bin/` where the file is located.

```json
{
    "provider_list":
    [
        {
            "name": "standard_104",
            "role": "layout",
            "executable": "../app/layout/standard_104/easyvrui_layout_standard_104.exe",
            "argument_list": []
        },
        {
            "name": "EasyVRUI English",
            "role": "ime",
            "language": "en",
            "executable": "../app/ime/en/easyvrui_english/easyvrui_ime_english.exe",
            "argument_list": []
        },
        {
            "name": "EasyVRUI拼音",
            "role": "ime",
            "language": "zh",
            "executable": "../app/ime/cn/easyvrui_pinyin/easyvrui_ime_chinese_pinyin.exe",
            "argument_list": []
        },
        {
            "name": "EasyVRUI日本語",
            "role": "ime",
            "language": "ja",
            "executable": "../app/ime/jp/easyvrui_japanese/easyvrui_ime_japanese.exe",
            "argument_list": []
        }
    ]
}
```

The values `name`, `role`, and `executable` for each item are required and must be strings. The name and path must be non-empty. The layout name must be unique, and the IME name must be unique within the same language. `role` is set to either `layout` or `ime`. `argument_list` is an array of strings; if omitted, it is `[]`. The IME's `language` must be a non-empty string, defaulting to `en`, with the common code being `zh/en/ja`. This field is omitted in the layout. The installer registers these four items and their installation paths. When the Engine encounters a missing `provider_list` in manual configuration, it will fill in the built-in default value. An explicit `"provider_list": []` indicates an empty list.

When the Engine starts up, it loads the configuration list and attempts to launch all configuration programs. The list ID is allocated each time the program runs; entries are retained after the configuration components exit and switch to the inactive state. The engine can still call start/select again while running.

Non-configuration components that are dynamically registered after startup are marked as `configured=false`. Entries are removed after disconnection or exit. The Engine manages the lifecycle of its own sub-processes, monitors the exit of external SDK applications, and cleans up their resources.

Once a role has configuration entries or successfully registered components, that role becomes a necessary role during the Engine's current run. When an active component becomes invalid, the system first tries to use the candidate of the same role that is already running, then waits for the candidate that is starting, or launches the configuration candidate that has not failed yet. When all necessary candidates are exhausted, an error is reported, and the engine exits. Even after a dynamic component exits and removes its entry, the necessary status of that role remains. Roles with no configuration and no registered components can remain absent. When the engine is still running, manual retries can be initiated through the component start/select.

When the input area is enabled, fault recovery is handled as a serial input path switch: First, the invalid connections are disqualified, the remaining old participating components are cleared, the valid current window and input rectangle are retained, and the subsequent new inputs are temporarily stored. When the replacement component is ready, the new state is sent and delivery is resumed. Texts that have been successfully submitted in the old path are retained, and unfinished old processes are cleaned up with the invalid path.

When the input area is closed, the path to the SDK that leads directly to the window continues to run, and the components manage the recovery independently. The caller queries the running and active status through the latest component list; ordinary applications can actively call `input_provider_list`, and when a complete list snapshot is received, the local component list is updated overall.

#### Desktop Application

After installation, `bin/config.json` specifies the program triggered by Ctrl+Pause using `desktop`.

```json
{
    "desktop":
    {
        "executable": "../app/desktop/easyvrui_desktop.exe",
        "argument_list": []
    }
}
```

`executable` is a non-empty path string, with relative paths based on the directory where the configuration file is located. `argument_list` is an array of strings; if omitted, it is `[]`. The installer writes the above Desktop entry. The ordinary application list in Desktop comes from `app/desktop/config.json` and user configuration, and is merged within the Desktop process by application ID. See [Desktop application list](./application_manifest#desktop-application-list) for configuration files and update rules.

The Engine starts the configuration program when Ctrl+Pause is first pressed. Subsequent presses switch between displaying and hiding in the Desktop window, reusing the running process and window instances. After the program exits, it can be restarted the next time it is called. By default, the Desktop creates a list window for applications using the world reference object through the SDK, displaying application icons, date and time, and network status. Its windows, events, and sessions follow ordinary application rules. When the Engine exits, it closes its own Desktop sub-processes that it started.

Each time it is displayed, the current valid headset pose is positioned once in the front, and then that world pose is maintained. When it is called again, the position is re-determined using the headset pose at that time. The Desktop and built-in input method selection dialogs default to using the world reference object; the input bar, IME, and layout position themselves according to auxiliary surface rules, while application custom dialogs determine the reference relationship based on the SDK and application configuration.

The Engine requests the SDK to display or hide Desktop windows through `window_visibility`. The SDK calls the window `set_visible()` and operates normally `present`; after the display update is received by the Engine and the window becomes interactive, the Engine places it in the foreground and selects it. When hiding, the Engine releases the corresponding input routes and captures according to the current window rules, while the Desktop process and window instances are retained for the next display.

When invoking, a 10-second timeout is used to wait for Desktop sessions and metadata of ordinary and enabled windows. Hidden windows can also be targets. If window metadata arrives but the display pose is temporarily missing, the display request is reserved until tracking is restored; during this phase, it remains in a started state, and after the pose becomes valid, positioning, display, and window selection are completed.

### Permissions and resource constraints

#### Session and resource isolation

* TLS public key fingerprint verifies server identity, and HMAC validates the client's access qualification through shared access credentials.
* The session token must match the current connection, and resource operations are performed according to the associated session.
* Ordinary window operations are searched by the local ID of this session. Cross-session input interface positioning is resolved by the Engine based on the current application, input rectangle, and active components.
* Provider input requires the sender to be the current active component, with valid current window, input area, and active IME, conforming to the current emptying phase; the layout also requires a new press event and the virtual mode, and the component actually participates in the input path. Layout generates keys based on its interface interactions, and the specific surface display state is maintained by the component. `ime_submit` submits the final text through the active IME.

#### Session operation permissions

The client authenticates using shared access credentials. The same access credentials are used for both local and remote clients.

* Both local and remote clients can read and write the host clipboard, modify the global laser offset, reset the body center, as well as query, start, and select input components.
* Both local and remote clients can register input components. The registration of `default_provider=false` may take over the current role.
* The ordinary application session to which the current window belongs can invoke the input interface through the window and input area rectangle, create `auxiliary=true` input bars, and maintain the focus and editing rules of controls within the window. Auxiliary positioning takes effect when the input area is enabled and the associated window is valid. The surface created by the layout/IME session automatically adopts auxiliary positioning, receiving component inputs and laser events. Focusable application controls can receive keyboard input.
* `input_provider_send.event` is verified by the Engine for object type, event type, registered roles, key field, and emptying phase; the SDK and input components handle extended fields according to their own conventions.

* Continuous tracking and ordinary pointer updates use a combined strategy; other responses and events retain their respective sending rules.
* Failures such as exhaustion of input component candidates can cause the Engine to exit, affecting global availability.

### Other system interfaces

The Engine calls Windows keyboard hooks/keys, clipboard, process, and TLS interfaces, as well as SteamVR/OpenVR and Direct3D/Direct2D/DirectWrite.

The keyboard module is in the same process as the Engine, communicating through an internal queue and shared state. Layout and IME are registered as independent processes through TCP/TLS. During installation, the Engine and input components are deployed separately to `bin/` and `app/`, with their respective built-in language packs compiled into binary form. Configuration and TLS keys are managed by the corresponding local module.