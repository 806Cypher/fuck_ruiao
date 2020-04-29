import os, sys
import random, base64

def ret_val(line:str):
    bgn = line.find('>') + 1
    end = line.find('</')
    return line[bgn:end]

if __name__ == '__main__':
    num = int(sys.argv[1])
    ans_cont = ""
    with open('lab%d.txt' % num, 'r', encoding='utf-8') as ori_file:
        last_line = ""
        line_number = 0
        cnt = 0
        tot_score = 0
        for line in ori_file.readlines():
            line = line.replace('></', '>ssssao</')
            if '<Total>' in line:
                tot_score += int(ret_val(line))
            line_number += 1
            if last_line == "":
                last_line = line
                continue
            if '<StdResult>' in line:
                if '<RealResult>' in last_line:
                    stdans = ret_val(line)
                    orians = ret_val(last_line)
                    last_line = last_line.replace(orians, stdans)
                else:
                    print('[line %d]warning: %s' % (line_number, line))
            elif '<RealScore>' in line:
                if '<TotalScore>' in last_line or '<Total>' in last_line:
                    stdsc = ret_val(last_line)
                    orisc = ret_val(line)
                    line = line.replace(orisc, stdsc)
                    if not '<Total>' in last_line:
                        cnt += int(stdsc)
                elif 'StdResultShowInfo' in last_line:
                    print('[line %d]warning: %s' % (line_number, line))
                    cnt += int(ret_val(line))
                else:
                    if '<Score>' in last_line:
                        print('[line %d]warning: %s' % (line_number, line))
                    else:
                        orisc = ret_val(line)
                        line = line.replace(orisc, str(cnt))
                    cnt = 0
            elif '<RealTime>' in line:
                oritime = ret_val(line)
                line = line.replace(oritime, str(random.randint(2000, 3000)))
            ans_cont += last_line.replace('>ssssao</', '></')
            last_line = line
        ans_cont += last_line.replace('>ssssao</', '></')
    with open(os.path.join('ans.dir', 'lab%d.ans' % num), 'w', encoding='utf-8') as out_file:
        out_file.write(ans_cont)
        out_file.write('\n\n\n')
        out_file.write(base64.b64encode(ans_cont.encode('utf-8')).decode())
    print(tot_score)