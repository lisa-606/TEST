from doubleSpellingApplication.Stimulation_Operation.CommonSystem.MessageReceiver.EventManager import  Event
import time
import logging

logger = logging.getLogger("DoubleSpellingApplication.operate_exchange_message_fcn")


def operate_exchange_message_fcn(message_queue, event_manager, stop):
    while True:
        if message_queue.qsize() > 0:
            message = message_queue.get()
            if len(message) > 4:
                str_split = message.split('^')
                # event = Event(type_ = message[0:4])
                # result = int(message[5:7])
                # next_mode = int(message[8:9])
                event = Event(type_ = str_split[0])
                result = int(str_split[1])
                next_mode = int(str_split[2])
                up_text = str_split[3]
                down_text = str_split[4]
                candidate_char = str_split[5]
                speak = str_split[6]
            else:
                event = Event(type_ = message)
                result = 0
                next_mode = 0
                up_text = ''
                down_text = ''
                candidate_char = ''
                speak = 0
            event.message = {'result': result,
                             'next_mode': int(next_mode),
                             'up_text': up_text,
                             'down_text': down_text,
                             'candidate_char': candidate_char.split('|'),
                             'speak':int(speak)}
            event_manager.SendEvent(event)
        if stop():
            logger.debug("Exiting operate_exchange_message_fcn!")
            break
        time.sleep(0.5)
