import glob
import yaml
from RPi import GPIO
from mfrc522 import SimpleMFRC522
import RPi_I2C_driver
import time
import os


GPIO.cleanup()
#mpg123 -q -R --fifo /tmp/player.pipe > /tmp/player.out
GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.OUT)
GPIO.output(6, 1)

display = RPi_I2C_driver.lcd()
big_num = [
        # Char 0 - UL
        [ 0x01, 0x07, 0x0F, 0x0F, 0x1F, 0x1F, 0x1F, 0x1F],
        # Char 1 - UR
        [ 0x18, 0x1C, 0x1E, 0x1E, 0x1F, 0x1F, 0x1F, 0x1F],
        # Char 2 - LL
        [ 0x1F, 0x1F, 0x1F, 0x1F, 0x0F, 0x0F, 0x07, 0x03],
        # Char 3 - LR
        [ 0x1F, 0x1F, 0x1F, 0x1F, 0x1E, 0x1E, 0x1C, 0x18],
        # Char 4 - UC
        [ 0x1F, 0x1F, 0x1F, 0x00, 0x00, 0x00, 0x00, 0x00],
        # Char 5 - LC
        [ 0x00, 0x00, 0x00, 0x00, 0x00, 0x1F, 0x1F, 0x1F],
        # Char 6 - UB
	[ 0x1F, 0x1F, 0x1F, 0x00, 0x00, 0x00, 0x1F, 0x1F],
        # Char 7 - LB
	[ 0x1F, 0x00, 0x00, 0x00, 0x00, 0x1F, 0x1F, 0x1F],]

display.lcd_load_custom_chars(big_num)

#symbols: 0..9, speaker, tape, percent
upper = [ "\0\4\1", "\4\1 ", "\6\6\1", "\6\6\xFF", "\0 \xFF",
          "\xFF\6\6", "\0\6\6", "\4\4\1", "\0\6\1", "\0\6\1",
          "\5\0", "\0\4\1  \0\4\1", "\xA5/"]

lower = [ "\2\5\3", "\5\xFF\5", "\xFF\7\7", "\7\7\3", "\4\4\xFF",
          "\7\7\3", "\2\5\3", "  \xFF", "\2\7\3", "\7\7\3",
          "\4\2", "\2\5\xFF\5\5\xFF\5\3", "/\xA5"]

display.lcd_clear()
#                               U       N       T       O   N       IE
display.lcd_display_string_pos("\xFF\xFF\0\1\xFF\4\xFF\4\0\1\0\1\xFFo\0\6",1,0)
#                               U   N       T     O   N       I   E
display.lcd_display_string_pos("\2\3\xFF\2\3 \xFF \2\3\xFF\2\3\xFF\2\7",2,0)

def print_song(number):
    display.lcd_clear()
    number = number+1
    display.lcd_display_string_pos(upper[number//10]+" "+upper[number%10],1,5)
    display.lcd_display_string_pos(lower[number//10]+" "+lower[number%10],2,5)

def print_vol(number):
    display.lcd_clear()
    display.lcd_display_string_pos(upper[10]+" "
                                   +upper[number//10]+" "+upper[number%10],1,3)
    display.lcd_display_string_pos(lower[10]+" "
                                   +lower[number//10]+" "+lower[number%10],2,3)

    
def name(path) :
    end_ptr=0
    for i in range(len(path)-1,0,-1) :
        if end_ptr == 0 and path[i]=="." :
            end_ptr = i
        if path[i]=="/" :
            break
    return path[i+1:end_ptr]

def break_16(msg):
    last_break = 0
    last_space = 0
    lines = []
    for i in range (0, len(msg)):
        if msg[i] == " " :
            last_space = i
        if i % 16 == 0 and i != 0:
            if last_space == last_break :
                lines.append(msg[last_break:i])
                last_break = i
            else :
                lines.append(msg[last_break:last_space])
                last_break = last_space + 1
            last_space = last_break
    if (last_break<len(msg)):
        lines.append(msg[last_break:])
    if len(lines) == 0 :
        lines.append(msg)
    return lines

def play(filename):
    player = open("/tmp/player.pipe","w")
    player.write("load " + filename + "\n")
    GPIO.output(amp_ena, 1)
    player.close
    print("PLAY " + filename)
#    lines = break_16(name(filename))
#    if len(lines) >0:
#       display.lcd_display_string_pos(lines[0],1,0)
#    if len(lines) >1:
#        display.lcd_display_string_pos(lines[1],2,0)

def stop():
    player = open("/tmp/player.pipe","w")
    player.write("pause\n")
    player.close
    GPIO.output(amp_ena, 1 - GPIO.input(amp_ena))
    #display.backlight(0)
    #display.lcd_display_string_pos("STOP!",1,0)

def set_vol(volume):
    player = open("/tmp/player.pipe","w")
    player.write("V " + str(volume) + "\n")
    player.close
    print_vol(volume)
    print("VOL: " + str(volume))
    
clk_pin = 27
dir_pin = 17
tap_pin = 4
nxt_pin = 16 
prv_pin = 19 
amp_ena = 23
bth_pin = 5
dis_ena = 6

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
GPIO.setup(bth_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(amp_ena, GPIO.OUT)
GPIO.setup(dis_ena, GPIO.OUT)

GPIO.output(amp_ena, 1)
#GPIO.output(v24_ena, 0)
GPIO.output(dis_ena, 1)
#GPIO.output(pwr_lgt, 0)
#GPIO.output(prv_lgt, 0)
#GPIO.output(nxt_lgt, 0)
#GPIO.output(bth_lgt, 0)

GPIO.add_event_detect(clk_pin, GPIO.BOTH, callback=encoder_clk)

card_reader = SimpleMFRC522()
def read_card_id():
    id = card_reader.read_id_no_block()
    return id

curr_id = 0
curr_track = 0
curr_vol = 40

#init rotary encoder variables
tap_last = GPIO.input(tap_pin)
nxt_last = GPIO.input(nxt_pin)
prv_last = GPIO.input(prv_pin)
bth_last = GPIO.input(bth_pin)

yaml_db = open('Music/db.yaml','r')
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
                    if curr_track >= tracks_cnt:
                        curr_id = 0
                        stop()
                        display.lcd_clear()
                        #                               U       N       T       O   N       IE
                        display.lcd_display_string_pos("\xFF\xFF\0\1\xFF\4\xFF\4\0\1\0\1\xFFo\0\6",1,0)
                        #                               U   N       T     O   N       I   E
                        display.lcd_display_string_pos("\2\3\xFF\2\3 \xFF \2\3\xFF\2\3\xFF\2\7",2,0)
                    else:
                        play(tracks[curr_track])
                        print_song(curr_track)

        # Read card
        card_id = read_card_id()
        if (card_id is not None):
            if (card_id != curr_id):
                curr_id = card_id
                curr_track = 0
                tracks = sorted(glob.glob("Music/" + title_db[curr_id] + "/*.mp3"))
                tracks_cnt = len(tracks)
                play(tracks[curr_track])
                print_song(curr_track)
        else:
            pass
            #stop()

        # Read wheel command
        if (encoder_out != 0 and curr_id != 0):
            curr_vol += encoder_out * 5
            if curr_vol > 99:
                curr_vol = 99
            if curr_vol == 94:
                curr_vol = 95
            if curr_vol < 0:
                curr_vol = 0
            encoder_out = 0
            set_vol(curr_vol)
 
        # Read simple buttons
        tap_st = GPIO.input(tap_pin)
        nxt_st = GPIO.input(nxt_pin)
        prv_st = GPIO.input(prv_pin)
        bth_st = GPIO.input(bth_pin)
        if (tap_st == 0 and tap_last == 1):
            stop()
        if (nxt_st == 0 and nxt_last == 1 and curr_id != 0):
            curr_track += 1
            curr_track %= tracks_cnt
            play(tracks[curr_track])
            print_song(curr_track)
        if (prv_st == 0 and prv_last == 1 and curr_id != 0):
            curr_track -= 1
            if curr_track < 0:
                curr_track = tracks_cnt - 1
            play(tracks[curr_track])
            print_song(curr_track)
        if (bth_st == 0 and bth_last == 1):
            print("BT Button")
        tap_last = tap_st
        nxt_last = nxt_st
        prv_last = prv_st
        bth_last = bth_st
        time.sleep(0.05)
finally:
    GPIO.cleanup()
