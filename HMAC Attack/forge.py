# This is the framework file for your programming assignment. Complete the three functions selective_forge, universal_forge and md_forge towards the bottom of the file and upload to Gradescope.

#------------------CODE FOR MAC------------------------------------
KEY_ROWS = KEY_COLS = 16

def MAC_check(msg):
    if (type(msg) != tuple or len(msg) != 2): 
        raise Exception("Input msg must be a tuple of length 2")
    if (type(msg[0])!=int or type(msg[1])!=int):
        raise Exception("Elements of the tuple must be integers")
    if (not(0<=msg[0]<KEY_ROWS and 0<=msg[1]<KEY_COLS)): 
        raise Exception(f"The msg must be of the form (m, n) where 0<=m<{KEY_ROWS} and 0<=n<{KEY_COLS}") 
    


def sample_MAC(msg):
    MAC_check(msg)
    key = [[(i+(10*j))%101 for i in range(KEY_COLS)] for j in range(KEY_ROWS)]

    m, n = msg 
    s, t = (0, 0)

    for row in key[:m+1]:
        s+=row[n]

    for element in key[m][:n+1]:
        t+= element 

    return (s, t)
#---------------------------------------------------------------------
#---------------------CODE FOR HASH-AND-MAC---------------------------

def MD_check(msg):
    if (type(msg) != list or len(msg) > 2**16): 
        raise Exception("Input msg must be a list of length less than 2**16") 
    for i in msg:
        if (type(i) != int or not(0<=i<256)):
            raise Exception("Elements must be integers between 0 and 255, both inclusive")
   

def MD_pad(msg):
    ln = len(msg)
    num_zeros = (6 - ((ln+3)%6))%6
    pad = msg + [1] + [0 for i in range(num_zeros)] + [ln//256, ln%256]
    return pad

def MD_hash(pad):
    def h(x, z):
        new_z = [0] * 6
        for i in range(6):
            new_z[i] = ((z[i]*x[i])%256 + x[(i+1)%6])%256
        return new_z
    
    z = [17 for i in range(6)]

    for i in range(len(pad)//6):
        z = h(pad[i*6:i*6+6], z)    
    return z


def MD_tag(hash):
    tag = [0] * 6
    for i in range(6):
        tag[i] = sample_MAC((hash[i]//16, hash[i]%16))
    return tag

def sample_MD(msg):
    MD_check(msg)

    pad = MD_pad(msg)
    hash = MD_hash(pad)
    tag = MD_tag(hash)
    return (hash,tag)

#-----------------------------------------------------------------------
#------------COMPLETE THE FOLLOWING FUNCTIONS----------------------------
def selective_forge(MAC): 
    # In this task, you must return a msg of your choice with a valid tag that would be produced by running the MAC protocol specified by sample_MAC
    # You may query MAC for any message different from the one you return. 
    # Completion of the task with fewer queries is worth more points!
    # Below is an example that does not work!
    query_msg1 = (0, 1)
    query_tag1 = MAC(query_msg1)

    s1, t1 = query_tag1
    val = t1 - s1
  
    forged_msg = (0,0)
    
    forged_tag = (val,val)
    return (forged_msg, forged_tag)

def selective_forge_first_attempt(MAC,b): 
    # In this task, you must return a msg of your choice with a valid tag that would be produced by running the MAC protocol specified by sample_MAC
    # You may query MAC for any message different from the one you return. 
    # Completion of the task with fewer queries is worth more points!
    # Below is an example that does not work!

    query_msg2 = (1, 1)
    query_tag2 = MAC(query_msg2)
    s2, t2 = query_tag2
    #f_msg = (1,0)
    if(b == 1):
        query_msg1 = (0, 1)
        s1,t1 = MAC(query_msg1)
        forged_msg = (1,0)
        oneone = s2 - s1
        tf = t2 - oneone
        sf = tf + t1 - s1
    else:
        #f_msg = (0,1)
        query_msg1 = (1, 0)
        s1,t1 = MAC(query_msg1)
        forged_msg = (0,1)
        oneone = t2 - t1
        sf = s2 - oneone
        tf = sf + s1 - t1

    forged_tag = (sf,tf)
    return (forged_msg, forged_tag)

def universal_forge(MAC, msg):
    # In this task, you must return the valid tag for the input message that would be produced by running the MAC protocol specified by sample_MAC
    # You may query MAC for any message different from the input. 
    # Completion of the task with fewer queries is worth more points!
    # Below is an example that does not work!
    
    if(msg == (0,0)):
        _,t = selective_forge(MAC)
        return t
    if(msg == (1,0)):
        _,t = selective_forge_first_attempt(MAC, 1)
        return t
    if(msg == (0,1)):
        _,t = selective_forge_first_attempt(MAC, 0)
        return t

    m,n = msg
    if(n < 0 or m < 0 or n>=16 or m>=16 or (n == 15 and m == 15)):
        t = (0,0)
        return t

    if(m == n):
        qm1 = (m, n+1)
        qm2 = (m+1, n)
        qm3 = (m+1, n-1)
        qm4 = (m-1, n+1)
        s1, t1 = MAC(qm1)
        s2, t2 = MAC(qm2)
        s3, t3 = MAC(qm3)
        s4, t4 = MAC(qm4)

        sf = s2 - (t2 - t3)
        tf = t1 - (s1 - s4)
        t = (sf,tf)
        return t

    if(n == m+1 and msg != (0,1)):
        qm1 = (n, m)
        qm2 = (m, m)
        qm3 = (n, n)
        qm4 = (m-1, n)
        s1, t1 = MAC(qm1)
        s2, t2 = MAC(qm2)
        s3, t3 = MAC(qm3)
        s4, t4 = MAC(qm4)
        sf = s3 - (t3 - t1)
        tf = t2 + (s3 - (t3 - t1) - s4)
        t = (sf,tf)
        return t

    if(m == n+1 and msg !=(1,0)):
        qm1 = (n, m)
        qm2 = (n, n)
        qm3 = (m, m)
        qm4 = (m, n-1)
        s1, t1 = MAC(qm1)
        s2, t2 = MAC(qm2)
        s3, t3 = MAC(qm3)
        s4, t4 = MAC(qm4)
        sf = s2 + (t3-t4) - (s3-s1)
        tf = t3 - (s3-s1)
        t = (sf,tf)
        return t

    if(m == 0 and n != 0):
        s,t = MAC((n,m))
        return t,s
    if(m != 0  and n == 0):
        s,t = MAC((n,m))
        return t,s
    else:
        return (0,0)





def md_forge(MD):
    # In this task, you must return a msg of your choice with a valid tag that would be produced by running the Hash-and-MAC protocol specified by sample_MD
    # You may query MD for any message different from the one you return. 
    # Completion of the task with fewer queries is worth more points!
    # Below is an example that does not work!
    query_msg = [1,2,3,4,5,6]
    query_hashtag = MD(query_msg)
    forged_msg = [1,2,3,3,5,6]
    forged_hashtag = query_hashtag
    return (forged_msg, forged_hashtag)   

#-----------------------------------------------------------------------

def main():
    select_msg, select_tag = selective_forge(sample_MAC)
    print("The selected msg for MAC is: ", select_msg)
    print("The selected tag for MAC is", select_tag)
    print("The actual tag for the selected msg for MAC is", sample_MAC(select_msg))

    forged_tag = universal_forge(sample_MAC, (5,6))
    print("The forged tag for MAC is:", forged_tag)
    print("The actual tag for MAC is:", sample_MAC((5,6)))

    md_select_msg, md_select_tag = md_forge(sample_MD)
    print("The selected msg for MD is: ", md_select_msg)
    print("The selected tag for MD is", md_select_tag)
    print("The actual tag for the selected message for MD is", sample_MD(md_select_msg))



if (__name__ == "__main__"):
    main()
