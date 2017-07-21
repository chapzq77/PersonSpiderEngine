#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re
from url_operation import url_open_return_html
import sqlite3
from lxml import etree
import sys
import time
import urllib

reload(sys)
sys.setdefaultencoding('utf-8')



def baidu_parse(page):
    """
    功能：根据百度网页爬取的html，解析其中title，url，content
          以及右边的相关人名的信息
    返回值：result_list：网页左边的 title，url，content 列表
            related_list：网页右边的相关人名信息列表
    """
    result_list = []
    a = []
    '''
    # 匹配中文,数字和英文的形式。。
    xx = u"[\u4e00-\u9fa5a-zA-Z0-9]+"
    pattern = re.compile(xx)
    '''
    """
    class_list = []
    related_list = []
    a = []

   
    
    for t in page.xpath('//div[@class="opr-recommends-merge-content"]/div[@class="cr-title c-clearfix"]/span'):
         class1 = t.text
         class_list.append(class1)
    s = 0
    for t in page.xpath('//div[@class="opr-recommends-merge-panel opr-recommends-merge-mbGap"] | //div[@class="opr-recommends-merge-panel"]'):
         for q in t.xpath('.//div[@class="c-row c-gap-top"]/div'):
              for m in q.xpath('./div[@class="c-gap-top-small"]/a'):
                   name1 = m.text
                   url = m.get('href')
                   url = 'http://www.baidu.com'+url
                   related_list.append({ 'class1':class_list[s], 'name1':name1, 'url':url})
         s = s +1
    """
    for i in range(1,101):
         a.append(['%d' %i])
    #print "++++++++++++++++++++++++++++++++++"
    #print type(page)
    for t in page.xpath('//div[@id="content_left"]/div'):
        if t.xpath('./@id') in a:
            title = (''.join(t.xpath('./h3/a//text()')).strip())
            url = t.xpath('./h3/a/@href')[0]
            if url:
                content = ''
                for text in t.xpath('.//div[@class="c-abstract"]//text() | .//div[@class="c-span18 c-span-last"]/p[1]//text()'):
                    content = content + text.strip()

                #content = ''.join((''.join(t.xpath('.//div[@class="c-abstract"]/text() | .//div[@class="c-span18 c-span-last"]/p[1]//text()')))
                #content = (' '.join(pattern.findall(''.join(t.xpath('.//div[@class="c-abstract"]/text() | .//div[@class="c-abstract c-abstract-en"]/text()')))))
                result_list.append({ 'title':title, 'url':url, 'content':content})               
        else:
            continue
    return result_list
"""
def baidu_parse2(page):
    '''
    功能：根据百度网页爬取的html，解析其中title，url，content
          以及右边的相关人名的信息
    返回值：result_list：网页左边的 title，url，content 列表
            related_list：网页右边的相关人名信息列表
    '''
    result_list = []
    print type(page)
    for t in page.xpath('//div[@id="results"]/div[@class="result c-result c-clk-recommend"]'):
        for i in t.xpath('./div[@class="c-container"]'):
            title = (''.join(i.xpath('./a/h3//text()')).strip())
            url = i.xpath('./a/@href')
            if url:
                content = ''
                for text in i.xpath('.//div[@class="c-span12"]/a//text()'):
                    content = content + text.strip()

                #content = ''.join((''.join(t.xpath('.//div[@class="c-abstract"]/text() | .//div[@class="c-span18 c-span-last"]/p[1]//text()')))
                #content = (' '.join(pattern.findall(''.join(t.xpath('.//div[@class="c-abstract"]/text() | .//div[@class="c-abstract c-abstract-en"]/text()')))))
                result_list.append({ 'title':title, 'url':url[0], 'content':content})               
        else:
            continue
    return result_list
"""



def sogou_parse(page):
    """
    功能：根据搜狗引擎的html 页面，解析得到具体的title，url，content 等信息
    返回值：result_list: 网页左边的 title，url，content 列表
            related_list: 网页右边的相关人名信息列表
    """
    result_list = []
    """
    related_list = []
    class_title = []
    for t1 in page.xpath('//div[@id="kmap_entity_div"]'):
        for t2 in t1.xpath('./h3/@title'):
            class_title.append(t2) 
        for i,t3 in enumerate(t1.xpath('./ul')):
            for t4 in t3.xpath('./li'):
                name1 = t4.xpath('./a[not(@class="rvr-atpic2 rim-pic")]/@title')
                url = "https://www.sogou.com/web" + t4.xpath('./a[not(@class="rvr-atpic2 rim-pic")]/@href')
                related_list.append({'class1':class_title[i], 'name1':name1, 'url':url})
    """
    '''
    #匹配中文, 数字和英文的形式。。
    xx = u"[\u4e00-\u9fa5a-zA-Z0-9]+"
    pattern = re.compile(xx)
    '''

    for t in page.xpath('//div[@class="results"]/div[@class ="vrwrap"] | //div[@class="results"]/div[@class ="rb"]'):
        title = (''.join(t.xpath('./h3//text()')).strip())
        url = t.xpath('./h3/a')[0].get('href')
        if url:
            #content = (' '.join(pattern.findall(''.join(t.xpath('.//div[not(@style="display:none" or @class="fb")]//text()')))))
            content = ''
            for text in t.xpath('.//div[not(@style="display:none" or @class="fb")]//text()'):
                content = content + text.strip()
            result_list.append({'title': title, 'url': url, 'content': content})
       
    return result_list




"""
def sogou_parse2(page):
    '''
    功能：根据搜狗引擎的html 页面，解析得到具体的title，url，content 等信息
    返回值：result_list: 网页左边的 title，url，content 列表
            related_list: 网页右边的相关人名信息列表
    '''
    result_list = []
    '''
    related_list = []
    class_title = []
    for t1 in page.xpath('//div[@id="kmap_entity_div"]'):
        for t2 in t1.xpath('./h3/@title'):
            class_title.append(t2) 
        for i,t3 in enumerate(t1.xpath('./ul')):
            for t4 in t3.xpath('./li'):
                name1 = t4.xpath('./a[not(@class="rvr-atpic2 rim-pic")]/@title')
                url = "https://www.sogou.com/web" + t4.xpath('./a[not(@class="rvr-atpic2 rim-pic")]/@href')
                related_list.append({'class1':class_title[i], 'name1':name1, 'url':url})
    '''


    for t in page.xpath('//div[@class="results"]/div[@class ="vrResult" and contains(@id,"sogou_vr")]'):
        title = (''.join(t.xpath('./h3//text()')).strip())
        url = t.xpath('./h3/a')[0].get('href')
        if url:
            #content = (' '.join(pattern.findall(''.join(t.xpath('.//div[not(@style="display:none" or @class="fb")]//text()')))))
            content = ''
            for text in t.xpath('.//div[@class="text-layout"]//text()'):
                content = content + text.strip()
            result_list.append({'title': title, 'url': url, 'content': content})
       
    return result_list
"""


def bing_parse(page):

    """
    功能：根据bing网页爬取的html，解析其中title，url，content
          以及右边的相关人名的信息
    返回值：result_list：网页左边的 title，url，content 列表
            related_list：网页右边的相关人名信息列表
    """
    result_list = []
    """
    related_list = []
    #抽取右边的相关人名信息{相关属性：classname，人名：name，人名的链接：uel}
    for t in page.xpath('//div[@class="b_re"]'):
          text = t.xpath('./div[@class="re_twrap"]/h2')[0].text
          for y in t.xpath('./ul[@class="b_hList"]/li'):
              for x in y.xpath('./div[@class="image_attribution relatedEntityWidth"]'):
                  name = ' '.join(x.xpath('.//text()'))
                  url = "http://cn.bing.com/" + str(x.xpath('./div/a/@href'))
                  related_list.append({'class1':text,'name1':name,'url':url})
    """

    for i in page.xpath('//ol[@id="b_results"]/li[@class="b_algo"]'):
        title = ''.join(i.xpath('./h2/a//text()'))         
        url = i.xpath('./h2/a/@href')
        content = ''.join(i.xpath('./div/p//text()'))

        if url != []:
            if "http" not in url[0]:
                realurl = "http://cn.bing.com/" + url[0]
            else:
                realurl = url[0]
        else:
            realurl = None

        if realurl != None:
            result_list.append({'title':title,'url':realurl,'content':content})
    return result_list



def search(engine,name,save_path,url_list):
    """
    功能：根据引擎的类型：engine, 
          网页html，解析得到爬取的内容，并存储在数据库中
    """
    conn = sqlite3.connect(save_path )
    conn.text_factory = str
    c = conn.cursor()

    #每个搜索引擎的最大的下载页数
    max_page = 10
    for i in range(max_page):
        

        #html_et = etree.HTML(html.decode('utf-8', 'ignore'))
        #print html

        if engine == 'baidu':
            url= "http://www.baidu.com/s?wd=%s&&pn=%s" %(urllib.quote(name),str(i*10))
            html= url_open_return_html(url)
            html_et = etree.HTML(html.decode('utf-8', 'ignore'))
            result_list = baidu_parse(html_et)
        
            #网页的打开的问题(和搜狗一样会出现，网页结构变化，而且都是第一页，使得分析网页为空)
            while result_list == []:
                time.sleep(20)
                #print "++++++++++++++++++++++++++++++++++++++"
                html = url_open_return_html(url)
                html_et = etree.HTML(html.decode('utf-8', 'ignore'))
                result_list = baidu_parse(html_et)


        elif engine == 'sogou':
            url = "https://www.sogou.com/web?query=%s&page=%s&ie=utf8" %(urllib.quote(name),str(i+1))
            
            html,this_url = url_open_return_html(url)
            html_et = etree.HTML(html.decode('utf-8', 'ignore'))
            result_list = sogou_parse(html_et)
                      
            #网页的打开的问题(和搜狗一样会出现，网页结构变化，而且都是第一页，使得分析网页为空)
            while result_list == []:
                time.sleep(20)
                #print "==================="
                html= url_open_return_html(url)
                html_et = etree.HTML(html.decode('utf-8', 'ignore'))
                result_list = sogou_parse(html_et)


        else:
            url = "http://cn.bing.com/search?q=%s&first=%s&FORM=PERE2" %(urllib.quote(name),str(i*10+1))
            html = url_open_return_html(url)
            html_et = etree.HTML(html.decode('utf-8', 'ignore'))
            result_list = bing_parse(html_et)
                

            while result_list == []:
                time.sleep(20)
                print "---------------------------------"
                html = url_open_return_html(url)
                html_et = etree.HTML(html.decode('utf-8', 'ignore'))
                result_list = baidu_parse(html_et)

        
        # 去重url 并将数据存储在数据库中

        for j in range(len(result_list)):
            if result_list[j]['url'] not in url_list:
                c.execute("INSERT INTO retrievalresult(title,url,content,person) VALUES(?,?,?,?)", (result_list[j]['title'], result_list[j]['url'], result_list[j]['content'], str(name)))
                conn.commit()
                url_list.append(result_list[j]['url'])


        """
        # 相关的人名链接:只有第一页的有用，其他页的都是重复的
        if i < 1:
            for relate in related_list:
                self.c.execute("INSERT INTO personrelated(class,name,url,person) VALUES(?,?,?,?)",(relate['class1'],relate['name1'],relate['url'],str(name)))
                self.conn.commit()
        """
        
    conn.close()
    return url_list