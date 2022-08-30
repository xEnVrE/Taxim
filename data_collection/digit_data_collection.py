import time
import numpy
import cv2
from digit_interface import Digit

import sys
import select
import tty
import termios

class NonBlockingConsole(object):

    def __enter__(self):
        self.old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
        return self

    def __exit__(self, type, value, traceback):
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)


    def get_data(self):
        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            return sys.stdin.read(1)
        return False


# images = []
d = Digit("D20066") # Unique serial number
d.connect()
t0 = time.time()
i = 0
with NonBlockingConsole() as nbc:
    while True:
        time.sleep(1.0 / 30.0)

        rgb = d.get_frame()
        rgb = cv2.rotate(rgb, cv2.ROTATE_90_CLOCKWISE)

        user_input = nbc.get_data()
        if user_input == 'j':
            # images.append(rgb)
            cv2.imwrite('./images/frame_' + str(i) + '.png', rgb)
            i += 1
            print(i)
        elif user_input == 'k':
            break

        cv2.imshow('', rgb)
        cv2.waitKey(1)

d.disconnect()
