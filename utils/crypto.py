import struct
import sys
ACSII_A = 65
ACSII_Z = 90
ACSII_a = 97
ACSII_z = 122

_DELTA = 0x9E3779B9


def _long2str(v, w):
    n = (len(v) - 1) << 2
    if w:
        m = v[-1]
        if (m < n - 3) or (m > n):
            return ''
        n = m
    s = struct.pack('<%iL' % len(v), *v)
    return s[0:n]


def _str2long(s, w):
    n = len(s)
    m = (4 - (n & 3) & 3) + n
    s = s.ljust(m, "\0")
    v = list(struct.unpack('<%iL' % (m >> 2), s))
    if w:
        v.append(n)
    return v


class Crypto:
    """docstring for Crypto"""

    def __init__(self):
        super(Crypto, self).__init__()

    @staticmethod
    def encrypt_by_xxtea(str, key):
        if str == '':
            return str
        v = _str2long(str, True)
        k = _str2long(key.ljust(16, "\0"), False)
        n = len(v) - 1
        z = v[n]
        y = v[0]
        sum = 0
        q = 6 + 52 // (n + 1)
        while q > 0:
            sum = (sum + _DELTA) & 0xffffffff
            e = sum >> 2 & 3
            for p in range(n):
                y = v[p + 1]
                v[p] = (v[p] + ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4)
                                ^ (sum ^ y) + (k[p & 3 ^ e] ^ z))) & 0xffffffff
                z = v[p]
            y = v[0]
            v[n] = (v[n] + ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4)
                            ^ (sum ^ y) + (k[n & 3 ^ e] ^ z))) & 0xffffffff
            z = v[n]
            q -= 1
        return _long2str(v, False)

    @staticmethod
    def decrypt_by_xxtea(str, key):
        if str == '':
            return str
        v = _str2long(str, False)
        k = _str2long(key.ljust(16, "\0"), False)
        n = len(v) - 1
        z = v[n]
        y = v[0]
        q = 6 + 52 // (n + 1)
        sum = (q * _DELTA) & 0xffffffff
        while (sum != 0):
            e = sum >> 2 & 3
            for p in range(n, 0, -1):
                z = v[p - 1]
                v[p] = (v[p] - ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4)
                                ^ (sum ^ y) + (k[p & 3 ^ e] ^ z))) & 0xffffffff
                y = v[p]
            z = v[n]
            v[0] = (v[0] - ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4)
                            ^ (sum ^ y) + (k[0 & 3 ^ e] ^ z))) & 0xffffffff
            y = v[0]
            sum = (sum - _DELTA) & 0xffffffff
        return _long2str(v, True)

    @staticmethod
    def have_encrypt(path, sign):
        bytesFile = open(path, "rb+")
        buff = bytesFile.read()
        pre_sign = str(buff[0:len(sign)])
        bytesFile.close()
        return pre_sign == sign

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
