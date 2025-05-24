from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but they might need fine-tuning.
build_exe_options = {
    "excludes": ["unittest"],
    "zip_include_packages": ["encodings"],
}

def git_tag():
    import subprocess
    tag = ""
    try:
        tag = subprocess.check_output(["git", "--no-pager", "tag", "--sort", "-taggerdate", "--points-at" , "HEAD"]).strip().decode("utf-8")
        if tag.startswith("v"):
            tag = tag[1:]
    except Exception:
        tag = ""
    return tag


setup(
    name="SomaticVR-Eros-Flasher",
    version=git_tag(),
    description="Somatic Eros Firmware Updater",
    options={"build_exe": build_exe_options},
    executables=[Executable("FlashUtility.py", base="gui")],
)