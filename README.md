
 Windows PowerShell:
  usbipd list
   usbipd bind --busid #-#
   usbipd attach --wsl --busid #-#
WSL 
 esptool.py erase_flash
 esptool.py --baud 460800 write_flash 0 ESP32_GENERIC_S3-20260406-v1.28.0.bin 

WPS: usbipd attach --wsl --busid #-# 
WSL: lsusb -> Bus 001 Device 006: ID 303a:1001 Espressif USB JTAG/serial debug unit


# Class AiPiLite
## Pins
### Basic IO
- L = 1       #Left button
- R = 42      #Right button
- PWR = 10    # Power enable
- LED = 46    # Status LED
### Display IO
- BLI = 3     # Backlight PWM
- CS = 15     # Chip select
- DC = 7      # Data command
- RST = 18    # Reset
- SCK = 16    # SPI Clock
- MOSI = 17   # SPI Data
### Display Constants
- SPI_BAUD = 20000000
- BL_FREQ = 10000
- TEXT_MARGIN = 20
- X = 128
- Y = 128
### Audio IO
- SCL = 4     # I2C Master Clock
- SDA = 5     # I2C Data
- MCLK = 6    # I2S Master clock
- AMP = 9     # Amplifier enable
- BCLK = 14   # Bit clock SCK
- LRCLK = 12  # Word clock WS
- DOUT = 11   # Serial Data out SD
- DIN = 13    # Serial Data in
### Audio Constants
- SAMPLE_RATE = 16000
- BUFFER_SIZE = 1024
- MASTER_FREQ_HZ = SAMPLE_RATE*256 
- MASTER_DUTY = 32768
### Adjustable Config
- VOLUME = 70
- BL_DUTY = 32768
- WELCOME = "WELCOME  DUSTI"

## Functions
- print_text(input_string, color, size, index, nowrap, center)
- draw_char(pos, input_char, color, size, center)
- draw_pixel(pos, color)
- clean_screen(color)
- play_sound(buffer)
- light_off()


### Add
- set_light(color, brightness):
- record_sound(buffer)
- record_file(filename)
- play_file(filename)
- beep()
- shutdown()
- settings file
- settings update method

# Class AiPiLiteUI
## Constants
- LINEMAX = 6

## Variables
- _cursor_draw_index: int
- _cursor_data_index: int
- _line_draw_index: int
- _page_index: int
- _up_page_index: int

## Functions
- run_command(command)
- draw_lines()
- draw_page()
- load_page()
- select_page()
- up_page()
- draw_cursor()
- draw_pixels()
- inc_cursor()

### Add
- run_functions_from_master()
- popup(input_string)
- settings menu
- run local function

# One Off Functions
moon phase module
paranormal module
amplitude modulation of hall effect or capacitive value
