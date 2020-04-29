import json
import requests
import sys
import getopt

VERSION = "1.0"

def usage():
	print "Virustotal Subdomain Scanner {} ( github.com/ferhatcil )".format(VERSION)
	print "Usage: " +  sys.argv[0] + " [OPTIONS]"
	print "   --domain\texample.com" 
	print "   --version\tList version release" 
	print "   --help\tThis help menu\n"

	print "Example:"
	print "   python " + sys.argv[0] + " --domain example.com"
	sys.exit(1)

def virustotal(url):
	url = "https://www.virustotal.com/ui/domains/"+url+"/subdomains?relationships=resolutions&limit=40"
	r = requests.get(url)
	data = json.loads(r.text)
	for i in data['data']:
		print(i['id'])

if __name__ == "__main__":
	try:
		opts, args = getopt.getopt(sys.argv[1:], "d:hv", ["domain=", "help", "version"])
	except getopt.GetoptError, err:
		print(err)
		sys.exit(-1)

	for o, a in opts:
		if o in ("-d", "--domain"):
			virustotal(a)
		elif o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-V", "--version"):
			print VERSION
			sys.exit(0)
		else:
			assert False, "unhandled option"
			sys.exit(-1)

	argc = len(sys.argv)
	if argc != 3:
		usage()
