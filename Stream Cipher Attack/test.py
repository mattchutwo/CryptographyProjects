import sys
import random
from attack import*

def xGen():
    x = []
    for i in range(1000):
        x.append(random.randint(0,255))
    return x

def ivGen():
    x = []
    for i in range(256):
        x.append(random.randint(0,255))
    return x

iv = ivGen()
key = xGen()

y = []
(k,s) = init(iv,key)
for i in range(10):
    (x,k,s) = next(k,s)
    y.append(x)


r = xGen()
print(PRG_attack(iv,y))
print(PRG_attack(iv,r))

print("\n**************************************")
print("\n***************  EAV  ****************")
print("\n**************************************\n")


m1 = ranListGen(10)
m2 = ranListGen(10)
key = stringToByteList("supersecret")
l1 = m1
l2 = m2
iv = [133, 255, 33, 77, 231, 186, 180, 155, 18, 12, 95, 165, 194, 126, 90, 72, 99, 26, 91, 19, 1, 17, 13, 33, 183, 124, 200, 125, 120, 222, 65, 25, 234, 3, 139, 217, 224, 244, 201, 1, 4, 152, 227, 121, 0, 170, 211, 100, 163, 202, 4, 92, 238, 130, 158, 86, 6, 243, 45, 18, 176, 114, 118, 40, 184, 103, 223, 95, 222, 44, 58, 29, 35, 73, 148, 164, 118, 1, 72, 136, 65, 121, 194, 72, 172, 230, 61, 233, 226, 57, 41, 248, 223, 126, 38, 25, 139, 102, 236, 63, 46, 62, 76, 158, 190, 179, 98, 180, 175, 17, 252, 63, 226, 26, 174, 11, 9, 32, 116, 106, 205, 134, 124, 168, 249, 61, 79, 124, 105, 193, 214, 59, 197, 243, 210, 7, 233, 224, 210, 181, 242, 253, 175, 129, 62, 134, 67, 4, 183, 43, 128, 168, 100, 40, 152, 37, 153, 214, 131, 144, 145, 150, 101, 232, 243, 226, 48, 247, 119, 1, 211, 209, 173, 105, 101, 216, 55, 78, 13, 98, 195, 20, 21, 222, 100, 51, 187, 140, 86, 5, 18, 153, 57, 155, 145, 68, 241, 181, 27, 222, 38, 120, 167, 250, 105, 51, 254, 130, 142, 211, 160, 40, 166, 200, 206, 113, 118, 43, 87, 10, 114, 41, 226, 102, 186, 84, 229, 22, 56, 55, 49, 55, 152, 31, 17, 24, 107, 65, 187, 254, 156, 19, 190, 168, 58, 108, 218, 157, 80, 186, 253, 202, 114, 165, 173, 8]
print("This is the IV:", iv)
print("This is the Key:", key)

e1 = enc(iv, key, l1)
e2 = enc(iv, key, l2)
print(m1,":", dec(key, e1))
print("enc1:",e1[256:])
print(m2,":", dec(key, e2))
print("enc2:",e2[256:])
s1 = derriveShiftSequnce(l1,e1)
s2 = derriveShiftSequnce(l2,e2)
print("shiftseq1:",s1)
print("shiftseq2:",s2)


print("\n**************************************")
print("\n***************  DEC  ****************")
print("\n**************************************\n")

m3 = ranListGen(12)
m4 = ranListGen(10)
m = [m1,m4,m3,m2]

k = random.randint(10,20)
m = []
d3 = []
r = random.randint(4,10)
for i in range(k):
    moe = []
    if i == 3:
        moe = ranListGen(12)
    else:
        moe= ranListGen(10)
    
    if i == r:
        d3 = enc(iv,key, moe)
    m.append(moe)
        
d1 = decrypt(m,d3)
print("d1:", d1)


