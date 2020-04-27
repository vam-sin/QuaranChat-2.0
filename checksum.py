'''
Fields Required in Checksum:
0-3 bits: Version of the protocol (fixed)
            It'll be a constant value = 4
4-7 bits: Header Length = 5 (fixed)
8-15 bits: There are sub-parts
            8 - 10 bits are precedence bits and are now ignored (hence, can be fixed)
                000 (0) - Routine
                001 (1) - Priority
                010 (2) - Immediate
                011 (3) - Flash
                100 (4) - Flash Override
                101 (5) - Critical
                110 (6) - Internetwork Control
                111 (7) - Network Control
            11 - 14 bits represent the service; 4 types of service
                (11) Delay - when set to '1' the packet requests low delay.
                (12) Throughout - when set to '1' the packet requests high throughput.
                (13) Reliability - when set to '1' the packet requests high reliability.
                (14) Cost - when set to '1' the packet has a low cost.
            15 is unused, its always 0 (0)
16-31 bits: Gives the total length data. Specify as you please (fixed, I'm not sure)
32-47 bits: Identification. It is incremented when a value is sent from source to destination. Works as a sequenc number(important, increments by 1, sequence number?)
48-50 bits: Flag. 
            48 is left reserved
            49: If the values is 1, then IP datagram is never fragmented
            50: If it is set to 1, then represents fragmented datagram coming after it
51-63 bits: Useful if data is fragmented. Represents offset from start of datagram
64-71 bits: Represents TTL. Value typically set to be 32 or 64.
            At every hop, decremented by 1
            When it becomes 0, datagram is discarded
72-79 bits: Represents transport layer protocol (fixed)
80-95 bits: Header checksum. 
96-127 bits: source IP address
128-159 bits: destination IP address
160-191 bits: Other variable stuff like options, padding, not sure how the actual data sent fits into this
'''

def checksum(x):
    ip_address = str(x)

    n = 4
    strings = [ip_address[i:i+n] for i in range(0, len(ip_address), n)]
    print(strings)
    print("Length of the list is = ",len(strings))

    temp = 0
    for i in range(0,len(strings)):
        an_integer = int(strings[i], 16)
        print(an_integer)
        temp += an_integer
    
    ans = hex(temp)
    print(ans)

if __name__ == '__main__':
    print("Hello")

    x = "10"
    y = int(x, 16)
    print(y)

    input = "45000073000040004011b861c0a80001c0a800c7"
    checksum(input)
