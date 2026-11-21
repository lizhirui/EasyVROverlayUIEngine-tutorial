from argparse import ArgumentParser
import json
import os
from pathlib import Path
import shutil
import subprocess
from tempfile import TemporaryDirectory
from PIL import Image, ImageStat
SITE = Path(__file__).resolve().parents[1]
WORKSPACE = SITE.parent
OUTPUT = ((SITE / "docs") / "public") / "images"
WORK = SITE / ".work"
PARTS = WORK / "parts"
LOCALE_LIST = ("zh", "en", "ja")
CAPTURE_MAP = {"desktop": ("desktop",), "designer": ("form_designer",), "file_manager": ("file_manager",), "task_manager": ("task_manager",), "demo": ("demo_controls",), "keyboard": ("layout_keyboard",), "dialog": ("dialog_messagebox", "dialog_color", "dialog_font", "dialog_file_open"),}
CONTROL_CAPTURE_MAP = {"controls": ("window", "label", "button", "textbox", "checkbox", "radiobutton", "progressbar"), "controls_second": ("slider", "numericupdown", "combobox", "listbox", "panel", "scrollpanel", "splitter", "tabcontrol",), "controls_third": ("treeview", "listview", "grid", "menubar", "toolbar", "image", "screen", "blank"),}
TOPIC_IMAGE_LIST = ("dialog_inputbox", "dialog_file_save", "spatial_custom_drawing", "spatial_anchor_config")
STORY_IMAGE_LIST = ("basics_first_initial", "basics_first_clicked", "basics_form_initial", "basics_form_sent", "project_chatbox_idle", "project_chatbox_preview", "project_chatbox_cooldown", "project_chatbox_confirm", "project_gallery_idle", "project_gallery_filtered", "project_gallery_photo", "project_gallery_export", "project_avatar_idle", "project_avatar_edit", "project_avatar_preset", "project_wrist_compact", "project_wrist_level", "project_wrist_screen", "project_wrist_anchor", "project_kaomoji_config", "project_kaomoji_connected", "project_kaomoji_group", "project_kaomoji_history",)
ROLE_LIST = (tuple(CAPTURE_MAP) + ("ime", "project_story")) + tuple(CONTROL_CAPTURE_MAP)
APPLICATION_DIRECTORY_MAP = {"desktop": "desktop", "designer": "form_designer", "file_manager": "file_manager", "task_manager": "task_manager", "demo": "demo/cpp", "keyboard": "layout/standard_104", "pinyin": "ime/cn/easyvrui_pinyin", "japanese": "ime/jp/easyvrui_japanese",}

def build_capture_targets(build_directory, project, role_list):
    if not build_directory.is_relative_to(SITE):
        raise RuntimeError("Choose a capture build directory inside the tutorial checkout.")

    target_list = " ".join(f"tutorial_capture_{role}" for role in role_list)
    cmd = os.environ.get("ComSpec", r"C:\Windows\System32\cmd.exe")
    batch = SITE / "tools/build_capture.cmd"
    command = f'"{cmd}" /d /s /c ""{batch}" "{WORKSPACE}" "{build_directory}" "{project}" "{target_list}""'
    subprocess.run(command, cwd = SITE, check = True)

def prepare_fixture(directory):
    directory.mkdir()

    for name in ("Assets", "Examples", "Templates"):
        (directory / name).mkdir()

    sample = ((((WORKSPACE / "repo") / "app") / "demo") / "cpp") / "translator_window_ui.easyvruifrm"
    shutil.copyfile(sample, directory / "welcome.easyvruifrm")
    form = SITE / "examples/basics/04_form_designer/quick_shout_window.easyvruifrm"
    shutil.copyfile(form, directory.parent / form.name)
    (directory / "notes.txt").write_text("EasyVRUI tutorial sample\n", encoding = "utf-8")
    (directory / "settings.json").write_text('{\n    "language": "en"\n}\n', encoding = "utf-8")

def stage_installation(directory, repository, role_list):
    installer = repository / "install.bat"
    cmd = os.environ.get("ComSpec", "cmd.exe")
    subprocess.run(f'"{cmd}" /d /s /c ""{installer}" "{directory}""', cwd = SITE, check = True)

    if "desktop" in role_list:
        config = directory / "app/desktop/config.json"
        path_list = json.loads(config.read_bytes())["application_list"]
        entry_list = [json.loads((config.parent / path).read_bytes()) for path in path_list]
        id_set = {entry["id"].casefold() for entry in entry_list if entry["type"] == "application"}

        if (len(path_list) != 5) or (len(id_set) != 5):
            raise RuntimeError("Expected five unique application IDs in the installed Desktop configuration")

        print("Installed Desktop application IDs: " + ", ".join(sorted(id_set)), flush = True)

def run_capture(installation, build_directory, name, output, fixture, profile, locale, argument_list = ()):
    directory = APPLICATION_DIRECTORY_MAP.get(name)
    runtime = ((installation / "app") / directory) if directory else (installation / "bin")
    source = (build_directory / "bin") / f"tutorial_capture_{name}.exe"
    executable = runtime / source.name
    shutil.copy2(source, executable)
    env = dict(os.environ, EASYVRUI_LANGUAGE = locale, USERPROFILE = str(profile), APPDATA = str(profile / "Roaming"), LOCALAPPDATA = str(profile / "Local"),)
    output.mkdir(parents = True, exist_ok = True)
    print(f"[{locale}] WARP: {name}", flush = True)
    subprocess.run([str(executable), str(output), str(fixture), locale, *argument_list], cwd = runtime, env = env, check = True, timeout = 100,)

def check_image(path):
    with Image.open(path) as image:
        image.load()

        if ((image.format != "PNG") or (min(image.size) < 24) or (max(ImageStat.Stat(image.convert("RGB")).stddev) < 3.0)):
            raise RuntimeError(f"Missing visible raster content: {path}")

        return image.size

def get_ime_preview(output):
    with Image.open(output / "input_bar.png") as bar, Image.open(output / "candidate.png") as candidate:
        gap = 8
        width = max(bar.width, candidate.width)
        height = (bar.height + gap) + candidate.height
        combined = Image.new("RGBA", (width, height), (13, 24, 40, 255))
        combined.alpha_composite(bar.convert("RGBA"), ((width - bar.width) // 2, 0))
        combined.alpha_composite(candidate.convert("RGBA"), ((width - candidate.width) // 2, bar.height + gap))
        return combined

def combine_ime_preview(output):
    pinyin = get_ime_preview(output / "pinyin")
    japanese = get_ime_preview(output / "japanese")
    margin = 18
    gap = 28
    width = max(pinyin.width, japanese.width) + (2 * margin)
    height = ((pinyin.height + gap) + japanese.height) + (2 * margin)
    canvas = Image.new("RGBA", (width, height), (13, 24, 40, 255))
    canvas.alpha_composite(pinyin, ((width - pinyin.width) // 2, margin))
    canvas.alpha_composite(japanese, ((width - japanese.width) // 2, (margin + pinyin.height) + gap))
    canvas.save(output / "ime_candidates.png")

def combine_window_comparison(output):
    name_list = ("window_default", "window_custom_title", "window_no_close", "window_no_title")
    gap = 24

    with Image.open(output / "window_default.png") as first:
        width, height = first.size

    canvas = Image.new("RGB", ((2 * width) + (3 * gap), (2 * height) + (3 * gap)), "#101b2a")

    for index, name in enumerate(name_list):
        with Image.open(output / f"{name}.png") as image:
            x = gap + ((index % 2) * (width + gap))
            y = gap + ((index // 2) * (height + gap))
            canvas.paste(image, (x, y))

    canvas.save(output / "window_comparison.png")

def combine_menu_comparison(output):
    target = output / "menubar_comparison.png"

    with Image.open(output / "menubar_alt_held.png") as held, Image.open(target) as navigation:
        gap = 16
        canvas = Image.new("RGB", (held.width, (held.height + gap) + navigation.height), "#101b2a")
        canvas.paste(held.convert("RGB"), (0, 0))
        canvas.paste(navigation.convert("RGB"), (0, held.height + gap))

    canvas.save(target)

def capture_locale(stage, installation, build_directory, locale, role_list):
    profile = stage / f"profile_{locale}"
    (profile / "Roaming").mkdir(parents = True)
    (profile / "Local").mkdir()
    output = stage / locale
    fixture = stage / "Examples"
    name_list = []
    part_list = []

    for role in role_list:
        if role == "ime":
            for ime in ("pinyin", "japanese"):
                run_capture(installation, build_directory, ime, output / ime, fixture, profile, locale)

            combine_ime_preview(output)
            primary_ime = output / ("japanese" if (locale == "ja") else "pinyin")
            part_list.extend(primary_ime / f"{name}.png" for name in ("candidate", "input_bar", "input_box"))
            name_list.append("ime_candidates")
        elif role == "project_story":
            if locale == "zh":
                run_capture(installation, build_directory, role, output, fixture, profile, locale)
                name_list.extend(STORY_IMAGE_LIST)
        elif role == "menubar":
            if (locale == "zh") and ("controls_third" not in role_list):
                run_capture(installation, build_directory, "controls_third", output, fixture, profile, locale, ("--menubar-only",),)
                combine_menu_comparison(output)
                name_list.extend(("menubar_default", "menubar_comparison", "menubar_demo"))
        elif role in CONTROL_CAPTURE_MAP:
            if locale == "zh":
                run_capture(installation, build_directory, role, output, fixture, profile, locale)
                name_list.extend(f"{name}_{state}" for name in CONTROL_CAPTURE_MAP[role] for state in ("default", "comparison", "demo"))

                if role == "controls":
                    combine_window_comparison(output)
                elif role == "controls_third":
                    combine_menu_comparison(output)
                    name_list.extend(TOPIC_IMAGE_LIST)
        else:
            run_capture(installation, build_directory, role, output, fixture, profile, locale)
            name_list.extend(CAPTURE_MAP[role])

            if role == "designer":
                part_list.append(output / "designer_regions.json")

                if locale == "zh":
                    name_list.append("basics_form_design")

    image_list = [output / f"{name}.png" for name in name_list]

    for image in image_list:
        width, height = check_image(image)
        print(f"{locale}/{image.name} {width}x{height}")

    return image_list, part_list

def run():
    parser = ArgumentParser(description = "Build current EasyVRUI sources and capture actual UI rasters using the WARP test host.")
    parser.add_argument("--native-build", type = Path, default = WORK / "capture")
    parser.add_argument("--repository", type = Path, default = WORKSPACE / "repo", help = "EasyVRUI repository containing the independently built components.",)
    parser.add_argument("--output", type = Path, default = OUTPUT)
    parser.add_argument("--parts", type = Path, default = PARTS)
    parser.add_argument("--locale", choices = LOCALE_LIST, action = "append")
    parser.add_argument("--role", choices = ROLE_LIST + ("menubar",), action = "append")
    parser.add_argument("--reuse-binaries", action = "store_true", help = "Use already built capture executables from --native-build/bin.",)
    option = parser.parse_args()
    build_directory = option.native_build.resolve()
    repository = option.repository.resolve()
    destination = option.output.resolve()
    role_list = tuple(dict.fromkeys(option.role or ROLE_LIST))
    print(f"WARP resources: {repository}", flush = True)

    if not option.reuse_binaries:
        executable_map = {"ime": ("pinyin", "japanese"), "menubar": ("controls_third",)}
        name_list = dict.fromkeys(name for role in role_list for name in executable_map.get(role, (role,)))
        build_capture_targets(build_directory, SITE / "tools/capture_project.cmake", name_list)

    WORK.mkdir(parents = True, exist_ok = True)

    with TemporaryDirectory(prefix = "capture_", dir = WORK) as temporary:
        stage = Path(temporary)
        installation = stage / "installation"
        stage_installation(installation, repository, role_list)
        prepare_fixture(stage / "Examples")
        capture_map = {locale: capture_locale(stage, installation, build_directory, locale, role_list) for locale in dict.fromkeys(option.locale or LOCALE_LIST)}

        for locale, (image_list, part_list) in capture_map.items():
            for folder, source_list in ((destination / locale, image_list), (option.parts.resolve() / locale, part_list),):
                folder.mkdir(parents = True, exist_ok = True)

                for source in source_list:
                    shutil.copyfile(source, folder / source.name)

    print(f"Published {sum(len(result[0]) for result in capture_map.values())} PNG files at {destination}")

if __name__ == "__main__":
    run()