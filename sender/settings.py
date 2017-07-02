from queue 				import Queue , Empty
import threading

PORT = 4999

DTN_INTERFACE = "wlan0"

DCU_ID = 2

QUEUE_MAX_SIZE = 2048

N_BITS_FOR_WINDOW = 5

MAX_SEQ_NUMBER = 2**N_BITS_FOR_WINDOW -1

WINDOW_SIZE = int((MAX_SEQ_NUMBER + 1)/2)

IGNORE_PERCENT = 0.20 #for RTO calculation

class ConnectionInfo(object):

    def __init__(self, connected, start, endLastContact , prevsStateconn):
        self.connected = connected
        self.start = start
        self.endLastContact = endLastContact
        self.prevsStateconn = prevsStateconn


def init():

    ## test if connected to and OBU ##
    global connectionState
    global connected_lock
    connectionState = ConnectionInfo(False, -1, -1, False)
    connected_lock = threading.Lock()

    global rcv_seqNr
    rcv_seqNr = Queue()

    ## RTO Estimation ##
    global sumRTT
    global RTO
    global nTransm
    sumRTT = 0
    nTransm = 0
    RTO = 15
