import requests
import requests.exceptions
import json
import time
import settings

def get_sqNrList(start, end):

	jsonFiles = getRequest(start, end)

	getlist(jsonFiles)

def getRequest(start, end):

	## convert start/end in ISO timestamps ##
	tstart = time.strftime("%Y-%m-%dT%H:%M:%SZ", start)
	tend = time.strftime("%Y-%m-%dT%H:%M:%SZ", end)

	payload = {}
	payload["tsinit"] = tstart
	#payload["tsinit"] = "2017-04-11T14:24:00Z";
	payload["tsend"] = tend

	print(payload)

	## Prepare Request ##
	url = "http://api.veniam.com/api/v2.5/local/caruma/events"
	#payload = {"tsinit":"2017-04-20T09:00:00Z" , "tsend":"2017-04-20T09:20:00Z"}

	## Send Request ##
	jsonFiles = ""
	try:
		r = requests.get(url, params=payload, timeout = 0.3)
	except requests.exceptions.Timeout:
		print("request: timout")
		pass
	except requests.exceptions.ConnectionError:
		print("request: conection error")
		pass
	else: 
		jsonFiles = json.loads(r.text)
		print(jsonFiles)

	return jsonFiles


def getlist(jsonFiles):

	for elem in jsonFiles:
		data = elem.get('_data')
		try:
			data = json.loads(data)
		except:
			pass
		else:
			seqNr = data.get('seqNr')
			dcu_id = data.get('DCU_ID')
			if seqNr is not None:
				settings.sqNr_list[dcu_id].append(seqNr)

	print("seqNr_list:")
	print(settings.sqNr_list)
