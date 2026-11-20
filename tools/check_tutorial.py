from argparse import ArgumentParser
import ast
from html import unescape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit
from markdown_it import MarkdownIt
from PIL import Image
from capture_ui_screenshots import STORY_IMAGE_LIST
DOCS = Path(__file__).resolve().parents[1] / "docs"
EXAMPLES = DOCS.parent / "examples"
LOCALE_LIST = ("zh", "en", "ja")
CAPTURE_LIST = ("desktop", "form_designer", "file_manager", "task_manager", "demo_controls", "layout_keyboard", "ime_candidates", "dialog_messagebox", "dialog_color", "dialog_font", "dialog_file_open",)
MOCKUP_LIST = ("vr_hero_workspace", "vr_spatial_anchors", "vr_curvature_and_handles", "vr_input_stack", "vr_designer_annotated",)
CONTROL_CHAPTER_LIST = ("window", "label", "button", "textbox", "checkbox", "radiobutton", "progressbar", "slider", "numericupdown", "combobox", "listbox", "panel", "scrollpanel", "splitter", "tabcontrol", "treeview", "listview", "grid", "menubar", "toolbar", "image", "screen", "blank",)
CONTROL_IMAGE_LIST = tuple(f"{name}_{state}" for name in CONTROL_CHAPTER_LIST for state in ("default", "comparison", "demo"))
LESSON_IMAGE_LIST = (CONTROL_IMAGE_LIST + ("dialog_inputbox", "dialog_file_save", "spatial_custom_drawing", "spatial_anchor_config", "basics_form_design",)) + STORY_IMAGE_LIST
RETIRED_CHAPTER_SET = {"guide/01_text_button_tooltip.md", "guide/02_toggle_and_numeric.md", "guide/03_list_and_combobox.md", "guide/04_containers_and_tabs.md", "guide/05_tree_listview_grid.md", "guide/06_menu_toolbar_media.md",}
REFERENCE_LIST = ("python_api.md", "cpp_api.md", "engine_protocol.md", "application_manifest.md")
MARKDOWN = MarkdownIt("commonmark", {"html": True})
LEGACY_MANIFEST = re.compile(r'application_catalog|application_category|["\x27]category["\x27]', re.IGNORECASE)
LEGACY_API = re.compile(r"\b(?:dialog_future|event_data(?:_t)?|property_container|property_value|messagebox_result(?:_t)?|replace_selected_text|replace_selection|open_dropdown|close_dropdown|get_is_dropdown_open|get_listview_column_list|listview_(?:column|row)_t|set_node_list|[gs]et_node_expanded|tree_node_t|file_(?:open_|save_)?dialog_option_t|view_state|capture_view_state|restore_view_state|on_dialog_finished|get_dialog_active)\b|`tooltip`|(?:control/tooltip\.h|D:[/\\]Applications)", re.IGNORECASE,)
JSON_TOKEN = re.compile(r'"(?:[^"\\]|\\.)*"|-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?|true|false|null|[^\s]', re.S)

class image_html_parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.link_list = []

    def handle_starttag(self, tag, attr_list):
        if tag not in ("img", "source"):
            return

        for name, value in attr_list:
            if (name == "src") and (tag == "img") and value:
                self.link_list.append(value)
            elif (name == "srcset") and value and not value.startswith("data:"):
                self.link_list.extend(part.split()[0] for part in value.split(",") if part.strip())

def get_page_map():
    page_map = {locale: {} for locale in LOCALE_LIST}

    for file in sorted(DOCS.rglob("*.md")):
        relative = file.relative_to(DOCS)

        if any(part.startswith(".") for part in relative.parts) or (relative.parts[0] == "public"):
            continue

        locale = relative.parts[0] if (relative.parts[0] in ("en", "ja")) else "zh"
        name = Path(*relative.parts[1: ]).as_posix() if (locale != "zh") else relative.as_posix()
        page_map[locale][name] = file

    return page_map

def get_image_list(source):
    result = []
    pending = list(reversed(MARKDOWN.parse(source)))

    while pending:
        token = pending.pop()

        if token.type == "image":
            result.append(token.attrGet("src"))
        elif token.type in ("html_inline", "html_block"):
            parser = image_html_parser()
            parser.feed(token.content)
            result.extend(parser.link_list)

        if token.children:
            pending.extend(reversed(token.children))

    return result

def normalize_json(source):
    json.loads(source)
    token_list = JSON_TOKEN.findall(source)
    line_list = []
    line = ""
    depth = 0
    index = 0

    while index < len(token_list):
        token = token_list[index]
        index += 1

        if token in ("{", "["):
            empty_end = "}" if (token == "{") else "]"

            if (index < len(token_list)) and (token_list[index] == empty_end):
                line += ((" " if line.endswith(":") else "") + token) + empty_end
                index += 1
            else:
                if line:
                    line_list.append(("    " * depth) + line.rstrip())

                line_list.append(("    " * depth) + token)
                depth += 1
                line = ""
        elif token in ("}", "]"):
            if line:
                line_list.append(("    " * depth) + line.rstrip())

            depth -= 1
            line = token
        elif token == ",":
            line_list.append((("    " * depth) + line.rstrip()) + ",")
            line = ""
        elif token == ":":
            line += token
        else:
            line += (" " if line.endswith(":") else "") + token

    if line:
        line_list.append(("    " * depth) + line)

    return "\n".join(line_list)

def check_code_blocks(document, issue_list):
    source = document.read_text(encoding = "utf-8")
    relative = document.relative_to(DOCS)
    json_count = 0

    for match in LEGACY_API.finditer(source):
        line = source.count("\n", 0, match.start()) + 1
        issue_list.append(f"{relative}:{line}: outdated tutorial symbol {match[0]}")

    for token in MARKDOWN.parse(source):
        if (token.type != "fence") or (token.info.split()[: 1] != ["json"]):
            continue

        json_count += 1
        line = token.map[0] + 1

        try:
            if token.content.rstrip("\n") != normalize_json(token.content):
                issue_list.append(f"{relative}:{line}: JSON requires brace-on-own-line layout and four-space indentation")
        except ValueError as error:
            issue_list.append(f"{relative}:{line}: invalid JSON ({error})")

    return json_count

def get_example_code(document):
    code_map = {}
    source = document.read_text(encoding = "utf-8")

    for token in MARKDOWN.parse(source):
        if (token.type != "fence") or ("[" not in token.info):
            continue

        if token.info.startswith("python ") and (match := re.search(r"\b([\w]+\.py)\b", token.info)):
            code_map["python"] = (match[1], token.content.rstrip())
        elif token.info.startswith("cpp "):
            code_map["cpp"] = ("main.cpp", token.content.rstrip())

    for match in re.finditer(r"(?m)^<<< ([^\s]+)$", source):
        path = (document.parent / match[1]).resolve()

        if path.is_relative_to(EXAMPLES) and path.is_file() and (path.suffix in (".py", ".cpp")):
            language = "python" if (path.suffix == ".py") else "cpp"
            code_map[language] = (path.name, path.read_text(encoding = "utf-8").rstrip())

    return code_map

def check_example_data(issue_list):
    expected_set = {"basics/04_form_designer/quick_shout_window.easyvruifrm", "guide/08_spatial_drawing_deploy/python/wrist_watch.easyvrui", "projects/01_vrc_chatbox/python/vrc_chatbox.easyvrui",}
    path_list = sorted(path for path in EXAMPLES.rglob("*") if path.suffix in (".easyvruifrm", ".easyvrui"))
    actual_set = {path.relative_to(EXAMPLES).as_posix() for path in path_list}

    for entry in sorted(expected_set.difference(actual_set)):
        issue_list.append(f"missing example data: {entry}")

    for path in path_list:
        try:
            source = path.read_text(encoding = "utf-8").rstrip("\n")

            if source != normalize_json(source):
                raise ValueError("requires brace-on-own-line layout and four-space indentation")

            if path.suffix == ".easyvrui":
                if LEGACY_MANIFEST.search(unescape(source)):
                    raise ValueError("contains an obsolete application manifest name")

                data = json.loads(source)
                launch = data["launch"]

                if (launch["runtime"] == "python") and not (path.parent / launch["script"]).is_file():
                    raise ValueError("launch script does not exist alongside the manifest")
        except (OSError, ValueError, KeyError, TypeError) as error:
            issue_list.append(f"{path.relative_to(EXAMPLES)}: {error}")

def check_examples(page_map, issue_list):
    directory_list = sorted(path.parent.parent for path in EXAMPLES.rglob("cpp/CMakeLists.txt"))
    expected_count = 15 + len(CONTROL_CHAPTER_LIST)

    if len(directory_list) != expected_count:
        issue_list.append(f"expected {expected_count} C++ example projects; found {len(directory_list)}")

    block_count = 0

    for directory in directory_list:
        chapter = directory.relative_to(EXAMPLES).as_posix() + ".md"

        if chapter in RETIRED_CHAPTER_SET:
            continue

        primary = None

        for locale, group in page_map.items():
            if chapter not in group:
                issue_list.append(f"{locale}: no tutorial chapter for {chapter}")
                continue

            code_map = get_example_code(group[chapter])

            if set(code_map) != {"cpp", "python"}:
                issue_list.append(f"{group[chapter].relative_to(DOCS)}: missing runnable Python or C++ block")
                continue

            if locale == "zh":
                primary = code_map

            if primary and any((name != primary[language][0]) for language, (name, _) in code_map.items()):
                issue_list.append(f"{group[chapter].relative_to(DOCS)}: example entry filename differs by locale")

            try:
                ast.parse(code_map["python"][1])
            except SyntaxError as error:
                issue_list.append(f"{group[chapter].relative_to(DOCS)}: Python code block does not parse ({error})")

            for language, (name, source) in code_map.items():
                block_count += 1

                if locale != "zh":
                    continue

                file = (directory / language) / name

                if not file.is_file():
                    issue_list.append(f"{chapter}: missing source file {language}/{name}")
                elif file.read_text(encoding = "utf-8").rstrip() != source:
                    issue_list.append(f"{chapter}: {language}/{name} differs from the corresponding source block")

        if primary:
            launcher = (directory / "python") / "run.cmd"
            name = primary["python"][0]

            if (not launcher.is_file()) or (f'"%~dp0{name}"' not in launcher.read_text(encoding = "utf-8")):
                issue_list.append(f"{chapter}: missing CMD launcher for {name}")

    print(f"Examples: {len(directory_list) - len(RETIRED_CHAPTER_SET)} active projects; {block_count} localized Python/C++ source blocks")

def get_local_image(document, link):
    url = urlsplit(link)

    if url.scheme or url.netloc:
        return None

    path = unquote(url.path)
    location = ((DOCS / "public") / path.lstrip("/")) if path.startswith("/") else (document.parent / path)
    location = location.resolve()

    if not location.is_relative_to(DOCS):
        raise ValueError("image target leaves docs root")

    return location

def verify_tutorial(report_inventory):
    issue_list = []
    page_map = get_page_map()
    all_page_set = set().union(*(set(group) for group in page_map.values()))
    print("Tutorial Markdown " + ", ".join(f"{locale}={len(page_map[locale])}" for locale in LOCALE_LIST))

    for locale, group in page_map.items():
        for name in sorted(all_page_set.difference(group)):
            issue_list.append(f"{locale}: missing translation for {name}")

        for name in sorted(RETIRED_CHAPTER_SET.intersection(group)):
            issue_list.append(f"{locale}: retired chapter remains at {name}")

    baseline_route_list = []

    for locale, group in page_map.items():
        sidebar = (DOCS / f".vitepress/locales/{locale}.mts").read_text(encoding = "utf-8")
        route_list = re.findall(r"link: '(/[^']*)'", sidebar.partition("themeConfig:")[2])
        prefix = f"/{locale}" if (locale != "zh") else ""
        path_list = [route.removeprefix(prefix).lstrip("/") for route in route_list]

        for route, path in zip(route_list, path_list, strict = True):
            chapter = (path + "index.md") if (not path or path.endswith("/")) else (path + ".md")

            if chapter not in group:
                issue_list.append(f"{locale}: navigation route has no page: {route}")

        if locale == "zh":
            baseline_route_list = path_list
        elif path_list != baseline_route_list:
            issue_list.append(f"{locale}: navigation route sequence differs from zh")

    print(f"Navigation: {len(set(baseline_route_list))} routes checked per language")

    for name in REFERENCE_LIST:
        if ("reference/" + name) not in page_map["zh"]:
            issue_list.append(f"missing Chinese reference page: {name}")

    check_examples(page_map, issue_list)
    check_example_data(issue_list)
    link_count = 0
    external_count = 0
    document_list = [file for group in page_map.values() for file in group.values()]
    json_count = 0

    for document in document_list:
        json_count += check_code_blocks(document, issue_list)
        content = document.read_text(encoding = "utf-8")

        if match := LEGACY_MANIFEST.search(unescape(content)):
            issue_list.append(f"{document.relative_to(DOCS)}: obsolete manifest name {match[0]}")

        for link in get_image_list(content):
            link_count += 1
            relative = document.relative_to(DOCS)

            if not link:
                issue_list.append(f"{relative}: image source is empty")
                continue

            try:
                image = get_local_image(document, link)
            except ValueError as error:
                issue_list.append(f"{relative}: {link} ({error})")
                continue

            if image is None:
                external_count += 1
            elif not image.is_file():
                issue_list.append(f"{relative}: missing image {link}")

    print(f"Image links checked: {link_count - external_count} local; {external_count} external URLs")
    print(f"Legacy API and JSON format checks: {len(document_list)} Markdown pages; {json_count} JSON blocks")
    present_count = 0
    image_root = DOCS / "public/images"
    baseline_set = {path.name for path in (image_root / "zh").glob("*.png")}
    required_set = {f"{name}.png" for name in (CAPTURE_LIST + MOCKUP_LIST) + LESSON_IMAGE_LIST}

    for locale in LOCALE_LIST:
        actual_set = {path.name for path in (image_root / locale).glob("*.png")}
        missing_set = (baseline_set | required_set) - actual_set

        for name in sorted(missing_set):
            issue_list.append(f"{locale}: missing PNG {name}")

        for name in sorted(actual_set - baseline_set):
            issue_list.append(f"{locale}: PNG has no corresponding zh file: {name}")

        for name in sorted(actual_set):
            path = (image_root / locale) / name

            try:
                with Image.open(path) as image:
                    if image.format != "PNG":
                        raise ValueError("expected PNG")

                    width, height = image.size
                    image.verify()

                present_count += 1

                if report_inventory:
                    print(f"{locale}/{name}.png\t{width}x{height}")
            except (OSError, ValueError) as error:
                issue_list.append(f"{path.relative_to(DOCS)}: {error}")

    expected_count = len(LOCALE_LIST) * len(baseline_set | required_set)
    print(f"PNG assets checked: {present_count}/{expected_count}")

    for issue in issue_list:
        print(issue, file = sys.stderr)

    return bool(issue_list)

def run():
    parser = ArgumentParser(description = "Check localized tutorial routes, Markdown image links, and the published PNG inventory.")
    parser.add_argument("--inventory", action = "store_true", help = "Print the dimensions of each required PNG.")
    option = parser.parse_args()
    raise SystemExit(verify_tutorial(option.inventory))

if __name__ == "__main__":
    run()