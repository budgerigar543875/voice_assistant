from unittest.mock import Mock
from commands.light_off import Command

def test_light_off():
    gpio = Mock()
    cmd = Command(gpio, [123])
    result = cmd.execute()

    gpio.off.assert_called_once_with(123)
    assert result == "でんきをけしたよ！"