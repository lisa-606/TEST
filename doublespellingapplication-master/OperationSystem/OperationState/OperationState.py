class OperationState:
    def __init__(self):
        #数据采集状态
        #INIT; % initial
        #CTNS; % connectToNeuroScan
        #DCNS; % disconnectToNeuroScan;
        #STAR; % startReceivedData
        #STOP; % stopReceivedData

        self.receiver_state = 'INIT'
        #基本控制状态
        #INIT; % initial
        #STON; % startOperation
        #SPON; % stopOperation
        #CSAL; % CloseAllOperation
        #EXIT; % ExitProgram

        self.control_state = 'INIT'
        #检测阶段处理状态
        #INIT; % initial
        #STRD; % StartRealTimeDetection
        self.current_detect_state = 'INIT'
