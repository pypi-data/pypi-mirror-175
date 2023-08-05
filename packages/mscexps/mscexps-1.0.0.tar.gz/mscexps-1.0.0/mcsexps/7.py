# Walsh Code
import numpy as np
 
# print complete array 
np.set_printoptions(threshold=np.inf)
 
code_length=64; # length of each code word: you can change.
code=np.array([[-1, -1], [-1, +1]]) # Initialization: -1=0 and +1=1
r, c=code.shape
 
while r < code_length:
    col1 = np.concatenate([code, code])
    col2 = np.concatenate([code, -1*code])
    code = np.concatenate([col1, col2], axis=1)
    r,c = code.shape
 
for i in range(r):
    for j in range(c):
        if code[i,j] == -1:
            code[i,j] = 0
 
 
print(code)
print(code.shape)
 
print('pilot channel: W0')
print(code[0,:])
 
print('paging channel: W1-W7')
print(code[1,:]) # print any one of em
 
print('synchronization channel: W32')
print(code[32,:])
 
print('Traffic Channels: W8-W31 and W33-W63')
print(code[8,:])