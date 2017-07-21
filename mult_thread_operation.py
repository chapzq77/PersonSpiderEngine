#!/usr/bin/env python
# -*- coding: utf-8 -*-


from threading import Thread, Lock,current_thread
from Queue import Queue
import threading
import time
from url_operation import download_html
from spiderhtmlparse import search




class Fetcher:
    """
    多线程抓取的类：输入的队列中的所有的放入任务队列中，设置多线程进行抓取和存储
    """

    def __init__(self, threads,save_path):
        self.lock = Lock()  # 线程锁
        self.q_req = Queue()  # 任务队列
        self.q_ans = Queue()  # 完成队列
        self.all_url_list = [] #url的一个集合，用于 url 的去重
        self.threads = threads
        self.file_save_path = save_path
        for i in range(threads):
            t = Thread(target=self.threadget)  # 括号中的是每次线程要执行的任务
            t.setDaemon(True)  # 设置子线程是否随主线程一起结束，必须在start()
                              # 之前调用。默认为False
            t.start()  # 启动线程
        self.running = 0  # 设置运行中的线程个数

    def __del__(self):  # 解构时需等待两个队列完成
        time.sleep(0.5)
        self.q_req.join()  # Queue等待队列为空后再执行其他操作
        self.q_ans.join()

    # 返回还在运行线程的个数，为0时表示全部运行完毕
    def taskleft(self):
        return self.q_req.qsize() + self.q_ans.qsize() + self.running

    def push(self, req):
        self.q_req.put(req)

    def pop(self):
        return self.q_ans.get()

    # 线程执行的任务，根据req来区分
    def threadget(self):
        while True:
            term = self.q_req.get()
            name = term[0]
            engine = term[1]

            '''
            Lock.lock()操作，使用with可以不用显示调用acquire和release，
            这里锁住线程，使得self.running加1表示运行中的线程加1，
            如此做防止其他线程修改该值，造成混乱。
            with下的语句结束后自动解锁。
            '''

            with self.lock:
                self.running += 1

            #根据搜索引擎和人名下载网页，每个人名下载10页100左右的网页：url_list是个全局的变量是为了网页的去重处理。。。
            url_list = search(engine,name,self.file_save_path,self.all_url_list)
            self.all_url_list = url_list

            
            time.sleep(2)

            # self.q_ans.put((req,ans)) # 将完成的任务压入完成队列，在主程序中返回
            self.q_ans.put(term)
            with self.lock:
                self.running -= 1
            self.q_req.task_done()  # 在完成一项工作之后，Queue.task_done()
                                   # 函数向任务已经完成的队列发送一个信号
            time.sleep(0.1)  # don't spam



if __name__ == "__main__":
    Fetcher()
    
