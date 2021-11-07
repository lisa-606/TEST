from doubleSpellingApplication.CommonSystem.MessageReceiver.EventManager import  Event
import time
import logging

logger = logging.getLogger("DoubleSpellingApplication.operate_exchange_message_fcn")

def operate_exchange_message_fcn(message_queue, event_manager, stop):
    while True:
        if message_queue.qsize() > 0:
            message = message_queue.get()
            if len(message) > 4:
                event = Event(type_ = message[0:4])
                result = int(message[5:])
            else:
                event = Event(type_ = message)
                result = 0
            event.message = {'result': result}
            event_manager.SendEvent(event)
        if stop():
            logger.debug("Exiting operate_exchange_message_fcn!")
            break
        time.sleep(0.5)
