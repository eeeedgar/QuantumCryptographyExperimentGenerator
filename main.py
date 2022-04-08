from random import randint


def wordToCode(w):
    wLowerCase = w.lower()
    code = ''
    for s in wLowerCase:
        s_code = str(bin(ord(s) - ord('a')))
        s_code = s_code.split('b')[1]
        toAppend = 5 - len(s_code)

        sCode = ''
        for i in range(toAppend):
            sCode += '0'

        for i in s_code:
            sCode += i

        code += sCode

    return code



class AliceEveBob:
    def __init__(self, aBasis, aBit, eBasis, bBasis):
        self.aBasis = aBasis
        self.aBit = aBit

        self.eBasis = eBasis
        self.eBit = -1

        self.bBasis = bBasis
        self.bBit = -1


def experimentSimple(s):
    if s.bBasis == s.aBasis:
        s.bBit = s.aBit
    else:
        s.bBit = randint(0, 1)


def experimentInterception(s):
    if s.eBasis == s.aBasis:
        s.eBit = s.aBit
    else:
        s.eBit = randint(0, 1)

    if s.bBasis == s.eBasis:
        s.bBit = s.eBit
    else:
        s.bBit = randint(0, 1)


def AliceBobToString(s):
    return str(s.aBasis) + '\t' + str(s.aBit) + '\t' \
           + str(s.bBasis) + '\t' + str(s.bBit) + '\n'


def AliceEveBobToString(s):
    return str(s.aBasis) + '\t' + str(s.aBit) + '\t'\
           + str(s.eBasis) + '\t' + str(s.eBit) + '\t'\
           + str(s.bBasis) + '\t' + str(s.bBit) + '\n'


def getSimpleLabel():
    return 'Alice Basis\tAlice Bit\tBob Basis\tBob Bit\n'


def getInterceptionLabel():
    return 'Alice Basis\tAlice Bit\tEve Basis\tEve Bit\tBob Basis\tBob Bit\n'


def genetateAliceEveBob():
    aBasis = randint(0, 1)
    if aBasis == 0:
        aBasis = '+'
    else:
        aBasis = 'x'

    aBit = randint(0, 1)

    eBasis = randint(0, 1)
    if eBasis == 0:
        eBasis = '+'
    else:
        eBasis = 'x'

    bBasis = randint(0, 1)
    if bBasis == 0:
        bBasis = '+'
    else:
        bBasis = 'x'

    return AliceEveBob(aBasis, aBit, eBasis, bBasis)


def encodeWord(code, encryptionKey):
    encoded = ''
    for i in range(len(encryptionKey)):
        encoded += str(
            (int(encryptionKey[i]) + int(code[i])) % 2
        )

    return encoded


exp1 = []
exp1success = []
exp1counter = 0
exp1encryptionKey = ''

print("exp1:")

f = open('exp1.txt', 'w')

f.write(getSimpleLabel())

while len(exp1success) < 20 or exp1counter < 52:
    sy = genetateAliceEveBob()
    experimentSimple(sy)
    exp1.append(sy)

    if sy.bBit == sy.aBit and len(exp1success) < 20:
        exp1success.append(sy)

    exp1counter += 1


for e in exp1:
    f.write(AliceBobToString(e))

# f.write(str(len(exp1success)) + '\n')

for e in exp1success:
    exp1encryptionKey += str(e.bBit)
    # f.write(str(e.bBit) + '\t')

f.close()

print('encryption key:')
print(exp1encryptionKey)

print('Enter 4-symbol word')

word = input()

code = wordToCode(word)

print('origin code:')
print(code)

print('encoded word:')
print(encodeWord(code, exp1encryptionKey))


exp2 = []
exp2success = []
n = 52

f = open('exp2.txt', 'w')

f.write(getInterceptionLabel())

for i in range(n):
    s = genetateAliceEveBob()
    experimentInterception(s)
    exp2.append(s)

    if s.bBasis == s.aBasis:
        exp2success.append(s)

for e in exp2:
    f.write(AliceEveBobToString(e))
f.close()

exp2errors = 0

for e in exp2success:
    if e.bBit != e.aBit:
        exp2errors += 1

print('exp 2:')
print('bases matches:', len(exp1success))
print('errors:', exp2errors)
