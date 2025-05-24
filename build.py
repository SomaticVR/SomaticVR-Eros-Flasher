from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but they might need fine-tuning.
build_exe_options = {
    "excludes": ["unittest"],
    "zip_include_packages": ["encodings"],
}

setup(
    name="SomaticVR-Eros-Flasher",
    version="0.1",
    description="Somatic Eros Firmware Updater",
    options={"build_exe": build_exe_options},
    executables=[Executable("FlashUtility.py", base="gui")],
)