#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s-[%(asctime)s][%(module)s][%(funcName)s][%(lineno)d]: %(message)s')

import sys
import os
import time
import copy
#import threadpool
import threading
import sqlite3
from lxml import etree
from os.path import join as pjoin
from mult_thread_operation import Fetcher
sys.path.append('../server_base')

current_path = os.path.abspath('.')


class SpiderOperation():
    '''
    功能：爬取百度，搜狗，bing等搜引擎的检索人名，返回的网页的所有网页的title、url、content，以及相关的人名属性
    '''

    def __init__(self):
        # self.pool = threadpool.ThreadPool(pool_num)  # 创建线程池
        self.task_lock = threading.Lock()  # 线程锁
        self.task_result_list = []  # 任务结果列表
        self.url_list = []  # url 的列表为了去重处理
        
        
        #self.c.execute('''CREATE TABLE IF NOT EXISTS personrelated(id integer primary key autoincrement, class text, name text,url varchar(1000), persom text)''')
        
    def update_task_list(self, one_task_result):
        '''
        多线程操作共享的类对象资源，互斥访问,
        将每个线程处理的结果存入self.task_result_list
        '''
        if self.task_lock.acquire():
            self.task_result_list.append(one_task_result)
            self.task_lock.release()


    def start_spider(self, one_task):
        '''
        引擎的对任务处理的核心操作，此处one_task为task_list中的一个任务，
        将{时间戳: one_task['url']}写入one_task['path']指定目录下，
        并在将结果拼接到任务后面写入结果队列
        '''
        file_save_path = one_task['path']
        conn = sqlite3.connect(file_save_path )
        conn.text_factory = str
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS retrievalresult(id integer primary key autoincrement, title text, url varchar(1000), content text, person text)''')
        conn.close()
        name = one_task['person']
        engine = one_task['engine']
        
        
        list_thread = []
        for term in engine:
            list_thread.append((name,term))
        
        #通过线程类来进行数据的爬取
        f = Fetcher(threads=10, save_path = file_save_path)   #设置线程数
        for term in list_thread:
            f.push(term)         #所有的待处理 term 推入下载队列
        while f.taskleft():     #若还有未完成的的线程
            f.pop() 
        

        # 没有结果，结果都存在数据库中了
        task = copy.copy(one_task)
        task['path'] = file_save_path
        task['result'] = "%s run win!" %str(name)

        self.update_task_list(task)

    def task_operate(self, task_list):
        '''
        TestEngine调用接口，接受任务并处理
        '''
        self.task_result_list = []  # 每个任务执行前初始化结果列表
        for one_task in task_list:
            self.start_spider(one_task)




if __name__ == '__main__':
    spideroperation = SpiderOperation()
    task_list = [{'person': '李超', 'engine': ['bing'],
                  'path': pjoin(os.path.abspath('.'),'lichao.db')}]
    spideroperation.task_operate(task_list)
