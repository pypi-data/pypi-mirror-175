##
logger.info( utils.logMemUsage(10, inspect.stack()[0][3] ))     # 调试锚点：随删
##

持续优化的问题：
- 计算ED那里，对比测试多进程的情况。
- 自定义多进程模块中，等待睡眠为1s是否合理。
- 做一个对比各个特征计算时间的函数。
- 构建函数：输入一个或多个新特征，能把采集结果追加到已有的DF.csv。这要涉及到`自定义特征采集函数`的API
- 关于每slot如何构建全局拓扑图：还是要结合pl.DF来加速计算，避免逐条消息更新。
- requirement的预安装，特别是bgpdump


# BGP特征提取工具

## 组织结构

### 库路径

- fastFE  
├── BGPMAGNET/          BGP原始数据下载工具(by倪泽栋)  
├── collectData.py      主模块：数据收集，包括下载、解析  
├── featTradition.py    传统特征采集功能集合
├── featTree.py         特征树，集成所有特征及其pl.Expr  
├── logConfig.json      日志配置  
├── FET.py              主模块：特征采集  
├── utils.py            工具集合  
├── README.md  
└── requirements.txt 

### cwd 默认路径
- cwd  
├── Dataset  
│   ├── raw_cmpres              原始数据下载存放路径  
│   │   ├── rrc00/  
│   │   └── routeviews./  
│   └── raw_parsed              原始数据解析存放路径  
│       └── 事件名  
│           └── 采集器名/  
├── log                         日志路径  
│   ├── errors.log  
│   └── info.log  
└── event_list.csv              事件列表路径  

## 使用方法

1. 在当前工作目录下新建`event_list.csv`，写入感兴趣的事件列表
    - 格式：事件名；起始时间；结束时间（可缺省）；采集器（可多个，用`,`相隔）
    - 举例：`GoogleLeak,2017/08/25 05:00:00,2017/08/25 06:00:00,rrc06,rrc05`

2. 在自己的脚本中使用如下代码。所有事件的采集结果存储于在`stored_dir`目录下
    ```python
    from fastFET.FET import FET
    fet= FET( increment=0 )
    interest_feats= []                  
    fet.setCustomFeats(interest_feats)  # 设置感兴趣的特征。详见 `特征目录`
    stored_dir= fet.run()
    ```
3. 其他功能
    - 获取库中现已集成的特征列表：`feats= fet.getAllFeats()`
    - 获取所有事件标准化起止时间：
        ```python
        from fastFET.collectData import GetRawData
        grd= GetRawData()
        event_dict= grd.getEventsDict()
        ```

## 框架解释
- RIPE NCC和RouteViews的`.gz`和`.bz2`原始数据经 `bgpdump`工具转码得到的`.txt`文件，根据事件和采集器名分类存入`/data/bgpdata/parsed_txt/`
- 利用 `polars`数据分析工具高效提取BGP特征，按事件名存入 `./data/date__event__collector.csv`。
- 顺便收集了事件中出现的MOAS消息，存入`./data/MOAS/`

## 容量、耗时等的估算
1. 

### - 特征提取（89）：
总列：
'v_total', 'v_A', 'v_W', 'v_IGP', 'v_EGP', 'v_ICMP', 'v_peer', 'v_pfx_t_cnt', 'v_pfx_t_avg', 'v_pfx_t_max', 'v_pfx_A_cnt', 'v_pfx_A_avg', 'v_pfx_A_max', 'v_pfx_W_cnt', 'v_pfx_W_avg', 'v_pfx_W_max', 'v_pp_t_cnt', 'v_pp_t_avg', 'v_pp_t_max', 'v_pp_A_cnt', 'v_pp_A_avg', 'v_pp_A_max', 'v_pp_W_cnt', 'v_pp_W_avg', 'v_pp_W_max', 'v_oriAS_t_cnt', 'v_oriAS_t_avg', 'v_oriAS_t_max', 'v_oriAS_peer_cnt', 'v_oriAS_peer_avg', 'v_oriAS_peer_max', 'v_oriAS_pfx_cnt', 'v_oriAS_pfx_avg', 'v_oriAS_pfx_max', 'v_oriAS_pp_cnt', 'v_oriAS_pp_avg', 'v_oriAS_pp_max', 'path_len_max', 'path_len_avg', 'path_unq_len_max', 'path_unq_len_avg', 'AS_total_cnt', 'AS_total_avg', 'AS_total_max', 'AS_rare_max', 'AS_rare_sum', 'is_WA', 'is_AW', 'is_WAW', 'is_longer_path', 'is_shorter_path', 'is_longer_unq_path', 'is_shorter_unq_path', 'is_new', 'is_dup_ann', 'is_AWnA', 'is_imp_wd', 'is_WnA', 'is_AWn', 'is_AnW', 'is_WAn', 'is_dup_wd', 'is_dup', 'is_flap', 'is_NADA', 'is_imp_wd_spath', 'is_imp_wd_dpath', 'type_0', 'type_1', 'type_2', 'type_3', 'ED_max', 'ED_avg', 'ED_0', 'ED_1', 'ED_2', 'ED_3', 'ED_4', 'ED_5', 'ED_6', 'ED_7', 'ED_8', 'ED_9', 'ED_10'

字段            |  说明 | 备注
 ----           |  ----
time_bin        |  时间块号
timestamp       |  时间戳（UTC）
vol类：
v_total   |  消息总数   |
v_A     |  宣告消息总数 |
v_W     |  撤销消息总数|
v_IGP     |  属于IGP的消息总数
v_EGP     |  属于EGP的消息总数
v_ICPT     |  属于IMCOMPLETE的消息总数
v_peer    |  不重复的peer的数量
v_pfx    |  不重复的prefix的数量    |`pfx_ann ∪ pfx_wd`
v_pfx_avg |  不同prefix出现过的平均次数 | v_A/v_pfx
v_pfx_max |  不同prefix出现过的最大次数 | 要对每个pfx计数
v_pfx_a_count |  宣告的不同prefix数量 | 
v_pfx_a_max   |  宣告的不同prefix出现过的最大次数
pfx_a_avg   |  宣告的不同prefix出现过的平均次数
pfx_w_count |  撤销的不同prefix数量
pfx_w_max   |  撤销的不同prefix出现过的最大次数
pfx_w_avg   |  撤销的不同prefix出现过的平均次数
|
path_len_max    |  最大路径长度
path_len_avg    |  平均路径长度
path_unq_len_max|  去重后的最大路径长度
path_unq_len_avg|  去重后的平均路径长度
|
AS_count        |  出现过的AS的数量
AS_count_max    |  不同AS出现过的最大次数 
AS_count_avg    |  不同AS出现过的平均次数
AS_ori_count    |出现过的源AS的数量
AS_ori_max      |出现过的源AS的最大出现次数
AS_ori_avg      |出现过的源AS的平均出现次数
PoAS_num        |不同prefix-originAS对的数量
PoAS_max        |不同prefix-originAS对出现过的最大次数
PoAS_avg        |不同prefix-originAS对出现过的平均次数
|
AS_rare_max     |  一条消息的路径中含有稀有AS的最大数量(平均数量太小，不统计)
AS_rare_sum     |  所有消息的路径中含有稀有AS的总共数量
|
pp_num          |  不同peer-prefix对的数量
pp_max          |  不同peer-prefix对出现过的最大次数
pp_avg          |  不同peer-prefix对出现过的平均次数
|
is_WA           |  同一peer-prefix下，属于撤销后宣告
is_AW           |  同一peer-prefix下，属于宣告后撤销
is_WAW          |  同一peer-prefix下，属于撤销-宣告-撤销
is_longer_path  |  同一peer-prefix下，路径变长
is_shorter_path |  同一peer-prefix下，路径变短
is_longer_unq_path  |  同一peer-prefix下，去重后路径变长
is_shorter_unq_path |  同一peer-prefix下，去重后路径变短
is_MOAS             |  同一peer-prefix下，源AS改变了
is_new          |  同一peer-prefix下，属于全新宣告
is_dup_ann      |  同一peer-prefix下，属于完全重复宣告
is_AWnA         |  同一peer-prefix下，属于宣告-撤销多次-宣告
is_imp_wd       |  同一peer-prefix下，属于隐式撤销（重复宣告，但其他属性变化）
is_WnA          |  同一peer-prefix下，属于撤销多次-宣告
is_AWn          |  同一peer-prefix下，属于宣告-多次撤销
is_AnW          |  同一peer-prefix下，属于多次宣告-撤销
is_WAn          |  同一peer-prefix下，属于撤销-多次宣告
is_dup_wd       |  同一peer-prefix下，属于重复撤销  
is_dup          |  同一peer-prefix下，属于重复宣告/撤销
is_flap         |  同一peer-prefix下，属于宣告-撤销-宣告，且属性完全不变
is_NADA         |  同一peer-prefix下，属于宣告-撤销-宣告，但属性有变化
is_imp_wd_spath |  同一peer-prefix下，属于路径属性不变的隐式撤销
is_imp_wd_dpath |  同一peer-prefix下，属于路径属性变化的隐式撤销
|
edit_dist_max   |  同一peer-prefix下的消息中，最大的编辑距离值
edit_dist_avg   |  同一peer-prefix下的消息中，平均的编辑距离值
ED_0            |  同一peer-prefix下，编辑距离为0的消息数量
ED_1~10         |  同一peer-prefix下，编辑距离为1~10的消息数量  
|
FirstOrderRatio |  最活跃的宣告前缀/宣告总数（即 `vol_ann_pfx_max / vol_ann_num`）
ratio_ann       |  宣告量占更新消息总量之比（即`vol_ann_num / vol_total_num`）注：空值换0
ratio_wd        |  撤销量占更新消息总量之比（即`vol_wd_num / vol_total_num`）
ratio_origin0   |  IGP占宣告量之比（即`vol_origin0 / vol_ann_num`）
ratio_origin1   |  EGP占宣告量之比（即`vol_origin1 / vol_ann_num`）
ratio_origin2   |  IMCOMPLETE占宣告量之比（即`vol_origin2 / vol_ann_num`）
ratio_dup_ann   |  完全重复宣告占宣告量之比（即`is_dup_ann / vol_ann_num`）
ratio_flap      |  属性完全不变的宣-撤-宣 占宣告量之比（即`is_flap / vol_ann_num`）
ratio_NADA      |  属性有变化的宣-撤-宣 占宣告量之比（即`is_NADA / vol_ann_num`）
ratio_imp_wd    |  隐式撤销 占宣告量之比（即`is_imp_wd / vol_ann_num`）
ratio_imp_wd2   |  隐式撤销 占隐式撤销+撤销之比（即`is_imp_wd / (is_imp_wd+ vol_wd_num)`）
ratio_exp_wd    |  真正撤销 占隐式撤销+撤销之比（即`vol_wd_num / (is_imp_wd+ vol_wd_num)`）
ratio_imp_wd_dpath  |  路径属性不同的隐式撤销 占隐式撤销之比（即`is_imp_wd_dpath / is_imp_wd`）
ratio_imp_wd_spath  |  路径属性相同的隐式撤销 占隐式撤销之比（即`is_imp_wd_spath / is_imp_wd`）
ratio_new       |  全新宣告 占宣告量之比（即`is_new / vol_ann_num`）
ratio_wd_dups   |  重复撤销 占撤销量之比（即`is_dup_wd / vol_wd_num`）
ratio_longer_path   |  更长路径宣告 占宣告量之比（即`is_longer_path / vol_ann_num`）
ratio_shorter_path  |  更短路径宣告 占宣告量之比（即`is_shorter_path / vol_ann_num`）
ratio_longer_path2  |  更长路径宣告 占更长/短宣告量之比（即`is_longer_path / (is_longer_path+ is_shorter_path)`）
ratio_shorter_path2 |  更短路径宣告 占更长/短宣告量之比（即`is_shorter_path / (is_longer_path+ is_shorter_path)`）

## tag
- 提取时间尺度问题：默认为1分钟。文件分块可能会导致最终结果有时间序号相同的情况。

## 特征补充

字段            |  说明
 ----           |  ----
ConcentratRatio |  前三个最活跃的宣告前缀/宣告总数（即 `vol_ann_pfx_max / vol_ann_num`）


# 其他
- BGP RAW DATA：采集时间间隔不统一，如rrc00，20030723.0745之前为15min（且时刻不固定），之后为5min（时刻固定）。
- 针对异常类型的特征设计：子前缀劫持、路径劫持、路由泄露等，连接其他框架？

# DEBUG
## path字段的格式问题
以下格式均实际存在：
- 58057 6939 4635 4788 38044 23736
- 58057 6939 4635 4788 38044 {23736}
- 58057 6939 1299 2603 2603 2603 6509 {271,7860,8111,53904}

facebook_outage,2021/10/04 12:00:00,2021/10/04 16:00:00,rrc00
GoogleLeak,2017/08/25 05:00:00,2017/08/25 10:00:00,rrc06

# 发现：
- 劫持震荡：
当`is_MOAS`很大，而`vol_oriAS_peer_pfx`或`vol_oriAS_pfx`很小时，说明存在一个prefix反复被多个AS宣告的情况。