import tkinter as tk
from tkinter import filedialog, ttk
import esptool
import requests
import os
import sys
import threading
import serial.tools.list_ports
import re

class TextRedirector(object):
    def __init__(self, widget, rootwin):
        self.widget = widget
        self.rootwin = rootwin

    def write(self, string):
        value = re.findall("\(([0-9]*) \%\)", string)
        #print(value)
        # self.widget["value"] = value
        if value:
            # self.widget.insert("end", int(value[0]))
            self.widget["value"] = int(value[0])
        # self.widget.configure(state="disabled")
        self.rootwin.update_idletasks()

    def flush(self):
        pass

class SomaticErosFirmwareUpdater:
    def __init__(self, root):
        self.root = root
        self.root.geometry("640x480")
        self.root.title("Somatic Eros Firmware Update")

        self.label = tk.Label(root, text="Please plug in your tracker and hold down the button while flashing.")
        self.label.pack(pady=10)

        # self.file_path_var = tk.StringVar()
        # self.entry = tk.Entry(root, textvariable=self.file_path_var, state="readonly", width=50)
        # self.entry.pack(pady=10)

        self.browse_button = tk.Button(root, text="Browse", command=self.browse_file)
        self.browse_button.pack(pady=10)

        self.status_bar = tk.Label(root, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.v_scrollbar = tk.Scrollbar(root, orient='vertical')
        # self.v_scrollbar.pack(side=tk.RIGHT, fill='none')
        # self.text_output = tk.Text(root, height=5, width=40)#, yscrollcommand=self.v_scrollbar.set)
        # self.text_output.pack(side=tk.BOTTOM)

        # self.download_progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.update_progress = ttk.Progressbar(root, orient="horizontal", length=300, maximum = 100, mode="determinate")
        self.update_progress.pack(side=tk.BOTTOM, fill=tk.X)
        sys.stdout = TextRedirector(self.update_progress, root)

        self.update_button = tk.Button(root, text="Update Firmware", command=self.open_port_window, state=tk.DISABLED)
        self.update_button.pack(pady=10)

        # Download firmware file from the new URL
        firmware_url = "https://github.com/SomaticVR/SomaticVR-Eros-Flasher/raw/main/Firmware/firmware.hex"
        self.firmware_file = "firmware.hex"  # Specify the local file name

        download_thread = threading.Thread(target=self.download_firmware, args=(firmware_url, self.firmware_file))
        download_thread.start()

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Firmware Files", "*.bin, *.hex")])
        if file_path is not None:
            self.firmware_file = file_path

    def open_port_window(self):
        # Get a list of serial ports that match the specified criteria
        port_list = [port.device for port in serial.tools.list_ports.comports() if "303A:1001" in port.hwid]
        if (len(port_list) == 1):
            self.update_firmware(port_list[0])
        elif (len(port_list) > 1):
            port_window = tk.Toplevel(self.root)
            port_window.title("Select Serial Port")

            port_label = tk.Label(port_window, text="Select Serial Port:")
            port_label.pack(pady=10)


            port_var = tk.StringVar(value=port_list)

            port_menu = tk.OptionMenu(port_window, port_var, *port_list)
            port_menu.pack(pady=10)

            confirm_button = tk.Button(port_window, text="Confirm", command= self.update_firmware(port_var.get(), port_window))#lambda port_var, port_window: threading.Thread(target = self.update_firmware, args = (port_var.get(), port_window)).start())
            confirm_button.pack(pady=10)
        else:
            pass

    def download_firmware(self, firmware_url, firmware_file):
        try:
            response = requests.get(firmware_url, stream=True)
            total_size = int(response.headers.get('content-length', 0))

            # self.download_progress.pack(pady=10)
            self.root.update_idletasks()

            with open(firmware_file, 'wb') as file:
                for data in response.iter_content(chunk_size=1024):
                    file.write(data)
                    # self.download_progress["value"] += len(data)
                    self.root.update_idletasks()

            self.update_status("Firmware downloaded successfully!")
            self.update_progress["value"] = 0  # Reset progress bar for the next update

            # Enable the "Update Firmware" button
            self.update_button["state"] = tk.NORMAL

        except requests.exceptions.RequestException as e:
            self.update_status(f"Failed to download firmware: {e}")

    def update_firmware(self, selected_port, port_window = None):
        self.update_progress["value"] = 0  # Reset progress bar for the next update
        if not self.firmware_file:
            self.update_status("Please select a firmware file.")
            return

        # If no port is selected, use the first port in the list
        if not selected_port:
            port_list = [port.device for port in serial.tools.list_ports.comports() if "303A:1001" in port.hwid]
            if port_list:
                selected_port = port_list[0]
            else:
                self.update_status("No suitable serial ports found.")
                return

        if port_window is not None:
            port_window.destroy()  # Close the port selection window
        self.update_status("Firmware update started... Please wait")
        try:
            # Run esptool to flash the firmware
            command = ['--chip', 'esp32c3', '--port', selected_port, '--baud', '460800'] 
            command.extend(['--before', 'default_reset', '--after', 'hard_reset', 'write_flash', '-z', '--flash_mode', 'dio'])
            command.extend(['--flash_freq', '80m', '--flash_size', '4MB'])
            # command.extend(['0x0000', './Firmware/bootloader.bin'])
            # command.extend(['0x8000', './Firmware/partitions.bin'])
            # command.extend(['0xe000', './Firmware/boot_app0.bin'])
            # command.extend(['0x10000', firmware_file])
            command.extend(['0x0000', self.firmware_file])


            print(f'Using command {" ".join(command)}')
            esptool.main(command)

            self.update_status("Firmware updated successfully!")

        except Exception as e:
            self.update_status(f"Firmware update failed: {e}")

        self.root.update_idletasks()

    def set_update_progress(self, position, total):
        # For esptool.write_flash, position is the number of bytes written, and total is the total size
        self.update_progress["value"] = position
        self.update_progress["maximum"] = total
        self.root.update_idletasks()

    def update_status(self, message):
        self.status_bar["text"] = message

if __name__ == "__main__":
    root = tk.Tk()
    app = SomaticErosFirmwareUpdater(root)
    root.mainloop()
