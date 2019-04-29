# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 18:20:01 2019

@author: yxx
"""
#导入neo4j链接驱动库
from py2neo import *
from DataTransfer import *
import json
#import simplejson as json
import os
import time#时间库
time_start=time.time()#程序开始运行时间
url = "bolt://localhost:11001"#本机数据胡地址
user="neo4j"                #数据库用户名
password="123456"           #数据库密码
graph=Graph(url, username=user,password=password)# 连接到一个图数据库
deep_length=1#路径深度
"""
程序说明：
1.port所有的列表
2.for port_id in port_id_list:
    初始化node_list, links_list
    执行命令：“match(n:port)-[:r..deep_length]-(m)
              where id(n)=port_id
              return m,n,r” 获取返回数据
    transfer data into two lists
    把数据中的点和边写入到一个result_list
    把result_list写入到文档，命名为port_id。
"""
#对于核心港口获取nodes_list和links_list，生成一个json并保存。
nodes_list=[]
links_list=[]
result_dic={}
#获取与核心港口存在联系的所有一度结点
query_str="MATCH(n:port)-[r*..1]-(m) WHERE id(n)=64 RETURN n,r,m"
records_data=list(graph.run(query_str))
#获取nodes_list和links_list
requir_record_data(graph ,records_data, nodes_list ,links_list)
result_dic['nodes_list']=nodes_list
result_dic['links_list']=links_list
result_json_str=json.dumps(result_dic)
f=open("C:/Users/yaoxi/Desktop/work/"+str(64)+".json",'w')
f.write(result_json_str)
print("数据导出完毕。")
time_end=time.time()
print('time cost',time_end-time_start,'s')#打印程序运行时间