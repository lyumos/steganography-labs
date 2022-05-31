import sys
from PIL import Image, ImageDraw
from math import *
global bitset

def usage():
    print('usage: python3 {} IMAGE MESSAGE'.format(sys.argv[0]))
    exit()

def letter_to_bitset(letter):
    bitset = bin(ord(letter))[2:]
    while len(bitset) < 8:
        bitset = '0' + bitset
    return bitset

def word_to_bitset(word):
    bitset = ''
    for letter in word:
        bitset += letter_to_bitset(letter)
    return bitset

def decrypt_bitset(bitset):
    word = ''
    for i in range(0, len(bitset), 8):
        letter = bitset[i:i+8]
        letter = int(letter, 2)
        word += chr(letter)
        if letter == 0:
            break
    return word

def dct(arr):
    res = []
    for p in range(8):
        line = []
        for q in range(8):
            if p == 0:
                ap = (1/8)**0.5
            else:
                ap = (2/8)**0.5
            if q == 0:
                aq = (1/8)**0.5
            else:
                aq = (2/8)**0.5
            sum = 0
            for i in range(8):
                for j in range(8):
                    sum += arr[i][j][0] * cos(pi * p * (2*i+1) / 16) * cos(pi * q * (2*j+1) / 16)

                line.append(round(sum*ap*aq))
        res.append(line)
    return res

def rev_dct(arr):
    res = []
    for i in range(8):
        line = []
        for j in range(8):
            sum = 0
            for p in range(8):
                for q in range(8):
                    if p == 0:
                        ap = (1 / 8) ** 0.5
                    else:
                        ap = (2 / 8) ** 0.5
                    if q == 0:
                        aq = (1 / 8) ** 0.5
                    else:
                        aq = (2 / 8) ** 0.5
                    sum += ap * aq * arr[p][q] * cos(pi * p * (2 * i + 1) / 16) * cos(pi * q * (2 * j + 1) / 16)
            line.append(round(sum))
        res.append(line)
    return res

def encrypt(image, width, height, pix):
    global bitset
    size = str(len(sys.argv[2:]))
    words = ' '.join(sys.argv[2:])
    words += '\0\0\0\0'
    bitset = word_to_bitset(words)
    draw = ImageDraw.Draw(image)
    for i in range(0, width, 8):
        for j in range(0, height, 8):
            block8x8 = block(pix, i, j)
            r_encrypt = encrypt_block(block8x8)
            for k in range(i, i + 8):
                for l in range(j, j + 8):
                    draw.point((k, l), (r_encrypt[k - i][l - j], block8x8[k - i][l - j][1], block8x8[k - i][l - j][2]))
    image.save('result.bmp', "BMP")

def encrypt_block(arr):
    global bitset
    if not len(bitset):
        return [[arr[i][j][0] for j in range(8)] for i in range(8)]
    dct_arr = dct(arr)
    for i in range(64):
        if not len(bitset):
            break
        if dct_arr[i // 8][i % 8] % 2 and bitset[0] == '0':
            dct_arr[i // 8][i % 8] -= 1
        elif not dct_arr[i // 8][i % 8] % 2 and bitset[0] == '1':
            dct_arr[i // 8][i % 8] += 1
        bitset = bitset[1:]
    return rev_dct(dct_arr)

def decrypt(width, height, pix):
    message = ''
    for i in range(0, width, 8):
        for j in range(0, height, 8):
            block8x8 = block(pix, i, j)
            message += decrypt_block(block8x8)
            if not ord(message[-1]):
                break
        if not ord(message[-1]):
            break
    return (word_to_bitset(message[:-1]))

def decrypt_block(arr):
    word = ''
    dct_arr = dct(arr)
    for line in dct_arr:
        bitset = ''
        for num in line:
            if num%2:
                bitset += '1'
            else:
                bitset += '0'
        letter = decrypt_bitset(bitset)
        word += letter
        if not ord(letter):
            break
    return word

def block(arr, x, y):
    res = []
    for i in range(8):
        line = [arr[x+i, y+j] for j in range(8)]
        res.append(line)
    return res

def main():
    if len(sys.argv) < 3:
        usage()
        return None
    bitset = word_to_bitset(' '.join(sys.argv[2:]))
    image = Image.open(sys.argv[1])
    width = image.size[0]
    height = image.size[1]
    pix = image.load()
    encrypt(image, width, height, pix)
    image = Image.open('result.bmp')
    pix = image.load()
    res_bitset = decrypt(width, height, pix)
    print('original -', bitset)
    print('result -', res_bitset)
    size = min(len(bitset), len(res_bitset))
    same = 0
    for i in range(size):
        if bitset[i] == res_bitset[i]:
            same += 1
    print('accuracy - ' + str(100 * same / size) + '%')
    RMSE_PSNR()

def RMSE_PSNR():
    src = sys.argv[1]
    res = 'result.bmp'
    image = Image.open(src)
    res_image = Image.open(res)
    pix = image.load()
    res_pix = res_image.load()
    width = image.size[0]
    height = image.size[1]
    MSE = 0
    PIXEL_MAX = 255.0
    for x in range(width):
        for y in range(height):
            r = pix[x, y][0]
            g = pix[x, y][1]
            b = pix[x, y][2]
            med = (r + g + b) / 3
            r1 = res_pix[x, y][0]
            g1 = res_pix[x, y][1]
            b1 = res_pix[x, y][2]
            med1 = (r1 + g1 + b1) / 3
            MSE += (med - med1)** 2
    MSE /= (width*height)
    if MSE == 0:
        print('Значение PSNR = inf')
        exit()
    RMSE = sqrt(MSE)
    PSNR = 20 * log10(PIXEL_MAX / RMSE)
    print('PSNR -', PSNR)
    print('RMSE -', RMSE)
    
if __name__ == '__main__':
main()