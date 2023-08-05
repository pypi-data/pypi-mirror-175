'''
Description: 
version: 1.0
Author: JamesRay
Date: 2022-05-26 14:24:30
LastEditors: Please set LastEditors
LastEditTime: 2022-07-19 05:34:57
'''
import os ,sys, re
import datetime as dt
import polars as pl
import pandas as pd
import glob
from collections import defaultdict
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from fastFET.collectData import GetRawData
from fastFET.utils import d_d_list



def getDFPath(path, event_dic):
    ''' return {event_name: { collector: file_name } }'''
    flist= os.walk(path).__next__()[2]
    DFPath = d_d_list()
    for f in flist:
        subl= f[:-4].split('__')
        DFPath[subl[1]][subl[2]]= path+ f
    return DFPath

def make_label(event_dic: dict, DFPath: dict):
    ''' ① make label with anomaly=1, normal=0 at column `timestamp`
        ② delete the row which has the duplicate `time_bin` value
        ③  write to file.'''
    for event, dic in event_dic.items():
        for collector, lis in dic.items():
            staT= lis[0].timestamp()
            endT= lis[1].timestamp()
            f= DFPath[event][collector]
            df= pl.read_csv(f)
            df= (df.with_column(
                    pl.when((pl.col('timestamp')>= staT) & (pl.col('timestamp')<= endT)).then(1).otherwise(0)
                    .alias('label')
                )
                .filter((pl.col('time_bin')- pl.col('time_bin').shift()) !=0)
                .drop('timestamp')
            )
            df.write_csv(f, sep=',')
            print('have made label with %s.' % f)

if __name__== "__main__":
    grd= GetRawData(increment=0)
    event_dic= grd.getEventsDict()
    path= 'Dataset/features/tradition/'
    DFPath= getDFPath(path, event_dic)
    make_label(event_dic, DFPath)