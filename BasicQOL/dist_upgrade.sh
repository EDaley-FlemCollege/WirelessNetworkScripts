#!/bin/bash
BRed='\033[1;31m'

apt update && apt dist-upgrade -y
printf "${BRed}Don't forget to reboot VM"
