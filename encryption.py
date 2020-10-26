from cryptography import fernet
import json


class Encryption():

    def gen_key(self):
        return fernet.Fernet.generate_key()

    def encryptMsg(self, msg, key, username="Anonymous", clientId=None):
        encryptionType = fernet.Fernet(key)

        msg = {
               "msg": msg,
               "code": 1234,
               "username": username,
               "clientId": clientId
               }
        msg = json.dumps(msg)
        msg = msg.encode("utf-8")
        msg = encryptionType.encrypt(msg)

        return msg

    def decryptMsg(self, msg, key):
        encryptionType = fernet.Fernet(key)

        msg = encryptionType.decrypt(msg)
        # msg = msg.decode("utf-8")
        msg = json.loads(msg)
        return msg
