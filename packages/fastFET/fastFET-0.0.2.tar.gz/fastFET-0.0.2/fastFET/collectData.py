import math
import os, sys, csv, re
import datetime as dt
from datetime import datetime
from copy import deepcopy
import glob
import time

import multiprocessing

#sys.path.append( os.path.dirname(os.path.dirname(__file__)))
from fastFET.BGPMAGNET.dataGetter import downloadByParams
from fastFET.BGPMAGNET.base import base_params, bgpGetter
from fastFET.BGPMAGNET.params import BGP_DATATYPE
from fastFET.utils import logger
from fastFET import utils

class GetRawData(object):
    
    def __init__(self, 
    event_list_path= 'event_list.csv',
    increment= 4,  
    duration= 2,   # 
    parent_folder= "Dataset/",   #   /data/bgpdata/
    ribs= False
    ):
        '''`event_list.csv` -> download `.gz`files -> `bgpdump` to `.txt` -> `.txt`files   

        args:
        - increment: 定义事件起止时间的增量(h)
        - duration: 当事件缺省结束时间时，将其指定为 start_time + duration (h)
        - collection_data_lib: 定义BGP原始数据存放位置
        - updates: 是否需要收集updates数据。取消这个参数。因为不用问，传统特征、图特征的提取都需使用update消息。
        - ribs: 是否需要收集ribs数据
        '''
        self.path= event_list_path
        self.increment= increment
        self.duration= duration

        self.ribTag= ribs
        self.collection_data_lib= parent_folder+ 'raw_cmpres/'
        self.collection_data_lib_parsed= parent_folder+ "raw_parsed/"

        logger.info('')
        s= '# download & decode to ASCII #'
        logger.info('#'* len(s))
        logger.info(s)
        logger.info('#'* len(s))
  
    def getEventsDict(self):
        '''
        - description: read events from `self.path`.  
        - 主要目的：把用户自定义事件起止时间规范化为符合raw文件名的、并考虑到了increment和rib表更新等参数的  起止时间
            - 若FET类不采图特征，则只收集updates文件：`新起止时间= (原起止± increment)*标准化`
            - 若FET类要采图特征，则还需收集ribs文件： 在上式基础上，添加一个datetime_atRIB。图特征的采集需要从datetime_atRIB到datetime_end的全部updates消息。``
        - return {'eventName':{'collector': [datetime_start, datetime_end, datetime_atRIB]}} arg3可能为None。'''
        # get time slot of each event
        with open(self.path) as f:
            event_list= []
            csv_file= csv.reader(f)
            for line in csv_file:
                event_list.append(list(line))
        # get time slot of each event which to be collected. 
        res= utils.d_d_list()
        for event in event_list:
            if len(event):
                start= dt.datetime.strptime(event[1].strip(), "%Y/%m/%d %H:%M:%S")- dt.timedelta(hours= self.increment )
                if event[2].strip():
                    end = dt.datetime.strptime(event[2].strip(), "%Y/%m/%d %H:%M:%S")+ dt.timedelta(hours= self.increment )
                else:
                    end = dt.datetime.strptime(event[1].strip(), "%Y/%m/%d %H:%M:%S")+ dt.timedelta(hours= self.increment+ self.duration)

                for monitor in event[3:]:
                    monitor= monitor.strip()
                    interval_upd= utils.intervalMin('updates', monitor)     # 为5 或 15
                    satTime, endTime= utils.normSatEndTime(interval_upd, start, end)
                    # 如上拿到了该事件该采集器下的标准化的起止时间。此时若ribtag关，则直接导出起止时间。若开，起始时间还需往前找
                    satTime_atRIB= None
                    if self.ribTag:
                        interval_rib= utils.intervalMin('ribs', monitor)    # 为480 或 120
                        satTime_atRIB, _= utils.normSatEndTime(interval_rib, satTime, endTime)
                    res[event[0]][monitor]= [satTime, endTime, satTime_atRIB]

        return res

    def isDwlad(self, type, monitor, satTime: datetime, endTime: datetime):
        '''- 若下载过起止时间内的文件，则返回裁剪后的文件名列表；若未下载过，返回空列表'''
        try:
            ppath, _, files = os.walk(self.collection_data_lib+ monitor).__next__()
            assert len(files) != 0
            try:
                # Note: 只选择目录中的rib或updates的一类文件。
                files= sorted( [ f for f in files if type in f])
                files_cuted= utils.cut_files_list(files, satTime, endTime)
                res= [ppath+ os.sep+ file for file in files_cuted]
                return res
            except:
                return []
        except:
            return []

    def download(self, type:str, monitor, satTime, endTime):
        '''- download files in whole days. 
        - then cut files to sat and end. 
        - return: cuted_files.'''
        sat= satTime.strftime('%Y-%m-%d')+ "-00:00"
        end= endTime.strftime('%Y-%m-%d')+ "-23:59"
        bgpdbp=downloadByParams( 
            urlgetter=bgpGetter(base_params(
                start_time= sat,
                end_time  = end,
                bgpcollectors=[monitor],
                data_type=BGP_DATATYPE[type.upper()]
            )),
            destination= self.collection_data_lib,
            save_by_collector=1
        )
        bgpdbp.start_on()
        # check_error_list(sys.path[0]+ "/errorInfo.txt")
        whole_files= glob.glob(self.collection_data_lib+ monitor+ os.sep+ monitor+ '_'+ type+ '*')
        dest_files= utils.cut_files_list(whole_files, satTime, endTime)
        return dest_files

    # 用于raw2txt中的多进程
    def trans_multiproc(self, tup):
            os.system('bgpdump -m '+ tup[1] + ' > '+ tup[0] +  os.path.basename(tup[1])+ '.txt')

    def raw2txt(self, dest_dir, raw_files):       
        '''- description: transform BGP update raw data to .txt by command `bgpdump`
        - return `.txt list`
        '''
        dest_dirs= [ dest_dir ]* len(raw_files)
        
        pool= multiprocessing.Pool(multiprocessing.cpu_count()//2)
        pool.map(self.trans_multiproc, zip(dest_dirs, raw_files))
        pool.close()
        pool.join()

        parsed_files= sorted(glob.glob(dest_dir + '/*'))
        return parsed_files

    def oneMonitor(self, txt_dir, monitor, fact_satTime, endTime):
        '''- getUpdTxts的子函数，用于单个monitor的下载（已下载则不再下载）和解析操作
        - return：txtfiles 文件名列表'''
        curDir= utils.makePath( txt_dir+ monitor+ '/' )
        os.system(' rm -r '+ curDir+ '*')
        raw_files= self.isDwlad('updates', monitor, fact_satTime, endTime)
        if not len(raw_files):    # 未下载
            st1= time.time()
            raw_files= self.download('updates', monitor, fact_satTime, endTime)
            logger.info(' '*4+ '- %s dwladed: %.3f sec, %d files.' %( monitor, time.time()- st1, len(raw_files)))
        st2= time.time()
        txtfiles= self.raw2txt( curDir, raw_files )
        logger.info(' '*4+ '- %s parsed: %.3f sec, %d files.' %( monitor, time.time()- st2, len(raw_files)))

        return txtfiles

    def getUpdTxts(self, events_dict):
        '''解析updates文件
        - return:  `{'evtNm': {'monitor': ( [ .txt, ...], str|None ) } } `'''
        res= deepcopy( events_dict )
        ppath, dirs, _= os.walk( self.collection_data_lib_parsed ).__next__()
        for evtNm, moniDict in events_dict.items():
            logger.info(' '*2+ '- %s:' % evtNm )
            if evtNm in dirs:   # 当事件名目录已存在
                p2, moni_dirs, _ = os.walk( ppath+ evtNm+ os.sep ).__next__()
                for monitor,[ satTime_tradiFeat, endTime, satTime_graphFeat ] in moniDict.items():
                    # 以上3个时间都是标准化了的。updates消息的起始解析时刻有两种：
                    #   - 只有传统特征时，就是`原starttime`
                    #   - 要解析图特征时，把`原starttime`替换为`satTime_atRIB`
                    # 需求的文件名列表是否都在 实际的文件名列表中 allin
                    txtfiles= sorted(glob.glob(p2+ monitor+ os.sep+ monitor+ '_updates*'))
                    if not satTime_graphFeat :
                        fact_satTime= satTime_tradiFeat
                        watershed_= None
                    else:
                        fact_satTime= satTime_graphFeat
                        watershed_= satTime_tradiFeat.strftime('%Y%m%d.%H%M')

                    interval= utils.intervalMin('updates', monitor[:3])
                    allin= utils.allIn(interval, txtfiles, fact_satTime, endTime)

                    if monitor in moni_dirs and allin :
                        target_files= utils.cut_files_list(txtfiles, fact_satTime, endTime)
                        # 变量 watershed_ 用在有图特征的情况下，切分updates的文件列表target_files。使其前部分用于更新拓扑；后部分用于计算传统特征。
                        res[evtNm][monitor]= ( target_files, watershed_ )
                        logger.info(' '*4+ '- %s: upds has existed, don\'t need to parse.' % monitor)
                    else:   # 未解析过该采集器
                        res[evtNm][monitor]= ( self.oneMonitor(p2, monitor, fact_satTime, endTime), watershed_ )
                        
            else:   # 未解析过该事件
                for monitor,[ satTime_tradiFeat, endTime, satTime_graphFeat ] in moniDict.items():
                    if not satTime_graphFeat :
                        fact_satTime= satTime_tradiFeat
                        watershed_= None
                    else:
                        fact_satTime= satTime_graphFeat
                        watershed_= satTime_tradiFeat.strftime('%Y%m%d.%H%M')

                    res[evtNm][monitor]= ( self.oneMonitor(ppath+ evtNm+ '/', monitor, fact_satTime, endTime), watershed_ )
        return res

    def getRibTxts(self, events_dict):
        '''解析rib文件。每个 event/monitor 下仅需一个rib（startTime的左邻近）'''
        strmap= {'rrc': 'bview.', 'rou': 'rib.'}
        res= deepcopy( events_dict )
        ppath, dirs, _= os.walk( self.collection_data_lib_parsed ).__next__()
        for evtNm, moniDict in events_dict.items():
            logger.info(' '*2+ '- %s:' % evtNm )
            if evtNm not in dirs:
                for monitor,_ in moniDict.items():
                    utils.makePath( ppath+ evtNm+ '/' + monitor+ '/' )

            for monitor,[ _, _, satRIBtime ] in moniDict.items():
                # 这个唯一rib表的路径的部分表示
                rib_path= self.collection_data_lib+ monitor+ os.sep+ monitor+ '_'+ strmap[monitor[:3]]+ satRIBtime.strftime('%Y%m%d.%H')
                # download
                lkup= glob.glob(rib_path+ '*')
                if len(lkup):   # 不用下载
                    path_raw= lkup[0]
                else:   # 只下载一个rib文件
                    sat= satRIBtime.strftime('%Y-%m-%d-%H:%M')
                    bgpdbp=downloadByParams( 
                        urlgetter=bgpGetter(base_params(
                            start_time= sat,
                            end_time  = sat,
                            bgpcollectors=[monitor],
                            data_type=BGP_DATATYPE['RIBS']
                        )),
                        destination= self.collection_data_lib,
                        save_by_collector=1
                    )
                    bgpdbp.start_on()
                    res= glob.glob(rib_path+ '*')
                    path_raw= res[0]

                # parse the only one rib file
                path_par = ppath+ evtNm+ os.sep+ monitor+ os.sep+ os.path.basename(path_raw)+ '.txt'
                lkup= glob.glob(path_par)
                if not len(lkup):   # 当没解析过，且需要rib数据时才解析—— 耗时严重
                    st3= time.time()
                    os.system('bgpdump -m '+ path_raw + ' > '+ path_par )
                    logger.info(' '*4+ '- %s parsed: %.3f sec, at `%s`.' %( monitor, time.time()- st3, path_par))
                else:
                    logger.info(' '*4+ '- %s: ribs has existed, don\'t need to parse.' % monitor)
                res[evtNm][monitor]= path_par                
        return res

    def getRawTxts(self, events_dict: dict):
        '''- including download and parse
        - return `{ 'updates': {'evtNm': {'monitor': ([ '.txt', ...], str|None) } }, 
                    'ribs'    : {'evtNm': {'monitor': '.txt' } }
                  }`
        - 其中`ribs`的值在不求图特征时为 `{}`'''
        if not os.path.exists( self.collection_data_lib_parsed ):   # 多余
            utils.makePath( self.collection_data_lib_parsed )
        resUpd, resRib= {},{}
        # 收集updates文件
        logger.info('Start: parse `updates` data:')
        resUpd= self.getUpdTxts(events_dict)
        logger.info('End: `updates` data.')
        # 收集rib文件
        if self.ribTag:
            logger.info('Start: parse `ribs` data:')
            resRib= self.getRibTxts(events_dict)
            logger.info('End: `ribs` data.')
        return {'updates': resUpd, 'ribs': resRib} 
    

    def run(self):
        '''return `{ 'updates': {'evtNm': {'monitor': ( [ .txt, ...], str|None ) } },
                     'ribs'   : {'evtNm': {'monitor': [ .txt, ...]               } } | {}   } `
                     - 其中updates中的str为日期分水岭，当ribs的值为空，则此处为None
        '''
        evtDic= self.getEventsDict()
        txtDic= self.getRawTxts(evtDic)

        return txtDic
        
if __name__=='__main__':
    
    obj= GetRawData(increment=0, collection_data_lib='Dataset/')