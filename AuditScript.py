#!/usr/bin/env python

import time,sys,subprocess,os
from scapy.all import Dot11, Dot11Deauth, Dot11Disas, RadioTap, Dot11Elt, sendp, sniff, conf, EAPOL, Dot11EltRSN

def main():
	input = 99
	while not (1 <= input <= 8):
		input = Get_Input()
	print(input)

def Set_Monitor():
	subprocess.run("sudo airmon-ng check kill > /dev/null", shell=True, executable="/bin/bash")
	subprocess.run("sudo airmon-ng start wlan0 > /dev/null", shell=True, executable="/bin/bash")

def Set_Managed():
	pass

def Set_Channel(channel):
	change_channel="sudo iwconfig wlan0 channel "+channel
	subprocess.run(change_channel, shell=True, executable="/bin/bash")

def Print_Options():
	options ="""1. Configure Wlan0
2. Wifi analysis
3. WPA2 cracking attack
4. DoS w/ authentication flood
5. DoS w/ deauth attack
6. DoS w/ beacon flood (2.4GHz band)
7. DoS w/ beacon flood (single channel)
8. Quit"""
	subprocess.run("clear", shell=True, executable="/bin/bash")
	print(options)
	option = input('Enter Selection: ')
	return(option)

def Get_Input():
	input = Print_Options()
	try:
		input = int(input)
	except:
		input = int(99)
	return input

if __name__ == '__main__':
    main()
