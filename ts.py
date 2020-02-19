import numpy as np
import math
import sys
import random
import copy
import json
tabu_limit = 50

def processing_data(fname):
    fin = open(fname, 'r')
    a = fin.readlines()
    fout = open("att48.txt", 'w')
    b = ''.join(a[6:-1])
    fout.write(b)


def read_coordinate(fname):
    coordiante = []
    with open("att48.txt") as f:
        for each_line in f:
            tmp = each_line.split()
            xy = [int(tmp[1]), int(tmp[2])]
            coordiante.append(xy)
    return coordiante


def getdis(coordinate):
    num = int(coordinate.shape[0])
    dis_mat = np.zeros((num, num))
    for i in range(num):
        for j in range(i, num):
            d_x = coordinate[i][0] - coordinate[j][0]
            d_y = coordinate[i][1] - coordinate[j][1]
            rij = math.sqrt((d_x * d_x + d_y * d_y) / 10)
            tij = round(rij)
            if tij == 0:
                dis_mat[i][j] = dis_mat[j][i] = sys.maxsize
            else:
                dis_mat[i][j] = dis_mat[j][i] = int(tij) if tij > rij else int(tij) + 1
    return dis_mat


def cal_dis(route,distance, n):
    sumdis = 0
    for i in range(n - 1):
        sumdis += distance[route[i]][route[i+1]]
    sumdis += distance[route[n-1]][route[0]]
    return sumdis


def swap_fun(index1, index2, arr):
    current_list = copy.copy(arr)
    current = current_list[index1]
    current_list[index1] = current_list[index2]
    current_list[index2] = current
    return current_list


def initial(n, distance):
    global best_route
    global best_distance
    global tabu_time
    global current_tnum
    global current_distance
    global current_route
    global tabu_list
    current_route = random.sample(range(0, n), n)
    best_route = copy.copy(current_route)
    current_distance = cal_dis(current_route, distance, n)
    best_distance = current_distance

    tabu_list.clear()
    tabu_time.clear()
    current_tnum = 0


def move(n, distance, candidate_number):
    global best_route
    global best_distance
    global current_tnum
    global current_distance
    global current_route
    global tabu_list
    swap_fun_position = []
    temp = 0
    while True:
        current = random.sample(range(0, n), 2)
        if current not in swap_fun_position:
            swap_fun_position.append(current)
            candidate[temp] = swap_fun(current[0], current[1], current_route)
            if candidate[temp] not in tabu_list:
                candidate_distance[temp] = cal_dis(candidate[temp], distance, n)
                temp += 1
            if temp >= candidate_number:
                break

    candidate_best = min(candidate_distance)
    best_index = candidate_distance.index(candidate_best)
    current_distance = candidate_best
    current_route = copy.copy(candidate[best_index])

    if current_distance < best_distance:
        best_distance = current_distance
        best_route = copy.copy(current_route)

    tabu_list.append(candidate[best_index])
    tabu_time.append(tabu_limit)
    current_tnum += 1


def update_tabu(n):
    global current_tnum
    global tabu_time
    delet_num = 0
    temp = [0 for col in range(n)]
    tabu_time = [x-1 for x in tabu_time]
    for i in range(current_tnum):
        if tabu_time[i] == 0:
            delet_num += 1
            tabu_list[i] = temp

    current_tnum -= delet_num
    while 0 in tabu_time:
        tabu_time.remove(0)

    while temp in tabu_list:
        tabu_list.remove(temp)


def main(runtime, candidate_number):
    processing_data("att48.tsp")
    data_list = read_coordinate("att48.txt")
    coordinate = np.array(data_list)
    dis_mat = getdis(coordinate)
    n = coordinate.shape[0]
    rt = runtime
    initial(n, dis_mat)
    for runtime in range(rt):
        move(n, dis_mat, candidate_number)
        update_tabu(n, tabu_time)
    dic = {
        "best distance:": best_distance,
        "tabu_time:": tabu_limit,
        "candidate number:": candidate_number,
        "best route:": best_route
    }
    js = json.dumps(dic)
    file_object = open('ts.txt', 'a+')
    file_object.write(js)
    file_object.write('\n')
    file_object.close()


for i in range(31):
    tabu_list = []
    tabu_time = []
    candidate_number = 300
    runtime = 3000
    current_tnum = 0
    candidate = [[0 for i in range(48)] for j in range(candidate_number)]
    candidate_distance = [0 for i in range(candidate_number)]
    best_route = []
    best_distance = sys.maxsize
    current_route = []
    current_distance = 0.0
    main(runtime, candidate_number)