'''
    ===========================================================================
    Filename:       cidr.py
    Description:    Parses a CIDR block representation of a subnetwork
    Author:         Michael Kruzil (mkruzil@mikruweb.com) 
    Date Created:   1/17/2020 11:00 PM
    ===========================================================================
'''
import re

#Prompt user for CIDR representation of an IPv4 network block
#cidr = "149.166.11.7/23"
cidr = input('Enter a CIDR block in the format x.x.x.x/x): ')

match = re.search("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2}$", cidr)
if match == None:
    print("Invalid CIDR block! Exiting...")
    exit()

#Number of bits in an IPv4 address
ipv4_bits = 32

#Split CIDR block into host address and subnet bits
tmp = cidr.split("/")
if len(tmp) == 2:
    cidr_address = tmp[0]
    cidr_bits = int(tmp[1])

#Convert host address string into ints
host_ints = []
host_strs = cidr_address.split(".")
for x in host_strs:
   host_ints.append(int(x))

#Convert host ints into host bits
host_bits = []
for x in host_ints:
   #Convert int to byte
   byte = bin(x)
   #Trim off the leading "0b"
   byte = byte[2:]
   #Add leadding 0s if needed
   byte = byte.zfill(8)
   #Convert the byte to a string
   byte = str(byte)
   #Save each character in the string to an element in an array
   for x in byte:
      host_bits.append(x)

#Represent the subnet mask as bits
subnet_bits = []
for i in range(ipv4_bits):
   if i < cidr_bits:
      subnet_bits.append(1)
   else: 
      subnet_bits.append(0)
   i = i + 1

#Perform a bitwise "and" between host address bits and subnet mask bits to get the network bits
network_bits = []
for i in range(ipv4_bits):
    network_bit = int(host_bits[i]) & int(subnet_bits[i])
    network_bits.append(network_bit)

#Convert network bits into bytes
def charsToBytes(bits):
    bytes = []
    tmp = ""
    y = 1
    for i in range(0, ipv4_bits):
        tmp = tmp + str(bits[i])
        if (y == 8):
            bytes.append(tmp)
            tmp = ""
            y = 1
        else:
            y = y + 1
    return bytes

#Convert network bytes into an network address
def bytesToAddress(bytes):
    address = ""
    for x in bytes:
       if not address:
          address = str(int(x, 2))
       else:
          address = address + "." + str(int(x, 2))
    return address

#Calcuate the network address
network_bytes = charsToBytes(network_bits)
network_address = bytesToAddress(network_bytes)

#Calcuate the subnet mask
subnet_bytes = charsToBytes(subnet_bits)
subnet_mask = bytesToAddress(subnet_bytes)

#Reverse the subnet bits to get the host bits
host_bits = []
for x in subnet_bits:
   if (x == 0): 
      x = 1
   else:
      x = 0
   host_bits.append(x)

#Calculate the broadcast address
broadcast_address = ""
host_bytes = charsToBytes(host_bits)
i = 0
for host_byte in host_bytes:
    num = int(host_byte, 2) + int(network_bytes[i], 2) 
    if not broadcast_address:
        broadcast_address = str(num)
    else:
        broadcast_address += "." + str(num)
    i = i + 1

#Take 2 to the power of the available host bits
total_hosts = 2**(ipv4_bits - cidr_bits)

#Subtract the network address and broadcast address which are not usable
#Take the absolute value in the case this is a single /32 address
usable_hosts = abs(total_hosts - 2)

if usable_hosts > 1:
   #FIRST ADDRESS
   split_address = network_address.split(".")
   split_address[len(split_address) - 1] = str(int(split_address[len(split_address) - 1]) + 1)
   first_address = ""
   for x in split_address:
    if not first_address:
        first_address = str(x)
    else:
        first_address += "." + str(x)
  #LAST ADDRESS
   split_address = broadcast_address.split(".")
   split_address[len(split_address) - 1] = str(int(split_address[len(split_address) - 1]) - 1)
   last_address = ""
   for x in split_address:
    if not last_address:
        last_address = str(x)
    else:
        last_address += "." + str(x)
else:
   first_address = network_address
   last_address = broadcast_address

print("CIDR Block: " + cidr)
print("Subnet Mask: " + subnet_mask)
print("Network Address: " + network_address)
print("Broadcast Address: " + broadcast_address)
print("Usable hosts: " + str(usable_hosts))
print("Usable addresses: " + first_address + " through " + last_address)
