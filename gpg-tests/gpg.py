# https://pythonhosted.org/python-gnupg/

# plik roboczy implementujący gnupg - docelowo te metody mają zostać wcielone w kod enigmy

import gnupg

gpg = gnupg.GPG(gnupghome="/home/czarny/PycharmProjects/enigma/gpg-tests")
gpg.encoding = "utf-8"

params = {
    'key_type': "RSA",
    'key_length': 1024,
    'Name-Real': 'maciek',
    'Name-Comment': '',
    'Name-Email': '',
    'Expire-Date': '',
    'Passphrase': 'sekret'
}

# generowanie klucza gpg
# RSA: https://pl.wikipedia.org/wiki/RSA_(kryptografia)
# input_data = gpg.gen_key_input(**params)
# key = gpg.gen_key(input_data)
# print(gpg.list_keys())
# keys = {
#     'keyid': key for keyid in gpg.list_keys()
# }
keyfile_path = '/home/czarny/PycharmProjects/enigma/gpg-tests/keyfile.asc'
message_path = '/home/czarny/PycharmProjects/enigma/gpg-tests/message'

# with open(keyfile_path, 'w') as file:
#     file.write(gpg.export_keys(str(key), secret=True, passphrase='sekret'))
#     file.write(gpg.export_keys(str(key)))
#
# with open(message_path, 'w') as file:
#     message = 'elo elo 3 2 0'
#     encrypted_message = gpg.encrypt(message, str(key))
#     file.write(str(encrypted_message))

# rng-tools - generowanie entropii dla kluczy, aby się szybciej generowały

# gpg.import_keys(open(''))

# import działa tylko, jeżeli klucza jeszcze nie ma w keyringu
key_data = open(keyfile_path).read()
imported_key = gpg.import_keys(key_data)
print(imported_key.fingerprints)
mesyg = open(message_path).read()
print(mesyg)
print("decrypted message:")
print(gpg.decrypt(mesyg, passphrase='sekret'))