from RPi import GPIO
from time import sleep

clk_pin = 17
dir_pin = 18
tap_pin = 27

def edge(pin):
    print("Edge detected")
    print(pin)
    clk_st = GPIO.input(clk_pin)
    dir_st = GPIO.input(dir_pin)
    
    
    if dir_st != clk_st:
        print("UP!")
    else:
        print("DOWN!")


    
GPIO.setmode(GPIO.BCM)
GPIO.setup(clk_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dir_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(tap_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(clk_pin, GPIO.BOTH, callback=edge)

try:
    counter = 100
    clk_last = GPIO.input(clk_pin)
    tap_last = GPIO.input(tap_pin);
    while True:
        clk_st = GPIO.input(clk_pin)
        dir_st = GPIO.input(dir_pin)
        tap_st = GPIO.input(tap_pin)

        if clk_st != clk_last:
            if dir_st != clk_st:
                counter+=1
            else:
                counter-=1
            print(counter)    
            clk_last = clk_st
        if tap_st != tap_last:
            tap_last = tap_st
            print(tap_st)
        sleep(0.01)
finally:
    GPIO.cleanup()
