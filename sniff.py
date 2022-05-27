from scapy.all import *
from ipaddress import *
import mysql.connector
from csv import DictWriter
import pyfiglet
from termcolor import colored
import os
art = pyfiglet.figlet_format("IDS-Analytics")
color_art = colored(art, color="green")
cwd = os.getcwd()
parent = os.path.dirname(cwd)
print(art)

con = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="capstone"
)

crules=input("Do you want to define your custom rules? (Y/N): ")
if(crules == "Y"):
    monsrcip=input("Enter the IP you want to monitor: ")
    monsrcport=input("Enter the source port you want to monitor (20,21,22-25): ")
    monhostport=input("Enter the port of your device you want to monitor: ")
    monflags=input("Enter the flags you want to monitor (F,A,P,R,S,U): ")
    monsrciplist=None
    monsrcportlist=None
    monhostportlist=None
    monflagslist=None
    if monsrcip == "":
        monsrcip="0.0.0.0"
    if "," in monsrcip:
        monsrciplist=monsrcip.split(",")
        
    if monsrcport == "":
        monsrcport="N"
    elif "," in monsrcport or "-" in monsrcport:
        try:
            monsrcportlist=monsrcport.split(",")
        except:
            monsrcportlist=monsrcport.split("-")
        print(monsrcportlist)
        monsrcportlist2=[]
        for ports in monsrcportlist:
            if "-" in ports:
                minport=int(ports.split("-")[0])
                maxport=int(ports.split("-")[1])
                monsrcportlist.remove(ports)
                for allport in range(minport,(maxport+1)):
                    monsrcportlist2.append(str(allport))
        try:
            for x in monsrcportlist2:
                monsrcportlist.append(x)
        except:
            pass
        print(monsrcportlist)
    else:
        monsrcport=int(monsrcport)
        
    if monhostport == "":
        monhostport="N"
    elif "," in monhostport or "-" in monhostport:
        try:
            monhostportlist=monhostport.split(",")
        except:
            monhostportlist=monhostport.split("-")
        monhostportlist2=[]
        for ports in monhostportlist:
            if "-" in ports:
                minport=int(ports.split("-")[0])
                maxport=int(ports.split("-")[1])
                monhostportlist.remove(ports)
                for allport in range(minport,(maxport+1)):
                    monhostportlist2.append(str(allport))
        try:
            for x in monhostportlist2:
                monhostportlist.append(x)
        except:
            pass
    else:
        monhostport=int(monhostport)

    if monflags != "":
        if len(monflags) > 1:
            monflagslist=monflags.split(",")
    else:
        monflags="N"



elif(crules == "N" or crules=="n"):
    l=[]
    with open(parent+'\web\\python\\compromised_ip_full.txt','r') as f:
        lines = f.readlines()
        for ip in lines:
            l.append(ip.replace("\n",""))
    monsrcip="Y"
    monsrcport="Y"
    monhostport="Y"
    monflags="Y"
    monsrciplist=l
    monsrcportlist=["20","21","22","23","24","25","51","80","138","139","443"]
    monhostportlist=["21","22","23","80","443"]
    monflagslist=["U","F","P"]


logpacket="n"
flag=0
#if monsrcip != "N":
#    ipobj = IPv4Network(monsrcip)

totalpackets=0
defaulterpackets=0

def process_packet(packet):
    from datetime import datetime
    global logpacket
    global monsrcip
    global monsrciplist
    global totalpackets
    global defaulterpackets
    global flag
    totalpackets+=1
    
    srcip="NULL"
    destip="NULL"
    srcport="NULL"
    destport="NULL"

    packetlen="NULL"
    packetttl="NULL"
    protocol="NULL"
    ose="NULL"
    
    flags="NULL"
    comments="NULL"

    date=None
    time=None

    dt=datetime.now()
    datetime=dt.strftime("%Y/%m/%d %H:%M:%S")
    datetime=datetime.split(" ")
    date=datetime[0]
    time=datetime[1]
    datef=dt.strftime("%Y-%m-%d")

    #===========================================================================================================MAIN OPERATIONS DONE



    
    print("[+]",packet.summary())
    if packet.haslayer(IP) and packet[IP] != None:  #IP is scapy packet obj #name 'ip' is not defined
        srcip=packet[IP].src
        destip=packet[IP].dst                       #protocol=packet[IP].proto
        packetlen=packet[IP].len
        packetttl=packet[IP].ttl
        if packetttl == 128:
            ose="W"
        elif packetttl == 64:
            ose="L"
        elif packetttl == 60:
            ose="M"
        else:
            ose="O"
        if monsrcip != "0.0.0.0" and (monsrciplist == None):
            ipobj = IPv4Network(monsrcip)
            if ((IPv4Address(srcip) in ipobj) or (IPv4Address(destip) in ipobj)):
                print("[-]Logged| Source IP: ",srcip," Destination IP: ",destip)
                logpacket="y"
                if comments=="NULL":
                    comments="[IP]"
                else:
                    comments=comments+"[IP]"
        if monsrcip != "0.0.0.0" and (monsrciplist != None):
            for monsrcip in monsrciplist:
                #print("\n",monsrcip,"\n")
                ipobj = IPv4Network(monsrcip)
                if ((IPv4Address(srcip) in ipobj) or (IPv4Address(destip) in ipobj)):
                    print("[-]Logged| Source IP: ",srcip," Destination IP: ",destip)
                    logpacket="y"
                    if comments=="NULL":
                        comments="[IP]"
                    else:
                        comments=comments+"[IP]"
                    break

     #============================================================================================================IP & ARP       

        
    if packet.haslayer(ARP) and packet[ARP] != None:
        srcip=packet[ARP].psrc
        destip=packet[ARP].pdst
        if monsrcip != "N" and (monsrciplist == None):
            ipobj = IPv4Network(monsrcip)
            if ((IPv4Address(srcip) in ipobj) or (IPv4Address(destip) in ipobj)):
                print("[-]Logged| Source IP: ",srcip," Destination IP: ",destip)
                logpacket="y"
                if comments=="NULL":
                    comments="[IP]"
                else:
                    comments=comments+"[IP]"
        if monsrcip != "N" and (monsrciplist != None):
            for monsrcip in monsrciplist:
                ipobj = IPv4Network(monsrcip)
                if ((IPv4Address(srcip) in ipobj) or (IPv4Address(destip) in ipobj)):
                    print("[-]Logged| Source IP: ",srcip," Destination IP: ",destip)
                    logpacket="y"
                    if comments=="NULL":
                        comments="[IP]"
                    else:
                        comments=comments+"[IP]"
                    break





    #============================================================================================================
    #============================================================================================================IP FILTERING COMPLETED
    #============================================================================================================
    



    
    if packet.haslayer(TCP) and packet[TCP] != None:
        srcport=packet[TCP].sport
        destport=packet[TCP].dport
        protocol="TCP"
        flags=str(packet[TCP].flags)
        if (monsrcport != "N") and (monsrcportlist == None) and (monsrcport == srcport):
            print("[-]Logged| Source port: ",srcport," Destination port: ",destport)
            logpacket="y"
            if comments=="NULL":
                comments="[PORT]"
            else:
                comments=comments+"[PORT]"
        if (monhostport != "N") and (monhostportlist == None) and (monhostport == destport):
            print("[-]Logged| Destination port: ",destport," Source port: ",srcport)
            logpacket="y"
            if comments=="NULL":
                comments="[PORT]"
            else:
                comments=comments+"[PORT]"

        if (monsrcport != "N") and (monsrcportlist != None):
            for port in monsrcportlist:
                if int(port) == srcport:
                    print("[-]Logged| Source port: ",srcport," Destination port: ",destport)
                    logpacket="y"
                    if comments=="NULL":
                        comments="[PORT]"
                        break
                    else:
                        comments=comments+"[PORT]"
                        break
        if (monhostport != "N") and (monhostportlist != None):
            for port in monhostportlist:
                if int(port) == destport:
                    print("[-]Logged| Destination port: ",destport," Source port: ",srcport)
                    logpacket="y"
                    if comments=="NULL":
                        comments="[PORT]"
                        break
                    else:
                        comments=comments+"[PORT]"
                        break

        
        if monflags != "N" and monflagslist == None:
            if monflags in flags:
                logpacket="y"
                if comments=="NULL":
                    comments="[FLAG]"
                else:
                    comments=comments+"[FLAG]"
        if monflags != "N" and monflagslist != None:
            for flag in monflagslist:
                if flag in flags:
                    logpacket="y"
                    if comments=="NULL":
                        comments="[FLAG]"
                        break
                    else:
                        comments=comments+"[FLAG]"
                        break



    #============================================================================================================TCP COMPLETED FLAG FILTERING COMPLETED
                    
            
                                                                    #returns 443 if https
    if packet.haslayer(UDP) and packet[UDP] != None:                                          #IndexError: Layer [UDP] not found
        srcport=packet[UDP].sport
        destport=packet[UDP].dport
        protocol="UDP"
        if (monsrcport != "N") and (monsrcportlist == None) and (monsrcport == srcport):
            print("[-]Logged| Source port: ",srcport," Destination port: ",destport)
            logpacket="y"
            if comments=="NULL":
                comments="[PORT]"
            else:
                comments=comments+"[PORT]"
        if (monhostport != "N") and (monhostportlist == None) and (monhostport == destport):
            print("[-]Logged| Destination port: ",destport," Source port: ",srcport)
            logpacket="y"
            if comments=="NULL":
                comments="[PORT]"
            else:
                comments=comments+"[PORT]"
        if (monsrcport != "N") and (monsrcportlist != None):
            for port in monsrcportlist:
                if int(port) == srcport:
                    print("[-]Logged| Source port: ",srcport," Destination port: ",destport)
                    logpacket="y"
                    if comments=="NULL":
                        comments="[PORT]"
                        break
                    else:
                        comments=comments+"[PORT]"
                        break
        if (monhostport != "N") and (monhostportlist != None):
            for port in monhostportlist:
                if int(port) == destport:
                    print("[-]Logged| Destination port: ",destport," Source port: ",srcport)
                    logpacket="y"
                    if comments=="NULL":
                        comments="[PORT]"
                        break
                    else:
                        comments=comments+"[PORT]"
                        break




    #============================================================================================================
    #============================================================================================================PORT FILTERING COMPLETED
    #============================================================================================================
                




    #===========================================================================================================IF DEFAULTER

    if logpacket == "y":
        defaulterpackets+=1
        
        hexdump(packet)

        print("\n\nSource IP: ",srcip," Destination IP: ",destip,"\nSource port: ",srcport," Destination port: ",destport,"\nPacket length: ",packetlen," Packet TTL: ",packetttl," OS: ",os,
              "\nProtocol: ",protocol," Flags: ", flags,"\nDate: ",date," Time: ",time)
        
        insQuery= ("insert into packet"
        "(id, sourceip, destinationip, sourceport, destinationport, packetlength, packetttl, os, protocol, flags, date, time, comments)"
        "VALUES ('NULL', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

        dataQuery = (srcip, destip, srcport, destport, packetlen, packetttl, ose, protocol, flags, date, time, comments)

        cursor = con.cursor()
        cursor.execute(insQuery, dataQuery)
        con.commit()

        logpacket="n"

    #===========================================================================================================FILE OPERATIONS

    pkt=(srcip, destip,srcport,destport, ose, flags,protocol,packetttl,packetlen, date, time, comments)
    dire=parent+"\web\\data\\raw"
    with open(f"{dire}\{datef}.csv", "a") as file:
        if flag == 0:
            headers = ["Sourceip", "Destinationip", "Sourceport", "Destinationport" , "OS", "Flags","Protocol","TTL","Length", "Date", "Time", "Comments"]
            csv_writer = DictWriter(file, fieldnames=headers)
            csv_writer.writeheader()
            flag=1
        headers = ["Sourceip", "Destinationip", "Sourceport", "Destinationport","OS", "Flags","Protocol","TTL","Length", "Date", "Time", "Comments"]
        csv_writer = DictWriter(file, fieldnames=headers)
        csv_writer.writerow({"Sourceip": pkt[0], "Destinationip": pkt[1], "Sourceport": pkt[2],"Destinationport": pkt[3],"OS": pkt[4],"Flags": pkt[5], "Protocol": pkt[6], "TTL": pkt[7], "Length": pkt[8], "Date": pkt[9], "Time": pkt[10], "Comments": pkt[11]})
    
    print("===========================================================================")        
     
capture=sniff(prn=process_packet, store=False)



