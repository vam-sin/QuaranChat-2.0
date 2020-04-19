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