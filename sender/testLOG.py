import os.path
RTO = 45

if __name__ == '__main__':

  count = 0
  sum = 0

  fp = open("TransmInfo_Log.txt", 'r')
  data = fp.read()

  bundleInfo = data.split('/')
  for elem in bundleInfo:
    count += 1
    inf = elem.split('-')
    print(inf)
    sum += int(inf[1])

  settings.RTO = int(sum/count)
