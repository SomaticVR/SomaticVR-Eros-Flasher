#!/bin/python3
import sys
import shutil

if (len(sys.argv) > 2):
    shutil.copy2(str(sys.argv[1]) + '/.pio/build/esp32c3/bootloader.bin', './Firmware/bootloader.bin')
    shutil.copy2(str(sys.argv[1]) + '/.pio/build/esp32c3/partitions.bin', './Firmware/partitions.bin')
    shutil.copy2(str(sys.argv[2]) + '/.platformio/packages/framework-arduinoespressif32/tools/partitions/boot_app0.bin', './Firmware/boot_app0.bin')
    shutil.copy2(str(sys.argv[1]) + '/.pio/build/esp32c3/firmware.bin', './Firmware/firmware.bin')
else:
    print("Error: 2 arguments required")
    print("cpFirmware [firmware Source] [platformio source]")
