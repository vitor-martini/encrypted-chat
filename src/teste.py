import math


def toBinary(a):
  l,m=[],[]
  for i in a:
    l.append(ord(i))
  for i in l:
    m.append(
        
        str(bin(i)[2:])[::-1].ljust(8, "0")[::-1]
    
    )
  return ''.join(m)

def toString(str):

  a = []
  for i in range(len(str)):
      if i % 8 == 0 and i != 0:
          a.append(str[i-8:i])

  l=[]
  m=""
  for i in a:
    b=0
    c=0
    i = int(i)
    k=int(math.log10(i))+1
    for j in range(k):
      b=((i%10)*(2**j))   
      i=i//10
      c=c+b
    l.append(c)
  for x in l:
    m=m+chr(x)
  return m

plaintext = 'Hello world'
binary = toBinary(plaintext)
string_again = toString(binary)
print(plaintext)
print(binary)
print(string_again)
#teste