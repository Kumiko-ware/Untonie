from subprocess import Popen, PIPE
import time


process = Popen(['mpg123','-R'],stdin=PIPE,stdout=PIPE,stderr=PIPE)
process.communicate(b"load soundy/20gran~1/01manu~1.mp3\n")
print("#.#")
#print(process.stdout.read())
print("#.#")
time.sleep(2)
print(process.communicate(b"pause\n"))
print("#.#")
sleep(1)
print(process.communicate(b" \n"))
print("#.#")
sleep(1)
print(process.communicate(b" \n"))
print("#.#")
sleep(1)
print(process.communicate(b" \n"))
print("#.#")
sleep(1)
print(process.communicate(b" \n"))
print("#.#")
sleep(1)
print(process.communicate(b" \n"))
print("#.#")
sleep(1)
print(process.communicate(b" \n"))
print("#.#")
sleep(1)


