#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import random
from config import AGENTS
import time 



def url_open_return_html(geturl,proxy = None):

    """
    功能：给定一个 url 打开，并返回一个 html
    返回值： html  
    """
    '''
    搜狗允许重定向allow_redirects = True
    print "next url:",geturl
    bing是个奇葩，没有跳转，而且出错的界面的解析器和原始网页的解析器是一套，所以会出现较大的重复的网页。。。。
    如果出现bing 反爬虫，将url 特征添加到下面对对应的地方
    '''
    headers = {'User-Agent': random.choice(AGENTS)}
    while True:
            try:
                get_content = requests.get(url= geturl, headers=headers, proxies =proxy)
                if get_content.status_code != requests.codes.ok:

                    #出现反爬虫机制了。。。。
                    if "www.sogou.com/antispider/?from=" in get_content.url:
                        #睡眠10分钟。。。
                        time.sleep(100)
                        continue

                    #百度反爬虫机制。。。。。
                    if '="http://verify.baidu.com' in get_content.url:
                        time.sleep(100)
                    
                    else:
                        #其他的情况，可能是网速的慢，返回的错误的
                        time.sleep(5)
                        continue                    

                else:
                    #print "跳转",get_content.history
                    return get_content.text
                                  
            except Exception,e:
                print "error info:", e
                continue

