import utime
from machine import SoftI2C, Pin
from mpu6886 import MPU6886
from neopixel import NeoPixel

i2c = SoftI2C(scl=Pin(21), sda=Pin(25))
sensor = MPU6886(i2c)

gpio27 = Pin(27, Pin.OUT)
neopixels = NeoPixel(gpio27, 25)

class Font:

    def __init__(self):
        self.blocks = {'A': b'\x1e\x05\x05\x1e', 'B': b'\x1f\x15\x15\x0a',
                       'A90': b'\x06\x09\x0f\x09\x09'
                      }

    def bit_blit(self, char, pixels,
                     destination_x, destination_y, destination_w, destination_h,
                     foreground_color, background_color,
                     pindexFunc = lambda x,y,destination_w : y + destination_w * x):
        block = self.blocks[char]
        for source_x in range(len(block)):
            x = source_x + destination_x
            if x >= 0 and x < destination_w:
                column = block[source_x]
                for source_y in range(5):
                    y = source_y + destination_y
                    if y >= 0 and y < destination_h:
                        pixel_index = pindexFunc(x,y,destination_w)
                        row_mask = 1 << source_y
                        pixels[pixel_index] = foreground_color if column & row_mask > 0 else background_color


    def showChar(self, char, neoPixels, angle=0, color=(20,20,20)):
        background = (0,0,0)
        for pixel_index in range(25):
            neoPixels[pixel_index] = background

        if angle == 0:
            self.bit_blit(char,neoPixels,0,0,5,5,color,background)
        elif angle == 90: 
            self.bit_blit(char+'90',neoPixels,0,0,5,5,color,background)
        elif angle == 180: 
            self.bit_blit(char,neoPixels,0,0,5,5,color,background,
                          lambda x,y,destination_w : y + destination_w * (destination_w - x - 1))
        elif angle == 270:
            self.bit_blit(char+'90',neoPixels,0,0,5,5,color,background,
                          lambda x,y,destination_w : y + destination_w * (destination_w - x - 1))

        neoPixels.write()


font = Font();

while True:
    # print(sensor.acceleration)
    (x,y,z) = sensor.acceleration
    print(y)
    if y > 9:
        font.showChar('A', neopixels, 90)
    elif y > -4:
        font.showChar('A', neopixels, 0)
    else:
        font.showChar('A', neopixels, 270)

    utime.sleep_ms(500)
