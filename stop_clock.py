#!/usr/bin/env python
# Send IR STOP signal when button is pressed.
# First *.mp3 file found in this directory will be played as well.
#
# Adam Spontarelli

import time, os, glob
import subprocess
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

def press_stop():
    for i in range(3):
        os.system("irsend SEND_ONCE /home/pi/lircd.conf KEY_STOP")
        time.sleep(0.1)
        
    mp3_file = glob.glob("*.mp3")[0]
    if mp3_file is not None:
        play_mp3("/home/pi/OneWayOut/"+mp3_file)
    else:
        print("Error: *.mp3 file not found.")
        return

    
def play_mp3(path):
    print("Playing: " + path)
    subprocess.Popen(['mpg123', '-q', path]).wait()
    print("Done playing")
    main()
    

def main():
    GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    try:
        GPIO.wait_for_edge(24, GPIO.FALLING)
        print("Button Pressed")
        press_stop()
    except KeyboardInterrupt:
        GPIO.cleanup()       # clean up GPIO on CTRL+C exit
    GPIO.cleanup()           # clean up GPIO on normal exit
        
if __name__ == '__main__':
    main()
