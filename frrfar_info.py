# -*- coding: cp936 -*-
import os
import msvcrt

fh = open('FRR.txt')
f  = open('FAR.txt')
fd = open('frrfar_info.txt', 'w+')

usr = 1

fr = 0.0
verify_word = 'raw'
verify_count = 0.0

#d是一个字典，key值放的用户目录，value值放的是FR发生的个数
d = {}
#d_person同样是一个字典，key值放的是用户目录，value值放的是，用户比对的次数
d_person = {}

#FA
fa = 0.0
fa_verify_count = 0.0

def count_person_fr(line):
    user_path = line.split()[1].split("/")
    winning_index = int(line.split()[3])
    while '' in user_path:
        user_path.remove("")
    #user_path[2],即为解析出来的 0001~0010， 不局限到0010，有多大就会解析都多大
    if (user_path[usr] not in d.keys()):
        d[user_path[usr]] = 0.0
    if (user_path[usr] not in d_person.keys()):
        d_person[user_path[usr]] = 0.0

    d_person[user_path[usr]] += 1
    if winning_index == 1:
        d[user_path[usr]] += 1


def count_person_fa(line):
    winning_index = int(line.split()[2])
    global fa
    global fd
    if winning_index == 0:
        fa += 1
        print line
        fd.writelines(line)
    

#search frr.txt
for line in fh.readlines():
    if verify_word in line:
        verify_count += 1
        count_person_fr(line)
fr_list = sorted(d.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
print fr_list

fh.close()

print "USER     FR       FRR"
fd.write("USER     FR       FRR\n")

key = ''
for i in fr_list:
    key = i[0]
    fr += i[1]
    print "%s  %5d   %5.5f" %(key, d[key], d[key]/d_person[key])
    fd.write("%s  %5d   %5.5f\n" %(key, d[key], d[key]/d_person[key]))
print "FR=%d, Total=%d, FRR=%.5f" % (fr, verify_count, fr/verify_count)

##for key in d:
##    fr += d[key]
##    print "%s  %5d   %5.5f" %(key, d[key], d[key]/d_person[key])
##    fd.write("%s  %5d   %5.5f\n" %(key, d[key], d[key]/d_person[key]))
##print "FR=%d, Total=%d, FRR=%.5f" % (fr, verify_count, fr/verify_count)
fd.write("FR=%d, Total=%d, FRR=%.5f\n" % (fr, verify_count, fr/verify_count))

#search far.txt
for line in f.readlines():
    if verify_word in line:
        fa_verify_count += 1
        count_person_fa(line)
f.close()
print "FA=%d, Total=%d, FAR=%.7f\n" % (fa, fa_verify_count, fa/fa_verify_count)
fd.write("FA=%d, Total=%d, FAR=%.7f\n" % (fa, fa_verify_count, fa/fa_verify_count))
fd.close()

msvcrt.getch()



