#!/usr/bin/python
import getopt
import json
import sys
import requests

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hd:", ["domain="])
    except getopt.GetoptError:
        print('test.py -d example.com')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -d example.com')
            sys.exit()
        elif opt in ("-d", "--domain"):
            domain = arg
            hstspreload(domain)
        else:
            print('test.py -d example.com')

def hstspreload(domain):
    r = requests.get('https://hstspreload.org/api/v2/preloadable?domain=' + domain)
    jsonData = json.loads(r.text)
    for i in jsonData['errors']:
        if 'response.no_header' in i['code']:
            print("Yanıtta HSTS başlığı yok.")
        elif 'domain.tls.invalid_cert_chain' in i['code']:
            print(domain + ", eksik veya geçersiz bir sertifika zinciri kullanıyor. Sitenizi https://www.ssllabs.com/ssltest/ adresinden inceleyin.")

if __name__ == "__main__":
    print("HSTS Checker")
    main(sys.argv[1:])
