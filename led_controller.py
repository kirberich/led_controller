import serial
import argparse
import random

from api import Api


class Led(object):
    def __init__(self, index, red, green, blue):
        self.index = index
        self.red = red
        self.green = green
        self.blue = blue

    def __repr__(self):
        return "c%s %s %s %s" % (self.index, self.red, self.green, self.blue)


class LedController(object):
    def __init__(self, dev, num_leds):
        self.ser = serial.Serial(dev, 115200, timeout=1)
        self.api = Api(led_controller=self)

        self.leds = [Led(x, 0, 0, 0) for x in range(num_leds)]

    def loop(self):
        self.api.demonize(port=8082)
        while True:
            for event, kwargs in self.api.events:
                if event == "update":
                    self.send_message(self.make_message(self.leds), wait_for_reply=False)
                    self.send_message('s')

    def send_message(self, message, wait_for_reply=True, wait_for_empty_buffer=False):
        """ Send serial message to arduino  
            Set wait_for_reply to wait and return reply 
            wait_for_empty_buffer to continue reading until the buffer is empty
        """
        print message
        retval = []
        self.ser.write(message+"\n")
        if wait_for_reply:
            retval.append(self.ser.readline().strip())

        if wait_for_empty_buffer:
            while self.ser.inWaiting():
                retval.append(self.ser.readline().strip())

        return retval

    def make_message(self, commands):
        return "".join([str(c) for c in commands])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generic arduino-based LED controller')
    parser.add_argument('dev', type=str, help='Serial device the arduino is connected to')
    args = parser.parse_args()

    led_controller = LedController(dev=args.dev, num_leds=300)
    led_controller.loop()