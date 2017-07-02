from threading import Timer
from sender import send_bundle, build_acksList
import time
import settings

class WindowBuffer_Element(object):

    def __init__(self, seqNr):
        self.bundle = ""
        self.ack = False
        self.seqNr = seqNr
        self.nRetransm = 0
        self.timeFstTransm = 0
        self.start = 0
        self.sent = False #se ja retransmiti no contacto nContact

    def set_ack(self, ack):
        self.ack = ack

    def set_timeFstTransm(self, curtime):
        self.timeFstTransm = curtime

    def set_bundle(self, bundle):
        self.bundle = bundle

    def get_bundle(self):
        return self.bundle

    def get_timeFstTransm(self):
        return self.timeFstTransm;

    def get_ack(self):
        return self.ack

    def get_seqNr(self):
        return self.seqNr

    def get_start(self):
        return self.start

    def get_nRetransm(self):
        return self.nRetransm

    def set_seqNr(self, seqNr):
        self.seqNr = seqNr

    def set_nRetransm(self, nTry):
        self.nRetransm = nTry

    def set_start(self, time):
        self.start = time

    def check_timer(self, windowPos):
        
        print("___________CHECK TIMER_____________")
       
        if windowPos == 0:
            RTO = settings.RTO -2
        else:
            RTO = settings.RTO

        settings.connected_lock.acquire()
        connected = settings.connectionState.connected
        nContact = settings.connectionState.nContact
        startContact = settings.connectionState.start
        settings.connected_lock.release()

        now = int(time.time())
        print("nContact:%d" % nContact)     
        expired = False
       
        if self.ack == False and connected == True:

            #devo retransmitir se:
    
            # se contacto par (altura de receber acks - transmite só o 1º para receber os acks de todos)
            if windowPos == 0 and nContact % 2 == 0 and (now-self.start) > RTO:
                expired = True
                print("contact par - Retransmit first element: %d" % int(time.time()))

            # se contacto impar (n recebi ack no par, devo retransmitir)
            if nContact % 2 != 0 and (now-self.start) >  RTO:
                expired = True
                print("contact impar: %d" % int(time.time()))
            
            # contacto longo, já passou RTO e ainda não recebi ack    
            #elif (now - startContact) > RTO and (now-self.start) > ((self.nRetransm + 1) * RTO):
                #print("N retransmition")
                #expired = True
                #print("now - start > ((self.nRetransm +1) * RTO): %d > %d" % (int(now-self.start), ((self.nRetransm +1) * RTO)))


        if expired == True:
           send_bundle(self.bundle)
           self.start = int(time.time())
           self.nRetransm += 1 
           print("bundle %d RETRANSMSISSION %d" % (self.seqNr, self.nRetransm))
