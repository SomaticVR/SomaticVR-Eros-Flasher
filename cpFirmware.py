#!/bin/python3
import sys
# import shutil
import esptool

if (len(sys.argv) > 2):
    # esptool.py --chip ESP32 merge_bin -o merged-flash.bin --flash_mode dio --flash_size 4MB 0x1000 bootloader.bin 0x8000 partition-table.bin 0x10000 app.bin
    command = ['--chip', 'esp32c3'] 
    command.extend(['merge_bin', '--flash_mode', 'dio'])
    command.extend(['--format', 'hex'])
    command.extend(['-o', './Firmware/firmware.hex'])
    command.extend(['--flash_size', '4MB'])
    command.extend(['0x0000', str(sys.argv[1]) + '/.pio/build/esp32c3/bootloader.bin'])
    command.extend(['0x8000', str(sys.argv[1]) + '/.pio/build/esp32c3/partitions.bin'])
    command.extend(['0xe000', str(sys.argv[2]) + '/.platformio/packages/framework-arduinoespressif32/tools/partitions/boot_app0.bin'])
    command.extend(['0x10000', str(sys.argv[1]) + '/.pio/build/esp32c3/firmware.bin'])

    print(f'Using command {" ".join(command)}')
    esptool.main(command)
    # shutil.copy2(str(sys.argv[1]) + '/.pio/build/esp32c3/bootloader.bin', './Firmware/bootloader.bin')
    # shutil.copy2(str(sys.argv[1]) + '/.pio/build/esp32c3/partitions.bin', './Firmware/partitions.bin')
    # shutil.copy2(str(sys.argv[2]) + '/.platformio/packages/framework-arduinoespressif32/tools/partitions/boot_app0.bin', './Firmware/boot_app0.bin')
    # shutil.copy2(str(sys.argv[1]) + '/.pio/build/esp32c3/firmware.bin', './Firmware/firmware.bin')
else:
    print("Error: 2 arguments required")
    print("cpFirmware [firmware Source] [platformio source]")
