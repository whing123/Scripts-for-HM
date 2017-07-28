# run HM

import os
import subprocess
import shutil
import time

# os.system('pause')

# get time stamp
time_stamp = time.strftime('%y_%m_%d_%H_%M_%S', time.localtime(time.time()))

fenclog = open('enc.txt', 'w')
fenclog.write('\n' + 'Copyright @ 2016-2017' + '\n')
fenclog.write('\n' + 'This is ' + time_stamp + '\n')
fenclog.write('\n' + '---Starting---' + '\n')


config_file_name = 'config.txt'
with open(config_file_name, 'r') as fp:
    line = ' '
    while line:
        line = fp.readline()
        line = line.strip()

        if line.startswith('identifier:'):
            identifier = line
            fenclog.write(identifier + '\n')
            #print(identifier)

        elif line.startswith('exe path:'):
            before, encoder_exe = line.split('exe path:')
            encoder_exe = encoder_exe.strip()
            before, after = encoder_exe.split('\\')
            encoder_name, after = after.split('.exe')
            fenclog.write('exe path: ' + encoder_exe + '\n')
            #print(encoder_exe)

        elif line.startswith('cfg1 path:'):
            before, cfg1 = line.split('cfg1 path:')
            cfg1 = cfg1.strip()
            fenclog.write('cfg1 path: ' + cfg1 + '\n')
            #print(cfg1)

        elif line.startswith('cfg2 path:'):
            if '#' in line:    # 之后为注释
                before, after = line.split('#')
                before, cfg2_path = before.split('cfg2 path:')
            else:
                before, cfg2_path = line.split('cfg2 path:')
            cfg2_path = cfg2_path.strip()
            fenclog.write('cfg2 path: ' + cfg2_path + '\n')
            #print(cfg2_path)

        elif line.startswith('seq path:'):
            before, seq_path = line.split('seq path:')
            seq_path = seq_path.strip()
            fenclog.write('seq path: ' + seq_path + '\n')
            #print(seq_path)

        elif line.startswith('result path:'):
            before, result_path = line.split('result path:')
            result_path = result_path.strip()
            fenclog.write('result path: ' + result_path + '\n')
            #print(result_path)

            # make output dir with time
            output_path = result_path + 'output_' + time_stamp + '_' + encoder_name
            os.mkdir(output_path)
            # make subdir for logs, rec YUV, bin
            yuvbin_path = output_path + '\yuvbin'
            logs_path = output_path + '\logs'
            os.mkdir(yuvbin_path)
            os.mkdir(logs_path)

            fenclog.write('output path: ' + output_path + '\n')
            fenclog.write('yuvbin path: ' + yuvbin_path + '\n')
            fenclog.write('logs path: '   + logs_path   + '\n')

        elif line.startswith('extra cmd:'):
            extra_cmd = ''
            if '#' in line:
                continue
            else:
                before, extra_cmd = line.split('extra cmd:')
                extra_cmd = extra_cmd.strip()
            fenclog.write('extra cmd: ' + extra_cmd + '\n')

        elif line.startswith('mode:'):
            before, after = line.split('mode:')
            mode, after = after.split('#')
            mode = mode.strip()
            if mode == '1':
                mode_str = 'Rate Control'
            elif mode == '0':
                mode == 'QP'
                mode_str = 'Const QP'
            else:
                print('No mode was selected')
                os.system('pause')

            fenclog.write('mode: ' + mode_str + '\n')

        elif line.startswith('testing seq and rate:'):
            while line:
                line = fp.readline()
                line = line.strip()

                if line.startswith('***end***'):
                    break

                before, class_name = line.split(':')
                class_name = class_name.strip()
                fenclog.write('\n' + 'class name: ' + class_name + '\n')
                #print(class_name)

                while line:
                    line = fp.readline()
                    line = line.strip()
                    if '#' in line:
                        break

                    seq = line.split()
                    seq_name = seq[0]
                    vals = seq[1:]
                    fenclog.write('sequence name: ' + seq_name + '\n')
                    #print(seq_name)

                    for idx, val in enumerate(vals):

                        if mode == '1':
                            mode_cmd = '--RateControl=1' + ' ' + '--TargetBitrate=' + val + '000'
                            mode_s = 'Rate'
                        elif mode == '0':
                            mode_cmd = '--QP=' + val
                            mode_s = 'QP'
                        fenclog.write(mode_s + ' ' + str(idx + 1) + ': ' + val + '\n')
                        #print(mode_s + ' ' + str(idx + 1) + ': ' + val + '\n')

                        cmd = encoder_exe + ' -c ' + cfg1 + ' -c ' + cfg2_path + seq_name.split('_')[0] + '.cfg' + ' ' \
                              + '--InputFile=' + seq_path + class_name + '\\' + seq_name + '.yuv' + ' ' \
                              + '--BitstreamFile=' + yuvbin_path + '\\' + seq_name + '_' + val + '.bin' + ' ' \
                              + '--ReconFile=' + yuvbin_path + '\\' + seq_name + '_' + val + '.yuv' + ' ' \
                              + mode_cmd + ' ' \
                              + '>' + logs_path + '\\' + seq_name + '_' + val + '.log' + ' ' \
                              + extra_cmd


                        fenclog.write('cmd: ' + '\n' +cmd + '\n')
                        #print(cmd)
                        #os.popen(cmd)
                        #os.system(cmd)  # only one at once
                        subprocess.Popen(cmd, shell=True)

            # end here
            if line.startswith('***end***'):
                break

fp.close()

fenclog.write('\n' + '---THE END---')
fenclog.close()


# create readme.txt
ftxt = open(output_path + r'\readme.txt', 'w')
ftxt.write(identifier)
ftxt.close()

# copy current cofig.txt
shutil.copyfile('config.txt', output_path + r'\config.txt')
shutil.copyfile('enc.txt', output_path + r'\enc.txt')

os.remove('config.txt')
os.remove('enc.txt')
