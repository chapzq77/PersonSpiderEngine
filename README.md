# 人名爬虫引擎说明
- 爬取百度，bing， 搜狗等浏览器的检索的返回的网页
- 使用多线程爬取，多线程的类 Fetcher，是自己写的，可以替代threadpool   
- 爬取的数据的存取，我使用的轻量级的数据库 sqlite
![](http://i.imgur.com/ojUvZAK.png)

-  输入的形式
  ```
    ["person" : "张三", #文件中指定输入的人名
    "engine" : ["baidu","sogou","bing"], #爬取的引擎
	"path" : "/person_spider/zhangsan.db" # 存储的文件路径和文件名]
    #可以在task_list 中添加多个query
  ```
- 爬取说明

```
python Spider.py
```