"""
"""
import time, math, struct, gc
from machine import Pin
import neopixel
from aipi_lite import AiPiLite
from aipi_lite_ui import AiPiLiteUI

def dummy(self):
    print("Bound to the dummy")

def generate():
    sample_rate = 16000
    frequency = 440 # A4 note
    samples = 10000
    buffer = bytearray(samples * 4) # 2 bytes per sample, 2 channels
    for i in range(samples):
        value = int(math.sin(2 * math.pi * frequency * i / sample_rate) * 10000)
        # Struct pack to create stereo (left+right same value)
        struct.pack_into('<hh', buffer, i * 4, value, value)
    return buffer


def test_main():
    """Run the TFT print test sequence."""
    master = AiPiLite()
    x = 0
    while True:
        time.sleep(2)
        x += 1
        if x ==1:
            ui = AiPiLiteUI(master,"./home.json")
        if x == 5:
            gc.collect()
            print("Allocated:", gc.mem_alloc(), "bytes")
            print("Free:", gc.mem_free(), "bytes")

test_main()



