#pip install -U numpy
from copy import deepcopy
import gc
import math
import numpy as np
from sklearn import metrics

N = 4

file_main_name = "/Users/dubc/main_chain.dat"
file_side_name = "/Users/dubc/side_chain.dat"
file_MM_name = "/Users/dubc/MM.dat"
file_SS_name = "/Users/dubc/SS.dat"
file_MS_name = "/Users/dubc/MS.dat"

file_main = open(file_main_name, 'r')
main_angle_lines = file_main.readlines()
file_main.close()

main_angle_mount = len(main_angle_lines[0].split())
lines_mount = len(main_angle_lines)

main_angle_list = [[0 for x in range(lines_mount)] for y in range(main_angle_mount)]

for index_line in range(0, lines_mount):
    line_sample_list = main_angle_lines[index_line].strip('\n').split()
    for index_angle in range(0, main_angle_mount):
        main_angle_list[index_angle][index_line] = float(line_sample_list[index_angle])

for i in range(0, main_angle_mount):
    for j in range(0, lines_mount):
        del main_angle_lines[i][j]
    del main_angle_lines[i]
del main_angle_lines

main_sort_list = [[0 for x in range(N+1)] for y in range(main_angle_mount)]
for index_angle in range(main_angle_mount):
    sort_list = sorted(main_angle_list[index_angle], key = float)
    for index_count in range(0, lines_mount, lines_mount / N):
        main_sort_list[index_angle][index_count / (lines_mount / N)] = sort_list[index_count]
gc.collect()

for index_angle in range(0, main_angle_mount):
    for index_line in range(0, lines_mount):
        for index_count in range(0, N+1):
            if main_sort_list[index_angle][index_count] >= main_angle_list[index_angle][index_line]:
                main_angle_list[index_angle][index_line] = index_count
                break
            if main_sort_list[index_angle][-1] < main_angle_list[index_angle][index_line]:
                main_angle_list[index_angle][index_line] = N
                break
gc.collect()


file_side = open(file_side_name, 'r')
side_angle_lines = file_side.readlines()
file_side.close()
side_angle_mount = len(side_angle_lines[0].split())
side_angle_list = [[0 for x in range(lines_mount)] for y in range(side_angle_mount)]

for index_line in range(lines_mount):
    line_sample_list = side_angle_lines[index_line].strip('\n').split()
    for index_angle in range(side_angle_mount):
        side_angle_list[index_angle][index_line] = float(line_sample_list[index_angle])

for i in range(0, side_angle_mount):
    for j in range(0, lines_mount):
        del side_angle_lines[i][j]
    del side_angle_lines[i]
del side_angle_lines
gc.collect()

side_sort_list = [[0 for x in range(N+1)] for y in range(side_angle_mount)]
for index_angle in range(side_angle_mount):
    sort_list = sorted(side_angle_list[index_angle], key = float)
    for index_count in range(0, lines_mount, lines_mount / N):
        side_sort_list[index_angle][index_count / (lines_mount / N)] = sort_list[index_count]
gc.collect()

for index_angle in range(0, side_angle_mount):
    for index_line in range(0, lines_mount):
        for index_count in range(N+1):
            if side_sort_list[index_angle][index_count] >= side_angle_list[index_angle][index_line]:
                side_angle_list[index_angle][index_line] = index_count
                break
            if side_sort_list[index_angle][-1] < side_angle_list[index_angle][index_line]:
                side_angle_list[index_angle][index_line] = N
                break
gc.collect()

        #Entropy
    #1st order
'''
for index_angle in range(0, main_angle_mount):
    unique_values = np.unique(main_angle_list[index_angle][:], return_counts = True)
    sum_sample = sum(unique_values[1][:])
    probability = 0
    entropy_1st = 0
    for sample in unique_values[0]:
        probability =  float(unique_values[1][sample]) / float(sum_sample)
        entropy_1st = probability * math.log(probability) + entropy_1st
print entropy_1st,


for index_angle in range(0, side_angle_mount):
    unique_values = np.unique(side_angle_list[index_angle][:], return_counts = True)
    sum_sample = sum(unique_values[1][:])
    probability = 0
    entropy_1st = 0
    for sample in unique_values[0]:
        probability =  float(unique_values[1][sample]) / float(sum_sample)
        entropy_1st = probability * math.log(probability) + entropy_1st
print entropy_1st
'''
#Mutral Information
    #2nd_order
        #MM
file_MM = open(file_MM_name, 'w')
for index_angle_A in range(0, main_angle_mount):
    for index_angle_B in range(index_angle_A+1, main_angle_mount):
        mutual_info = metrics.mutual_info_score(main_angle_list[index_angle_A][:],main_angle_list[index_angle_B][:])
        char = '%3d %3d %10.8lf \n'%(index_angle_A, index_angle_B, mutual_info)
        file_MM.write(char)
        char = ''
file_MM.close()

        #SS
file_SS = open(file_SS_name, 'w')
for index_angle_A in range(0, side_angle_mount):
    for index_angle_B in range(index_angle_A + 1, side_angle_mount):
        mutual_info = metrics.mutual_info_score(side_angle_list[index_angle_A][:], side_angle_list[index_angle_B][:])
        char = '%3d %3d %10.8lf \n'%(index_angle_A, index_angle_B, mutual_info)
        file_SS.write(char)
        char = ''
file_SS.close()

        #MS
file_MS = open(file_MS_name, 'w')
for index_angle_A in range(0, main_angle_mount):
    for index_angle_B in range(0, side_angle_mount):
        mutual_info = metrics.mutual_info_score(main_angle_list[index_angle_A][:], side_angle_list[index_angle_B][:])
        char = '%3d %3d %10.8lf \n'%(index_angle_A, index_angle_B, mutual_info)
        file_MS.write(char)
        char = ''
file_MS.close()

