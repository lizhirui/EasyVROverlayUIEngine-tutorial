# Application Manifest Reference

`.easyvrui` is in UTF-8 JSON format. The Desktop and File Manager read the list through the SDK and launch the application on the computer of the caller. The relative paths within the list and the working directory of the sub-process are based on the directory where the list is located. The list of built-in ordinary applications is in `app/...` in the installation directory corresponding to the program. For example, `launch.script` of `app/demo/python/easyvrui_demo_python.easyvrui` is `main.py`.

## List Structure

```json
{
    "id": "example",
    "name":
    {
        "en": "Example",
        "zh": "示例",
        "ja": "サンプル"
    },
    "type": "application",
    "icon":
    {
        "path": "example.ico"
    },
    "launch":
    {
        "runtime": "native",
        "executable": "example.exe",
        "argument_list": []
    }
}
```

|Field|Rules|
|---|---|
|`id`|Application identifier; if omitted, take the list file name (without the extension)|
|`name`|Multilingual name object, must include the non-empty `en` field|
|`type`|Optional `application`, `desktop`, `layout`, or `ime`, default is `application`|
|`icon`|Optional icon object, must include one of `path` or `base64`|
|`launch`|Required startup configuration object|

The above table lists all valid top-level fields. Single-instance coordination is handled by the application itself.

The language matching order is: first match the complete system language, then strip the region or script sub-tags level by level, and finally revert to `en` (for example, `zh-Hant-TW` tries `zh-hant-tw`, `zh-hant`, `zh`, `en` in order). Language tags are case-insensitive, underscores are considered hyphens; if duplicate tags exist after normalization, an error will be reported.

`icon.path` points to external image files; `icon.base64` directly embeds file content supported by Windows image decoder such as PNG and ICO files (standard Base64 strings). Example is as follows:

```json
{
    "base64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQIHWP4z8DwHwAFgAI/ScLttAAAAABJRU5ErkJggg=="
}
```

## Native Program

When `launch.runtime` is `native`, use the following startup fields:

|Field|Rules|
|---|---|
|`runtime`|Required, fixed as `native`|
|`executable`|Required, executable file path (relative path is based on the directory where the list is located)|
|`argument_list`|Optional string parameter array, default is `[]`|

## Python Program

When `launch.runtime` is `python`, use the following startup fields:

|Field|Rules|
|---|---|
|`runtime`|Required, fixed as `python`|
|`script`|Required, Python main script path, relative path is based on the directory where the list is located|
|`argument_list`|Optional string parameter array, default is `[]`|

```json
{
    "id": "python_example",
    "name":
    {
        "en": "Python Example",
        "zh": "Python示例",
        "ja": "Pythonサンプル"
    },
    "launch":
    {
        "runtime": "python",
        "script": "main.py",
        "argument_list": []
    }
}
```

The SDK executes `python.exe -B <主脚本> <参数列表>` through `python.exe` in the PATH, and the main script must exist. The SDK first looks up the installation root directory from the list directory upwards, and then from the framework directory of the caller. After finding the installation, prepend `sdk/api/python/` to the sub-process' `PYTHONPATH` and keep the original value, while setting `EASYVRUI_NATIVE_DIR` to that directory. The SDK also sets `PYTHONDONTWRITEBYTECODE=1`. The application script is directly `import easyvrui`, and the interpreter must match the installed x64 native extension and CPython version.

## Parameters and Connection Information

Parameters in `argument_list` are passed item by item as they are, retaining complete empty strings, spaces, quotes, backslashes, and Unicode text. When calling `launch_application(manifest_path, extra_argument_list)`, additional parameters will be added after the list parameters; NUL characters are not allowed in names, identifiers, paths, or parameters.

If neither the list nor the additional parameters specify remote connection options, the SDK will automatically inherit `--easyvrui-host=`, `--easyvrui-port=`, `--easyvrui-access-credential=`, and `--easyvrui-public-key-fingerprint=` from the current calling process to the sub-process; if you need to specify them actively, follow the [remote SDK connection rules.](./engine_protocol) provides complete configuration.

## Desktop Application List

Desktop reads two configurations. The installer will register the built-in application in `app/desktop/config.json`. User configurations are located in `%USERPROFILE%\easyvrui\desktop\config.json`; when `USERPROFILE` is not set, `HOME` will be used.

The respective paths for the `application_list` record lists, with relative paths based on the directory where the configuration files are located. The system configuration example is as follows.

```json
{
    "application_list":
    [
        "../demo/cpp/easyvrui_demo_cpp.easyvrui",
        "../form_designer/easyvrui_form_designer.easyvrui"
    ]
}
```

Desktop reads the valid list of ordinary applications and merges them in memory based on the application ID `id`. When comparing, the case of ASCII letters in the ID is ignored. The system configuration takes precedence, and duplicate entries within each file are determined by the first valid record. If the list or startup entry is invalid, it will be skipped. Refreshing will reread both configurations.

When adding an application, Desktop checks whether the ID already exists in the merged list. Only user configurations are updated when adding or removing applications. System configurations are generated by the installer, and the registration path for built-in applications is managed by this file.

## File Manager file association

File Manager reads `association_map` from `app/file_manager/file_manager.json`. The key is the file extension with `.`, case-insensitive. The value is the `.easyvrui` list path, with relative paths based on the directory where the File Manager executable is located. When associating with installed Form Designer configuration files, the following mapping can be added to the object:

```json
{
    "association_map":
    {
        ".easyvruifrm": "../form_designer/easyvrui_form_designer.easyvrui"
    }
}
```

Double-clicking on `.easyvrui` in File Manager will launch the corresponding application. When double-clicking on a file with an associated extension, the SDK will pass the absolute path of the file as an additional parameter to the target application.