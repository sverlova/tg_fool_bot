from fool_bot import interface
from time import sleep

interface.authorize()

while True:
    interface.handle_updates()
    sleep(1)
