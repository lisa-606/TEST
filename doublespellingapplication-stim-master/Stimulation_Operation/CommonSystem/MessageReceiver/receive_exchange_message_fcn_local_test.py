import time

# operation_test:
# def receive_exchange_message_fcn_local_test(message_queue):
#     time.sleep(3)
#
#     message_queue.put('STON')
#     time.sleep(3)
#     while True:
#         message_queue.put('STRD')
#         time.sleep(3)
#     time.sleep(70)
#
#     message_queue.put('TNOK')
#
#     time.sleep(60)
#
#     message_queue.put('RSLT')

# stimulation_test:
def receive_exchange_message_fcn_local_test(message_queue):
    time.sleep(5)
    message_queue.put('CTOK')
    time.sleep(5)
    message_queue.put('TROK')
    time.sleep(20)

    message_queue.put('TNOK')

    time.sleep(5)

    # for i in range(0,3):
    #     # RSLT:alphabet_id,next_mode
    #     # 格式：RSLT:00,0
    #     message_queue.put('RSLT:resut_id:mode:up_text:down_text:candidate_char')
    #     time.sleep(5)

    # message_queue.put('RSLT:33:1:test1up:test1down:一,,,四,五,六,七,八,九,十')
    # time.sleep(5)
    # message_queue.put('RSLT:33:0:test2up:test2down:一,,,四,五,六,七,八,九,十')
    # time.sleep(5)
    # message_queue.put('RSLT:33:1:test3up:test3down:一,,,四,五,六,七,八,九,十')
    # time.sleep(5)
    #
    # time.sleep(5)
    # message_queue.put('PROK')
    # time.sleep(5)
    # message_queue.put('DCOK')
    # time.sleep(5)
    # message_queue.put('CAOK')
    # time.sleep(5)