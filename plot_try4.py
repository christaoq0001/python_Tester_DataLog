# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 20:47:23 2016

@author: Chris
"""

import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import itertools

def setdim(n):
    ''' This fucntion take integer input n and return a proper
    row and  colums for proper subplots '''
    rows = np.floor(np.sqrt(n))
    colums = np.ceil(n/rows)
    return [int(rows), int(colums)]
    
def splitparam(param):
    if '_' in param:
        return param.split('_', maxsplit=1)
    else:
        txt = str()
        num = str()       
        for letter in param:
            if letter.isnumeric():
                num += letter
            elif letter.isalpha():
                txt +=letter
            else:
                pass                         
        return txt, num
        
def scatter(excel_name, *args, **kwargs):    
    raw = pd.read_excel(excel_name)
    for ix, item in enumerate(raw.columns):
        raw.columns.values[ix] = item.strip()
    # process input
    df = raw.set_index(list(args))
    df = df.sort_index()
    # process input arguments
    idx_dict = kwargs
    for k, v in enumerate(args):
        if v not in kwargs.keys():
            idx_dict[v] = df.index.levels[k].values
    # plot according to input requirements
    idx = pd.IndexSlice
    if len(args) == 3:
        if len(kwargs['params']) == 1:
            [r,c] = setdim(len(idx_dict[args[2]]))
            for d3_ix, d3 in enumerate(idx_dict[args[2]]):
                plt.subplot(r,c,d3_ix+1)
                lc = itertools.cycle(['r','b','c','m','k', 'g'])
                mk = itertools.cycle(['o','D','+','.','^','*'])
                for d2_ix, d2 in enumerate(idx_dict[args[1]]):
                    data = df.loc[idx[:, d2, d3], kwargs['params']]
                    x = list(data.index.labels[0])
                    y = data.values
                    plt.plot(x,y,label = d2, color=next(lc),ls='solid', \
                            linewidth=3, marker=next(mk), markersize = 10 )
                plt.title(d3)
                plt.xlabel(args[0])
                plt.ylabel(kwargs['params'])
                plt.legend()
            plt.show()
        else:
            cb_list = list(itertools.product(idx_dict[args[2]], idx_dict[args[1]]))
            [r,c] = setdim(len(cb_list))
            for cb_ix, cb in enumerate(cb_list):
                plt.subplot(r,c,cb_ix+1)
                lc = itertools.cycle(['r','b','c','m','k', 'g'])
                mk = itertools.cycle(['o','D','+','.','^','*'])
                for param_ix, param in enumerate(kwargs['params']):
                    data = df.loc[idx[:, cb_list[cb_ix][1], cb_list[cb_ix][0]], param]
                    x = list(data.index.labels[0])
                    y = data.values
                    plt.plot(x,y, label=param, color=next(lc),ls='solid', \
                            linewidth=3, marker=next(mk), markersize = 10)
                plt.title(cb,fontsize=20)
                plt.xlabel(args[0],fontsize=20)
                plt.ylabel(param, fontsize=20)
                plt.legend()
            plt.show()
    else:
        pass
