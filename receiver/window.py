
def isBetween(lowerlimit, seqNr, upperlimit):
	if (lowerlimit <= seqNr and seqNr < upperlimit) or (upperlimit < lowerlimit and lowerlimit <= seqNr) or (seqNr < upperlimit and upperlimit < lowerlimit):
		return True
	else:
		return False

class Window(object):

	def __init__(self, DCU_id, window_elements, seqNr, acks):
		self.DCU_id = DCU_id
		self.window_elements = window_elements
		self.seqNr = seqNr #counter
		self.acks_list = acks

class Window_Element(object):

	def __init__(self, bundleId):
		self.bundleId = bundleId
		self.ack = False

	def get_id(self):
		return self.bundleId

	def set_id(self, bundleId):
		self.bundleId = bundleId

	def set_ack(self, ack):
		self.ack = ack

	def get_ack(self):
		return self.ack
