'''
UDP Header:-
Requires the following fields:
Source IP address
Destination IP address
Reserved UDP Protocol Numbrt
Length of pseudo header

Source Port
Dest Port
UDP Length
UDP Data
'''

import math

#used to deal with overflows and use them as a carry around
def ModifyCarry(z):
    if z >= 2**16:
        z -= 2**16
        z += 1
        # print(z)
        # print(bin(z))

    return z

def onesComplement(n): 
    # Find number of bits in 
    # the given integer 
    number_of_bits = (int)(math.floor(math.log(n) /
                                math.log(2))) + 1; 
  
    # XOR the given integer with poe(2,  
    # number_of_bits-1 and print the result  
    return ((1 << number_of_bits) - 1) ^ n; 

def ChecksumCalculation(source_ip,destination_ip,protocol,length,source_port,dest_port,udp_length,data):
    z = 0

    #calculation of adding respective parts of the source IP address
    #only 16 bits can be added at once, so the IP address is split into two halfs and are added
    #so, if I have the IP a.b.c.d, then I do: ab + cd where ab corresponds to the binary 16 bits tring of a and b concatenated together
    #similarly for cd as well
    #x represents the sum of the last 16 bits of the binary number
    # print("Part-1")
    res = source_ip.split('.')

    x = int(res[1]) + int(res[3]) #x = b + d
    y = int(res[0]) + int(res[2]) #y = a + c
    y = y*256

    z = x+y
    # print(z)
    # print(bin(z))
    z = ModifyCarry(z) #after every addition, we have to check whether there has been an oveflow or not

    #calculation of adding respective parts of the destination IP address
    # print("Part-2")
    res = destination_ip.split('.')

    x = int(res[1]) + int(res[3])
    y = int(res[0]) + int(res[2])

    y = y*256
    z = z+x+y
    # print(z)
    # print(bin(z))
    z = ModifyCarry(z)

    # print("Part-3")
    z += int(protocol)  #adding the protocol number
    # print(z)
    # print(bin(z))
    z = ModifyCarry(z)
    

    # print("Part-4")
    z += int(length) #adding the length of the pseudo-header
    # print(z)
    # print(bin(z))
    z = ModifyCarry(z)

    # print("Part-5")
    z += int(source_port) #adding the source port number
    # print(z)
    # print(bin(z))
    z = ModifyCarry(z)

    # print("Part-6")
    z += int(dest_port) #adding the destination port number
    # print(z)
    # print(bin(z))
    z = ModifyCarry(z)

    # print("Part-7")
    z += int(udp_length) #adding the length of the UDP header
    # print(z)
    # print(bin(z))
    z = ModifyCarry(z)

    # print()
    # print("Part-8")
    #adding the data sent
    for i in range(0,len(data)):
        # print("Presently at ",data[i]," , that is: ",ord(data[i]))
        if i%2 == 0:
            temp = ord(data[i])
            temp = temp * 2**8
            z += temp
        else:
            temp = ord(data[i])
            z += temp
        # print(z)
        # print(bin(z))
        ModifyCarry(z)

    checksum = onesComplement(z)
    # print(checksum)
    # print(bin(checksum))

    return checksum

#used to verify whether the computed checksum is right or wrong.
#this will be called on the receiver's side
#contains same parameters as ChecksumCalculation + checksum which was computed
def ChecksumVerification(source_ip,destination_ip,protocol,length,source_port,dest_port,udp_length,data,checksum):
    val = ChecksumCalculation(source_ip,destination_ip,protocol,length,source_port,dest_port,udp_length,data)
    if val == checksum:
        return 1
    else:
        return 0

if __name__ == '__main__':
    print("Hello")
    checksum = ChecksumCalculation('192.168.0.31','192.168.0.30',17,10,20,10,10,'Hi') #calculates the checksum
    print()
    ChecksumVerification('192.168.0.31','192.168.0.30',17,10,20,10,10,'Hi',checksum) #verifies the checksum
    print("Checksum = ",bin(checksum))
    #checksum = 0011 0101 1100 0101