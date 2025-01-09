#!/usr/bin/env python

from threading import Thread
import time,sys,subprocess,os
from scapy.all import Dot11, Dot11Deauth, Dot11Disas, RadioTap, Dot11Elt, sendp, sniff, conf, EAPOL, Dot11EltRSN

channels = [1,2,3,4,5,6,7,8,9,10,11,32,36,40,44,48,52,56,60,64,68,96,100,104,108,112,116,120,124,128,132,136,140,144,149,153,157,161,165,169,173,177]
hmac = '5A:6D:67:AC:90:90'
index = 0
id_list = set()
s=conf.L2socket(iface='wlan0')

def main():
	Set_Monitor()
	Set_Channel(str(channels[index]))
	counter_thread = Thread(target=counter)
	counter_thread.daemon = True
	counter_thread.start()

	sniff(iface='wlan0',prn=Process_Frame,lfilter=lambda pkt: pkt.haslayer(Dot11), store=0)

def Set_Monitor():
	subprocess.run("sudo airmon-ng check kill > /dev/null", shell=True, executable="/bin/bash")
	subprocess.run("sudo airmon-ng start wlan0 > /dev/null", shell=True, executable="/bin/bash")

def Set_Managed():
	subprocess.run("systemctl start NetworkManager", shell=True, executable="/bin/bash")

def Set_Channel(channel):
	change_channel="sudo iwconfig wlan0 channel "+channel
	subprocess.run(change_channel, shell=True, executable="/bin/bash")

def Process_Frame(packet):
	global id_list
	if packet.type == 0 and packet.subtype == 5:
		ssid = str(packet[Dot11Elt].info)
		ssid = ssid.split("'")
		id_stat = f"{ssid[1]}/{packet.addr2}"
		id_list.add(id_stat)

def counter():
	global channels
	global index
	global id_list
	while True:
		id_list = set()
		time.sleep(2)
		print(f"Channel: {channels[index]}")
		#id_list = list(dict.fromkeys(id_list))
		for item in id_list:
			id_values = item.split("/")
			print(f"SSID: {id_values[0]}, BSSID: {id_values[1]}")
		print("")
		index +=1
		if index > 41:
			index = 0
		change_channel="sudo iwconfig wlan0 channel "+ str(channels[index])
		subprocess.run(change_channel, shell=True, executable="/bin/bash")
		probe_req=RadioTap()/Dot11(type=0,subtype=4,addr1='FF:FF:FF:FF:FF:FF',addr2=hmac,addr3=hmac)/Dot11Elt(ID=0,info="",len=0)
		for i in range(1,3):
			s.send(probe_req)

if __name__ == '__main__':
    main()
