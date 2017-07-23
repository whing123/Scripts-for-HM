
import os
import xlwt
import time

# os.system('pause')

# get time stamp
time_stamp = time.strftime('%y_%m_%d_%H_%M_%S', time.localtime(time.time()))

items = ['Seq name', 'target_rate', 'actual_rate', 'Y-PSNR', 'U-PSNR', 'V-PSNR', 'encoding_time']
added_items = []

config_file_name = 'config.txt'
with open(config_file_name, 'r') as fp:
    line = ' '
    while line:
        line = fp.readline()
        line = line.strip()

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
            if after:
            	added_items = after.split()
            	items.extend(added_items)
            	#print(added_items)
        elif line.startswith('***'):
            break
fp.close()

# new excel file
wb = xlwt.Workbook(encoding='utf-8')
ws = wb.add_sheet('HM Test')

for idx, item in enumerate(items):
    ws.write(0,idx,item)

# process logs
logs = os.listdir(logs_path)
row = 1
for log_name in logs:
    log_str = os.path.splitext(log_name)
    if log_str[1] != '.log':
        continue

    file = open(logs_path + log_name, 'r')
    tmp = log_str[0].split('_')
    seq_name = '_'.join(tmp[:-1])
    #print(seq_name)
    ws.write(row, 0, seq_name)
    target_rate = tmp[len(tmp)-1]
    #print(target_rate)
    ws.write(row, 1, target_rate)

    line = ' '
    while not line.startswith('Total Time:'):
        line = file.readline()
        line = line.strip()
        if not line.startswith('SUMMARY'):
            continue
        else:
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

    row = row + 1 # next file

wb.save(output_path + 'data_' + time_stamp +'.xls')