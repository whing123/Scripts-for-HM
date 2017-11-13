import os
import xlwt
import xlrd

seq_all = {}
orders = []

config_file_name = 'config.txt'
with open(config_file_name, 'r') as fp:
    while True:
        line = fp.readline()
        line = line.strip()

        if not line:
            continue

        if line.startswith('logs path:'):
            before, logs_path = line.split('logs path:')
            logs_path = logs_path.strip()
            # print(logs_path)
        elif line.startswith('output path:'):
            before, output_path = line.split('output path:')
            output_path = output_path.strip()
            # print(output_path)
        elif line.startswith('col order:'):
            cnt = 0
            line = ''
            while not line: # junp next 2 rows
                line = fp.readline()
                line = line.strip()
                if line:
                    cnt = cnt + 1
                    if cnt == 3:
                        break;
                    else:
                        line = ''
            orders = line.split()
        elif line.startswith('seq names:'):
            line = ''
            while not line:
                line = fp.readline()
                line = line.strip()

            num = int(line)
            i = 1
            while i <= num:
                line = ''
                while not line:
                    line = fp.readline()
                    line = line.strip()

                items = line.split()
                dict = {}
                dict['id'] = i # seq order
                for j in range(1,5): # mode order
                    dict[items[j]] = j
                seq_all[items[0]] = dict # seq name -> {'id':, QP1:, QP2:, QP3:, QP4:} QP or rate

                i = i + 1
        elif line.startswith('***end***'):
            break
fp.close()

wb = xlwt.Workbook(encoding='utf-8')
ws = wb.add_sheet('HM Test')

bk = xlrd.open_workbook(logs_path) # read excel
#sh = bk.sheet_by_name(u'HM Test')
sh = bk.sheet_by_index(0) # get sheet
nrows = sh.nrows # number of rows
for i in range(0,nrows): # process every row
    row_data = sh.row_values(i) # get row data
    if i == 0:
        for idx, val in enumerate(row_data):
            ws.write(i, int(orders[idx]), val)
    else:
        seq_dict = {}
        seq_dict = seq_all[row_data[0]] # seq name -> its dict
        row_num = (seq_dict['id']-1) * 4 + seq_dict[str(int(row_data[1]))] # new row num
        for idx, val in enumerate(row_data):
            ws.write(row_num, int(orders[idx]), val)

# remove path and get name
if '\\' in logs_path:
    tmps = logs_path.split('\\')
    log_name = tmps[len(tmps)-1]
else:
    log_name = logs_path
log_name = log_name.split('.')[0] # remove format
wb.save(output_path + log_name +'_new.xls')