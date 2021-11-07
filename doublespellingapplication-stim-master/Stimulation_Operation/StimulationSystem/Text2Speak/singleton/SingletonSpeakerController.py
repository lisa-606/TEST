"""
@ author : Markov Wang
@ date : 2020/11/22
@ IDE : PyCharm
"""
from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.Text2Speak.SpeakerImplement import SpeakerImplement

controller_SpeakerController = SpeakerImplement(gender='male',rate=150,volume=1)


if __name__ == '__main__':

    controller_SpeakerController.speak("裂开")