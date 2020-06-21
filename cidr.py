'''
    ===========================================================================
    Filename:       cidr.py
    Description:    Parses a CIDR block representation of a subnetwork
    Author:         Michael Kruzil (mkruzil@mikruweb.com) 
    Date Created:   1/17/2020 11:00 PM
    ===========================================================================
'''
import sys
import re

#Convert a decimal number to a binary octet string
def decimalToBinaryOctet(decimal):
   #Make sure the decimal is an int
   decimal = int(decimal)
   #Convert decimal number to binary number
   octet = bin(decimal)
   #Trim off the leading "0b"
   octet = octet[2:]
   #Add leading 0s as needed to fill in digits lost from trimming
   octet = octet.zfill(8)
   #Convert the binary octent to a string
   octet = str(octet)
   return octet

#Convert an array of bit strings into an array of binary octet strings
def bitsToBinaryOctets(bits):
    octets = []
    tmp = ""
    j = 1
    for i in range(0, ipv4_bits):
        tmp = tmp + str(bits[i])
        #If we have concatenated 8 bit strings (aka 1 octet)
        if (j == 8):
            #Store the octet in the octets array and clear out the tmp variable
            octets.append(tmp)
            tmp = ""
            #Reset the octet counter to 1
            j = 1
        else:
            #Increment the octet counter
            j = j + 1
    return octets

#Convert an array of binary octet strings into an IP address string
def binaryOctetsToDecimalAddress(octets):
    address = ""
    for x in octets:
       decimal = str(binaryOctetToDecimal(x))
       if not address:
          address = decimal
       else:
          address = address + "." + decimal
    return address

def binaryOctetToDecimal(octet):
    return int(octet, 2)

#Prompt the user for a CIDR representation of an IPv4 network block
#Example CIDR block = 149.166.11.7/23
prompt = 'Enter a CIDR block in the format x.x.x.x/x): '
if sys.version_info[0] < 3:
   cidr = raw_input(prompt)
else:
   cidr = input(prompt)

#Verify the input is in fact a CIDR block, and if not, exit
match = re.search("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2}$", cidr)
if match == None:
    print("Invalid CIDR block! Exiting...")
    exit()

#Number of bits in an IPv4 address
ipv4_bits = 32

#Split the CIDR block into a host address and subnet bits
tmp = cidr.split("/")
if len(tmp) == 2:
    cidr_address = tmp[0]
    cidr_bits = int(tmp[1])

#Convert the host address string into an array of decimal strings
host_decimals = cidr_address.split(".")

#Convert the host decimal array into a host bit array
host_bits = []
for x in host_decimals:
   octet = decimalToBinaryOctet(x)
   #Save each character in the octet string to an element in an array
   for x in octet:
      host_bits.append(x)

#Represent the subnet mask as an array of bits
subnet_bits = []
for i in range(ipv4_bits):
   if i < cidr_bits:
      subnet_bits.append(1)
   else: 
      subnet_bits.append(0)
   i = i + 1

#Perform a bitwise "and" between the host address bits and the subnet mask bits to get the network bits
network_bits = []
for i in range(ipv4_bits):
    network_bit = int(host_bits[i]) & int(subnet_bits[i])
    network_bits.append(network_bit)

#Calcuate the network address
network_octets = bitsToBinaryOctets(network_bits)
network_address = binaryOctetsToDecimalAddress(network_octets)

#Calcuate the subnet mask
subnet_octets = bitsToBinaryOctets(subnet_bits)
subnet_mask = binaryOctetsToDecimalAddress(subnet_octets)

#Reverse the subnet bits to get the host bits
#Alternate method = https://stackoverflow.com/questions/1779286/swapping-1-with-0-and-0-with-1-in-a-pythonic-way
host_bits = []
for x in subnet_bits:
   if (x == 0): 
      x = 1
   else:
      x = 0
   host_bits.append(x)

#Calculate the broadcast octets by adding the host decimals and network decimals together
broadcast_octets = []
host_octets = bitsToBinaryOctets(host_bits)
i = 0
for host_octet in host_octets:
    decimal = binaryOctetToDecimal(host_octet) + binaryOctetToDecimal(network_octets[i]) 
    octet = decimalToBinaryOctet(decimal)
    broadcast_octets.append(octet)
    i = i + 1

#Calculate the broadcast address
broadcast_address = binaryOctetsToDecimalAddress(broadcast_octets)

#Calculate the total number of hosts
#Total hosts = 2 to the power of the available host bits
bits_available_for_hosts = ipv4_bits - cidr_bits
total_hosts = 2**(bits_available_for_hosts)

if total_hosts > 2:

   #FIRST ADDRESS
   last_octet_pos = len(network_octets) - 1
   octet = network_octets[last_octet_pos] 
   decimal = binaryOctetToDecimal(octet) + 1
   network_octets[last_octet_pos] = decimalToBinaryOctet(decimal)
   first_address = binaryOctetsToDecimalAddress(network_octets)

   #LAST ADDRESS
   last_octet_pos = len(broadcast_octets) - 1
   octet = broadcast_octets[last_octet_pos] 
   decimal = binaryOctetToDecimal(octet) - 1
   broadcast_octets[last_octet_pos] = decimalToBinaryOctet(decimal)
   last_address = binaryOctetsToDecimalAddress(broadcast_octets)

   usable_hosts = total_hosts - 2

elif  total_hosts == 2:
   #192.168.1.0/31 = only two hosts: network and broadcast
   first_address = "NA"
   last_address = "NA"
   usable_hosts = 0
else:
   #192.168.1.0/32 = only one host, therefore cannot determine nature of network
   first_address = network_address
   last_address = broadcast_address
   network_address = "NA"
   broadcast_address = "NA"
   usable_hosts = 1

print("CIDR Block: " + cidr)
print("Subnet Mask: " + subnet_mask)
print("Network Address: " + network_address)
print("Broadcast Address: " + broadcast_address)
print("Usable hosts: " + str(usable_hosts))
print("Usable addresses: " + first_address + " to " + last_address)
