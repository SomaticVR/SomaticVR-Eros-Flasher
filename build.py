from cx_Freeze import setup, Executable
import os
import subprocess

# Dependencies are automatically detected, but they might need fine-tuning.
build_exe_options = {
    "excludes": ["unittest"],
    "zip_include_packages": ["encodings"],
}

version = "0.0"
try:
	version = subprocess.check_output(["git", "describe", "--abbrev=0", "--tags"]).strip().decode("utf-8")
	if version.startswith("v"):
		version = version[1:]
except Exception:
	version = "0.0"
	
setup(
    name="SomaticVR-Eros-Flasher",
    version=version,
    description="Somatic Eros Firmware Updater",
    options={"build_exe": build_exe_options},
    executables=[Executable("FlashUtility.py", base="gui")],
)