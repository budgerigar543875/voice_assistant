from commands.what_time import Command
from datetime import datetime
import pytest

def get_datetime(hour: int, minute: int, second: int) -> datetime:
    return datetime(2026, 1, 1, hour, minute, second)

@pytest.mark.parametrize(
    "hour, min, sec, message", 
    [
        (0, 0, 0, "れいじれいふんれいびょうだよ！"),
        (4, 1, 9, "よじいっぷんきゅうびょうだよ！"),
        (7, 8, 52, "しちじはちふんごじゅうにびょうだよ！"),
        (9, 6, 6, "くじろっぷんろくびょうだよ！"),
        (10, 20, 30, "じゅうじにじゅっぷんさんじゅうびょうだよ！"),
        (22, 15, 3, "にじゅうにじじゅうごふんさんびょうだよ！"),
    ],
)
def test_convert(hour, min, sec, message):
    cmd = Command()

    assert cmd.execute(get_datetime(hour, min, sec)) == message
