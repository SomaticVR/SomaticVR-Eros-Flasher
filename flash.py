import serial.tools.list_ports as port_list
import serial
import esptool
# import wait_key.wait_key as wait_key
def wait_key():
    input("Press <ENTER> to continue")

def flash(port):
    command = ['--chip', 'esp32c3', '--port', port.device, '--baud', '460800'] 
    command.extend(['--before', 'default_reset', '--after', 'hard_reset', 'write_flash', '-z', '--flash_mode', 'dio'])
    command.extend(['--flash_freq', '80m', '--flash_size', '4MB'])
    command.extend(['0x0000', './Firmware/bootloader.bin'])
    command.extend(['0x8000', './Firmware/partitions.bin'])
    command.extend(['0xe000', './Firmware/boot_app0.bin'])
    command.extend(['0x10000', './Firmware/firmware.bin'])

    print(f'Using command {" ".join(command)}')
    esptool.main(command)

def sendCommand(port, command, expected, timeout=1):
    with serial.Serial(port.device, 9600, timeout=timeout) as ser:
        print (f"connecting to {ser.name} and sending command {command}")
        if (ser.write((command + "\n").encode('utf-8')) > 0):
            ser.read_until(expected=expected)

def setWifi(port, ssid, passwd):
    sendCommand(port, f'SET WIFI "{ssid}" "{passwd}"', "CMD SET WIFI OK:")
    print("WiFi information updated")

def factoryReset(port):
    sendCommand(port, "FRST", "FACTORY RESET")
    print("Factory Reset Completed. Device will shut down unless charging.")

if (len(sys.argv) > 2):
    ssid = str(sys.argv[1])
    passwd = str(sys.argv[2])

    while True:
        ports = list(port_list.grep("303A:1001"))
        if ports:
            flash(ports[0])
            wait_key()
            setWifi(ports[0], ssid, passwd)
            wait_key()
            # factoryReset(ports[0])
            # wait_key()
else:
    print("Error: 2 arguments required")
    print(f"{sys.argv[0]} [ssid] [passwd]")
