import sys
from PIL import Image, ImageDraw

def usage():
    print('usage: python3 {} IMAGE [TEXT_FILE WORD_COUNT]'.format(sys.argv[0]))
    exit()
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
def decrypt_bitset(bitset):
    word = ''
    for i in range(0, len(bitset), 16):
        letter = bitset[i:i + 16]
        letter = int(letter, 2)
        if letter == 0:
            break
        word += chr(letter)
    print(word)
def encrypt(image, width, height, pix):
    f = open(sys.argv[2])
    words = f.read().split()[:int(sys.argv[3])]
    bitset = word_to_bitset(words[0])
    for word in words[1:]:
        bitset += word_to_bitset(' ' + word)
    draw = ImageDraw.Draw(image)
    for i in range(width):
        for j in range(height):
            r = bin(pix[i, j][0])[2:-1] + "0"
            g = bin(pix[i, j][1])[2:-1] + "0"
            b = bin(pix[i, j][2])[2:-1] + "0"
            if len(bitset) != 0:
                r = r[:-1] + bitset[0]
                bitset = bitset[1:]
                if len(bitset) != 0:
                    g = g[:-1] + bitset[0]
                    bitset = bitset[1:]
                    if len(bitset) != 0:
                        b = b[:-1] + bitset[0]
                        bitset = bitset[1:]

            r = int(r, 2)
            g = int(g, 2)
            b = int(b, 2)
            draw.point((i, j), (r, g, b))

    image.save(sys.argv[1].split('.')[0] + sys.argv[3] + ".bmp", "BMP")
def decrypt(image, width, height, pix):
    bitset = ''
    for i in range(width):
        for j in range(height):
            r = bin(pix[i, j][0])[2:]
            g = bin(pix[i, j][1])[2:]
            b = bin(pix[i, j][2])[2:]
            bitset += r[-1:] + g[-1:] + b[-1:]
    decrypt_bitset(bitset)

ac = len(sys.argv)
if ac != 2 and ac != 4:
    usage()
image = image.open(sys.argv[1])
width = image.size[0]
height = image.size[1]
pix = image.load()
if ac == 4:
    encrypt(image, width, height, pix)
else:
    decrypt(image, width, height, pix)