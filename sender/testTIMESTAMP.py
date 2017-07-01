import time

if __name__ == '__main__':
	tstart = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime(time.time()))
	print(tstart)
