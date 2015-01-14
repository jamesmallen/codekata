# This Python file uses the following encoding: utf-8

# Bloom filters are very simple. Take a big array of bits, initially all zero.
# Then take the things you want to look up (in our case we’ll use a dictionary of
# words). Produce ‘n’ independent hash values for each word. Each hash is a
# number which is used to set the corresponding bit in the array of bits.
# Sometimes there’ll be clashes, where the bit will already be set from some
# other word. This doesn’t matter.
#
# To check to see of a new word is already in the dictionary, perform the same
# hashes on it that you used to load the bitmap. Then check to see if each of the
# bits corresponding to these hash values is set. If any bit is not set, then you
# never loaded that word in, and you can reject it.
#
# The Bloom filter reports a false positive when a set of hashes for a word all
# end up corresponding to bits that were set previously by other words. In
# practice this doesn’t happen too often as long as the bitmap isn’t too heavily
# loaded with one-bits (clearly if every bit is one, then it’ll give a false
# positive on every lookup). There’s a discussion of the math in Bloom filters at
# www.cs.wisc.edu/~cao/papers/summary-cache/node8.html.
#
# So, this kata is fairly straightforward. Implement a Bloom filter based spell
# checker. You’ll need some kind of bitmap, some hash functions, and a simple
# way of reading in the dictionary and then the words to check. For the hash
# function, remember that you can always use something that generates a fairly
# long hash (such as MD5) and then take your smaller hash values by extracting
# sequences of bits from the result. On a Unix box you can find a list of words
# in /usr/dict/words (or possibly in /usr/share/dict/words). For others, I’ve
# put a word list up here.1
#
# Play with using different numbers of hashes, and with different bitmap sizes.
#
# Part two of the exercise is optional. Try generating random 5-character words
# and feeding them in to your spell checker. For each word that it says it OK,
# look it up in the original dictionary. See how many false positives you get.

from hashlib import md5
from random import randint
# md5 returns a 128-bit hash (32 hex digits)


BYTES_PER_HASH = 3
BITMAP_SIZE = int('FF' * BYTES_PER_HASH, 16) + 1 # 16-bit hash (4 hex digits)

WORD_LIST = '/usr/share/dict/words' # location on Mac
# WORD_LIST = 'words.txt'

bitmap = [False] * BITMAP_SIZE
word_set = set()

def main():
    """Test out bloom method using random 5-character words"""
    
    ITERATIONS = 1000
    false_pos = 0
    for i in range(ITERATIONS):
        w = random_word(5)
        if lookup_word(w) and not w in word_set:
            false_pos += 1
    
    print "%d/%d false positives (%.2f%%)" % (false_pos, ITERATIONS, float(false_pos)/ITERATIONS*100)
    

def random_word(length):
    word = ""
    for i in range(length):
        word += chr(ord('a') + randint(0, 25))
    
    return word

def md5_word(w):
    return md5(w).hexdigest()
    

def add_word(w):
    word_hash = md5_word(w)
    for i in range(0, len(word_hash), BYTES_PER_HASH * 2):
        small_hash = word_hash[i:i + BYTES_PER_HASH * 2]
        idx = int(small_hash, 16)
        
        #print idx
        
        bitmap[idx] = True
    
    if __name__ == '__main__':
        word_set.add(w)


def lookup_word(w):
    word_hash = md5_word(w)
    for i in range(0, len(word_hash), BYTES_PER_HASH * 2):
        small_hash = word_hash[i:i + BYTES_PER_HASH * 2]
        idx = int(small_hash, 16)
        
        #print idx
        
        if not bitmap[idx]:
            return False
    
    # if we reach here, all small hashes passed
    return True
    

# load default dictionary
with open(WORD_LIST, 'r') as f:
    for line in f:
        add_word(line.strip())


if __name__ == '__main__':
    main()
        
    