from hashlib import shake_128
import itertools
import sys
import random


def check_byte(num, name):
    """
  Checks if the input is a byte.  Name is used to report where the error is.
  """
    if type(num) != int or num < 0 or num > 255:
        raise Exception(name + ' is not a byte.')
        check_result = False
    else:
        check_result = True
    return check_result

def check_byte_list(list_to_check, length, name):
    """
  Checks if the provided list (list_to_check) is actually a list of bytes of the
  specified length.  If length is 0 then the list can be any length except *not*
  empty.  Name is used to report where the error is.
  """
    check_result = True
    if type(list_to_check) != list:
        raise TypeError(name + ' is not a list.')
        check_result = False
    elif length != 0 and len(list_to_check) != length:
        raise Exception(name + ' has ' + str(len(name)) +
                        ' entries instead of ' + str(length))
        check_result = False
    elif length == 0 and len(list_to_check) == 0:
        raise Exception(name + ' is empty.')
        check_result = False
    else:
        entry_name = 'entry of ' + name
        for j in list_to_check:
            if not check_byte(j, entry_name):
                check_result = False
    return check_result


def init(IV, k):
    """
  Initializes the stream cipher with input IV (the initial value), which is a list of
  256 entries, each of which is an integer from 0 to 255, and k, which is a list of
  some number of integers from 0 to 255.  Init returns a tuple (i, state), with i an 
  integer from 0 to 255 and state a list of 256 entries, each of which is itself a 
  number from 0 to 255.  These will comprise the internal state of the stream cipher.
  """
    # Look for errors in input format:
    check_byte_list(IV, 256, 'IV')
    check_byte_list(k, 0, 'key')
    # Initialize output variables:
    i = 0
    state = list(IV)
    # Apply key transformations to state:
    for j in k:
        if j > 0:
            for t in range(j):
                shift = state.pop(0)
                state.append(shift)

    return (i, state)


def next(i, state):
    """
  Produces a single byte from the stream cipher.  Takes as input a single number i
  between 0 and 255 and a state of 256 bytes.  It returns j, an updated value of i and 
  state following an x which is the product of the stream cipher.
  """
    # Look for errors in input format:
    check_byte_list(state, 256, 'state')
    check_byte(i, 'i')
    # Run next:
    x = state[i]
    j = (i + state[(i + 1) % 256]) % 256
    return (x, j, state)


def enc(IV, k, m):
    """
  Given input IV, the initial value (which should be a list of 256 random numbers 
  between 0 and 255), k, the key (a list of any length of numbers between 0 and 255), 
  and m, the message to be encrypted (given as a list of any length of numbers between
  0 and 255), returns a ciphertext c in the form of a list of numbers between 0 and
  255.
  
  Note that IV is supposed to be random; in principle, the enc function should be 
  generating it randomly itself, but I have put IV as an input for more flexibility.  
  The default length for k is 16 bytes, but the algorithm doesn't check or make use of 
  that.  The encrypt a text message, it should be first converted to a list of bytes,
  e.g., the ASCII encoding of the characters.
  """
    # Look for errors in input format:
    check_byte_list(IV, 256, 'IV')
    check_byte_list(k, 0, 'key')
    check_byte_list(m, 0, 'message')
    # Initialize stream cipher and ciphertext.  The ciphertext begins with the IV:
    (i, state) = init(IV, k)
    c = list(IV)
    # Get one byte from the stream cipher and use it to encode one byte of the message:
    for b in m:
        (x, i, state) = next(i, state)
        c.append((x + b) % 256)
    return c


def dec(k, c):
    """
  Takes as input k, the key (a list of any length of numbers between 0 and 255), and c,
  the ciphertext (a list of any length of numbers between 0 and 255).  Returns a
  message m (a list of numbers between 0 and 255) decrypted from the ciphertext with 
  that k.  
  """
    # Look for errors in input format:
    check_byte_list(k, 0, 'key')
    check_byte_list(c, 0, 'ciphertext')
    if len(c) <= 256:
        print('Error: ciphertext is too short.')
    # Determine IV, which is the first 256 bytes of the ciphertext:
    IV = c[0:256]
    # Initialize stream cipher and message list:
    (i, state) = init(IV, k)
    m = []
    # Decrypt by getting one byte at a time from the stream cipher:
    # We can start in the ciphertext at spot 256, after the IV is done
    for b in c[256:]:
        (x, i, state) = next(i, state)
        m.append((b - x) % 256)
    return m

def PRG_attack(IV, x):
    """ Complete this function! given an Initial Value [list of 256 bytes] to the Cipher `IV` and a byte stream `x` [list of bytes of variable length], return 1 if the `x` is random, and 0 if pseudorandom (generated by the stream cipher)."""
    # Your function should return 0 if x is an output of the stream cipher with that IV and some seed and 1 if x was generated by a random process.
    # do an init of the IV with x as k

    # we are given an output of init and next as x
    # x is some permutation of the IV based on the key.
    # our list of states is initialized as the list of IV
    # then is each state is shifted based on each entry of k

    # get dictionary of IV entries
    d = {}
    for k in IV:
        if d.get(k):
            d[k] += 1
        else:
            d[k] = 1
    for j in x:
        if d.get(j) == None:
            return 1
    
    return 0

def EAV_choose(length):
    """ Complete this function! Given a length, return two different messages (lists of bytes) of the given length."""
    m0 = ranListGen(length)
    m1 = ranListGen(length)

    
    # Your code here!
    return (m0, m1)

def EAV_attack(m0, m1, c):
    """ Complete this function! Given the two messages selected by you, and the ciphertext c, return 0 if the ciphertext is an encryption of the message m0, and 1 if the ciphertext is an encryption of the message m1 """
    # Your code here!
    # WILL NOT WORK IF IV CONTAINS ALL INTERGERS 0-255
    iv = c[0:256]
    s0 = derriveShiftSequnce(m0,c)
    s1 = derriveShiftSequnce(m1,c)

    # given the ciphertext, one of the sequences will contain an element not in the IV
    # in other words
    # the correct message will be the one with all shift sequence values in the IV
    # the wrong message will have a unique element in its shift sequence that is not in the IV

    for x in s0:
        if x not in iv:
            return 1 #s1
    for x in s1:
        if x not in iv:
            return 0 #s0

    #look at decrypt 
    return 0

def decrypt(m_list,c):
    """ Complete this function! Given a list m_list of possible messages and the ciphertext c, return i if the ciphertext is an encryption of m_list[i]."""
    # Determine IV, which is the first 256 bytes of the ciphertext:
    d = {}
    i = 0
    iv = c[0:256]
    p = []
    # map messages with valid squence to index
    for m in m_list:
        # they will all have unique shift sequences
        s = derriveShiftSequnce(m,c)
        if s != []:
            d[i] = s
        i += 1
    
    # for every shift sequence in the map
    for (k,s) in d.items():
        # check if we have a unique shift
        allin = True
        for x in s:
            if x not in iv:
                allin = False
        # append the index of the corresponding message/shift sequence
        if allin == True:
            p.append(k)
                
    return p[0]

def ranListGen(length):
    c = []
    for i in range(length):
        c.append(random.randint(0,255))
    return c

def stringToByteList(message):
    m = []
    for ele in message:
        m.append(ord(ele))
    return m

def derriveShiftSequnce(plaintext, ciphertext):
    """" Given the plaintext and ciphertext, we can obtain the sequence x found from iterations of next(i,state) """
    # plaintext_byte = ciphertext_byte - x(from stream) mod 256
    # we are solving for x 
    # x = 256 - plaintext_byte + ciphertext_byte
    if len(plaintext) != len(ciphertext[256:]):
        return []
    key = []
    c = ciphertext[256:]
    for i in range(len(plaintext)):
        key.append((256 - plaintext[i] + c[i])% 256)
    return key

#shits are the values of the states traversed through from enc 
#get shift sequence of both m1 and m2 compared to c. reverse shift c with both keys.
# IF ONE OF THE SHIFTS ARE NOT IN THE IV THEN THAT MESSAGE IS OUT



