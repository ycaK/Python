"""
Program which can provide password generation and password decryption using bruteforce and dictionary attack
Needs to specify alphabet and length to generate passwords, algorythm and hash is only required for attacks
Author: Kacy538 (ycak)
"""

import hashlib
import itertools


class bruteGen(object):
    def __init__(self, alphabet, length, algorythm=None, hash=None):
        self.alphabet = alphabet
        self.length = length
        self.algorythm = algorythm
        self.hash = hash
        self.done = False

    def gen_passwords(self):  # Password generator
        try:
            for pw in itertools.product(self.alphabet, repeat=self.length):
                yield pw
        except:
            return 'Error GEN_PASSWORDS'

    def unhash(self):  # Bruteforces hash to plain text with provided hash, algorythm and passwords
        if self.hash != None:
            try:
                for guess in self.gen_passwords():
                    if hashlib.new(self.algorythm, ''.join(guess).encode()).hexdigest() == self.hash:
                        return ''.join(guess)
                return 'Password not found'
            except:
                return 'Wrong hash type'
        else:
            return 'Need to set hash!'

    def unhash_from_dict(self, dict_name):
        try:
            with open(dict_name, 'r') as dict:
                for guess in dict.readlines():
                    if hashlib.new(self.algorythm, guess.replace('\n', '').encode()).hexdigest() == self.hash:
                        return guess.replace('\n', '')
                return 'Password not found!'
        except:
            return 'Dictionary Error (FILE ERROR)'


"""

#  Examples  #

alphabet = "abcdefghijklmnopqrstuvwxyz"  # DATA: Letters of alphabet in lower
password_length = 3  # DATA length: ???
hash = 'a5f45d41e85cad7ec07bd10b4d4b56a8155e9ea9ea454064bdce2c8f5065f298'  # SHA256 -> r'zyz'


bruter = bruteGen(alphabet=alphabet,  # Alphabet to be used by password generator
                  length=password_length,  # Password length for password generator
                  hash=hash,  # If the unhash function isn't used it may be skiped
                  algorythm='sha256')  # If the unhash function isn't used it may be skiped

print("Password: {}".format(bruter.unhash_from_dict('ex.dict')))  # ex.dict contains only 3 letter long passwords for testing

print("Password: {}".format(bruter.unhash())) # Decrypts password using bruteforce attack

"""