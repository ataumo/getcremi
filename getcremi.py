#!/usr/bin/env python3

import requests
import sys
import getopt
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
from Crypto.Cipher import AES


__LIST_ROOM__=[4,5,7,8,9,101,102,103,104,105,201,202,203,204,205,206,207,208]

__ROOM__ = "008"
__USER__ = "yourid"
__PASSWORD__ = ""
__CIPHERPASS__ = b'(\xb1\x11;\t\xed\xb6\x00\x1e\x9a/\xf3\x9e\xe0hb'

def getpass(word):
    key = word.encode()

    # ciper text
    cipher_text=__CIPHERPASS__

    # Decryption
    try:
        decryption_suite = AES.new(key, AES.MODE_ECB)
        plain_text = decryption_suite.decrypt(cipher_text)
        return plain_text.decode()
    except ValueError:
        print("Key error")
        return False

def clear_number(num):
    if len(num)==1:
        num="00"+num
    if len(num)==2:
        num="0"+num
    return num

def usage():
    print("usage : python3 getpython.py -r [room_number] -u [-a]")
    print("-h : help")
    print("-r : number of cremi's room (008 to default)")
    print("-u : discover UP host")
    print("-a : scan util found a a room with UP host")
    print("-e : to encrypt your password")


def get_url_data(room):
    url = 'https://services.emi.u-bordeaux.fr/nagios3/cgi-bin/status.cgi?hostgroup=Salle_'+room+'&style=overview'
    r = requests.get(url, auth=HTTPBasicAuth(__USER__, __PASSWORD__))
    return r.content

def data_parser(html):
    soup = BeautifulSoup(html, 'html.parser')
    body = soup.find("body",recursive=True)

    childrend=body.findChildren(recursive=False)

    intro=(childrend[1]).get_text()

    print(intro)

    hosts=(childrend[2]).findChildren(recursive=False)
    hosts_2=(hosts[0]).findChildren(recursive=False)
    hosts_3=(hosts_2[0]).findChildren(recursive=False)
    hosts_4=(hosts_3[0]).findChildren(recursive=False)
    hosts_5=(hosts_4[0]).findChildren(recursive=False)
    hosts_6=(hosts_5[1]).findChildren(recursive=False)
    hosts_7=(hosts_6[0]).findChildren(recursive=False)

    #creat list of hosts
    List_of_hosts=[]

    for i in range(1,len(hosts_7)):
        List_of_contents=[]
        mach=hosts_7[i]
        values=mach.findChildren(recursive=False)
        #get name and adress
        button=(values[0]).find("a",recursive=True)
        adress=button.get("title")
        name=button.get_text()
        #get status
        status=(values[1]).get_text()
        buttons=(values[2]).find_all("a",recursive=True)
        #get services
        List_of_services=[]
        for j in buttons:
            List_of_services.append(j.get_text())
        List_of_hosts.append([name,adress,status,List_of_services])

    return List_of_hosts

def print_hosts(L):
    for i in L:
        print("name : ",i[0])
        print("adress : ",i[1])
        print("===================")
        print("status : ",i[2])
        print("===================")
        for j in i[3]:
            print(j)
        print("===================")
        print("\n")

def exist_UP_host(L):
    UP_host=[]
    for i in L:
        if i[2]=="UP":
            UP_host.append(i)
    return UP_host

def scan_room(room):
    content=get_url_data(room)
    List_of_hosts=data_parser(content)
    print_hosts(List_of_hosts)

def scan_only_UP(room):
    content=get_url_data(room)
    List_of_hosts=data_parser(content)
    List_of_UP_hosts=exist_UP_host(List_of_hosts)
    if len(List_of_UP_hosts)>0:
        print_hosts(List_of_UP_hosts)
    else :
        print("No host is UP")

def scan_only_UP_in_all_cremi():
    for i in __LIST_ROOM__:
        room=clear_number(str(i))
        content=get_url_data(room)
        List_of_hosts=data_parser(content)
        List_of_UP_hosts=exist_UP_host(List_of_hosts)
        if len(List_of_UP_hosts)>0:
            print_hosts(List_of_UP_hosts)
            break;
        else :
            print("No host is UP")

def main(argv):
    room = __ROOM__
    try:
        opts, args = getopt.getopt(argv, "hr:duae:", ["help", "room","up",'all','encrypt'])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt == '-d':
            global _debug
            _debug = 1
        elif opt in ("-r", "--room"):
            room = arg
            int_room=int(room)
            if int_room not in __LIST_ROOM__:
                print("Sorry, but host group 'Salle_",room,"' doesn't seem to exist...")
                sys.exit()
        elif opt in ("-u", "--up"):
            scan_only_UP(room)
            sys.exit()
        elif opt in ("-a", "--all"):
            scan_only_UP_in_all_cremi()
            sys.exit()
    scan_room(room)


if __name__ == "__main__":
    try:
        __PASSWORD__=getpass(sys.argv[1])[:-5]
    except TypeError:
        sys.exit("error pass")
    main(sys.argv[2:])
