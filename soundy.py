import glob
import yaml
from RPi import GPIO
from mfrc522 import SimpleMFRC522
import RPi_I2C_driver
import time
import os

#mpg123 -q -R --fifo /tmp/player.pipe > /tmp/player.out

display = RPi_I2C_driver.lcd()

display.lcd_display_string_pos("Antony 0.0.0.1",1,0)

# mpg123 -R  --fifo /tmp/player.pipe &
def play(filename):
    player = open("/tmp/player.pipe","w")
    player.write("load " + filename + "\n")
    player.close
    print("PLAY " + filename)
    
    display.lcd_display_string_pos(filename,1,0)

def stop():
    player = open("/tmp/player.pipe","w")
    player.write("pause\n")
    player.close
    display.lcd_display_string_pos("STOP!",1,0)

def set_vol(volume):
    player = open("/tmp/player.pipe","w")
    player.write("V " + str(volume) + "\n")
    player.close
    print("VOL: " + str(volume))
    
clk_pin = 27
dir_pin = 17
tap_pin = 4
nxt_pin = 16
prv_pin = 12

encoder_out = 0


def encoder_clk(pin):
    global encoder_out
    clk_st = GPIO.input(clk_pin)
    dir_st = GPIO.input(dir_pin)
    if dir_st != clk_st:
        encoder_out = 1
    else:
        encoder_out = -1
    
GPIO.setmode(GPIO.BCM)
GPIO.setup(clk_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dir_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(tap_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(nxt_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(prv_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(clk_pin, GPIO.BOTH, callback=encoder_clk)

card_reader = SimpleMFRC522()
def read_card_id():
    id = card_reader.read_id_no_block()
    return id
        
curr_id = 0
curr_track = 0
curr_vol = 50


#init rotary encoder variables
tap_last = GPIO.input(tap_pin)
nxt_last = GPIO.input(tap_pin)
prv_last = GPIO.input(tap_pin)

yaml_db = open('db.yaml','r')
title_db = yaml.safe_load(yaml_db);

player_out = open("/tmp/player.out","r")
os.set_blocking(player_out.fileno(), False)

try:
    while True:
        # Check if we finished the track
        try:
            feedback = player_out.read()
        except:
            pass
        else:
            if curr_id != 0 :
                if "@P 0" in feedback:
                    curr_track += 1
                    curr_track %= tracks_cnt
                    play(tracks[curr_track])

        # Read card
        card_id = read_card_id()
        if (card_id is not None):
            if (card_id != curr_id):
                curr_id = card_id
                curr_track = 0
                tracks = sorted(glob.glob("Soundy/" + title_db[curr_id] + "/*.mp3"))
                tracks_cnt = len(tracks)
                play(tracks[curr_track])
        else:
            pass
            #stop()

        # Read wheel command
        if (encoder_out != 0):
            curr_vol += encoder_out * 5
            if curr_vol < 0 :
                curr_vol = 0
            if curr_vol > 100:
                curr_vol = 100
            set_vol(curr_vol)
            encoder_out = 0

        # Read simple buttons
        tap_st = GPIO.input(tap_pin)
        nxt_st = GPIO.input(nxt_pin)
        prv_st = GPIO.input(prv_pin)
        if (tap_st == 0 and tap_last == 1):
            stop()
        if (nxt_st == 0 and nxt_last == 1 and curr_id != 0):
            curr_track += 1
            curr_track %= tracks_cnt
            play(tracks[curr_track])
        if (prv_st == 0 and prv_last == 1 and curr_id != 0):
            curr_track -= 1
            if curr_track < 0:
                curr_track = tracks_cnt - 1
            play(tracks[curr_track])

        tap_last = tap_st
        nxt_last = nxt_st
        prv_last = prv_st
        time.sleep(0.05)
finally:
    GPIO.cleanup()
