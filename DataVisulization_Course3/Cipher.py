

# Part 1 - Use a dictionary that represents a substition cipher to
# encrypt a phrase

# Example of a cipher dictionary 26 lower case letters plus the blank
CIPHER_DICT = {'e': 'u', 'b': 's', 'k': 'x', 'u': 'q', 'y': 'c', 'm': 'w', 'o': 'y', 'g': 'f', 'a': 'm', 'x': 'j', 'l': 'n', 's': 'o', 'r': 'g', 'i': 'i', 'j': 'z', 'c': 'k', 'f': 'p', ' ': 'b', 'q': 'r', 'z': 'e', 'p': 'v', 'v': 'l', 'h': 'h', 'd': 'd', 'n': 'a', 't': ' ', 'w': 't'}

def encrypt(phrase, cipher_dict):
    """
    Take a string phrase (lower case plus blank)
    and encypt it using the dictionary cipher_dict
    """
    encryptedString=""
    DCIPHER_DICT={}
    for charchter in phrase:
        if CIPHER_DICT.get(charchter)!= None:
            encryptedString+=CIPHER_DICT.get(charchter)

    return encryptedString
# Tests
#print("Output for part 1")
#print(encrypt("pig", CIPHER_DICT))
#print(encrypt("hello world", CIPHER_DICT))
#print()


# Output for part 1
#vif
#hunnybtygnd



def make_decipher_dict(cipher_dict):
    """
    Take a cipher dictionary and return the cipher
    dictionary that undoes the cipher
    """

    decipher_dict={}
    for letter in cipher_dict:
        decipher_dict[cipher_dict[letter]]=letter

    return decipher_dict
CIPHER_DICT = {'e': 'u', 'b': 's', 'k': 'x', 'u': 'q', 'y': 'c', 'm': 'w', 'o': 'y', 'g': 'f', 'a': 'm', 'x': 'j', 'l': 'n', 's': 'o', 'r': 'g', 'i': 'i', 'j': 'z', 'c': 'k', 'f': 'p', ' ': 'b', 'q': 'r', 'z': 'e', 'p': 'v', 'v': 'l', 'h': 'h', 'd': 'd', 'n': 'a', 't': ' ', 'w': 't'}

#print(make_decipher_dict(CIPHER_DICT))

import random

def make_cipher_dict(alphabet):
    """
    Given a string of unique characters, compute a random
    cipher dictionary for these characters
    """
    shuffelist=['a','b','c','d','q','w','e','r','t','y','u','i','o','p']
    cipher_dict={}
    for character in alphabet:
        shuffeledChar = random.sample(shuffelist,1)
        #print(shuffeledChar)
        cipher_dict[character]=shuffeledChar
    return cipher_dict

print(make_cipher_dict("cat"))
print(make_cipher_dict("abcdefghijklmnopqrstuvwxyz "))