from unittest.mock import Mock
from commands.light_on import Command

def test_light_on():
    gpio = Mock()
    cmd = Command(gpio, [357, 246])
    result = cmd.execute()
    
    gpio.on.assert_called_once_with(357)
    assert result == "でんきをつけたよ！"