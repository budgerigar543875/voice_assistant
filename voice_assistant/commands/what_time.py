from datetime import datetime

class Command:
    def __init__(self):
        self.tens_digit = {
            0:"",
            1:"じゅう",
            2:"にじゅう",
            3:"さんじゅう",
            4:"よんじゅう",
            5:"ごじゅう",
        }
        self.ones_place_hour = {
            0:"れいじ",
            1:"いちじ",
            2:"にじ",
            3:"さんじ",
            4:"よじ",
            5:"ごじ",
            6:"ろくじ",
            7:"しちじ",
            8:"はちじ",
            9:"くじ",
        }
        self.ones_place_minute = {
            0:"れいふん",
            1:"いっぷん",
            2:"にふん",
            3:"さんぷん",
            4:"よんふん",
            5:"ごふん",
            6:"ろっぷん",
            7:"ななふん",
            8:"はちふん",
            9:"きゅうふん",
        }
        self.ones_place_second = {
            0:"れいびょう",
            1:"いちびょう",
            2:"にびょう",
            3:"さんびょう",
            4:"よんびょう",
            5:"ごびょう",
            6:"ろくびょう",
            7:"ななびょう",
            8:"はちびょう",
            9:"きゅうびょう",
        }

    def _get_hour_str(self, hour:int) ->str | None:
        if hour < 0 or hour > 23:
            return None
        if hour == 0:
            return self.ones_place_hour[hour]
        tens = hour // 10
        ones = hour % 10
        if ones == 0:
            return self.tens_digit[tens] + "じ"
        return self.tens_digit[tens] + self.ones_place_hour[ones]

    def _get_minute_str(self, minute:int) ->str | None:
        if minute < 0 or minute > 59:
            return None
        if minute == 0:
            return self.ones_place_minute[minute]
        tens = minute // 10
        ones = minute % 10
        if ones == 0:
            return self.tens_digit[tens].replace("じゅう", "じゅっ") + "ぷん"
        return self.tens_digit[tens] + self.ones_place_minute[ones]

    def _get_second_str(self, second:int) ->str | None:
        if second < 0 or second > 59:
            return None
        if second == 0:
            return self.ones_place_second[second]
        tens = second // 10
        ones = second % 10
        if ones == 0:
            return self.tens_digit[tens] + "びょう"
        return self.tens_digit[tens] + self.ones_place_second[ones]
    
    def execute(self, now: datetime | None = None):
        if now is None:
            now = datetime.now()
        hour = self._get_hour_str(now.hour)
        if hour is None:
            return ""
        minute = self._get_minute_str(now.minute)
        if minute is None:
            return ""
        second = self._get_second_str(now.second)
        if second is None:
            return ""
        return f"{hour}{minute}{second}だよ！"