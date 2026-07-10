import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

save_data = "Hello NFC"

try:
    reader.write(save_data)
    print("Data written")
finally:
    GPIO.cleanup()
    
