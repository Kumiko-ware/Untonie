import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

save_data = "Hello NFC"

try:
    print("Put tag!")
    id = reader.read_id_no_block()
    print(id)
finally:
    GPIO.cleanup()
    
