#!/bin/bash

apt update
apt install -y linux-headers-$(uname -r) build-essential bc dkms git libelf-dev rfkill iw
apt install realtek-rtl8814au-dkms
apt install mdk4
