import json
import requests
import settings
import requests.exceptions
import time


def send_bundle(bundle):

	print("SEND BUNDLE %s" %bundle)
	print(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime(time.time())))
	
	## Prepare http POST Request ##
	headers = {'Content-Type': 'application/json'}
	url = "http://api.veniam.local/ext/caruma/v1.0/event/:test_device/" ## pode se mudar o event - fico com um "dominio" só meu
	payload = {"priority":"critical"}

	## Send Request ##
	try:
		r = requests.post(url,  headers=headers, params=payload, data = json.dumps(bundle), timeout=0.2)
	except requests.exceptions.Timeout:
		print("TIMEOUT")
		pass
	except requests.exceptions.ConnectionError:
		print("Connection Error")
		pass
	else:
		print("Response from server: %s" % r.status_code)
		if r.status_code == 201:
			build_acksList(r)

def build_acksList(respJson):

	dict_acks = respJson.json()

	tmp = dict_acks.get('acks')

	acksList = tmp.split(",")
	print(acksList)

	for ack in acksList:
		if ack != 'EMPTY':
			settings.rcv_seqNr.put(ack)
