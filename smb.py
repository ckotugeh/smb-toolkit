#!/bin/bash

target=$1
lhost=$2
echo "[*] Starting SMB Attack Toolkit against $target"

# Enumeration
nmap -p 445 --script smb-os-discovery,smb-enum-users,smb-enum-shares $target -oN enum_nmap_$target.txt
enum4linux-ng -A $target | tee enum4_$target.txt

# Test for Null session share mount
smbclient -L //$target -N | tee smbclient_$target.txt

# Optional: EternalBlue (MS17-010)
echo "[*] Launching MS17-010 check..."
msfconsole -q -x "use auxiliary/scanner/smb/smb_ms17_010; set RHOSTS $target; run; exit"

echo "[*] Finished."
