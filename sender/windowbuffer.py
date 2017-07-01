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

    def check_timer(self):

        settings.connected_lock.acquire()
        connected = settings.connectionState.connected
        start = settings.connectionState.start
        settings.connected_lock.release()

        now = time.time()

        if self.ack == False:

            #devo retransmitir se:
            if connected == True and self.nContact % 2 == 0 and self.sent == False:
                print("RETRANSMSISSION bundle %d" % self.seqNr)
                send_bundle(self.bundle)
                self.nRetransm += 1
                self.sent = True
                print("NRETRANSM: %d" % self.nRetransm)

            else if connected == True and self.nContact % 2 == 0 and (now-start) >= (self.nRetransm*10):
                print("RETRANSMSISSION bundle %d" % self.seqNr)
                send_bundle(self.bundle)
                self.nRetransm += 1
                print("NRETRANSM: %d" % self.nRetransm)
