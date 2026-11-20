# Language APIs and engine_interface

In C++, `label.get_text()` is written, and in Python, `label.text` is read. Both ultimately access the same type of native objects. This chapter covers from links to actual event dispatch, then discusses how long an object can survive and how the designer generates construction code. By following this chain, you can understand where a property is stored, when it needs to enter the Python interpreter, and why the form can still be read by the caller after it is closed.

Native controls, language binding, events, and object lifecycle in ![,](/images/en/advanced_sdk_binding_lifecycle.png)

## 1. How a native implementation provides two forms of linking

`engine_interface/CMakeLists.txt` uses the same source code list to build the static library `engine_interface_static` and the shared library `engine_interface`. C++ includes the public header in `sdk/api/cpp/include`, with the common entry point being `easyvrui.h`. The header file provides declarations and visible object layouts, while the library provides implementations. The actual consumer link compiles the library, eliminating the need to copy control implementation source code into your own project.

A static library is a set of compiled object files. The linker integrates the required implementations into the final module based on the symbols introduced by the application. DLLs keep the implementations in separate binaries, and the import library provides the information needed for linking. During process loading, the actual DLL must also be found. Both static libraries and DLL import libraries may end with `.lib` on Windows, and it's impossible to determine which type they are based on the extension. Static linking only changes how client code enters the process; the application still uses the Engine service through independent connections.

`ENGINE_INTERFACE_API` allows the compiler to distinguish between three scenarios: exporting symbols when building the DLL, importing symbols when consuming the DLL, and using ordinary declarations when defining `ENGINE_INTERFACE_STATIC`. It doesn’t determine whether the call comes from Python or C++. For example, when compiling `button` to construct a call, the application only needs to know the parameters and types. The linking options then decide how the reference is resolved, and the control is actually constructed during program execution.

ABI is a convention followed at the binary level. Both parties must transfer parameters in a compatible manner, place return objects, understand the memory layout of classes, and access virtual functions. If one DLL provides `std::u32string` and another module releases this string, their views on runtime libraries, standard libraries, and debugging iterators must also be consistent. Successful construction does not guarantee safe destruction, and functions with the same name are not enough to prove ABI compatibility.

The project’s `EngineInterfaceRuntime.cmake` selects `/MT` or `/MTd` for static targets, and `/MD` or `/MDd` for DLL methods, and checks the consumer’s `MSVC_RUNTIME_LIBRARY`. When a program uses multiple modules simultaneously, it’s possible to infer why runtime compatibility is needed from the values passed in return strings, collections, or event closures. When encountering loading or linking issues, prioritize checking target bit depth, Debug or Release, CRT configuration, actual header entry, and corresponding library version. Changing the binary name generally cannot resolve inconsistencies in symbols or layout.

## 2. How public header files limit dependencies and internal access

### Observe the impact of the two build methods on fault patterns

If component A only links to the static SDK, you need to re-link component A after modifying the control implementation to apply the new implementation. If component A uses the accompanying DLL, the process will resolve the DLL import symbols when starting. Choosing the wrong DLL in the deployment directory may result in import errors or loading another set of compatible symbols. Looking only at the `#include <easyvrui.h>` in the source code, these two paths are almost identical. Troubleshooting can involve checking the targets selected by CMake, the linking inputs, and confirming the actual loading location of the module. This breaks down the issue of "code not working" into three visible problems: generation, linking, and loading.

Built-in C++ applications and installed Python native extensions defaultly link to `engine_interface_static`. The installer places the unique Python SDK in `sdk/api/python/`, along with packages, extensions, and build descriptions. When building extensions with shared linking, the corresponding DLL is required. The interpreter version, architecture, and linking mode must match the extension. Value objects with read-only bindings and native control-derived classes also use matching declarations at the binary boundary.

Engine, SDK, and built-in applications each embed the built-in language pack into the target files. Static linking brings the SDK's language resources into the executable or extensions, while the DLL method allows the SDK's DLLs to provide the same built-in text. Applications can load independent custom language packs through `language_pack.load_directory()`.

Public headers are organized by value type and classes available for application calls. If Windows platform handles, network classes, and device objects are directly embedded in the button header file, callers will see these types and all their indirect dependencies. Other headers' macros and types will also enter the application compilation unit along with their inclusion relationships. Leaving platform details in the driver implementation files means that modifications to extended device implementations are more focused, and applications can see the dependencies they truly need from the public declarations.

PIMPL refers to "pointer to implementation." Taking the internal `connection` as an example, the forward declaration allows the class to hold a pointer to `implementation`, with the actual layout of threads, condition variables, and message queues defined in the implementation file. Callers operate through method calls, without needing to know what container is used inside the queue. Subordination, destruction timing, and indirect access are part of this design. Not every value type is suitable for PIMPL; for example, a geometric vector with only components is clearer to pass by value.

Reducing the public layout helps to compress the scope of changes. It still cannot guarantee that any two versions of headers and libraries can be used together. As long as the layout, inheritance, or virtual function conventions of a public class change, interfaces with the same name may generate different machine codes. Using the matching SDK headers, binary, and toolchain is a more direct basis for deployment than relying on a single export macro.

The internal `control_access` is another type of boundary. Using C++'s friend rule, controls allow controlled internal access to a few states, enabling SDK to perform necessary operations. Applications only see business-oriented attributes, collections, events, and derived extension points. The permissions here are compile-time class access rules, unrelated to Engine-side authentication, window numbering, or TCP connectivity. If the business wants to change the text box content, it can call the public setter or write a Python property. The editor, capture, and drawing cache are still managed by their respective objects.

## 3. Understand subscription, snapshot, and dispatch of C++ events

`event_signal<source_type, argument_type_list...>` uses the sending object and payload type as template parameters. The internally stored entries contain a token and `std::function<void(source_type &, argument_type_list &...)>`. Most control events use a common alias `event_container<argument_type_list...>` to fix the sender as `control_base`. Therefore, they often use `control_base &` as the sender and a strongly typed parameter reference. When the template is instantiated, the compiler already knows which fields can be written before closing and which string is provided for text input. If a processor that only accepts key events is bound to a regular click, errors will be detected at the C++ call.

During subscription, `add()` checks the function's validity, assigns a number, and adds them in registration order. `+=` can also be subscribed, and when precise removal is needed later, a number is reserved with `add()`, then `remove(token)` is called. The dispatched `call()` first copies the callback list and then executes this snapshot in order. Thus, adding another callback in one callback is usually visible only in the next dispatch. Similarly, removing a later callback in an ongoing snapshot does not rewrite the already copied content. Input components also use a dispatch path with lifecycle checks, stopping further dispatch when the associated object becomes invalid.

Snapshots bring an easily overlooked C++ detail. If a mutable lambda is captured by value as an ordinary integer, the capture is copied along with its `std::function`, and modifying the lambda fields in this snapshot may not accumulate to the saved subscriptions. To achieve persistent counting, the business instance can save the count or store the value in shared state with a clear lifespan. Callbacks are only responsible for obtaining the current state from the owner and submitting the changes. Applications can naturally separate the state triggered each time from the long-running business state.

Each callback sees a reference to the same current payload. For example, the first shutdown processor finds unsaved data and sets `cancel` to true. Subsequent processors can still read this decision. Finally, the code that issued the shutdown request reads the final value to decide whether to continue. This does not conflict with snapshots, which protect the callback list; the parameters passed to each callback still represent the same event. Similarly, `handled` for keys, text, pointers, and scrolling is interpreted by the publisher according to event semantics.

## 4. Eighteen derived parameters and empty base classes

Click, load, and many property-specific change events use the empty `event_args_t` structure. Eighteen other event argument types publicly derive from it. A log helper can accept `const event_args_t &` to handle any event payload, while a closing handler can take `cancel_event_args_t &` directly. The base has no virtual functions or data members, so empty base optimization generally avoids adding a byte to the derived object. Its size still depends on its fields and their alignment. A stand-alone object of the empty base type has a nonzero size.

Inheritance gives the argument types a common base. A base reference sees the base interface, while the original derived reference still exposes its own fields. Copying a derived object into a base value keeps only the base subobject. The base has no virtual dispatch or runtime type identification. The event selects the callback signature at compile time. By default, `cancel_event_args_t{}` has `cancel=false`. With C++20 aggregate initialization, `cancel_event_args_t{{}, true}` uses the first `{}` to initialize the empty base.

|Derived types|Loadings|
|---|---|
|`cancel_event_args_t`|`cancel`, closed decision can be canceled|
|`key_event_args_t`|`key`, Shift, Ctrl, Alt, Meta, and `handled`|
|`text_input_event_args_t`|Input text and `handled`|
|`pointer_event_args_t`|Left and right hands, windows, and local coordinates, active positions, modifier keys, capture, cancel, and processing states|
|`scroll_event_args_t`|Left and right hands, `delta_x`, `delta_y`, `handled`|
|`interaction_end_event_args_t`|`cancelled`, used to indicate normal completion or cancellation|
|`property_changed_event_args_t`|`property_name`, read from the public property when a new value is needed|
|`control_collection_event_args_t`|Control pointers and indices|
|`menu_item_event_args_t`|Menu item pointers and indices|
|`tabpage_event_args_t`|Tab page pointers and indices|
|`listview_column_event_args_t`|Columns held by `shared_ptr` and indices|
|`listview_item_event_args_t`|Items held by `shared_ptr` and indices|
|`grid_column_event_args_t`|Column indices and widths|
|`grid_cell_event_args_t`|Lines, columns, and editing error fields|
|`tree_node_event_args_t`|Tree node pointers|
|`render_error_event_args_t`|Rendering error messages|
|`controller_event_args_t`|Left and right hands, triggers, side grips, joystick axes, and button states|
|`control_input_event_args_t`|Input types, positions, keys, text, and related states used by derived extensions|

The events returned by objects and the parameters required for events indicating changes are different. Table failure events can provide the error cell, while general property events only provide the name. When an event carries a control pointer, it remains an object representation within the process, and the number identifying a window in the protocol is two different types of data. Understanding it as an entity accessible by the processor during execution helps avoid writing internal reference errors into transmissions or files.

## 5. How Python extensions catch native types and events

### How does the value flow between two processors?

Suppose we first bind the Python processor P to a close event, and then bind another processor Q. The native initial payload can be denoted as `E0={cancel:false}`. When entering P, the binding uses the native payload to create an independent parameter object, which is equivalent to copying the value to `P0`. After P sets `cancel`, when returning, the modifiable state of `P0` is copied back to the same native payload. Q obtains the updated `E1` when it starts distributing. If Q is also a Python processor, it will create its own parameter object from `E1`. The source code copies and modifies in the exception branch before throwing the exception. Whether the caller continues to distribute depends on the exception path; the copy after the exception cannot be understood as continuing to normally trigger other callbacks.

Compare this process with C++ processors. The C++ processor directly gets a payload reference. Python wrapping takes care of the lifetime of the language object and synchronizes it with the interpreter. The business purposes of writing to both sides are the same, and their memory management methods are suitable for their respective languages. For these distributed parameters, reading and writing immediately within the callback can preserve the semantics of the event and prevent leaving the reference closure in another thread. During debugging, you can first set the value in the first processor and then print the received fields in the second one. Seeing it change with distribution verifies the transmission path without starting a time-consuming background action.

The event bridge also passes the sender as an independent parameter to Python. For example, the same business function can bind four buttons, and determine which one was clicked from `source.name` or object identity. Event fields represent data specific to the same action. Mouse or laser coordinates are parameters, and the public name of the control belongs to the sender. Writing both as a single universal dictionary requires guessing the field and value type temporarily each time it's used. Strong type adaptation precludes these choices in registration and binding definitions.

Python uses the public `easyvrui` package. `engine_interface_native*.pyd` explicitly binds constructors, methods, properties, and object containers through pybind11. The native `get_text()` and `set_text()` can be merged into Python's `text` properties. Collections support Python's iteration, indexing, and `len`, with data stored in native objects. The installed package and extensions are located in the same `sdk/api/python/` directory. When loading fails, first check the interpreter and module search paths, then check the Engine connection.

The eighteen derived payloads of C++ also inherit from `event_args` with corresponding Python types. `issubclass(easyvrui.cancel_event_args, easyvrui.event_args)` is established. When actually writing events, just set `event.cancel = True` according to the convention in the `on_closing` processor. Python binding adapts the native event into an object available to the Python processor. At the end of the callback, the modifications are sent back to the C++ logic, and any possible exceptions are propagated. Keeping one callback input parameter and changing it in the future does not restart the completed close or recalculate past input decisions.

The lock has two different responsibilities here. The GIL coordinates access to the interpreter object. The UI thread ensures the operation order of the control tree. When Python calls the native `run()` or blocks `show_dialog()`, it can release the GIL. The event bridge needs to obtain the GIL when executing Python callbacks. Even if the background thread has obtained the GIL, directly changing the control created by another thread does not satisfy control ownership. The correct approach is to deliver a task to the owner thread of the control, and the task updates the native control within the callback.

The entry points of the event bridge and the virtual function bridge are also different. The ordinary `button.on_click += handler` subscribes to a business action. The native derived behavior is found through trampoline to be rewritten by Python, and if necessary, enters the rewrite scope of `python_override_support`. When there is no corresponding rewrite, it runs along the native implementation. If a business button needs to be incremented, you can subscribe to events. To create a custom canvas, you need to consider the control derivation points opened through binding. Both paths can ultimately work within the same control tree.

## 6. Understanding object persistence from registration, display to close

`object_map` First, it is to search for the address index by object ID. `ui_runtime::register_object()` can use the non-ownership entry registration object constructed from an empty `shared_ptr` alias. The entry can find the address but will not create a new ownership for the stack object. During runtime, when searching for windows, ordinary controls, and containers, `weak_from_this().lock()` will be tried. If the object indeed has a living shared control block, a temporary ownership reference will be obtained. If the instance is held by the stack, the program still needs to ensure it is alive in the outer scope.

When displaying a window managed by a shared pointer, runtime will update the corresponding entry in `object_map` to a ownership reference, so that the displayed window does not disappear unexpectedly when local variables leave the scope. After closing the window, its activity record is removed, and the index is restored to a non-ownership entry. If the application still wants to read the dialog control at this time, it should hold its own shared reference or the corresponding Python instance. Closing the service window, stopping the event loop, and destroying the native object are three steps that can occur independently.

When accessing controls from a collection, it is also necessary to determine whether the object is held. Containers can retain their members through registered shared objects, and the temporarily obtained reference must respect the object's lifecycle. Pointers in collection events should be used on the spot within the callback. If an object is cached across callbacks, appropriate ownership can be obtained according to the actual API, or a business identifier that can be queried again can be saved, and the object is rechecked for validity. Saving the old control with a bare pointer, then deleting the entire page and waiting for the background to use that pointer, will make the object's lifespan out of the controllable range.

Delivering callbacks also requires judging the lifespan. `control_base::begin_invoke()` is handed over to the scheduling entry belonging to the thread. The internal `connection::post()` updates `callback_list` within a short lock and wakes up the thread. `get_dispatcher()` returns the function that captures weak references, and the callback is arranged only when the target implementation is still available and can be delivered. This weak holding avoids background tasks extending the entire connection's lifespan only because of saving the distribution handle. If the task itself captures a bare reference of an already destroyed object, the scheduler still cannot extend the object's lifespan for the business.

It is possible to imagine that the background loads a larger record set. This work first completes parsing, places the results in clearly owned objects, and then delivers a UI update. Delivering line by line can easily cause a large number of queuing operations to compete with input. The UI thread applies a batch of completed data to establish a layout within a continuous interval. If the user closes the window, the callback can detect whether the expected target is still valid. This judgment belongs to the business lifecycle judgment, and therefore can only be performed where it is truly needed.

## 7. Tree and verification of form design files

`.easyvruifrm` is the JSON during the design phase. The top-level records are `format`, `next_key`, and `root`. Each node record is `key`, `type`, `name`, `property_map`, `collection_name`, and `child_list`. Different types may have auxiliary collections, such as toolbar buttons, tree nodes, or columns and rows of a table. The data saves the layout and properties required to reconstruct the form. During runtime, the capture, scrolling, pending delivery cache, and local address inside the control remain in memory.

Below is the structure of the form document without child controls. When the program name is `counter`, the file can be named `counter.easyvruifrm`. The actual attributes need to match the declared types of all its controls.

```json
{
    "format": "easyvruifrm",
    "next_key": 2,
    "root":
    {
        "key": 1,
        "type": "window",
        "name": "counter",
        "property_map": {},
        "collection_name": "control_list",
        "child_list": []
    }
}
```

`key` provides a stable identification point within the document for the designer. After export, `name` must also become the programming member name. The exporter checks whether the target identifier is legal, whether it conflicts with other members of the same form, whether it uses reserved words, or conflicts with window properties. Naming a label with `label_count` allows identifying the same role from several locations: construction, property editing, code generation, and business reference. When a button is moved into a new container, the node position changes but the name can be retained. Renaming should also synchronize to use the business code that references it.

The control registration and property mode of the designer provide editable fields, value types, and required setters for the encoder, editor, and generator. For example, when there is a parent container, the acceptable sub-types will be determined. The width of table columns requires valid values. Some properties must be initialized before others, and the exporter will sort them according to the declaration phase. Understanding this, if the preview differs from the export, you can check item by item against "file declaration," "construction order," and "running object value," without attributing all problems to the JSON format.

## 8. How to combine generated classes and business classes

### From the file to the member declaration, gradually read through the generator

Assume that the root form is named `counter`, which contains a label and a button. The root node of the design document and its two child nodes each have their own `key`, and the two actual controls use `label_count` and `button_add` as names. The generator first traverses and verifies, then establishes an internal node table, recording the parent node number, target type, and identifiers to be output. This step avoids discovering that the parent-child relationship does not exist halfway through writing the output constructor. The keys in the internal table are used to parse references in the design file, and the output code uses meaningful member names to indicate access paths.

Taking C++ plain export as an example, the first round generates member declarations and construction statements. A label corresponds to `std::shared_ptr<easyvrui::label> label_count`, and an object is created using `std::make_shared` during construction. The second round generates attachment, adding the control to the `get_control_list().add(...)` of the parent node. The third round generates metadata and property assignments. Python uses the same traversal phase, writing `self.label_count = easyvrui.label(...)` in the first round, `control_list.add(...)` in the attachment phase, and finally writing the properties. Separating creation and attachment is justified. Some properties or metadata in the same form may reference another object; even if the latter is later in the tree, all instances can be created first.

For pages, the generator selects `page_list` or `control_list` from `collection_name` in `render_attachment()`. For menus and toolbars, special content also goes through corresponding attachment and initialization logic. Tables have two common models. The columns and items of `listview` are living objects in the public collection, while `grid` uses row, column, and cell data. Both may seem to have headers and grid areas, but they must be exported according to their respective data patterns during design. If the row structure of the latter is written for the former, even if the fields can be spelled out in JSON text, there is no correct runtime semantics.

When exporting icons and images, the design document provides the original data required for construction, and the exporter writes files for the corresponding resources, generating code that references paths it can find. To copy the output to another directory, the build files and resources needed for actual use should be processed together. Verifying whether the export is equivalent also requires checking the actual loading of resources; seeing that fields are not empty does not prove that images can be decoded from that path at runtime. The purpose of independent resource files is different from that of icons in the application manifest. One is for internal construction of forms, and the other is for application items to be displayed by starters like Desktop.

The order of attachment can be calculated manually. If A is the root form, B is the tab container, C is the page, and D is the button, after the first stage, all four objects exist, but they do not have a complete parent-child relationship yet. In the second stage, B is added to A, C is added to B's page collection, and D is placed in C. In the third stage, text and geometry are set, and then the business can reference D. If C from the second stage is incorrectly attached to A, compilation and binding may still succeed, but D will not hide with the page as expected when switching tabs. Verifying the actual tree relationship is more effective than just counting code lines.

`design_exporter.cpp` generates construction code based on the form description. The current C++ plain export writes the same-named `.h` and `.cpp` in the same directory. The header contains the window class and public control members, and the implementation contains the constructor. Python export is in the form of modules, where the `__init__` of the type creates controls, applies properties, and adds to collections. The exporter also offers a complete project option, allowing output of entry, manifest, and supporting project files. When searching for the generation result, actual class declarations and implementation files needed for compilation should be checked separately.

The generated type itself needs to inherit from `window` to use form functions. The business layer holds this generated instance, creates it during initialization, and then binds business methods using `ui->button_add` or `ui.button_add`. Counting, persistence, and background tasks are managed by the business class, while the constructed containers, buttons, and labels are provided by the generated form. This allows retaining the business implementation when re-generating the layout. If members are deleted or renamed, compilation errors or property access errors will accurately point to the references that need updating in the business.

A form with tabs illustrates why the construction order is important. The root form contains `tabcontrol`, two `tabpage` belong to its `page_list`, and buttons on each page are added to the page's `control_list`. If all controls are directly added to the root form, they will still display in the same coordinates, but they will lose the corresponding visibility and focus relationships when switching tabs. The generator selects the corresponding collection for attachment, producing a real control tree. This set of operations is mapped to equivalent public interfaces in both languages by the same design.

The combinations also make it easy to test them separately. First, create the generated types and verify that the members exist, and that their geometry and the positions where they are attached are correct. Then, let the business class handle the instances and verify the business state after button clicks. Finally, check the complete interaction between the window and the Engine during application runtime. When the layout changes, simply adjust the assertions affected in the first two experiments. For details about the API boundaries, see [, Chapter 03,](./03_ipc_tls_protocol.md). For callbacks and lifecycle events during modal behavior, see [, Chapter 04,](./04_session_and_context.md).

## 9. Verify end-to-end calls through combination instantiation

The following illustrates `counter_ui` generated by the designer, which provides `button_add` and `label_count`. The lifecycle of the business class covers `easyvrui.run()`. The processor is triggered by specific members of the generated object, and the business does not need to copy its interface construction statements. Instantiation, binding, and display are three steps in the program that can be observed separately.

```python
import easyvrui
from counter_ui import counter_ui

class counter_application:
    def __init__(self):
        self.ui = counter_ui()
        self.count = 0
        self.ui.button_add.on_click += self.button_add_click

    def button_add_click(self, source, event):
        self.count += 1
        self.ui.label_count.text = str(self.count)

def run_counter():
    easyvrui.set_application_name("计数器")
    application = counter_application()
    application.ui.show()
    easyvrui.run("计数器")
```

Here, `run_counter()` drives the window created by the current calling thread. After the first click, `count` becomes a continuously existing business instance, and the second click continues from the previous value. The generated `label_count` is held by the form and control collection. When the callback is written to it, it is already in the owner thread. In C++, the business class can hold `std::shared_ptr<counter_ui>` and call business member methods in event lambdas. The business object needs to last longer than the callback that holds a raw pointer to access it. If the control may exist independently of the business object, then subscriptions should be removed at the appropriate stage, or a weak reference should be used to attempt to obtain the business instance based on actual ownership.

The complete project export also has an option to export the business scaffolding. The existing template may provide a hollow shell inheriting from the generated class while retaining user files. The tutorial's business example uses combinations, and the normal export of generated constructions can still be used directly. When reading the default window name in the generated class, a different instance name can also be passed from the constructor to maintain multiple instances with the same interface design. Here, the instance name and the application session name are used as window and session identifiers respectively, and setting one will not rename the other. Two different workflows can use the same design file and control tree, and after entering the runtime phase, the session, window, and application business state will still be divided according to the previous rules.

After regenerating, three assertions can be verified layer by layer. First, `button_add` is indeed in the form member and the parent collection it should belong to. Second, simulate or actually click to call business methods, and write the numbers into local labels. Third, the Engine receives and displays the corresponding numbers. If the first item fails, check the documentation or the generator. If the second item fails, check the binding and focus. If the third item fails, check submission, graphics, or connections. By performing regression on these three levels, clear fault origins can be identified even when they run together.

### How to return from closing an event to the native caller

To add the behavior of "can only close after saving" on top of the counter, the most direct way is to subscribe to `on_closing`. If the state is not saved, set `cancel` of this event round to true. If the user has already saved, let the next close proceed normally. Each close first creates a new event payload, and the old boolean value will not be carried over to the next close. If you want to display a query in the callback, you can evaluate the calling position in combination with the modal owner relationship and the object destruction phase. Windows that have already entered the closed or non-interactive state can have specific owner checks fail, and after determining the interaction scenario, select the appropriate entry according to the conditions in Chapter 04 of [and Chapter 03 of](./04_session_and_context.md).

The corresponding experiment on the C++ side is to add a callback for the signal, and remove it with a token before the next distribution. This token belongs only to the management logic of the current event signal, should not be written into the form file, nor should it be passed to another signal removal. On the Python side, it can be removed with the corresponding callback object, especially when it is necessary to dismantle business modules that are long attached. The validity periods of the event list, form content, input focus, and business counts are different. Store them in appropriate objects, and when opening a window again, you can clearly decide which states to clear.

### How to identify connection errors and binding errors

When compiling or importing, if the class cannot be found, first verify the public interfaces, module paths, and binary compatibility. If the property type used during control creation is not appropriate, an error will usually occur during local construction or assignment. If the displayed window becomes invalid later due to a connection failure, the error occurs after the object has been successfully created. It’s necessary to check the session and transport layers for issues. After exporting the design in both languages, it’s possible to verify the construction by reading values locally. Then, observe the same service connection separately. This comparison doesn’t require modifying the protocol, allowing for pinpointing the exact layer where the issue occurs, whether it’s during generation, binding, native runtime, or service itself.

Another common misconception is that when certain rendering callbacks enter Python, it means that all construction and rendering operations will go through the interpreter. By default, the built-in behavior of native controls is implemented in C++. Only when Python callbacks or derived implementations are actually bound, does a language bridge become necessary. Performance tests should fix the window size, the number of nodes, and the number of business operations. It’s important to distinguish between construction, events, rendering, and transmission. If Python business callbacks are only used for short assignments, then the real hotspots might be in text measurement or remote submission delays. If the business processes draw many small elements per frame, then the number of bindings will increase accordingly. Even if the same SDK backend is used, the way the application’s code is organized can affect the running costs.