import time
import os

MESSAGE = os.getenv("MESSAGE")

count = 0
while True:
    count += 1
    message = f"{MESSAGE} - {count}"
    time.sleep(2)
    print(message)
