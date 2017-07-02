from settings import WINDOW_SIZE, MAX_SEQ_NUMBER, DCU_ID
import json
import time
from log import *

def window_LeftShift(window_elements):

	store_TransmInfo(window_elements[0])
	for i in range(WINDOW_SIZE-1):
		window_elements[i].set_nRetransm(window_elements[i+1].get_nRetransm())
		window_elements[i].set_ack(window_elements[i+1].get_ack())
		window_elements[i].set_seqNr(window_elements[i+1].get_seqNr())
		window_elements[i].set_bundle(window_elements[i+1].get_bundle())
		window_elements[i].set_timeFstTransm(window_elements[i+1].get_timeFstTransm())
		window_elements[i].set_start(window_elements[i+1].get_start())
				
def window_addEmptyElem(window_elements, seq_nr):

	window_elements[WINDOW_SIZE -1].set_ack(False)
	window_elements[WINDOW_SIZE -1].set_seqNr(seq_nr % (MAX_SEQ_NUMBER+1))
	window_elements[WINDOW_SIZE -1].set_bundle("")
	window_elements[WINDOW_SIZE -1].set_nRetransm(0)
	window_elements[WINDOW_SIZE -1].set_timeFstTransm(0)
	window_elements[WINDOW_SIZE -1].set_start(0)
	
def window_addNewElem(window_elements, n_buffered, bundle):

	seq_bundle = window_elements[n_buffered].get_seqNr()
	bundle = json.loads(bundle)
	bundle.update({'seqNr':seq_bundle}) #append seqNr to the message
	bundle.update({'DCU_ID': DCU_ID})
	window_elements[n_buffered].set_bundle(bundle)
	window_elements[n_buffered].set_timeFstTransm(int(time.time()))
	window_elements[n_buffered].set_start(int(time.time()))
	window_elements[n_buffered].set_nRetransm(0)

	return bundle
