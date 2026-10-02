from Gpio import Gpio

class Command:
    def __init__(self, gpio: Gpio, channels: list):
        self._gpio = gpio
        self._channel = channels[0]

    def execute(self):
        self._gpio.off(self._channel)
        return "でんきをけしたよ！"