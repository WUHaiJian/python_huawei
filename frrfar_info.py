# -*- coding: cp936 -*-
import os
#import msvcrt
import threading

fh = open('FRR.txt')
f  = open('FAR.txt')
fd = open('frrfar_info.txt', 'w+')

usr = 1

fr = 0.0
fr_list = []
verify_word = 'raw'
verify_count = 0.0

#d is a dirctory, key store user, value store winning index count
#d_per_total is a directory, key store user, value store the user total match count
d = {}
d_per_total = {}

#FA
fa = 0.0
fa_verify_count = 0.0


threads = []
def count_person_fr(line):
    user_path = line.split()[1].split("/")
    winning_index = int(line.split()[3])
    while '' in user_path:
        user_path.remove("")
    #user_path[usr],0001~0010
    if (user_path[usr] not in d.keys()):
        d[user_path[usr]] = 0.0
    #if (user_path[usr] not in d_per_total.keys()):
        d_per_total[user_path[usr]] = 0.0

    d_per_total[user_path[usr]] += 1
    if winning_index == 1:
        d[user_path[usr]] += 1


def count_person_fa(line):
    winning_index = int(line.split()[2]) 
    global fa
    global fd
    if winning_index == 0:
        fa += 1
        fd.writelines(line)
        #print line
    
def search_frr():
    #print r"================= Search FR  ===================="
    #search frr.txt
    global verify_count
    for line in fh.readlines():
        if verify_word in line:
            verify_count += 1
            count_person_fr(line)
    fh.close()
    global fr_list
    fr_list = sorted(d.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    
def search_far():
    #print r"================= Search FA  ===================="
    #search far.txt
    global fa_verify_count
    for line in f.readlines(): 
        if verify_word in line:
            fa_verify_count += 1
            count_person_fa(line)
    f.close()
   
def log_output():
    fd.write("USER     FR       FRR\n")
    global fr
    key = ''
    for i in fr_list:
        key = i[0]
        fr += i[1]
        print "%s  %5d   %5.5f" %(key, d[key], d[key]/d_per_total[key])
        fd.write("%s  %5d   %5.5f\n" %(key, d[key], d[key]/d_per_total[key]))
    #FRR/FAR result
    print r"================= Result ===================="
    print "FR=%d, Total=%d, FRR=%.5f" % (fr, verify_count, fr/verify_count)
    fd.write("FR=%d, Total=%d, FRR=%.5f\n" % (fr, verify_count, fr/verify_count))
    print "FA=%d, Total=%d, FAR=%.7f\n" % (fa, fa_verify_count, fa/fa_verify_count)
    fd.write("FA=%d, Total=%d, FAR=%.7f\n" % (fa, fa_verify_count, fa/fa_verify_count))

class frr_thread(threading.Thread):
    def run(self):
        search_frr()

class far_thread(threading.Thread):
    def run(self):
        search_far()

def main():
    t1 = frr_thread()
    t2 = far_thread()
    t1.start()
    t2.start()
    t1.join()
    t2.join()  
    log_output()
    fd.close()

if __name__ == '__main__':
    main()

#msvcrt.getch()



