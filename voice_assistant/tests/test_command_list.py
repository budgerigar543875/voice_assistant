from command import CommandFactory, CommandList
from pathlib import Path

class GpioFake:
    def __init__(self):
        pass

    def on(self, channel: int):
        pass

    def off(self, channel: int):
        pass

def test_command_list():
    DIR = Path(__file__).resolve().parent

    gpio_fake = GpioFake()
    factory = CommandFactory(gpio_fake)

    cmds = CommandList(f"{DIR}/test_command_map.json", factory)

    assert cmds.execute("おはよう") == "おはようございます！"
    assert cmds.execute("でんきけして") == "でんきをけしたよ！"
    assert cmds.execute("てすと") == "'てすと'わみとうろくのコマンドだよ！"

    assert cmds.execute("あ、でんきけしてね") == "でんきをけしたよ！"
