
def exponentiate(m, d, n):
    #m ^ d % n
    #get the length of binary representation of d
    binary = bin(d)[2:]
    length = len(binary)

    #get 1 and 0 array representation of binary d
    bits = [(d >> bit) & 1 for bit in range(length - 1, -1, -1)]

    #calculate the value quickly as shown in book
    curr = m
    for x in bits[1:]:
        if x == 0:
            curr = (curr * curr) % n
        elif x == 1:
            curr = (curr * curr) % n
            curr = (curr * m) % n

    return curr


if __name__ == '__main__':
    m = int(input('Enter m: '))
    d = int(input('Enter d: '))
    n = int(input('Enter n: '))
    res = exponentiate(m, d, n)
    print('result = ', res)