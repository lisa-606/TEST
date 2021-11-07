import time

# operation_test:
def receive_exchange_message_fcn_local_test(message_queue):
    time.sleep(3)

    message_queue.put('STON')
    time.sleep(3)
    while True:
        message_queue.put('STRD')
        time.sleep(3)
    time.sleep(5)

    message_queue.put('TNOK')

    time.sleep(5)

    # message_queue.put('RSLT:9')
    #
    # while True:
    #     res = random.randInt(0, 7)
    #     message_queue.put('RSLT:'+str(res))
    #     time.sleep(5)

# stimulation_test:
# def receive_exchange_message_fcn_local_test(message_queue):
#     time.sleep(5)
#     message_queue.put('CTOK')
#     time.sleep(5)
#     message_queue.put('TROK')
#     time.sleep(15)
#
#     message_queue.put('TNOK')
#
#     time.sleep(5)
#
#     for i in range(0,3):
#
#         message_queue.put('RSLT')
#         time.sleep(5)
#
#     time.sleep(5)
#     message_queue.put('PROK')
#     time.sleep(5)
#     message_queue.put('DCOK')
#     time.sleep(5)
#     message_queue.put('CAOK')
#     time.sleep(5)