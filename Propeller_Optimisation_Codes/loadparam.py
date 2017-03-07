'''
Created on Nov 20, 2014

@author: Binoy Pilakkat
'''
import csv
import numpy as np


def ktparam():
    '''
    return coefficients and terms of the KT
    '''


    csv_file = open('kt_param.csv')
    data = list(csv.reader(csv_file))


    struct_data = np.zeros((39,),dtype=([('c','f8'),('s','i2'),('t','i2'),\
                               ('u','i2'),('v','i2')]))

    index = 0
    for line in data[1:]:
        struct_data[index] = tuple([np.float64(i) for i in line[1:]])
        index += 1
    return struct_data

def kqparam():
    '''
    return coefficients and terms of the KQ
    '''


    csv_file = open('kq_param.csv')
    data = list(csv.reader(csv_file))
    struct_data = np.zeros((47,),dtype=([('c','f8'),('s','i2'),('t','i2'),\
                               ('u','i2'),('v','i2')]))
    index = 0
    for line in data[1:]:
        struct_data[index] = tuple([np.float64(i) for i in line[1:]])
#             print float(line[1:][0])
        index += 1
    return struct_data
if __name__ == "__main__":
    kq = kqparam()
    kt = ktparam()
    print kq
    print kt['t']