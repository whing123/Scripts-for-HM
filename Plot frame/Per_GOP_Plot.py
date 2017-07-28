
import matplotlib.pyplot as plt 
import numpy as np


config_file_name = 'config.txt'
with open(config_file_name, 'r') as fp:

    while True:
        line = fp.readline()
        line = line.strip()

        if not line:
            continue

        if line.startswith('anchor:'):
    	    before, anchorFile = line.split('anchor:')
    	    anchorFile = anchorFile.strip()

        elif line.startswith('test:'):
    	    before, testFile = line.split('test:')
    	    testFile = testFile.strip()

        elif line.startswith('***end***'):
            break
fp.close()


### read anchor log 

d_Bit1 = []
d_PSNR1 = []
d_SSIM1 = []
d_MOSP1 = []
parts1 = []

with open(anchorFile,"r") as f1:
   for line in f1:
       
        if line.startswith('SUMMARY'):
            break

        elif line.startswith('POC'):
            parts1 = ''.join(e for e in line if (e is not ' '))

            # poc number
            before, after = parts1.split('TId')
            poc = ''.join(c for c in before if c.isdigit())
            
            # bits
            before, after = parts1.split('bits')
            before, bitrate = before.split(')')

            # Y PSNR
            before, after = parts1.split('dBU')
            before, PSNR = before.split('Y')

            d_Bit1.append(float(bitrate))
            d_PSNR1.append(float(PSNR))
            
        elif line.startswith('SSIM'):
            before, ssim = line.split(' ')
            d_SSIM1.append(float(ssim))

        elif line.startswith('MosP'):
            before, mosp = line.split(' ')
            d_MOSP1.append(float(mosp))       
f1.close()

### read my log

d_Bit2 = []
d_PSNR2 = []
d_SSIM2 = []
d_MOSP2 = []
parts2 = []

with open(testFile,"r") as f2:
   for line in f2:
       
        if line.startswith('SUMMARY'):
            break
        
        elif line.startswith('POC'):
            parts2 = ''.join(e for e in line if (e is not ' '))

            # poc number
            before, after = parts2.split('TId')
            poc = ''.join(c for c in before if c.isdigit())
            
            # bits
            before, after = parts2.split('bits')
            before, bitrate = before.split(')')

            # Y PSNR
            before, after = parts2.split('dBU')
            before, PSNR = before.split('Y')

            d_Bit2.append(float(bitrate))
            d_PSNR2.append(float(PSNR))
            
        elif line.startswith('SSIM'):
            before, ssim = line.split(' ')
            d_SSIM2.append(float(ssim))

        elif line.startswith('MosP'):
            before, mosp = line.split(' ')
            d_MOSP2.append(float(mosp))
          
f2.close()

### avg per GOP

sum_PSNR1 = 0
sum_Bit1  = 0
sum_SSIM1 = 0
sum_MOSP1 = 0

sum_PSNR2 = 0
sum_Bit2  = 0
sum_SSIM2 = 0
sum_MOSP2 = 0

avg_GOP_PSNR1 = []
avg_GOP_Bit1  = []
avg_GOP_SSIM1 = []
avg_GOP_MOSP1 = []

avg_GOP_PSNR2 = []
avg_GOP_Bit2  = []
avg_GOP_SSIM2 = []
avg_GOP_MOSP2 = []
for i in range(int(poc)+1):
       
    sum_PSNR1 = sum_PSNR1 + d_PSNR1[i]
    sum_Bit1  = sum_Bit1  + d_Bit1[i]
    sum_SSIM1 = sum_SSIM1 + d_SSIM1[i]
    sum_MOSP1 = sum_MOSP1 + d_MOSP1[i]

    sum_PSNR2 = sum_PSNR2 + d_PSNR2[i]
    sum_Bit2  = sum_Bit2  + d_Bit2[i]
    sum_SSIM2 = sum_SSIM2 + d_SSIM2[i]
    sum_MOSP2 = sum_MOSP2 + d_MOSP2[i]

    if (i+1) % 4 == 0:
        avg_GOP_PSNR1.append(sum_PSNR1/4.0)
        avg_GOP_Bit1.append(sum_Bit1/4.0)
        avg_GOP_SSIM1.append(sum_SSIM1/4.0)
        avg_GOP_MOSP1.append(sum_MOSP1/4.0)
        sum_PSNR1 = 0
        sum_Bit1  = 0
        sum_SSIM1 = 0
        sum_MOSP1 = 0
        
        avg_GOP_PSNR2.append(sum_PSNR2/4.0)
        avg_GOP_Bit2.append(sum_Bit2/4.0)
        avg_GOP_SSIM2.append(sum_SSIM2/4.0)
        avg_GOP_MOSP2.append(sum_MOSP2/4.0)
        sum_PSNR2 = 0
        sum_Bit2  = 0
        sum_SSIM2 = 0
        sum_MOSP2 = 0

### plot
        
xpoints= []

ypoints_bitrate1 = []
ypoints_PSNR1 = []
ypoints_SSIM1 = []
ypoints_MOSP1 = []

ypoints_bitrate2 = []
ypoints_PSNR2 = []
ypoints_SSIM2 = []
ypoints_MOSP2 = []

GOP_Num = (int(poc)+1)//4

for x in range (GOP_Num):
    xpoints.append(x)
    
    ypoints_bitrate1.append(avg_GOP_Bit1[x])
    ypoints_PSNR1.append(avg_GOP_PSNR1[x])
    ypoints_SSIM1.append(avg_GOP_SSIM1[x])
    ypoints_MOSP1.append(avg_GOP_MOSP1[x])

    ypoints_bitrate2.append(avg_GOP_Bit2[x])
    ypoints_PSNR2.append(avg_GOP_PSNR2[x])
    ypoints_SSIM2.append(avg_GOP_SSIM2[x])
    ypoints_MOSP2.append(avg_GOP_MOSP2[x])
    
# 设置坐标轴刻度显示大小
plt.rc('xtick', labelsize=8) 
plt.rc('ytick', labelsize=8)

# PSNR
fig, ax = plt.subplots()
ax.plot(xpoints, ypoints_PSNR1, 'b', xpoints, ypoints_PSNR2, 'r', linewidth=1)
ax.set_xticks([0,20,40,60,80,100,120])
ax.set_yticks(range(25,35))
ax.set_xlabel('GOP number')
ax.set_ylabel('Average PSNR per GOP')
ax.legend(['anchor','proposed'])

# SSIM
fig, ax = plt.subplots()
ax.plot(xpoints, ypoints_SSIM1, 'b', xpoints, ypoints_SSIM2, 'r', linewidth=1)
ax.set_yticks([0.75, 0.8, 0.85, 0.9, 0.95])
ax.set_xlabel('GOP number')
ax.set_ylabel('Average SSIM per GOP')
ax.legend(['anchor','proposed'])

# MOSp
fig, ax = plt.subplots()
ax.plot(xpoints, ypoints_MOSP1, 'b', xpoints, ypoints_MOSP2, 'r', linewidth=1)
ax.set_yticks([0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9])
ax.set_xlabel('GOP number')
ax.set_ylabel('Average MOSp per GOP')
ax.legend(['anchor','proposed'])
#ax.xaxis.grid(True, which='major') #x坐标轴的网格使用主刻度  
#ax.yaxis.grid(True, which='minor') #y坐标轴的网格使用次刻度

'''
# bitrate
fig, ax = plt.subplots()
ax.plot(xpoints, ypoints_bitrate1, 'b', xpoints, ypoints_bitrate2, 'r')
ax.set_xlabel('GOP number')
ax.set_ylabel('Average Rate per GOP')
ax.legend(['anchor','proposed'])
'''

#plt.grid(True) # 加网格
plt.show()
