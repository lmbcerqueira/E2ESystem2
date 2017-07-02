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
        self.nContact = 0
        self.sent = False #se ja retransmiti no contacto nContact

    def set_ack(self, ack):
        self.ack = ack

    def set_sent(self, sent):
        self.sent = sent

    def set_timeFstTransm(self, curtime):
        self.timeFstTransm = curtime

    def set_bundle(self, bundle):
        self.bundle = bundle

    def set_nContact(self, nContact):
        self.nContact = nContact

    def get_bundle(self):
        return self.bundle

    def get_sent(self):
        return self.sent

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

    def get_nContact(self):
        return self.nContact

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
        settings.connected_lock.release()

        now = int(time.time())
                
        expired = False
        if self.ack == False and connected == True:

            #devo retransmitir se:

            # acabou de se estabelecer um contacto par (n recebi ack no impar, devo retransmitir)
            if self.nContact % 2 == 0 and self.sent == False:
                expired = True
                self.sent = True
                print("new contact")
            
            # contacto longo, já retransmiti, já passou RTO e ainda não recebi ack    
            elif (now-self.start) > ((self.nRetransm + 1) * RTO):
                print("N retransmition")
                expired = True
                print("now - start > ((self.nRetransm +1) * RTO): %d > %d" % (int(now-self.start), ((self.nRetransm +1) * RTO)))

            # contacto longo, enviei a 1ª vez, ja passou RTO, não recebi ack (as seguintes retransmissoes entram no 2º elif) 
            #elif (now-self.start) >= RTO and self.nRetransm == 0:
                #print("1st retransmition")
                #expired = True
                #print("now-start > RTO: %d > %d" % ((now-self.start), RTO))


        if expired == True:
           send_bundle(self.bundle)
           self.start = int(time.time())
           self.nRetransm += 1 
           print("bundle %d RETRANSMSISSION %d" % (self.seqNr, self.nRetransm))
