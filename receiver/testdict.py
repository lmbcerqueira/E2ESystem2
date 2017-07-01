import json
		
if __name__ == '__main__':

	acks_list = {0,1,2,3}
	
	acks = dict()
	acks['seqNr'] = acks_list
	print(acks)
	
	message = json.dumps(acks)
	
	print(message)
