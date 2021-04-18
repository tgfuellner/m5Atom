import utime
from machine import SoftI2C, Pin
from mpu6886 import MPU6886
from neopixel import NeoPixel
from font5 import Font5

i2c = SoftI2C(scl=Pin(21), sda=Pin(25))
sensor = MPU6886(i2c)

gpio27 = Pin(27, Pin.OUT)
neopixels = NeoPixel(gpio27, 25)
font = Font5()

def showChar(char, font, neoPixels, color=(20,20,20)):
    background = (0,0,0)
    for pixel_index in range(25):
        neoPixels[pixel_index] = background

    font.bit_blit(char.upper(),neoPixels,0,0,5,5,color,background)
    neoPixels.write()


while True:
    # print(sensor.acceleration)
    (x,y,z) = sensor.acceleration
    if y > 0:
        showChar('A', font, neopixels)
    else:
        showChar('B', font, neopixels)

    utime.sleep_ms(500)
