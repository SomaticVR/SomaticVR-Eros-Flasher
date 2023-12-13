import serial.tools.list_ports as port_list
import serial
import sys

if (len(sys.argv) > 2):
    ssid = str(sys.argv[1])
    passwd = str(sys.argv[2])

    ports = list(port_list.grep("303A:1001"))
    print(ports[0].device)
    if ports:
        with serial.Serial(ports[0].device, 9600, timeout=1) as ser:
            # ser.baudrate = 9600
            # ser.port = ports[0]
            # ser.open()
            print (f"connecting to {ser.name}")
            if (ser.write(f'SET WIFI "{ssid}"" "{passwd}"'.encode('utf-8')) > 0):
                ser.read_until(expected="CMD SET WIFI OK:")
                print("WiFi information updated")
else:
    print("Error: 2 arguments required")
    print(f"{sys.argv[0]} [ssid] [passwd]")