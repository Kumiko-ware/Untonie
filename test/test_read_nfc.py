import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

save_data = "Hello NFC"

try:
    print("Put tag!")
    id,text = reader.read()
    print(id)
    print(text)
finally:
    GPIO.cleanup()
    
