import json
import importlib
from commands.unknown import Command as unknown
from vosk import Model, KaldiRecognizer
import sounddevice as sd
import queue
from pykakasi import kakasi
import pyttsx3
from Gpio import Gpio

class CommandFactory:
    def __init__(self, gpio: Gpio):
        self._gpio = gpio

    def create(self, config: dict):
        module = importlib.import_module(f"commands.{config['class']}")
        command_class = getattr(module, "Command")
        if "channels" in config:
            return command_class(self._gpio, config["channels"])
        else:
            return command_class()

class CommandList:
    def __init__(self, file_path:str, factory: CommandFactory):
        with open(file_path, "r", encoding="utf-8") as f:
            confs = json.load(f)
        self._commands = {}
        for key in confs:
            self._commands[key] = factory.create(confs[key])
        self._unknown = unknown()

    def execute(self, command:str) -> str:
        # 完全一致だと使い勝手が悪いので、
        # ===========================
        # マイクから入力された音声に
        # コマンドが含まれていればよい
        # ===========================
        # ということにする
        # 例：「あ、今何時？」でもOKにする
        for cmd in self._commands:
            if cmd in command:
                return self._commands[cmd].execute()
        return self._unknown.execute(command)

class RecordingConfig:
    def __init__(self, file_path: str):
        with open(file_path, "r", encoding="utf-8") as f:
            conf = json.load(f)
        self._model_path = conf["model_path"]
        self._sample_rate = int(conf["sample_rate"])
        self._block_size = int(conf["block_size"])

    def model_path(self) -> str:
        return self._model_path

    def sample_rate(self) -> int:
        return self._sample_rate

    def block_size(self) -> int:
        return self._block_size

class Microphone:
    def __init__(self, config: RecordingConfig):
        self._queue = queue.Queue()
        self._stream = sd.RawInputStream(
            samplerate=config.sample_rate(),
            blocksize=config.block_size(),
            dtype="int16",
            channels=1,
            callback=self._callback
        )
        self._stream.start()

    def _callback(self, indata, frames, time, status):
        self._queue.put(bytes(indata))

    def get(self, timeout=0.1):
        try:
            return self._queue.get(timeout=timeout)
        except queue.Empty:
            return None
    
    def close(self):
        self._stream.stop()
        self._stream.close()

class Recognizer:
    def __init__(self, config: RecordingConfig, converter):
        model = Model(config.model_path())
        self._recognizer = KaldiRecognizer(model, config.sample_rate())
        self._converter = converter

    def recognize(self, audio) -> str | None:
        if self._recognizer.AcceptWaveform(audio):
            result = self._recognizer.Result()
            result = json.loads(result).get("text", "").replace(" ","")
            if result:
                result = self._converter.convert(result)
            else:
                print("無音")
                result = None
        else:
            result = None
        return result
    
class StrConverter:
    def __init__(self, before, after, show_result=True):
        instance = kakasi()
        instance.setMode(before, after)
        self._converter = instance.getConverter()
        self._show_result = show_result

    def convert(self, text: str) -> str:
        result = self._converter.do(text)
        if self._show_result:
            print(f"変換結果：{text} => {result}")
        return result

class Speaker:
    def __init__(self):
        self._engine = pyttsx3.init()
        self._engine.setProperty('voice', 'jpx/ja')

    def speak(self, text):
        if text:
            print(text)
            self._engine.say(text)
            self._engine.runAndWait()

def main():
    gpio = None
    mic = None

    try:
        gpio = Gpio("gpio_config.json")
        factory = CommandFactory(gpio)

        commands = CommandList("command_map.json", factory)
        rec_conf = RecordingConfig("recording_config.json")

        mic = Microphone(rec_conf)
        converter = StrConverter("J", "H")
        rec = Recognizer(rec_conf, converter)
        speaker = Speaker()

        print("コマンド受付開始")
    
        while True:
            audio = mic.get()
            if audio is None:
                continue
            text = rec.recognize(audio)
            if text is None:
                continue
            result = commands.execute(text)
            speaker.speak(result)
    except KeyboardInterrupt:
        print("コマンド受付終了")
    except Exception as e:
        print("異常終了", e)
    finally:
        if gpio is not None:
            gpio.cleanup()
        if mic is not None:
            mic.close()

if __name__ == "__main__":
    main()