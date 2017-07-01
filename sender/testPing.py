import netifaces
import os
import settings

def get_ip_gw(ip):
        try:
                parsed_ip = ip.split(".")
                return parsed_ip[0] + '.' + parsed_ip[1] + '.' + parsed_ip[2] + '.1'
        except AttributeError:
                return None

if __name__ == '__main__':

        try:
                my_ip = netifaces.ifaddresses(DTN_INTERFACE)[2][0]['addr']
                print(my_ip)
        except Exception as e:
                my_ip = None

        if my_ip:
                obu_ip = get_ip_gw(my_ip)
                print(obu_ip)

                response = os.system("ping -w 1 " + obu_ip)

                #and then check the response...
                if response == 0:
                        print ("hostname, is up!")
                else:
                        print ("hostname, 'is down!")
        else:
                print("no_ip")
