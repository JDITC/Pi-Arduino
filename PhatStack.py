#!/usr/bin/env python
# This is my first attempt, so a tad rough, but I'll tidy it up and update the repo
# All credit goes to the team at Pimoroni, all I did was bolt together their scripts and code into the PhatStack block below ;-)
import time
import math
import sys
# shortened to flp to save typing..
import fourletterphat as flp
# call is needed for the "Alarm Clock" function using aplay
from subprocess import call
import blinkt
from blinkt import set_clear_on_exit, set_pixel, show, set_brightness
from envirophat import light, weather
# shortened to save typing
import scrollphathd as sphd
from scrollphathd.fonts import font5x7

def write(line):
    sys.stdout.write(line)
    sys.stdout.flush()

# Confidence Message to check initial settings and code running
write("--- PhatStack is running! ---")

# configure the blinkt
blinkt.set_clear_on_exit()
set_brightness(0.1)
REDS = [0, 0, 0, 0, 0, 16, 64, 255, 64, 16, 0, 0, 0, 0, 0, 0]
start_time = time.time()

# pulls together the temperature, pressure and light from Enviro, then converts to a string for scrollphat
temp = str(round(weather.temperature(),2))
temp = "Temp:"+temp+"c "
press = str(round(weather.pressure()/100,2))
press = "Press:"+press+"% "
lum = str(light.light())
lum = "Light:"+lum+" "
scroller = temp+press+lum
#Set a more eye-friendly default brightness
sphd.set_brightness(0.5)
sphd.write_string(scroller, x=0, y=0, font=font5x7)

while True:
    # Sine wave, spends a little longer at min/max
    # delta = (time.time() - start_time) * 8
    # offset = int(round(((math.sin(delta) + 1) / 2) * (blinkt.NUM_PIXELS - 1)))
    # Triangle wave, a snappy ping-pong effect
    delta = (time.time() - start_time) * 16
    offset = int(abs((delta % len(REDS)) - blinkt.NUM_PIXELS))

    for i in range(blinkt.NUM_PIXELS):
        blinkt.set_pixel(i , REDS[offset + i], 0, 0)

    blinkt.show()
    # Start Four Letter Clock
    flp.clear()
    # Convert the time into a string to display on flp
    str_time = time.strftime("%H%M")
    # Set your alarms here to play Pimoroni Test Tune!
    if str_time == "1130":
       call(["aplay", "/home/pi/Pimoroni/speakerphat/test/test.wav"])
    # Display the time
    flp.print_number_str(str_time)
    # Blink the middle decimal point
    # int(time.time() % 2) will alternate 1 0 1 0
    # which we can use to directly set the point
    flp.set_decimal(1, int(time.time() % 2))

    flp.show()
    
    output = """
Temp: {t}c
Pressure: {p}Pa
Light: {c}
""".format(
        t = round(weather.temperature(),2),
        p = round(weather.pressure(),2),
        c = light.light()
    )
    
    output = output.replace("\n","\n\033[K")
    write(output)
    lines = len(output.split("\n"))
    write("\033[{}A".format(lines - 1))
    
    sphd.show()
    sphd.scroll(1)
    time.sleep(0.1)

# And hopefully it all works, but if not, please let me know
