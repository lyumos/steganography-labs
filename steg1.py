import sys
def create_default_text(filename):
    default_text = 'default_' + filename
    try:
        f1 = open(default_text, 'r')
    except FileNotFoundError:
        f1 = open(default_text, 'w')
        cp_text(filename, default_text)

def usage():
    print('usage: python3 {} FILENAME ENCRYPTION_METHOD(1 - 3) [WORD]'.format(sys.argv[0]))
    exit()
def cp_text(src, dest):
    f1 = open(src, 'r')
    f2 = open(dest, 'w')
    f2.write(f1.read())
    f1.close
    f2.close
def letter_to_bitset(letter):
    bitset = bin(ord(letter))[2:]
    while len(bitset) < 16:
        bitset = '0' + bitset
    return bitset
def word_to_bitset(word):
    bitset = ''
    for letter in word:
        bitset += letter_to_bitset(letter)
    return bitset
def encrypt1(filename, word):
    text = open(filename, 'w')
    default = open('default_' + filename, 'r')
    bitset = word_to_bitset(word)
    for char in default.read():
        if len(bitset) == 0:
            text.write(char)
        elif char == 'а' and bitset[0] == '0':
            text.write('a')
            bitset = bitset[1:]
        elif char == 'р' and bitset[0] == '1':
            text.write('p')
            bitset = bitset[1:]
        else:
            text.write(char)

    text.close
    default.close
def encrypt2(filename, word):
    text = open(filename, 'w')
    default = open('default_' + filename, 'r')
    bitset = word_to_bitset(word)
    deftext = default.read()
    default.close
    for i in range(len(deftext)):
        if len(bitset) == 0 or deftext[i] != '\n':
            text.write(deftext[i])
            continue
        else:
            text.write(' ')
            if bitset[0] == '1':
                text.write(' ')
            bitset = bitset[1:]
            text.write('\n')

    text.close


def encrypt3(filename, word):
    text = open(filename, 'w')
    default = open('default_' + filename, 'r')
    bitset = word_to_bitset(word)
    for char in default.read():
        if (char == '-' or ord(char) == 8212) and len(bitset) != 0:
            if bitset[0] == '1':
                text.write(chr(8212))
            else:
                text.write('-')
            bitset = bitset[1:]
        else:
            text.write(char)

    text.close
    default.close

def decrypt_bitset(bitset):
    word = ''
    for i in range(0, len(bitset), 16):
        letter = bitset[i:i + 16]
        letter = int(letter, 2)
        if letter == 0:
            break
        word += chr(letter)
    print(word)


def decrypt1(filename):
    text = open(filename, 'r')
    bitset = ''
    for char in text.read():
        if char == 'a':
            bitset += '0'
        if char == 'p':
            bitset += '1'
    decrypt_bitset(bitset)


def decrypt2(filename):
    f = open(filename, 'r')
    text = f.read()
    bitset = ''
    for i in range(len(text)):
        if text[i] == '\n':
            if text[i - 2] == ' ':
                bitset += '1'
            else:
                bitset += '0'
    decrypt_bitset(bitset)


def decrypt3(filename):
    text = open(filename, 'r')
    bitset = ''
    for char in text.read():
        if char == '-':
            bitset += '0'
        if ord(char) == 8212:
            bitset += '1'
    decrypt_bitset(bitset)

ac = len(sys.argv)
if ac != 3 and ac != 4:
    usage()
filename = sys.argv[1]
method_num = sys.argv[2]
create_default_text(filename)
if ac == 4:
    word = sys.argv[3]
    if method_num == '1':
        encrypt1(filename, word)
    elif method_num == '2':
        encrypt2(filename, word)
    elif method_num == '3':
        encrypt3(filename, word)
    else:
        usage()
elif ac == 3:
    if method_num == '1':
        decrypt1(filename)
    elif method_num == '2':
        decrypt2(filename)
    elif method_num == '3':
        decrypt3(filename)
    else:
        usage()
else:
    usage()
