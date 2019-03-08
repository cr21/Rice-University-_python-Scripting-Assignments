import random
def count_letters(word_list):
    """ See question description """

    ALPHABET = "abcdefghijklmnopqrstuvwxyz"

    letter_count = {}
    for letter in ALPHABET:
        letter_count[letter] = 0

    for word in word_list:
        for c in word:
            letter_count[c]=letter_count.get(c,0)+1

    for idx in letter_count.keys():
        print(idx, letter_count[idx])


monty_quote = "listen strange women lying in ponds distributing swords is no basis for a system of government supreme executive power derives from a mandate from the masses not from some farcical aquatic ceremony"

monty_words = monty_quote.split(" ")



#count_letters(monty_words)

"""
Template for part 1
Using substitution ciphers to encrypt and decrypt plain text
"""
