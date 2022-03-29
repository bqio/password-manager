from utils.iolib import Writer, Reader
from os import path

CONF_PATH = "secure.dat"


class Config:
    @staticmethod
    def load():
        reader = Reader(open(CONF_PATH, "rb"))
        passwords_count = reader.read_u16()
        passwords = []
        for _ in range(passwords_count):
            name_length = reader.read_u16()
            name = reader.read_str(name_length)
            password_length = reader.read_u16()
            password = reader.read_str(password_length)
            passwords.append({'name': name, 'value': password})
        reader.close()
        return passwords

    @staticmethod
    def save(passwords):
        writer = Writer(open(CONF_PATH, "wb"))
        writer.write_u16(len(passwords))
        for password in passwords:
            writer.write_u16(len(password['name']))
            writer.write_str(password['name'])
            writer.write_u16(len(password['value']))
            writer.write_str(password['value'])
        writer.close()

    @staticmethod
    def is_created():
        return path.exists(CONF_PATH)
