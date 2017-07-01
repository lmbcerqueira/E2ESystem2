from windowbuffer		import WindowBuffer_Element
from settings 			import IGNORE_PERCENT 
import os.path
import time
import settings

RTT = []		

def store_TransmInfo(windowBuffer_elem):

    try:
        fp = open("TransmInfo_Log.csv", 'a')
    except:
        pass
    else:
        rcv_ack = int(time.time())
        fp.write("%d;%d;%d;%d\n" % (windowBuffer_elem.seqNr, windowBuffer_elem.timeFstTransm , rcv_ack, windowBuffer_elem.nRetransm))
        fp.close()

        settings.sumRTT += rcv_ack - windowBuffer_elem.timeFstTransm
        settings.nTransm += 1

        global RTT
        RTT.append(int(rcv_ack - windowBuffer_elem.timeFstTransm))

def compute_new_RTO():

    try:
        fp = open("RTO_evolution.csv", 'a')
    except:
        print("could not open RTO file")
        pass
    else:
        print("writting on RTO file")
        fp.write("%d\n" % settings.RTO)
        fp.close()

    #estimate new value
    if settings.nTransm != 0:
        
        global RTT
        tmp = RTT
        RTT = []

        tmp.sort()
        for i in tmp:
            print("tmp:%d" % i)
        totalElem = len(tmp)

        sum = 0
        sumUp = 0
        sumDown = 0
        nPos = 0
        count = 0
        nUp = 0
        nDown = 0
        for i in tmp:
               if nPos <= (0.5 * totalElem) and nPos >= (IGNORE_PERCENT * totalElem):
                    sumDown = sumDown + i
                    count += 1
                    nDown += 1    
               if nPos > (0.5 * totalElem) and nPos <= ((1-IGNORE_PERCENT) * totalElem):
                    sumUp = sumUp + i
                    count += 1
                    nUp += 1
               #if nPos >= (IGNORE_PERCENT * totalElem) and nPos <= ((1-IGNORE_PERCENT) * totalElem):
                        #sum = sum + i
                        #count += 1
               nPos +=1

        if count != 0:
               #settings.RTO = (int) (sum / count)
               settings.RTO = (int) (sumUp * (0.2/nUp) + sumDown * (0.8/nDown)) 
                      
               #print("sum:%d" % sum)
               print("new RTO: %d" % settings.RTO)
