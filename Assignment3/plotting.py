# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 14:19:02 2019

@author: looly
"""
from main import Triest
import matplotlib.pyplot as plt
import numpy as np

def plotting(dataset):
    
  #Plotting   
    if dataset == "1":
        M = [10,20,30,40,50,60,70,80,90,100]
        base_est = np.zeros((3,10))
        improved_est = np.zeros((3,10))
        dynamic_est = np.zeros((3,10))
        path = "./DataSet/out.contiguous-usa"
    elif dataset == "2":
        M = [500, 1000,2500, 5000, 7500, 10000]
        base_est = np.zeros((3,6))
        improved_est = np.zeros((3,6))
        dynamic_est = np.zeros((3,6))
        path = "./DataSet/out.petster-friendships-hamster-uniq"
    elif dataset == "3":
        M = [5000, 10000, 15000, 20000, 25000, 30000]
        base_est = np.zeros((3,6))
        improved_est = np.zeros((3,6))
        dynamic_est = np.zeros((3,6))
        path = "./DataSet/out.as-caida20071105"
    
    for i in range(3):
        for j, m in enumerate(M):
    
            triest_base = Triest(path, m)
            triest_base.triest_base()
            base_est[i,j] = triest_base.estimate
    
            triest_improved = Triest(path, m)
            triest_improved.triest_improved()
            improved_est[i,j]  = triest_improved.estimate
    
            triest_dynamic = Triest(path, m)
            triest_dynamic.triest_dynamic()
            dynamic_est[i,j] = triest_dynamic.estimate


    base_avg = np.mean(base_est, axis=0)
    improved_avg = np.mean(improved_est, axis=0)
    dynamic_avg = np.mean(dynamic_est, axis=0)
    plt.figure()
    plt.plot(M, base_avg)
    plt.plot(M, improved_avg)
    plt.plot(M, dynamic_avg)
    plt.xlabel('Number of M')
    plt.ylabel('Exsitmated Traingles')
    plt.legend(['Base', 'Improved', 'Dynamic'], loc='upper left')
    plt.title('Dataset: {}' .format(dataset))
    plt.savefig('Images/{}_avg.png' .format(dataset))
    plt.show()