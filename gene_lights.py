
import time
from neopixel import *
import argparse
import signal
import sys
import random


def signal_handler(signal, frame):
    colorWipe(strip, Color(0,0,0))
    sys.exit(0)

#LED strip configuration:
LED_COUNT   =300   #Number of LED pixels.
LED_PIN   = 18 #GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN   =10   #GPIO pin connectred to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000   #LED signal frquency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
#LED_BRIGHTNESS = 25   #Set to 0 for darkest and 255 for brightness
LED_INVERT = False  #True to invert the signal (when using NPN transistor level shift
LED_CHANNEL = 0     #set to 1 for GPIOs 13, 19, 41, 45 
LED_STRIP  = ws.WS2811_STRIP_GRB  # Strip type and color ordering


# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=2):
        """Wipe color across display a pixel at a time."""
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, color)
            strip.show()
            time.sleep(wait_ms/1000.0)


def set_brightness(nucleotide, bright_val):
#Set nucleotide brightness of each
    red = Color(bright_val, 0 ,0)
    blue = Color(0, bright_val, bright_val)
    green = Color(0, bright_val, 0)
    yellow = Color(bright_val, bright_val,0)
    if str(nucleotide).upper() == 'A':
        return blue
    elif str(nucleotide).upper() == 'C':
        return yellow
    elif str(nucleotide).upper() == 'G':
        return green
    elif str(nucleotide).upper() =='T':
        return red

def nucleotide_tails(seq_list,bright_val, fade_val,nucleotide,nuc_dict,args):
# Create a trailing tail
    bright_diminish=.7
    red = Color(bright_val, 0 ,0)
    blue = Color(0, bright_val, bright_val)
    green = Color(0, bright_val, 0)
    yellow = Color(bright_val, bright_val,0)
    for x in range(int(args.l)):     #REPLACED length)
        nuc_dict[str(nucleotide+'_nuc')] = set_brightness(nucleotide,bright_val)
        seq_list.insert(0,nuc_dict[str(nucleotide+'_nuc')])
        seq_list=seq_list[:-1]
        nuc_chase_delay(args, strip, seq_list)  #   separation)    trying argugment instead of sep
        bright_val = int(bright_val* bright_diminish)
    for x in range(args.s):  #separation):
        seq_list.insert(0, Color(0,0,0))
        seq_list = seq_list[:-1]
        nuc_chase_delay(args,strip, seq_list)
    return seq_list



    
def nuc_chase_delay(args,strip, seq_list):
    wait_ms=20
    counter=255
    for i in range(0, strip.numPixels()):
        strip.setPixelColor(i, seq_list[i])
        counter +=1
    strip.show()
    time.sleep(int(args.d)/1000.0)    # Delav



if __name__ == '__main__':
    #Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', action='store_true', help='clear the display on exit')
    parser.add_argument('-f', required=False, help='file name of gene', default='RUNX1.fa')
    parser.add_argument('-l', required=False, help='length of LED light', default=7, type=int)
    parser.add_argument('-s', required=False, help='separation', default=4, type=int)
    parser.add_argument('-d', required=False, help='Delay/speed', default=20, type=int)
    args = parser.parse_args()
    if args.c:
        signal.signal(signal.SIGINT, signal_handler)
    
    print 'input_file: {}'.format(args.f)
    DNA_list=['A','a','T','t','G','g','C','c']
    LED_BRIGHTNESS=255
    #Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    seq_list = []
    length=9         #length of each light
    separation=400     #distance between each light
    strip.begin()
    bright_val=255
    red = Color(bright_val, 0 ,0)
    blue = Color(0, bright_val, bright_val)
    green = Color(0, bright_val, 0)
    yellow = Color(bright_val, bright_val,0)
    comet_tailed_list=[]
    
    nuc_dict={'T_nuc': red, #Color(255,255,0),
          'A_nuc' : blue, #Color(0,0,255),
          'G_nuc' : green, #Color(0,255,0),
          'C_nuc' : yellow, #Color(0,0,0),
           }

#Populate seq_list, make to size of LED_COUNT
    for x in range(0, LED_COUNT):       #Create a blank canvas
        seq_list.append(Color(0,1,1))
        
    with open(str(args.f), 'rb') as f:
        while True:
            sequence = f.readline()
            if sequence[0]=='>':
                print sequence
            else:
                for nucleotide in sequence:
                   if nucleotide in DNA_list:
                      fade_val=bright_val/int(args.l)  #length
                      seq_list=nucleotide_tails(seq_list,bright_val, fade_val,nucleotide,nuc_dict,args)
                   else:
                       pass
