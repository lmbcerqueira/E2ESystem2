PORT_OBU = 8080

N_BITS_FOR_WINDOW = 5

MAX_SEQ_NUMBER = 2**N_BITS_FOR_WINDOW -1

WINDOW_SIZE = int((MAX_SEQ_NUMBER + 1)/2)

SERVER_IP = '192.168.254.17'

IGNORE_PERCENT = 0.10 #for RTO calculation

N_DCUS = 3

def init():
    global sqNr_list
    sqNr_list = []
    for i in range(N_DCUS):
        sqNr_list.append([])
