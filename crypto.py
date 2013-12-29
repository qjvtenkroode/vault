from Crypto.Cipher import AES
from Crypto import Random
import md5

def encrypt(passwd, raw):
    cipher, iv = getCipher(passwd)
    msg = iv + cipher.encrypt(raw)
    return msg

def decrypt(passwd, enc):
    cipher, iv = getCipher(passwd)
    msg = cipher.decrypt(enc)[AES.block_size:]
    return msg

def getCipher(passwd):
    key = md5.md5(passwd).hexdigest()
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    return (cipher, iv)

if __name__ == "__main__":
    import sys
    passwd = sys.argv[1]
    raw = b'Super secret message!'
    enc =  encrypt(b'test', raw)
    print "encrypted data: " + enc
    print "decrypted data: " + decrypt(passwd, enc)
