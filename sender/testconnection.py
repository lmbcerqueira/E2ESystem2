import netifaces
import os
import time
from settings import DTN_INTERFACE


def get_ip_gw(ip):
    try:
        parsed_ip = ip.split(".")
        gw_ip = parsed_ip[0] + '.' + parsed_ip[1] + '.' + parsed_ip[2] + '.1'
        return gw_ip
    except AttributeError:
        return None

def ping():

    try:
        my_ip = netifaces.ifaddresses(DTN_INTERFACE)[2][0]['addr']
    except Exception as e:
        #print("exception IP")
        my_ip = None

    if my_ip:
        gotIP = "IP"
        obu_ip = get_ip_gw(my_ip)

        response = os.system("ping -w 1 " + obu_ip + '>/dev/null 2>&1')

        #and then check the response...
        if response == 0:
            pingResponse = "OBU_RESP"
        else:
            pingResponse = "NO_OBU_RESP"
    else:
        gotIP = "NO_IP"
        pingResponse = "NO_OBU_RESP"

    fp = open("ConnectionLog.csv", 'a')
    iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime(time.time()))
    fp.write( iso  + ";" + gotIP + ";" + pingResponse )
    fp.write("\n")
    fp.close()


if __name__ == '__main__':

    while(True):
        ping()
