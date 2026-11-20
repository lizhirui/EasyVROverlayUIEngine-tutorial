# The Control Tree, Rendering Pipeline, and SteamVR Submission

Lighting a button involves three different objects. The SDK knows the text, focus, border, and position of the button. The Engine knows how to convert drawing instructions into a texture. SteamVR knows the spatial position of this texture in the headset and how to synthesize it with other images. When reading this pipeline, first track the control object, the received drawing nodes, and the drawn texture separately. They have their own life cycles and different "update completion" times.

This chapter starts with a text change and gradually checks along `ui_runtime::notify_changed()`, `command_renderer`, `present`, `service_runtime::present()`, `graphics_renderer`, and `IVROverlay`. Then, using a calculable memory example, it explains resource overhead and distinguishes between protocol errors, rasterization errors, and device exceptions using failed scenarios.

![SDK recording and difference submission, Engine shading and SteamVR synthesis](/images/en/advanced_render_pipeline.png)

## 1. How a control tree becomes drawable data

### Controls, instructions, and pixels manage each layer

A `window` is the control container held by the application. Sub-controls can be placed below it, and each sub-control can have local rectangles, text, colors, visible states, or other properties. The `left/top` of a control usually starts from the upper left corner of the parent container. When actually recording to the Engine, they need to be converted into logical pixels within the window. Only the original `left/top` of the sub-controls is directly given to the graphics device, and the drawn button will ignore the position of the nested container. The `command_renderer::get_rectangle()` of the SDK provides window coordinates, and the actual unclipped position is also considered on the scrolling container path. Clipping determines which pixels are visible, and position determines where the object was originally placed; both should be calculated separately.

For example, a panel within the window is located at `(40,60)`, and buttons within the panel are at `(12,8)`. The top left corner of the button in window coordinates is `(52,68)`. If the `10` logical pixels are scrolled up, the window vertical coordinate of the control may become `58`. However, the visible range of the panel still starts from `60`, so only the part that actually falls within the visible area is drawn. This is why simply pinning the top coordinate of the button to `60` is incorrect; the pinning will make the entire button stick to the edge of the scrolling area, missing the content that should be hidden.

The `render()` of the control receives `render_context`. The application can use it to fill rectangles, draw borders, write text, display images, or draw paths. In production environments, the `command_renderer` inherits this interface, converting specific calls into transferable instructions, which are recorded by the drawing command buffer. For the application, calling `fill()` expresses the drawing intention. The Engine knows what rectangles and colors will be filled next, but this request does not mean that D3D has already drawn the pixels. After treating the intention as data, the SDK can record the drawing plan in unit tests and compare it with the plan submitted in the previous round item by item.

Drawing nodes can be seen as a segment of recording attached to the control. Each recording can describe multiple operations. The background of the same form, regular controls, dropdown menus, and tooltips sometimes span different levels. If there is only one full-form recording, changing a word requires replacing the entire recording. If each instruction is assigned a permanent node, many IDs may need to be rearranged when removing borders, and there will be a large number of detailed indexes in the message. The project selects the control and drawing stage as the intermediate granularity. In a single control drawing, filling, drawing borders, and text can be executed sequentially, with each stage still identified by a stable ID.

### Why the order of nodes is different from the parent-child relationship of controls

`command_renderer::get_node_id(object_id,segment)` generates node numbers according to `object_id×NODE_SEGMENT_COUNT+segment`. The current `NODE_SEGMENT_COUNT` is `4`. It checks the object ID, segment number, and whether the multiplication and addition overflow. The same drawing segment of the same control should use the same number in multiple submissions. You can think of a segment as several sheets of paper reserved for a control. The submission order depends on hierarchical dependencies, so you should not simply sort node IDs as the drawing order.

`get_node_list()` Begin recording with the ordinary section of the window, fill the window background, then call the window's own `render()`. When the window reaches `render_control_list()`, the recorder ends the current node and opens sections for each ordinary control based on the control traversal results during runtime. The traversal ensures that the object still belongs to the window and skips the menu containers that are processed separately by the window. After processing the ordinary controls, the recorder returns to the middle section of the window. At `render_overlay_list()`, start a new layer section and call the control's `render_overlay()`, then return to the window's final section to draw the prompt. This way, the dropdown menu can cover the subsequent ordinary controls, and the prompt can also appear on the last layer. The ordinary drawing and the layered drawing can use different clipping ranges.

There are two possible sequences here. The control tree is responsible for expressing ownership relationships, layout, event propagation, and hit detection. The drawing order determines who covers whom. A parent control can provide a scrollable visible area, and a child control can draw menus that extend beyond the ordinary area during the layered stage. Understanding these two levels of order helps explain why the client needs to submit `order` and why it's impossible to reconstruct the complete behavior of a custom control from the Engine's node table.

### Nodes can be decoded independently, which is the result of the clipping stack balance.

The clipping stack has two actions. `push_clip` limits subsequent drawing to a rectangle, and the visible area after nesting is the intersection of constraints at each layer. `pop_clip` restores the previous layer. For example, first clip to a panel width of `100`, then to an editor width of `20`, so the actual drawable area satisfies both. Drawing only a prompt line that covers the entire window leaves only the intersection part. After restoring a layer, the same line can appear longer within the panel. This visual experiment shows that clipping affects subsequent instructions.

Multiple nodes within the window can be replaced independently, so a single node cannot leave the clipping to the next node. `command_renderer::begin_node()` replays the existing clipping to the new buffer. `render_control_list()` adds ancestor clipping to child controls, with the ancestor using its viewport when `scrollpanel`. `clip_floor` records the number of layers the control inherits upon entry, limiting the parent clipping from being removed when the control calls `pop_clip()`. After drawing ends, the newly created clipping is cleaned up, and `finish_node()` fills the inherited layers with paired `push_clip/pop_clip` before output. Engine's `drawing_reader::decode()` also checks each node for an empty stack and whether the end is zero.

As a result, each updated node comes with the necessary clipping context for drawing. Deleting the previous node allows the next node on the same window surface to reproduce the clipping. If a newly written control uses `push_clip` in one conditional branch and `pop_clip` in another, the fix is to match the entry and exit within the scope, rather than adding a matching command in the next control. The latter approach binds the resource boundaries of different nodes together.

## 2. From dirty flags to three types of differences

### The window version determines whether re-recording is worth it.

When a control change affects drawing, `ui_runtime::notify_changed()` increments the object's recorded `revision` and increases it level by level in the parent chain, allowing the window to observe internal changes. If a button is a child control of a scrollable panel, the window doesn't need to know the specific type of the button or where it needs to be updated. The cost of this failure propagation varies with tree depth. If only the child control has its own version number, changes to the child control will never be detected once the window uses the shortcut "do not enter if version doesn't change."

`flush_window_list()` records the version, activation state, modal blocking state, and focus editor cursor phase of the window. Any difference from the last recorded version may require recording. Window metadata is also assembled separately and compared. If both the recording threshold and metadata are stable, this round of recording can be skipped directly. If only metadata needs to be passed without re-recording, the metadata update path can also be used. Here, "only changing the position" means the final submission can be a separate metadata increment, while some SDK property change paths will still cause the window to re-record to ensure that the drawing content remains unchanged. Avoiding redundant updates during compilation and completely avoiding traversal on the CPU side are different optimizations.

Cursors, activations, and modals also belong to screen states. For example, if the title bars of two windows are drawn identically, clicking on one will make it the active window. Even if the text remains unchanged, the title effects may differ. After a modal window is opened, the effective `enabled` of the parent window in the protocol will be combined with the original control configuration to consider actual blocking. The Engine is responsible for window-level selection, while the SDK handles control-level visual and event handling. During testing in a modal state, you can simultaneously see the logical state of the parent window, the drawing nodes generated by the SDK, and the changes in the window-level interactive fields received by the Engine.

### Each submitted field undertakes a type of modification.

`surface_record_t` retains the data required for the next round of differences. The SDK compares new recorded instructions with current records by node ID, checks the sequence of visible nodes using the new and old order, and examines attribute fields with new metadata. The rules for these three fields are as follows.

|Field|Submitted content|Engine application method|
|---|---|---|
|`metadata`|Window properties that have changed|Merge by field, using the original value for missing fields|
|`node_list`|For newly added or modified nodes, each node sends the complete `command_list`|Replace the corresponding instruction list with `node`. Omission is equivalent to no node replacement this time.|
|`order`|The current complete node order is submitted only when needed.|Draw according to this order. Old nodes missing in the order will be removed from `node_map`.|

For example, the last `order=[400,404,408]`. When the cursor node `404` is updated, only the new commands for node `404` need to be submitted. When `404` is deleted, the new complete `order=[400,408]` should be submitted. If the order is set to `[408,400]`, the stacking relationship of the screen changes, but the command content remains. If the ID is retained but it is desired that this node does not draw anything this round, send `command_list: []` to the corresponding node. There is also a clear operation, `order: []`, which deletes all drawing nodes on that surface. Distinguishing between "no operations in this node" and "no nodes retained in this window" helps identify windows that suddenly become empty after updates.

This is a **node-level** difference. Suppose an input box node has four sets of operations: background, border, text, and cursor. When only the cursor is changed, the SDK can update only this node, but the complete list inside this node will still be transmitted. To locate changes to a single drawing command, additional stable identifiers, editing operations, and consistency rules are required. The current approach aims for simplicity in boundaries. Once an input box is replaced, the Engine only needs to take over with the new list, and other nodes reuse the old instructions. This granularity also makes it easier to compare SDK and Engine caches for consistency with complete nodes.

## 3. Read the difference as a complete `present` message

The following is an educational example at the local protocol layer. Session IDs and tokens are used for corresponding established sessions. In the example, the window `100` uses the upper-left position, and the constant `metadata.startup_position` is taken as `none`, so the specified position in the packet is retained. The Engine obtains positive logical width and height and positive physical magnification from the metadata of the newly created window. For an ordinary window, `reference` is set to `world`, and the SDK will also submit actual attributes such as name, title, and visibility. Two nodes are used to draw the background and text respectively. `window` is the window number within the session, and `node` is its drawing layer.

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
                "reference": "world",
                "startup_position": "none",
                "position":
                [
                    -0.32,
                    0.18,
                    -1.2
                ],
                "visible": true,
                "enabled": true,
                "name": "main_window",
                "title": "渲染示例"
            },
            "order":
            [
                400,
                404
            ],
            "node_list":
            [
                {
                    "node": 400,
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
                },
                {
                    "node": 404,
                    "command_list":
                    [
                        {
                            "type": "draw_text",
                            "rectangle":
                            {
                                "left": 24.0,
                                "top": 72.0,
                                "width": 592.0,
                                "height": 40.0
                            },
                            "text": "窗口已就绪",
                            "font":
                            {
                                "family": "Segoe UI",
                                "size": 20,
                                "bold": false,
                                "italic": false
                            },
                            "color": 4294967295,
                            "center": false
                        }
                    ]
                }
            ]
        }
    ]
}
```

Color in the protocol is a unsigned integer. `0x202020FF` represents opaque dark gray, which, when written as a valid JSON number, is `538976511`. The highest byte is `R`, followed by `G、B、A`. White `0xFFFFFFFF` corresponds to `4294967295`. Transparency is in the lowest byte, with `FF` being opaque. Beginners often write this order backwards, thinking that transparency is in the highest byte. You can first verify with the non-equivalent test color `0xFF000080`, which should be half-transparent red. If other almost transparent colors are displayed, prioritize checking the byte order of the fields.

The following is the update of existing windows one at a time. Since no nodes or levels are adjusted, the Engine retains the existing order and drawing data. The sender can repeat these position updates, allowing the window to move while always referencing the previously drawn texture.

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
            "metadata":
            {
                "position":
                [
                    -0.22,
                    0.18,
                    -1.2
                ]
            }
        }
    ]
}
```

A same request can contain multiple different windows. A window can also have multiple fields and nodes in one round. The sender does not need to send two separate messages for "changing the title after moving the window." Merging requests can reduce protocol fixed costs and allow the initial positions of the same batch of windows to be referenced to each other. This capability and underlying frame merging are two different things. Here, the application protocol clearly describes using one request to carry multiple windows, while the transport layer still reads according to its own header length and frame format.

## 4. What constraints are there for drawing commands at the Engine boundary?

`drawing_reader::decode()` extracts types, values, and parameter objects from JSON commands to generate drawing command objects within the Engine. Drawing geometry is expressed in logical pixels. Coordinates can be negative; for example, the path may cross the left edge of the window and then be constrained by clipping to finally be displayed. Width, height, or radius have clear non-negative limits, and line width must be greater than zero. Rectangles `left+width` and `top+height` also need to have finite results to avoid overflow when two individually readable numbers are added.

|Functions|Command|Fields to be understood|
|---|---|---|
|Fill and border|`fill_rectangle`、`outline_rectangle`|`rectangle` is `left/top/width/height`, with a separate `thickness` for the outline.|
|Lines|`draw_line`|Two points `x1/y1` and `x2/y2`, with color and line width.|
|Ellipses and circles|`fill_ellipse`、`outline_ellipse`|Inside `ellipse` are the center and two radii; if the radii are the same, it is a circle.|
|Rounded corners|`fill_rounded_rectangle`、`outline_rounded_rectangle`|Rectangles and `radius_x/radius_y`|
|Text|`draw_text`|Text, `rectangle`, color, `font`, and horizontal centering flag `center`.|
|Clipping|`push_clip`、`pop_clip`|Push into the rectangle; the stack for each node must be balanced.|
|Images|`draw_image`|Source width and height, `pixel_data` without pre-multipled RGBA, target rectangle, `opacity`.|
|Desktop|`draw_screen`|`screen_id` used for host machine collection and the target rectangle.|
|Paths|`fill_path`、`outline_path`|`path` with fill rules and segment lists; the outline has a separate line width.|

Paths can carry more curves compared to direct rectangles. First, `move` defines the starting point of a subpath, then connects `line` segments, `quadratic` quadratic bezier curves, `cubic` cubic bezier curves, or `arc` elliptical arcs. `quadratic` has one control point, while `cubic` has two control points. Control points control the curvature of the curve, used to generate shapes, but the graphic generally does not need to pass through control points. `close` connects from the end point back to the starting point of the subpath; the new `move` can start a new segment. Fill rules `even_odd` determine the interior based on the parity of the number of crossings, while `non_zero` determines the interior based on the number of directional circumambulations. Under double identical contours, the inner contour can have different colors in both rules. When an icon suddenly becomes hollow during debugging, check the original path direction and fill rules.

The text content is transmitted from the SDK's Unicode value through the protocol string to the Engine, which then uses DirectWrite for layout. In `draw_text`, `font` includes `family/size/bold/italic`. The font family name is not empty and contains no embedded NULs, and the font size is positive. `center` controls horizontal centering or alignment with the starting edge. The control uses a defined rectangle to convey drawing limitations. The Engine currently disables auto-wrap, allowing the SDK to coordinate with existing wrap and truncation logic. When long text exceeds expectations, check whether the control's calculation of the rectangle and layout should wrap. The font engine does not need to guess how the control wants to layout.

Images are more expensive than vector instructions. If the source image is wide `128` and high `64`, with four bytes per pixel for RGBA, the total original data is `32768` bytes, and the Base64 length is `4·ceil(32768/3)=43692` characters. The protocol transmits this data using standard Base64. Before decoding, verify that the product can be represented by the local size type and check the Base64 length. After decoding, verify the number of bytes. The target rectangle describes how large the image is, and the source size determines the number of pixels to read, which are independent of each other. Repeatedly setting a source image as new content per frame significantly increases transmission overhead. Desktop preview uses `draw_screen` references, which are collected by the Engine on the host side, keeping the real-time changing pixels closer to the graphics device.

## 5. Batch processing is a submission process with confirmed boundaries.

### Why wait for a response before updating the difference baseline?

Let's assume the currently confirmed screen of the window is `A`. The application records `B` and sends the difference from `A` to `B`. At this time, the user may have entered another character, and the application object has become `C`. The engine ultimately wants to see `C`. If `B` is sent and the local comparison baseline is always changed to `B`, encountering a server refusal, then the updates from `B` to `C` will miss those nodes in `B` that the engine never received. For example, `B` adds a new background, and `C` only changes the text inside. The increment may only reference the new background ID, and the old `A` on the server does not recognize it.

`flush_window_list()` saves `surface_update_map` and `metadata_update_map` for flying submissions, and `present_inflight` limits the batch of `present` that has not received results yet during the same runtime. This record is only placed in the committed cache after a successful callback confirmation. The application object can still change while waiting, and subsequent comparisons will use this confirmed batch of records with the latest object state. If the nodes' commands, order, and metadata are the same as the old record after the window is re-recorded, the Engine already has the same screen. The SDK can only update the local record used for comparison, so that subsequent rounds do not need to re-record the same results.

Receiving `present` response and receiving a device frame are two boundaries. The response indicates that the Engine has accepted and applied this batch of window behaviors, and the headset needs to wait for rendering and synthesis scheduling to see the results. The asynchronous response from the routing layer is distributed by the SDK's UI pump, and synchronous RPC only waits for its own response. When writing automated scripts, use clear pumping and screen observation as timing assertions. Using a synchronous request to "run all screen callbacks by accident" will confuse the two boundaries.

To avoid "the response only remembers the old object and then sends new properties down," the SDK applies a check when the first response is placed, to see if the window to be written back is still valid and whether its related properties still match. The first frame positioning of the new window is something that both the server and the SDK need to handle. The position changes returned by the protocol and the gestures happening need to be coordinated in the same comparison round, rather than letting the late response unconditionally overwrite the pose that has already been modified.

### The Engine first verifies the window candidates and then takes control of them.

The Engine reads the entire `window_list` from `service_runtime::present()`. The existing window uses the old records as a starting point, and metadata and commands are replaced accordingly. The new window candidates must meet certain constraints, such as logical dimensions, physical scaling, curvature, and normal references. There are two important integrity checks: First, each ID in `order` must exist in the merged node table, and it can only appear once. Second, the newly submitted node IDs must be present in the final `order`. Otherwise, the nodes will be discarded immediately, preventing consistent visualization. After the checks, the Engine removes any old nodes that are no longer needed, updating the state of the visualization. The list of unchanged commands continues to be used as an immutable shared object.

After all candidates are established, the Engine processes the first placement and window table submission. The ordinary new window record `startup_position` also references `startup_owner` when needed. The Engine resolves the first placements with dependencies among this batch of windows and then registers the updated objects in the session and global window mapping. Using the session and window number to query existing objects allows for safe differentiation between cases where both applications refer to `window=100`. Closing windows, changing visibility, and updating input area coordinates each have their own control paths, while window drawing nodes are still managed by the same surface object.

After protocol verification, `present` will return the corresponding results. If there is a first placement that needs feedback, it can include `window_list` and the corresponding local window number, position, and rotation in the response value. This list is used to coordinate metadata, and pixel data will not be sent from the Engine back to the SDK with the response. When no feedback is needed, the response value can be `null`. `render_error` is another type of subsequent event, corresponding to issues that occur during actual rendering or submission under the graphic path.

### Isolate other windows in the same batch to preserve them

Assuming `present` also carries the window `A、B、C`, where the drawing node of `B` references an non-existent ID. A batch error only informs the SDK of this submission failure, and a single batch error should not be used to determine if all three windows have the same fault. When multiple windows fail, the SDK removes duplicates from `present_retry_list` that need to be retried. If there are new windows dependent on source windows in this group, the source windows will be prioritized to maintain the order required for the first placement. Then, `flush_window_list()` takes valid windows from the queue and submits them one by one. Objects that have been closed and do not need to be updated can be skipped.

After this processing, the originally valid `A` and `C` can still be successfully refreshed. If the separately submitted `B` fails, the corresponding window record will retain the failed version or failed metadata, and generate `on_render_failed`. If the input state is exactly the same, repeatedly submitting the same erroneous data usually only increases bandwidth and triggers callbacks repeatedly. Failed records prevent infinite hot retries. After modifying the control state or related metadata, new candidates are generated, and the SDK compares whether it can be resent.

Isolation occurs at the protocol submission layer of the SDK. Another fault chain is earlier, when the application customizes `render()` and even fails to generate a valid node. The SDK records the failed version at the recording point and triggers `on_render_failed` for the window. There is also a later one, after the Engine receives valid content, the graphics API discovers errors in texture allocation, layout construction, or device status. The `report_render_error()` of the Engine sends events back to the session with the window. During debugging, recording which part first reports an error can determine whether it goes back to the drawing code, checks for protocol increments, or investigates D3D status.

Multi-window isolation also has costs. When a failed batch becomes a single-window sequence, more requests and waits are required. However, failures are usually rare, and batch processing advantages are still available. Re-generating data according to a certain window's subsequent version can also capture corrections made by the application while waiting. This is closer to the actual state in front of the user than continuously replaying old requests that have become invalid.

## 6. How Direct3D, Direct2D, and DirectWrite work together

### Drawing 2D UI into textures using the same device

The D3D11 texture can be understood as a two-dimensional pixel storage table held by the graphics device. Ordinary display applications often write the image into the swap chain. The goal of this project is to provide a texture for SteamVR that can be used as an overlay. Therefore, before presenting it through an independent swap chain, the image must first be written to the off-screen target. The `(0,0)` in the texture serves as the starting point for this pixel table. The position and angle of the window are determined by the subsequent overlay transformation.

`engine_host::initialize()` obtains the DXGI output adapter index from OpenVR, and then constructs `graphics_renderer` according to the hardware mode. This type of `create_device()` enumerates and selects the appropriate adapter when providing a valid adapter number, creating a D3D11 device with `D3D11_CREATE_DEVICE_BGRA_SUPPORT`. The device is responsible for resources such as textures, and the device context submits specific commands. Resources are created in a compatible format, allowing Direct2D to be used on the same device through DXGI interoperability. This eliminates the need to read the image to the CPU after each drawing and then send it to another set of graphics resources.

Direct2D is responsible for rendering two-dimensional geometry in the texture. `graphics_renderer` retrieves `IDXGIDevice` from the D3D device and then creates Direct2D devices and device contexts. When creating the window target, `create_target()` allocates `DXGI_FORMAT_B8G8R8A8_UNORM`'s `ID3D11Texture2D`, binding it as a rendering target and shader resource. Next, `IDXGISurface` is obtained, and a target bitmap view for Direct2D to write to is created using `CreateBitmapFromDxgiSurface()`. D3D textures and Direct2D bitmaps are different entries on the same surface storage; one is suitable for texture submission, and the other for two-dimensional rasterization.

DirectWrite is responsible for handling text layout and font characters. Text commands provide a string, font specifications, and target rectangle, and the layout phase converts the string into printable character relationships and coordinates. Finally, Direct2D renders using the layout and text color. Creating a DWrite font factory, layout, and device resources each has costs, so caching is implemented at both levels of granularity. `format_cache` stores `IDWriteTextFormat` according to font specifications. If two different labels use the same font specifications, the format can be reused. `node_renderer` also caches `IDWriteTextLayout` according to command objects, reserving layout for specific text and rectangles of the same stable node. After changing the text, rectangle, or node command object, the corresponding layout needs to be recreated. Caching the entire layout only according to the font name will mistakenly treat different texts as the same image.

Using vector commands allows the Engine to rasterize according to the window target size. After submission, the texture is sampled by SteamVR based on the viewing distance and physical size. The resolution still determines how many actual pixels the texture has. If `physical_scale` is enlarged to make a smaller texture appear larger, pixels or text will gradually become blurred. To improve clarity at a given physical size, the logical target resolution should be increased, and the physical ratio should be adjusted accordingly, along with re-evaluating the control layout and texture overhead.

### Why is there a distinction between RGBA and BGRA color formats?

The pixels of the transmitted image are arranged according to `R→G→B→A`, with independent colors and transparency. The D3D target uses a byte-order format of `B→G→R→A`, while Direct2D uses pre-multiplied Alpha. When importing images, the Engine rearranges the channels by pixel and pre-multiplies the colors. If the input pixels are `(R,G,B,A)`, the four values range from `0..255`. When replaced with `a=A/255`, pre-multiplied red is `R·a`, with green and blue being the same. During sampling or interpolation, the color of the transparent edges will match the actual contribution.

Pre-multiplication can be understood through an example. Semi-transparent red pixels are written as `(1,0,0,0.5)`, and after pre-multiplication, the color becomes `(0.5,0,0)`. When stacked on an opaque blue background, the commonly used source overlay formula is `C_out=C_src_premultiplied+(1−a_src)·C_dst_premultiplied`, resulting in approximately `(0.5,0,0.5)`. If the pre-multiplied red value `1` is used directly in this formula, the red edge will be too bright. Conversely, if pre-multiplied twice, the semi-transparent elements will be unusually dark. When debugging transparent edges, first determine whether the error lies in color interpretation order, source data format, or target Alpha mode. Directly adjusting a transparency constant can easily mask the real error.

Screen captures differ slightly from images. The screen represents real-time content on the host device, captured through a display device, with its own textures and update status. The captured desktop is generally used as an opaque source. When continuously observing a screen, the `screen_id` in `present` may remain unchanged, while new frames continue to redraw the target window. Therefore, "layout updates," "static image resources," and "external dynamic textures" must be processed with separate dirty sources. When observing the screen is unavailable, use `screen_state` to detect changes in availability, first checking whether the monitor still exists and whether the capture session can be restored normally.

## 7. Engine playback, double buffering, and SteamVR synthesis

### Which resources are reused, and which are regenerated

`graphics_renderer::get_surface()` reads the logical size and sequence of the window, checking if the valid textures match the size, if the saved version is outdated, and if the screen source is updated. If all conditions are stable, return directly to the existing `gpu_surface_t`. If redrawing is needed, first prepare a temporary storage target, then perform `SetTarget()`, `BeginDraw()`, and `Clear()`, and execute node commands according to the window's `order`. After clearing to transparency, redraw the entire target. The node differences only indicate how to update the drawing data in the Engine's memory. During normal redrawing, the Engine will fully playback the valid nodes of the window to maintain consistency between the background, semi-transparent content, clipping, and occlusion.

Caching doesn't lose its meaning just because it's played back every time. The Engine's `draw()` finds the `node_renderer` by node ID. When the immutable instruction list remains the same for the same object, the original text layout, image bitmaps, and path geometry can continue to be used. When a node is replaced, its `node_renderer` is rebuilt, and other nodes continue to use their existing caches. If a node is deleted, the corresponding cache is cleared. Windows that haven't changed can skip the entire redrawing. When redrawing changed windows, the constructed resources can be reused. Both save different steps.

Drawing uses two sets of targets: temporary storage and completed targets. After `EndDraw()` is successful, the textures and target views are exchanged. `generation` progresses with each successful redraw. If an exception occurs after clearing the screen or drawing, the old textures used for display are still valuable. Using the temporary storage area allows old resources to continue as the complete image from the last successful redraw, preventing the synthesizer from seeing half-removed windows. When only the spatial pose of the window changes, the texture can remain of the same generation, and the Overlay only updates meta-attributes such as spatial transformation or size.

The aforementioned "temporary textures" also need to be distinguished from screenshot reading. The `read_back()` for screenshots configures a dedicated `D3D11_USAGE_STAGING` resource for CPU reading, used for copying and reading pixels. The temporary drawing target for normal window operations is still an ordinary texture that can be drawn by the GPU. Both names can be translated as "temporary storage," but their uses are different. Placing daily images in CPU-readable resources adds unnecessary synchronization and copying to the GPU path.

### From textures to Overlay, spatial information is finally attached

`overlay_manager` maintains the OpenVR Overlay handle and applied property cache for each window. `submit_surface()` encapsulates the D3D11 texture pointer into `vr::Texture_t`, with the type set to `TextureType_DirectX`, the color space using `ColorSpace_Gamma`, and then calling `IVROverlay::SetOverlayTexture`. It compares the texture generation, usually only submitting when a new generation arrives, and paths such as visible and invisible switching can be forced to update. Applied transformations, width, curvature, and display states are maintained separately to avoid repeatedly sending the same settings during each VR refresh cycle.

SteamVR receives textures and surface parameters, not the applied control tree. The `SetOverlayTransformAbsolute`-related path uses the window's center pose, `SetOverlayWidthInMeters` provides width, and the curvature parameter is in `κW/(2π)`. For example, a window with a width of `1` and a total arc angle of `π/2`, the curvature itself is `π/2` per meter, and the normalized curvature received by OpenVR is approximately `0.25`. This is why the curvature ratio in the sampling log cannot be directly copied to the SDK properties. Detailed formulas for angles, radii, widths, and normalized number of circles are found in [spatial transformation](./07_spatial_math.md).

The front and back can share the same window texture, while the back requires corresponding geometric and texture sampling directions. For flat windows, the visible surface is obtained through reverse transformation, while for curved surfaces, segmentation approximation is used. The number of segments is determined by width, curvature, and allowable arc height error, with each segment having its own texture range. Suppose the angular span of a segment is `δ`, the chord length is `2R·sin(δ/2)`, and the distance from the arc center to the chord is `R·(1−cos(δ/2))`. Reducing the angular span per segment under the same radius significantly decreases the arc height error, but this comes at the cost of more Overlay handle updates and state changes. This is a method to control additional resources with display error control. The surface physical curvature and hit model still use cylindrical mathematics; only the back display undergoes this segmentation process.

After completing the front and back settings, the laser must also be drawn. The drawing of window content and the movement of laser endpoints are from different update sources. When the handle moves, the window texture remains stable, but the laser pose changes with each frame. Therefore, in a single frame update, only the laser or transformation may be submitted, and the window itself does not need to be rasterized. This helps determine whether the issue of "fast handle tracking but slow click effect" is due to updated geometric inputs or a long wait using `present`.

## 8. Two clocks, cursor timer, and resource control

### The refresh cycle and control frequency of controls are independent of each other.

The Engine's main loop waits for one display tick of SteamVR through `wait_frame_sync()`. Even if this tick is not obtained, the loop still processes necessary input components, keyboard, desktop, etc., and executes frame processing when ready. The display cycle determines when to update tracking and submit Overlay. The window version determines when to record and actually draw textures. If the headset runs at `90Hz`, it means there are about `90` display opportunities per second, so it's not necessary to rasterize the text of each static button `90` times.

The SDK's `wait_for_activity()` waits for the next activity based on connection condition variables, also considering cursor flickering of the focus editor, handle scrolling updates, and idle checks. `CARET_BLINK_INTERVAL_MILLISECOND` is for `500`, taking parity based on the half-second bucket of the monotonic clock. The window only includes this phase when it has a focus editor. The cursor can appear and disappear through the timer even without keyboard input. If a dialog box waits in the background without a focus editor, this flickering reason does not need to be driven to repaint every cycle. Assuming the editor always has focus, the visual state changes caused by the cursor are usually about twice per second, not synchronized with the headset refresh rate.

This helps to identify verifiable performance issues. Open the window and record the number of times `present` is sent by the SDK, as well as the number of times the Engine successfully advances the texture with `generation`. Move the window around to see if the metadata changes, while the texture generation remains unchanged. Finally, enter actual text; the text nodes will change, thereby advancing the texture generation. If the cursor flickers, many windows without focus will also be updated. Pay attention to which windows have focus and how the dirty flags are propagated. If the SDK submits few updates, but the Engine still redraws frequently, check whether `draw_screen` is being used or if resources are being reloaded repeatedly.

### Estimate memory and clarify counting range

Basic out-of-bounds checks first verify whether `width×4` can be represented as the line spacing required by D3D, then check the total size. Taking BGRA8 as an example, the theoretical data size of the texture is about `4·w·h`. `640×360` is a texture of about `0.88MiB`. `1920×1080` is about `7.91MiB`. If both the main target and the same-size temporary target have been established, the pure window target is about twice, i.e., `1.76MiB` and `15.82MiB`. Hardware alignment, driver space, intermediate resources for screenshots, and screenshot textures will affect the actual device usage and other components.

An example is keeping five `1920×1080` windows open. If each window has double buffering of about `15.82MiB`, the theoretical data of these five surfaces is close to `79.1MiB`. Adding the multiple large images used per window easily increases the number of resources. Reducing the window's physical size only changes the display scale, without affecting the number of pixels in the texture. To truly reduce surface resources, change the logical width and height or release unnecessary windows. If the main content of the screen is just a line of text, the window size can be chosen to fit the content, without defaulting to a texture with the same resolution as the desktop.

`graphics_renderer::get_byte_count()` is one of the resource counting entries in the source code. It aggregates the calculated volume of surface targets and node image caches. This value is suitable for comparing trends in two window layouts. When diagnosing the overall memory usage of the platform, it's also necessary to observe statistics on graphics drivers and other resources. When a window is removed, `discard()` clears the main texture, temporary targets, and node and screen records of that window. The texture resources are ultimately released according to the holding relationship. The Overlay also needs to clean up the corresponding handles. Closing it to just "blocking the screen" retains many historical states. Therefore, when troubleshooting recycling issues, it's important to distinguish between hidden windows and those truly removed from the session.

### Device recovery and WARP software backend

When D2D or D3D device errors need to be resolved, the device-related resources are re-established along the device inspection and recovery path. `graphics_renderer::prepare_frame()` is processed according to the recovery timing, with limited backoff between attempts. Once the device is successfully rebuilt, `device_generation` is added. `overlay_manager` marks the new device ID, which invalidates the previous texture cache. Subsequent surface redraws are then performed, and the available textures are submitted. The device ID and the texture ID for each window are two separate concepts. Window updates do not mean that the device needs to be restarted; instead, a device restart is required so that the textures for each window become available again.

`graphics_renderer` also supports the explicit `device_mode_t::software`. When this mode is selected, `D3D11CreateDevice` uses `D3D_DRIVER_TYPE_WARP`, with the CPU performing software rendering. Subsequently, it still uses D3D11, DXGI, and Direct2D interfaces. This backend allows for automated pixel checks on real text, colors, clipping, and transparent layers. During production Engine initialization, SteamVR's DXGI adapter is selected and hardware mode is used. Device loss recovery is rebuilt according to the current backend configuration. WARP is an independent optional testing or software execution path. Understanding this allows us to treat "normal rectangular screenshots during software rollback" and "correct overlay synthesis with real headsets" as two separate acceptance criteria. Headless WARP tests the rendering chain, while on actual machines, it also involves adapter, Overlay texture handles, and SteamVR synthesis timing.

## 9. Identifying issues with three sets of data

When a button click does not change the label, first confirm whether the application object's event has been distributed, and record the new text and window version. Then check in the next round of recording under the SDK whether `command_list` of the text node has changed, and whether `order` still contains that node. If the recording is correct but submission fails, check whether `present_inflight` is always waiting and whether the connection handles asynchronous callbacks. When the Engine returns success, then check the global mapping of the target window, rendering version, and texture algebra. If the texture algebra has changed but the headset screen does not appear, finally check the Overlay handle, display and hide, and device adapter. This order usually saves time compared to guessing "Direct2D font issues" from the start.

When the issue is that the page content scales beyond the clipping area, capturing a node `command_list` allows you to first check whether its inherited `push_clip` and its own `pop_clip` are paired in the same node. During testing, keep the adjacent nodes at a fixed color, deliberately change the source position and clipping size of the node being tested, and observe whether only the part that should be masked changes. If there are still remnants after removing a child control, check whether `order` has been updated and whether the Engine deletes old nodes in the new order. If only the color-changing node reuses an old text layout, check whether the old command object missed values due to comparison, or whether the new node replaced the expected ID.

You can perform three small checks to verify the boundaries of this chapter.

1. If `order=[4,8,12]` has already been submitted, how should the Engine handle the new text of node `8` and `order=[4,12]` now? The node `8` sent this time is missing in the final order, so the verification fails. To delete it, only send the new `order`; to keep it, keep `8` in the complete sequence.
2. A static `640×360` window doubles only `physical_scale`. How much does the theoretical byte count of the surface target change? If calculated using the original logical width and height, the theoretical value remains the same. However, its physical width and height become twice the original, and after sampling, it may look rougher. If you want to maintain the same density, you can increase the logical width and height and adjust the target physical size accordingly.
3. The SDK has received the batch of `ok=true`, but the old image still appears on the screen after a short period. What might be the issue? After the Engine receives the content, it needs to wait for the rendering to complete. Once rendered, the new texture data must be submitted to the synthesizer. By checking the consistency between `render_error`, the texture data, and the actual Overlay submission, we can distinguish between states such as not yet rendered, failed rendering, and submission not yet displayed.

Continuing the tracking, we go from the SDK's `render/command_renderer.cpp` and `core/ui_runtime_session.cpp` to the Engine's `core/service_runtime.cpp`, `render/drawing_reader.cpp`, `driver/graphics/graphics_renderer.cpp`, and `driver/steamvr/overlay_manager.cpp`. The next chapter will discuss the input routing of [and the serial draining of](./06_input_routing_and_drain.md), explaining how the user's actual actions lead to these graphical changes.