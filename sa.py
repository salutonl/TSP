import numpy as np
import math
import sys
import random
import copy
import json


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


def get_dis(coordinate):
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


def cal_dis(route, distance, n):
    sum_dis = 0
    for i in range(n - 1):
        sum_dis += distance[route[i]][route[i+1]]
    sum_dis += distance[route[n-1]][route[0]]
    return sum_dis


def get_new_route(route, times, n):
    current = copy.copy(route)

    if times % 2 == 0:
        u = random.randint(0, n-1)
        v = random.randint(0, n-1)
        temp = current[u]
        current[u] = current[v]
        current[v] = temp
    else:
        temp2 = random.sample(range(0, n), 3)
        temp2.sort()
        u = temp2[0]
        v = temp2[1]
        w = temp2[2]
        w1 = w + 1
        temp3 = [0 for col in range(v - u + 1)]
        j =0
        for i in range(u, v + 1):
            temp3[j] = current[i]
            j += 1

        for i2 in range(v + 1, w + 1):
            current[i2 - (v-u+1)] = current[i2]
        w = w - (v-u+1)
        j = 0
        for i3 in range(w+1, w1):
            current[i3] = temp3[j]
            j += 1
    return current


def main(T0, T1, ite, alpha):
    processing_data("att48.tsp")
    data_list = read_coordinate("att48.txt")
    coordinate = np.array(data_list)
    dis_mat = get_dis(coordinate)
    n = coordinate.shape[0]
    route = random.sample(range(0, n), n)
    total_dis = cal_dis(route, dis_mat, n)
    best = route
    best_total_dis = total_dis
    t = T0
    while True:
        if t <= T1:
            break
        for rt2 in range(ite):
            newroute = get_new_route(route, rt2, n)
            new_total_dis = cal_dis(newroute, dis_mat, n)
            delt = new_total_dis - total_dis
            if delt <= 0:
                route = newroute
                total_dis = new_total_dis
                if best_total_dis > new_total_dis:
                    best = newroute
                    best_total_dis = new_total_dis
            elif delt > 0:
                p = math.exp(-delt / t)
                ranp = random.uniform(0, 1)
                if ranp < p:
                    route = newroute
                    total_dis = new_total_dis
        t = t * alpha
    dic = {
        "best distance:": best_total_dis,
        "original temperature:": T0,
        "end temperature:": T1,
        "alpha:": alpha,
        "best route:": best
    }
    js = json.dumps(dic)
    file_object = open('sas.txt', 'a+')
    file_object.write(js)
    file_object.write('\n')
    file_object.close()


for i in range(31):
    main(100, 1e-8, 3000, 0.97)