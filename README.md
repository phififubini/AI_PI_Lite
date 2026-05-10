Flashing:
 Windows PowerShell:
  usbipd list
   usbipd bind --busid #-#
   usbipd attach --wsl --busid #-#
WSL 
 esptool.py erase_flash
 esptool.py --baud 460800 write_flash 0 ESP32_GENERIC_S3-20260406-v1.28.0.bin 

WPS: usbipd attach --wsl --busid #-# 
WSL: lsusb -> Bus 001 Device 006: ID 303a:1001 Espressif USB JTAG/serial debug unit



Updates:

# aipi_lite.py
- beep function
+ draw pixels
+ options for line spacing and overflow
- hold commands

# aipi_lite_ui.py
+ command functions w/ text def
gett attr from master
