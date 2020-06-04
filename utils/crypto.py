import struct
import sys
import xxtea
ACSII_A = 65
ACSII_Z = 90
ACSII_a = 97
ACSII_z = 122


class Crypto:
    """docstring for Crypto"""

    def __init__(self):
        super(Crypto, self).__init__()

    @staticmethod
    def have_encrypt(path, sign):
        bytesFile = open(path, "rb+")
        buff = bytesFile.read()
        pre_sign = str(buff[0:len(sign)])
        bytesFile.close()
        return pre_sign == sign

    @staticmethod
    def encrypt_file(path, key, sign):
        bytesFile = open(path, "rb+")

        buff = bytesFile.read()
        pre_sign = str(buff[0:len(sign)])
        if pre_sign == sign:
            print("have entrypt :" + path)
        else:
            print("entrypt file :" + path)
            encryBytes = xxtea.encrypt(buff, key)
            encryBytes = sign.encode("utf-8") + encryBytes
            bytesFile.seek(0)
            bytesFile.write(encryBytes)

        bytesFile.close()

    @staticmethod
    def encrypt_by_ascii(content, encode_key):
        new_content = ''
        debug = False
        index = 0
        for c in content:
            value = ord(c)
            # if c == '\\':
            #     new_content = new_content + str(chr(value))
            #     continue
            key_index = index % len(encode_key)
            key_bit_value = ord(encode_key[key_index])
            delt_value = 0
            # if debug:
            #     print c , encode_key[key_index], value, key_bit_value
            if key_bit_value >= ACSII_a and key_bit_value <= ACSII_z:
                delt_value = key_bit_value - ACSII_a
                pass
            elif key_bit_value >= ACSII_A and key_bit_value <= ACSII_Z:
                delt_value = key_bit_value - ACSII_A
                pass

            if value >= ACSII_a and value <= ACSII_z:
                value = value + delt_value
                if value > ACSII_z:
                    value = ACSII_a + (value - ACSII_z - 1)
                pass
            elif value >= ACSII_A and value <= ACSII_Z:
                value = value + delt_value
                if value > ACSII_Z:
                    value = ACSII_A + (value - ACSII_Z - 1)
                pass

            new_content = new_content + str(chr(value))
            index = index + 1
        return new_content

    @staticmethod
    def decrypt_by_ascii(content, encode_key):
        new_content = ''

        for x in range(0, len(content)):
            value = ord(content[x])

            key_index = x % len(encode_key)
            key_bit_value = ord(encode_key[key_index])
            delt_value = 0

            if key_bit_value >= ACSII_a and key_bit_value <= ACSII_z:
                delt_value = key_bit_value - ACSII_a
                pass
            elif key_bit_value >= ACSII_A and key_bit_value <= ACSII_Z:
                delt_value = key_bit_value - ACSII_A
                pass

            if value >= ACSII_a and value <= ACSII_z:
                value = value - delt_value
                if value < ACSII_a:
                    value = ACSII_z - (ACSII_a - value - 1)
                pass
            elif value >= ACSII_A and value <= ACSII_Z:
                value = value - delt_value
                if value < ACSII_A:
                    value = ACSII_Z - (ACSII_A - value - 1)
                pass

            new_content = new_content + str(chr(value))

        return new_content

    @staticmethod
    def encrypt_by_xor(content, encode_key):
        var = content.encode("utf-8")
        key = encode_key.encode("utf-8")
        i = 0
        ret = "".encode("utf-8")
        for b in var:
            k = key[i % len(key)]
            r = b ^ k
            bs = bytes([r])
            ret += bs
            # print("%s ^ %s = %s(%s)(%s)(%s)" % (b, k, r, chr(r), s, s2))
            # ret += str(chr(r))
            i += 1
        # print(ret2)
        return ret

    def encrypt_file_full(path, key):
        file = open(path, "rb+")
        buff = file.read()
        key_index = 0
        new_buff = '' + key

        for i in range(0, len(buff)):
            bit = chr(ord(buff[i]) ^ ord(key[i % len(key)]))
            # print i, str(ord(buff[i])) + ' => ' + str(ord(bit)), buff[i] + ' => ' + bit
            new_buff = new_buff + bit

        file.seek(0)
        file.write(len(key))
        file.write(key)
        file.write(new_buff)
        file.close()

    def decrypt_file_full(path, key):
        file = open(path, "rb+")
        buff = file.read()
        key_index = 0
        new_buff = ''

        for i in range(0, len(buff) - len(key)):
            bit = chr(ord(buff[i + len(key)]) ^ ord(key[i % len(key)]))
            # print i, str(ord(buff[i])) + ' => ' + str(ord(bit)), buff[i] + ' => ' + bit
            new_buff = new_buff + bit

        file.seek(0)
        file.write(new_buff)
        file.close()
