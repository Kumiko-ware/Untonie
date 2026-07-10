import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

save_data = "Hello NFC"

try:
    data = input("Data to write?")
    reader.write(data)
    print("Data written")
finally:
    GPIO.cleanup()
    
