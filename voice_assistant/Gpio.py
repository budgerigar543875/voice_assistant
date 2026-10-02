import RPi.GPIO as GPIO
from enum import IntEnum
import json

class Gpio:
    class Direction(IntEnum):
        OUT = GPIO.OUT
        IN = GPIO.IN

    class OutputValue(IntEnum):
        HIGH = GPIO.HIGH
        LOW = GPIO.LOW

    def __init__(self, file_path: str):
        with open(file_path, "r", encoding="utf-8") as f:
            conf = json.load(f)
        mode = GPIO.BCM if conf["mode"] == "bcm" else GPIO.BOARD
        self._out_channels = conf["channels"]["out"]
        self._in_channels = conf["channels"]["in"]

        GPIO.setmode(mode)
        for channel in self._out_channels:
            GPIO.setup(channel, self.Direction.OUT)
            self.off(channel)
        for channel in self._in_channels:
            GPIO.setup(channel, self.Direction.IN, GPIO.PUD_OFF)

    def input(self, channel: int) -> bool:
        return GPIO.input(channel)

    def output(self, channel: int, value: OutputValue) -> None:
        GPIO.output(channel, value)

    def on(self, channel: int) -> None:
        self.output(channel, self.OutputValue.HIGH)

    def off(self, channel: int) -> None:
        self.output(channel, self.OutputValue.LOW)

    def cleanup(self) -> None:
        GPIO.cleanup()
