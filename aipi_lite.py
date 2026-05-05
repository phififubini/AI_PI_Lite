'''


'''
from machine import Pin, PWM, SPI, SoftI2C, I2S, Timer
from neopixel import NeoPixel
from time import sleep_ms
from lib.ST7735 import TFT
from lib.ES8311 import ES8311
from lib.sysfont import sysfont
class AiPiLite:
    '''

    '''
    # Basic IO
    L = 1       #Left button
    R = 42      #Right button
    PWR = 10    # Power enable
    LED = 46    # Status LED
    HOLD_TIME_MS = 1000
    # Display IO
    BLI = 3     # Backlight PWM
    BLE = 3     # Backlight enable
    CS = 15     # Chip select
    DC = 7      # Data command
    RST = 18    # Reset
    SCK = 16    # SPI Clock
    MOSI = 17   # SPI Data
    # Display Config
    COLORS = {
        "BLACK": 0,
        "RED": 31,
        "GREEN": 2016,
        "BLUE": 63488,
        "WHITE": 65535
        }
    SPI_BAUD = 20000000
    BL_FREQ = 10000
    BL_DUTY = 32768
    WELCOME = "WELCOME  DUSTI"
    TEXT_MARGIN = 20
    X = 128
    Y = 128
    # Audio IO
    SCL = 4     # I2C Master Clock
    SDA = 5     # I2C Data
    MCLK = 6    # I2S Master clock
    AMP = 9     # Amplifier enable
    BCLK = 14   # Bit clock SCK
    LRCLK = 12  # Word clock WS
    DOUT = 11   # Serial Data out SD
    DIN = 13    # Serial Data in
    # Audio Config
    SAMPLE_RATE = 16000
    BUFFER_SIZE = 1024
    MASTER_FREQ_HZ = SAMPLE_RATE*256 
    MASTER_DUTY = 32768      # 50% duty cycle for 16-bit resolution (65535 / 2)
    VOLUME = 70
    # Pins
    _left: Pin
    _left_hold: bool
    _left_timer: Timer
    _right: Pin
    _right_hold: bool
    _right_timer: Timer
    _pwr: Pin
    _bli: PWM
    _ble: Pin
    _led: NeoPixel
    _mclk: PWM
    _amp: Pin
    _tft: TFT
    _audio_out: I2S
    _audio_in: I2S

    def __init__(self):
        self._left = Pin(self.L, Pin.IN,Pin.PULL_UP)
        self._left_hold = False
        self._left_timer = Timer(1)
        self._left.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self.left_click)
        self._right = Pin(self.R, Pin.IN,Pin.PULL_UP)
        self._right_hold = False
        self._right_timer = Timer(2)
        self._right.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self.right_click)
        self._led = NeoPixel(Pin(self.LED, Pin.OUT), 1)
        self._led[0] = [64,32,16]
        self._led.write()
        self._pwr = Pin(self.PWR, Pin.OUT)
        self._pwr.on()
        self.init_TFT()
        self.init_audio()

    def init_TFT(self):
        self._ble = Pin(self.BLE, Pin.OUT)
        self._ble.off()
        self._bli = PWM(Pin(self.BLI), freq=self.BL_FREQ)
        self._bli.duty_u16(self.BL_DUTY)
        spi=SPI(1, self.SPI_BAUD, polarity=0, phase=0, sck=Pin(self.SCK), mosi=Pin(self.MOSI), miso=None)
        self._tft = TFT(spi, self.DC, self.RST, self.CS, (self.X, self.Y))
        self._tft.initr()
        self._tft.rotation(1)
        self._tft.rgb(True)
        self._tft.fill(TFT.BLACK)
        self._tft.text((30,50), self.WELCOME, TFT.WHITE, sysfont, 2, nowrap=False)
        sleep_ms(100)
        self._ble.on()
        print("TFT Config")

    def init_audio(self):
        self._amp = Pin(self.AMP, Pin.OUT)
        self._amp.off()
        self._mclk = PWM(Pin(self.MCLK), freq=self.MASTER_FREQ_HZ, duty_u16=self.MASTER_DUTY)
        i2c = SoftI2C(scl=Pin(self.SCL), sda=Pin(self.SDA))
        codec = ES8311(i2c)
        codec.init_es8311()
        codec.set_dac_volume(self.VOLUME)
        self._audio_out = I2S(0,
                sck = Pin(self.BCLK),
                ws = Pin(self.LRCLK),
                sd = Pin(self.DOUT),
                mode = I2S.TX,
                bits = 16,
                format = I2S.MONO,
                rate = self.SAMPLE_RATE,
                ibuf = self.BUFFER_SIZE
                )
        self._audio_out.irq(self.end_play)
        self._audio_in = I2S(1,
                sck = Pin(self.BCLK),
                ws = Pin(self.LRCLK),
                sd = Pin(self.DIN),
                mode = I2S.RX,
                bits = 16,
                format = I2S.MONO,
                rate = self.SAMPLE_RATE,
                ibuf = self.BUFFER_SIZE
                )
        self._audio_in.irq(self.end_record)
    
    def print_text(self, input_string: str, color: str, size: int, index: int, nowrap: bool = True, center: int = 0):
        if color in self.COLORS:
            color_ref = self.COLORS[color]
        else:
            color_ref = TFT.WHITE
        y_pos = (self.TEXT_MARGIN/2 + self.TEXT_MARGIN * index) + (2-size)/4 * self.TEXT_MARGIN * center
        self._tft.text((self.TEXT_MARGIN / 2, y_pos), input_string, color_ref, sysfont, size, nowrap)

    def draw_char(self, pos: tuple, input_char: str, color: str, size: int, center: int = 0):
        if color in self.COLORS:
            color_ref = self.COLORS[color]
        else:
            color_ref =  TFT.WHITE
        x = self.TEXT_MARGIN/2 + self.TEXT_MARGIN * pos[0] + (2-size)/4 * self.TEXT_MARGIN * center
        y = self.TEXT_MARGIN/2 + self.TEXT_MARGIN * pos[1] + (2-size)/4 * self.TEXT_MARGIN * center
        new_pos = (x,y )
        self._tft.char(new_pos, input_char, color_ref, sysfont, (size, size))

    def draw_pixel(self, pos: tuple, color: str):
        if color in self.COLORS:
            color_ref = self.COLORS[color]
        else:
            color_ref =  TFT.WHITE
        self._tft.pixel(pos,color_ref)

    def clean_screen(self, color: str = "BLACK"):
        if color in self.COLORS:
            color_ref = self.COLORS[color]
        else:
            color_ref = TFT.BLACK
        self._tft.fill(color_ref)
        sleep_ms(50)
        
    def play_sound(self, buffer: bytearray):
        self._amp.on()
        self._audio_out.write(buffer)

    def end_play(self, pin):
        self._amp.off()
        
    def end_record(self, pin):
        return None
        
    def left_click(self, pin):
        if pin.value() == 1:
            self._left_timer.deinit()
            if not self._left_hold:
                self.send_command("LC")
        else:
            self._left_timer.init(mode=Timer.ONE_SHOT, period=self.HOLD_TIME_MS, callback=self.left_hold)
        self._left_hold = False
   
    def left_hold(self, timer):
        self._left_hold = True
        if self._right_hold:
            self.shutdown_aipi()
        self.send_command("LH")

    def right_click(self, pin):
        if pin.value() == 1:
            self._right_timer.deinit()
            if not self._right_hold:
                self.send_command("RC")
        else:
            self._right_timer.init(mode=Timer.ONE_SHOT, period=self.HOLD_TIME_MS, callback=self.right_hold)
        self._right_hold = False

    def right_hold(self, timer):
        self._right_hold = True
        if self._left_hold:
            self.shutdown_aipi()
        self.send_command("RH")
        
    def send_command(self, command: str):
        print("Unbound")
        
    def light_off(self):
        self._led[0] = [0,0,0]
        self._led.write()

    def shutdown_aipi(self):
        print("Shutdown")
        #self._pwr.off()