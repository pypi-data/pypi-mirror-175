'''
Description: 
version: 1.0
Author: JamesRay
Date: 2022-09-13 19:09:13
LastEditors: Please set LastEditors
LastEditTime: 2022-10-05 01:06:04
'''
from ast import arg
import sys,os,psutil
import pandas as pd
import polars as pl
import datetime as dt
from datetime import datetime
import multiprocessing
import json, re, math
from collections import OrderedDict, defaultdict
import time
from functools import wraps
import jsonpath
import logging
import logging.config

from fastFET.MultiProcess import ProcessingQueue

#########
# deal with files & file names#
#########

def makePath(path: str):
    '''given any path, if the intermediate nodes are not exist, make the dir.
    if basefile existed, clear the content.
    - return: arg: path'''
    folderPath = ""
    nodeList= path.split(os.sep)
    if nodeList[0]=="":
        folderPath += os.sep
        nodeList.pop(0)
    for node in nodeList[:-1]:
        folderPath += node + os.sep
        if(not os.path.isdir(folderPath)):
            os.mkdir(folderPath)
    if nodeList[-1] != '':
        path= folderPath + nodeList[-1]
        # 此时path代表一个文件，如果原文件存在，则要清空里面的内容
        open(path, 'w').close()
    return(path)

def intervalMin(type, prjtNm):
    '''- type: 'updates'(rrc间隔5分钟, route-views间隔15分钟) or 'ribs'(rrc间隔8小时；route-views间隔2小时)
    - prjtNm: 'rrc' or 'route-views'. 
    - return: int(min) '''
    strmap= {'updates': {'rrc': 5, 'rou': 15},
             'ribs'   : {'rrc': 8*60, 'rou': 2*60}}
    return strmap[type][prjtNm[:3]]

def normSatEndTime(interval, satTime: datetime, endTime: datetime):
    '''normalize the time to fit file names.
    - '''
    if interval== 5 or interval== 15:
        while 1:
            if satTime.minute % interval == 0:
                break
            satTime -= dt.timedelta(seconds= 60)
        while 1:
            if endTime.minute % interval == 0:
                break
            endTime += dt.timedelta(seconds= 60)
    if interval== 480 or interval== 120:
        while 1:
            if satTime.hour % (interval/60) == 0:
                break
            satTime -= dt.timedelta(seconds= 3600)
        while 1:
            if endTime.hour % (interval/60) == 0:
                break
            endTime += dt.timedelta(seconds= 3600)
    return (satTime, endTime)

def cut_files_list(files, satTime, endTime):
    '''裁剪文件名列表至指定的起止时间范围内。
    - 方法：提取文件名列表中所有的日期字符子串。等于未下载/未下载完全
    - Note: files仅含upd / rib 中一种，且不为空'''
    try:
        files= sorted(files)
        mmnts_in_files= [ re.search('\d{8}.\d{4}', file).group() for file in files ]
        satIdx= mmnts_in_files.index(satTime.strftime( '%Y%m%d.%H%M' ))
        endIdx= mmnts_in_files.index(endTime.strftime( '%Y%m%d.%H%M' ))
        cuted= files[ satIdx:endIdx+1 ]
    except:
        # 在文件名列表中找不到起止索引的原因：文件真的没有下载/解析完全；文件名中的时间子串的时间间隔格式不是5的倍数
        raise RuntimeError(f'can`t cut files like `{files[0]}`, you should check if existing incomplete files, or if having a different time format in file names.')
    return cuted

def allIn(interval, realFiles, satTime: datetime, endTime: datetime):
    '''- find time points which we `need`; 
    - compared with time points which we already `had`. 
    '''
    # get need-list
    need=[]
    while satTime.__le__( endTime ):
        need.append( satTime.strftime( '%Y%m%d.%H%M' ))
        satTime += dt.timedelta(seconds= interval* 60)
    # get had-list
    had= []
    try:
        had= [ re.search('\d{8}.\d{4}', file).group() for file in realFiles ]
    except:
        logger.error(f'some file names in `{realFiles}` have not contain format like `2020.1010` ')    
    # 求交集，needlist需全属于hadlist
    if len(set(need) & set(had)) != len(need):
        return False
    
    return True
    
#########
# other #
#########

def dict_list():
    return defaultdict(list)

def d_d_list():
    return defaultdict( dict_list )

def paralNum(k):
    '''用于选择并行时的核数
    - k代表使用当前总核数的1/k'''
    total= multiprocessing.cpu_count()
    if total>8:
        return total//k
    else:
        return total

def computMem(var):
    '''- 计算变量的内存（Mb）'''
    
    if isinstance(var, pd.DataFrame):
        res= var.memory_usage( deep=True).sum()/1024**2
    elif isinstance(var, pl.DataFrame):
        res=  var.estimated_size()/1024**2
    else:
        res=  sys.getsizeof(var)/1024**2
    res_str= '%.3f' % res
    return res_str
    

##############
# parse feats#
##############

def runJobs( file_dict, func, nbProcess= 4 ):
    '''- main function'''
    isParallel= False
    makePath( os.getcwd()+ os.sep+ 'Dataset_features/')

    logger.info(' ')
    logger.info(curMem())
    s= '# FEATURE EXTRACT #'
    logger.info('#'* len(s))
    logger.info(s)
    logger.info('#'* len(s))

    upd_evt_list= list(file_dict['updates'].items())
    rib_evt_list= list(file_dict['ribs'].items())
    if not len(rib_evt_list):
        rib_evt_list= [None]* len(upd_evt_list)
    jobs= zip( upd_evt_list, rib_evt_list )

    # debug: 放弃使用Pool，因为它不能在子进程中创建子进程（由于daemon的存在），因此自定义了一个多进程类。
    '''pool= multiprocessing.Pool(processes= nb_process)
    pool.map_async(func, zip( upd_evt_list, rib_evt_list))    # TODO:尝试map_异步等函数
    pool.close()
    pool.join()''' 
    # debug2: 放弃自定义进程池，由于内存压力，决定逐事件采集。
    if isParallel:
        processingQueue = ProcessingQueue(nbProcess=nbProcess)  # 开一个进程池
        for j in jobs:
            processingQueue.addProcess( func, args= j )         # 任务入队
        processingQueue.run(logger)                             # 执行子进程们的主函数。这里run内步骤的最后包含了close和join。'''
    
    else:
        for args in jobs:
            func( *args )


def csv2df(headers , paths:list, not_priming= True, space=6 ):   # space8()
    '''合并paths为大文件；读取数据到pl.dataframe。
    - a step with merging to a big file (need to <5G)
    - args: paths: 若读取rib，则列表中仅一个文件。若读取upds-priming，则列表中多个文件，此时not_priming=False。若读取upds, 则多文件，True
    - return: pl.DF'''
    paths= list(paths)
    merged= ''
    str_map= {True: 'upds', False: 'ribs' }

    if len(paths) != 1:     # 非rib
        # 先增加一个文件，内容为列名。防止pl读到首行是撤销
        s= '|'.join( headers )+ '|'
        out= os.path.dirname(paths[0])+ '/head.txt'
        os.system('echo \''+ s+ '\' > '+ out)
        paths_str= out+ ' '+ ' '.join(paths)
        # 后cat合并所有文件
        merged= os.path.dirname(paths[0])+ '/merged.txt'
        t1= time.time()
        os.system('time cat '+ paths_str+ ' > '+ merged)
        logger.info(' '*8+ str_map[not_priming]+ '---> merge upd files cost: %3.3fs; size: %.3fMb' % (time.time()-t1, os.path.getsize(merged)/1024**2 ) )
        
    # 后读取
    t2= time.time()
    isUpds= bool(len(paths)-1)
    file_map= {True: merged, False: paths[0] }
    
    df= pl.read_csv(file_map[ isUpds ], sep='|', has_header= isUpds , ignore_errors= True)
    if len(paths)==1:
        df.columns= headers   # 若果读取的是rib表，则要手动添加表头字段。
    logger.info(' '*8+ str_map[ (isUpds & not_priming)] +'---> read  csv files cost: %3.3fs; mem: %5.2fMb; shape: %s' % (time.time()-t2, df.estimated_size()/1024**2, str(df.shape) ) )

    # 最后删除merge.txt、head.txt
    if len(paths) != 1:
        os.system( 'rm -f '+ merged+ ' '+ out )
    
    return df

def splitChunk(paths:list, need_rib):
    '''为了加快polars读取过程，当文件集合需要按照整体size大小分块
    - 需要在此进行更复杂的分块：考虑到图特征、cpu数量、内存大小。
    - return: list[list]'''
    # 拿到paths的总sizeG
    size, chunksize= 0, 0
    res= []
    for f in paths:
        size+= os.path.getsize(f)
    sizeG= size/1024**3

    if not need_rib:
        chunksize= 1
        chunk= math.ceil( sizeG/chunksize )
        chunk_files= math.ceil( len(paths)/chunk )
        for i in range(chunk-1):
            res.append( paths[i*chunk_files: (i+1)*chunk_files])
        res.append( paths[(chunk-1)* chunk_files:] )
    else:
        # 需要图特征时，就复杂了：每个slot都有df_rib与df_upd的合并与计算以拿到分分钟更新的全局path，从而能构建全局拓扑。
        pass

    logger.info(f'    updates files: total size {sizeG:.3f}Gb; max limit per chunk {chunksize}Gb')

    return res

def exprDict( featNm_pfx:str):
    '''对目标列featNm输出三个polars表达式：计数、出现的均值、出现的最大值。不用输出`求和`，因为‘和’就是条目总数的统计。'''
    dic= {
        featNm_pfx+ "_cnt": pl.col(featNm_pfx).count().suffix("_cnt"),
        featNm_pfx+ "_avg": pl.col(featNm_pfx).mean().suffix("_avg"),  # debug: 无法使用.cast(pl.Float32)   在有的情况不能正常地f64转f32，原因未知。
        featNm_pfx+ "_max": pl.col(featNm_pfx).max().suffix("_max")
    }
    return dic

def featsGrouping(dictTree:dict, feats:list):
    '''实现对目标特征集合中的特征分组，并拿到每组的节点路径。
    - arg: dictTree:一个完整的字典树（叶为Expr，父为所有的featName，父以上为特征类别）, 
    - arg: feats:目标特征集合。
    - return: dict[key: 路径元组；val: 一个路径下的目标特征子集list ] '''
    # 先找到每个feat在特征树中的父节点路径。
    feats_paths= {} # key特征名；val路径元组
    for feat in feats:
        curpath= jsonpath.normalize(jsonpath.jsonpath(dictTree, '$..'+feat, result_type='PATH')[0])
        curNodes=tuple( curpath.split(';')[1:])
        feats_paths[ curNodes[-1]]= curNodes[:-1]
    paths_feats= {} 
    # 后交换key-val对，同时合并相同key(即路径元组)的val到一个list中（即特征分组了）
    for feat, path in feats_paths.items():
        if path not in paths_feats.keys():
            paths_feats[ path ]= [feat]
        else:
            paths_feats[ path ].append( feat )
    return paths_feats

def feat2expr( featTree, feats ):
    '''只是简化特征树，从featTree得到{特征名: expr}的单层字典'''
    feats_exprs= {} # key:特征名；val:expr
    for feat in feats:
        curexpr= jsonpath.jsonpath(featTree, '$..'+feat, result_type='VALUE')[0]
        feats_exprs[feat]= curexpr
    return feats_exprs

##############
# graph feats#
##############

def df2edge( df: pl.DataFrame ):
    '''从一个原始df中分析path字段，得到所有的边，以此构建全局AS拓扑图
    - 拓展：需不需在建图时给每个节点、边增加一些属性（如BML框架有属性‘IP数量’）。暂时不需要我认为。只需拿到边的集合即可
    - 处理path字段的方法：split成list，对于有 prePending的，不能用unique()，这会打乱AS顺序。
    - arg: df: 是原df，不是FET.chunkHandler中被preProcess()预处理后的df
    - return: list(tuple(ASNum, ASNum)) '''
    res= ( df.lazy()
        .filter(
            (pl.col("msg_type") != 'STATE') &   # TODO: 具体看看过滤啥。评判下是否peer-pfx具有唯一性。
            (~pl.col('path').str.contains('\{'))
            )
        #.groupby(['peer_AS', 'dest_pref']).tail(1)   # 注：df是从rib表来的，peer-pfx具有唯一性，因此不需分组取末行。
        .select( [
            pl.col('path').str.split(" ").alias('path_list')
            ])
        .with_row_count('index')       # 用于给rib_df的每个条目编号
        .explode('path_list')
        .groupby('index').agg([
            pl.col( 'path_list'),
            pl.col( 'path_list').shift(-1).alias('path_list_shift')     # 如此一来，同一行的这两列的值相结合的tuple，就得到一条边了，避免了for循环。
        ])
        .filter( ( pl.col( 'path_list_shift' ) != None) &
                 ( pl.col( 'path_list')== pl.col( 'path_list_shift') ) ) # 过滤掉prePending造成的`同点边`，和最右一个AS形成的`单点边`
        .select( pl.exclude( 'index' ))
    ).collect().rows()
    return res 


##############
# Decorator  #
##############

def timer(func):
    '''- in wrap, args[-1] is space, args[-2]  '''
    @wraps(func)    # 有效防止在多进程时候， 装饰器不能序列化
    def wrap(*args, **kwargs):
        begin_time = time.perf_counter()
        begin_memo = curMem()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        end_memo = curMem()

        try:
            funcName= func.__name__ if func.__name__ != 'run_cmpxFeat_inMulproc' else args[-2]
            logger.info(' '* args[-1] + f'func= `{funcName}`; cost={(end_time - begin_time):3.2f} sec; begin&end_memo= {begin_memo}->{end_memo}; ppid={os.getppid()} ') 
        except Exception as e:
            #raise e
            logger.info(' '*6+ f'..func= `{funcName}`; cost={(end_time - begin_time):3.2f} sec; begin&end_memo= {begin_memo}->{end_memo}; ppid={os.getppid()} ') 
        return result 
    return wrap

#########
#  log  #
#########

def setup_logging(configPath= os.path.dirname(__file__)+ '/logConfig.json',default_level=logging.DEBUG):
    ''' - config logging
        - dir `/log` located at current working dir.'''
    makePath(os.getcwd()+ '/log/')
    if os.path.exists(configPath):
        with open(configPath,"r") as f:
            config = json.load(f)
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

logger= logging.getLogger()

def logMemUsage( space:int, func_name:str ):
    '''- 获取锚点所在函数的名字、函数位于的进程(内存使用)、父进程(内存使用)'''
    s= " "*space+ "<mem usage> func: `%20s`, cur_pid: %d (%s), ppid: %d (%s)" % (
            func_name,
            os.getpid(),
            curMem(),
            os.getppid(),
            curMem()
    )
    return s

def curMem(is_ppid= False):
    '''- 调用了该函数的进程在当前时刻的内存使用情况(Mb)'''
    if is_ppid:
        res= psutil.Process(os.getppid()).memory_info().rss/1024**2
    else:
        res= psutil.Process(os.getpid() ).memory_info().rss/1024**2
    return "%.1fMb" % res


    
if __name__=='__main__':
    setup_logging()
    