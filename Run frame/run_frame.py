# get data from every frame for HM logs

import os
import xlwt
import time

# os.system('pause')

# get time stamp
time_stamp = time.strftime('%y_%m_%d_%H_%M_%S', time.localtime(time.time()))

seq_items = ['Seq name', 'target_rate', 'actual_rate', 'Y-PSNR', 'U-PSNR', 'V-PSNR', 'encoding_time']

frame_items = ['POC', 'type', 'nQP', 'QP', 'bits', 'Y_PSNR', 'U-PSNR', 'V-PSNR']

config_file_name = 'config.txt'
with open(config_file_name, 'r') as fp:
    line = ' '
    while line:
        line = fp.readline()

        if line.startswith('logs path:'):
            before, logs_path = line.split('logs path:')
            logs_path = logs_path.strip()
            #print(logs_path)
        elif line.startswith('output path:'):
            before, output_path = line.split('output path:')
            output_path = output_path.strip()
            #print(output_path)
        elif line.startswith('adding item:'):
            before, after = line.split('adding item:')
            after = after.strip()
            added_items = after.split()
            seq_items.extend(added_items)
            frame_items.extend(added_items)
            #print(added_items)
        elif line.startswith('***'):
            break
fp.close()

# new excel file
wb = xlwt.Workbook(encoding='utf-8')
ws = wb.add_sheet('HM Test')

row = 0
for idx, item in enumerate(seq_items):
    ws.write(row,idx,item)

row = 3
for idx, item in enumerate(frame_items):
    ws.write(row,idx,item)

# process logs
if '\\' in logs_path: 
    tmps = logs_path.split('\\')
    log_name = tmps[len(tmps)-1]
else:
    log_name = logs_path
    
log_str = os.path.splitext(log_name)
tmp = log_str[0].split('_')
seq_name = '_'.join(tmp[:-1])
#print(seq_name)

row = 1
ws.write(row, 0, seq_name)
target_rate = tmp[len(tmp)-1]
#print(target_rate)
ws.write(row, 1, target_rate)

file = open(logs_path, 'r')
line = ' '
row = 4
while not line.startswith('Total Time:'):
    line = file.readline()
    line = line.strip()
    if not line.startswith('SUMMARY'):
        
        if line.startswith('POC'):
            before, after = line.split('POC')
            before, after = after.split('TId:')
            poc = before.strip()
            ws.write(row, 0, poc)

            before, after = after.split('-SLICE,')
            before, slice_type = before.split('(')
            slice_type = slice_type.strip()
            ws.write(row, 1, slice_type)

            before, after = after.split(')')
            before = before.strip()
            tmps = before.split()
            ws.write(row, 2, tmps[1]) #nQP
            ws.write(row, 3, tmps[3]) #QP

            before, after = after.split('bits')
            bits = before.strip()
            ws.write(row, 4, bits)

            before, after = after.split('dB]')
            tmps = before.split('dB')
            before, Y_psnr = tmps[0].split('Y')
            Y_psnr = Y_psnr.strip()
            ws.write(row, 5, Y_psnr)

            before, U_psnr = tmps[1].split('U')
            U_psnr = U_psnr.strip()
            ws.write(row, 6, U_psnr)

            before, V_psnr = tmps[2].split('V')
            V_psnr = V_psnr.strip()
            ws.write(row, 7, V_psnr)

            for i in range(len(added_items)):
                line = file.readline()
                line = line.strip()
                it = line.split()[0]
                if it in added_items:
                    ws.write(row, i + 8, line.split()[1])

            row = row + 1
                
    else:
        row = 1
        line = file.readline()
        line = file.readline()
        line = line.strip()
        nums = line.split()
        #print(nums)
        actual_rate = nums[2]
        ws.write(row, 2, actual_rate)
        Y_PSNR = nums[3]
        ws.write(row, 3, Y_PSNR)
        U_PSNR = nums[4]
        ws.write(row, 4, U_PSNR)
        V_PSNR = nums[5]
        ws.write(row, 5, V_PSNR)

        i = 1
        while True:
            line = file.readline()
            line = line.strip()
            if line.startswith('Total Time:'):
                before, after = line.split('Total Time:')
                time, after = after.split('sec.')
                time = time.strip()
                ws.write(row, 6, time)
                break
            elif line:
                it = line.split()[0]
                if it in added_items:
                    ws.write(row, i + 6, line.split()[1])
                    i = i + 1

wb.save(output_path + 'data_' + time_stamp +'.xls')
