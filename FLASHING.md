# Flashing
## Get USB to WSL 
- Install USBIPD-WIN (Windows):
- Attach Device (Admin PowerShell):
-- usbipd list (Find your device and note the BUSID).
-- usbipd bind --busid <busid> (Share the device).
-- usbipd attach --wsl --busid <busid> (Connect to WSL)
## Get Firmware
https://micropython.org/download/ESP32_GENERIC_S3/

## Flash
- esptool.py erase_flash
- esptool.py --baud 460800 write_flash 0 ESP32_BOARD_NAME-DATE-VERSION.bin
- Repeat USB bind and attach
