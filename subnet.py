import sys
import json
import operator

def get_netmaskbit(ip):
	for i in range(len(ip)):
		ip[i] = str(bin(int(ip[i])))[2:].zfill(8)
	ip = ip[0] + ip[1] + ip[2] + ip[3]
	for i in range(len(ip)):
		if ip[i] == '0':
			nbit = len(ip) - i
			break
	return nbit

def next_power_of_2(x):  
    return 1 if x == 0 else 2**(x - 1).bit_length()

def get_power(x):
	i = 0
	while 2**i < x:
		i += 1
	return i

def get_ip(ip):
	n1 = [] # list for current netmask
	word = ""
	for i in range(32):
		word += ip[i]
		if i%8 == 7:
			n1.append(int(word,2))
			word = ""
	return (str(n1[0]) + "." + str(n1[1]) + "." + str(n1[2]) + "." + str(n1[3]))

def get_netmask(n_hosts):
	ntma = ""
	for i in range(32 - n_hosts):
		ntma = ntma + "1"
	for i in range(32 - n_hosts,32):
		ntma = ntma + "0"
	return ntma

def get_netaddr(net_addr,n_hosts):
	ntad = ""
	for i in range(32 - n_hosts):
		ntad += net_addr[i]
	for i in range(32 - n_hosts,32):
		ntad += "0"
	return ntad

INP_FILE = sys.argv[1]
filept = open(INP_FILE,"r")

jFile = json.loads(filept.read())

net_addr = jFile["network_addr"]
subnets = jFile["subnets"]
netmask = jFile["netmask"]

net_addr = net_addr.split('.')
for i in range(len(net_addr)):
	net_addr[i] = str(bin(int(net_addr[i])))[2:].zfill(8)
net_addr = net_addr[0] + net_addr[1] + net_addr[2] + net_addr[3]

#print net_addr

netmask = netmask.split('.')
netmask_bits = get_netmaskbit(netmask)
no_of_hosts_possible = 2**netmask_bits

subnets = sorted(subnets.items(), key=operator.itemgetter(1), reverse=True)

#print subnets

final_subnets = {}
success = True

for x in subnets:
	if (x[1]+2) > no_of_hosts_possible:
		success = False
		break

	n_hosts = next_power_of_2(x[1]+2)
	n_bit = get_power(n_hosts)

	# Getting netmask
	ntma = get_netmask(n_bit)
	ntma = get_ip(ntma)

	#Getting network address, start address, end address & next address
	ntad = get_netaddr(net_addr,n_bit)
	ltad = str(bin(int(ntad,2) + int(str(bin(2**n_bit - 1))[2:],2)))[2:].zfill(32)
	net_addr = str(bin(int(ltad,2) + int("1",2)))[2:].zfill(32)
	ntad = get_ip(ntad)
	ltad = get_ip(ltad)
	total_host = n_hosts - 2

	no_of_hosts_possible -= n_hosts

	current_subnet = {"network_addr":ntad, "netmask":ntma, "start_addr":ntad, "end_addr":ltad, "total_host_count":total_host}
	final_subnets[x[0]] = current_subnet

output = {}
if success == False:
	output["success"] = False
else:
	output["success"] = True
	output["subnets"] = final_subnets

output = json.dumps(output) + "\n"
print output





	







