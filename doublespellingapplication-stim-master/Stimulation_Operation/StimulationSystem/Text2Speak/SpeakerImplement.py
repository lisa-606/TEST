import pyttsx3
#speaker = SpeakerImplement(gender,rate,volume)
#gender = 'male' or 'female'
#rate >= 0
#volume = 0~1

#content = str
from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.Text2Speak.SpeakerInterface import SpeakerInterface


class SpeakerImplement(SpeakerInterface):
    def __init__(self, gender, rate, volume):
        super().__init__()
        self.gender = gender
        self.rate = rate
        self.volume =  volume
    def speak(self,content):
        engine = pyttsx3.init()
        if (self.volume >= 0) & (self.volume <= 1) & (self.rate >= 0) & ((self.gender == 'female') | (self.gender == 'male')):
            # 判断是否满足输入条件
            engine.setProperty('rate', self.rate)
            engine.setProperty('volume', self.volume)
            if self.gender == 'female':
                engine.setProperty('voice',
                                   'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ZH-CN_HUIHUI_11.0')
            else:
                engine.setProperty('voice',
                                   'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ZH-CN_KANGKANG_11.0')

            engine.say(content)
            engine.runAndWait()
        else:
            print('speak() parameter wrong input')



