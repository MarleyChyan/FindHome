#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Filename: if_name_main.py
#上海链家二手房爬虫系统 2.0 + 
# 其他城市仅需把下方的 #基址 sh改成 如成都cd，把下方市区索引zone改成对应城市的区域 
#其他可 自定义值 一般已用————————标出—————————
#partly-by：电子科技大学-樱空社*青空恋（ MarleyChyan @ github & gmail） 
#樱 空 社 http://sola.pink 这片天空期待你的故事~
baseurl = "https://sh.lianjia.com/ershoufang/" #基址
    #示例 https://sh.lianjia.com/ershoufang/pudong/pg2/
    #           上海  链 家 网   二 手 房    浦东  第2页
#市区索引：
zone=('pudong','minhang','baoshan','xuhui','putuo','yangpu','changning','songjiang','jiading','huangpu','jingan','hongkou','qingpu','fengxian','jinshan','chongming')
#      浦东     闵行       宝山      徐汇    普陀     杨浦     长宁        松江        嘉定       黄浦      静安      虹口      青浦      奉贤       金山      崇明
from bs4 import BeautifulSoup     #网页解析，获取数据
import re       #正则表达式，进行文字匹配
import urllib.request,urllib.error      #制定URL，获取网页数据
import xlwt     #进行excel操作
import sqlite3  #进行SQLite数据库操作
import random   #随机选取ip避免被封
random.seed
book = xlwt.Workbook(encoding="utf-8",style_compression=0)  #创建workbook对象
sheet = book.add_sheet('上海二手房',cell_overwrite_ok=False)    #创建工作表
col = ("房间链接","房间名字","房间价格(w)","房间细节","m^2单价","街道","小区","关注人数","发布时间","市域")#表头
for i in range(10):##———————————设定列名range(0,10)如上———————————
    sheet.write(0,i,col[i]) #写列名

p=2700##———————————限制单主页条数[2700]条———————————
pp=7#——————————————限制每市区页数（1页最多30条）——————
t=0;q=0#写表行计数
#自动随机切换ip代理，需要自定义代理请更改，注意为元组（" " ," "）格式
ips=(    
"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Zune 4.0; Tablet PC 2.0; InfoPath.3; .NET4.0C; .NET4.0E)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 7.1; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; AskTB5.5)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; InfoPath.2; .NET4.0C; .NET4.0E)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; FDM; .NET CLR 1.1.4322; .NET4.0C; .NET4.0E; Tablet PC 2.0)",
"Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0; Media Center PC 4.0; SLCC1; .NET CLR 3.0.04320)",
"Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 1.1.4322)",
"Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727)",
"Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.0; Trident/4.0; InfoPath.1; SV1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 3.0.04506.30)",
"Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 5.0; Trident/4.0; FBSMTWB; .NET CLR 2.0.34861; .NET CLR 3.0.3746.3218; .NET CLR 3.5.33652; msn OptimizedIE8;ENUS)",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.2; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; Media Center PC 6.0; InfoPath.2; MS-RTC LM 8)",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; Media Center PC 6.0; InfoPath.2; MS-RTC LM 8",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; Media Center PC 6.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C)",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.3; .NET4.0C; .NET4.0E; .NET CLR 3.5.30729; .NET CLR 3.0.30729; MS-RTC LM 8)",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Zune 3.0)",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; msn OptimizedIE8;ZHCN)",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; MS-RTC LM 8; InfoPath.3; .NET4.0C; .NET4.0E) chromeframe/8.0.552.224",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; MS-RTC LM 8; .NET4.0C; .NET4.0E; Zune 4.7; InfoPath.3)",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; MS-RTC LM 8; .NET4.0C; .NET4.0E; Zune 4.7)",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; MS-RTC LM 8)",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; Zune 4.0)",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E; MS-RTC LM 8; Zune 4.7)",
)#代理
ipkey='"User-Agent": \n'+'\"'+ips[0]+'\"'  #修饰ips格式为ipkey，此处额外需要引号，请珍惜代理资源
#随机ip代理
def main():
    global baseurl
    #示例 https://sh.lianjia.com/ershoufang/pudong/pg2/
    #            上海           二手房      浦东   第2页
    #爬取网页
    
    #savepath = "上海二手房.xls"
    dbpath = "house.db"#future
    #保存数据
    savepath='D:\InFILLEs\shesf\shesf.xls'#——————请选取本地目录———————

    for u in range(len(zone)):
        datalist = getData(baseurl,u)
        saveData(datalist,savepath,u)
    #saveData2DB(datalist,dbpath)

    #askURL("https://movie.douban.com/top250?start=")

#房间详情链接的规则
#深层备份findLink = re.compile(r'<div.*?<div.*?<a.*?class.*?href="(.*?)"')    #创建正则表达式对象，表示规则（字符串的模式）

findLink = re.compile(r'<a.*?class.*?href="(.*?)"')    #创建正则表达式对象，表示规则（字符串的模式）
#OK2#findTitle = re.compile(r'<a.*?class.*?href=".*?".*?>(.*?)<')
#<a class="" href="https://sh.lianjia.com/ershoufang/107104100610.html" target="_blank" data-log_index="1" data-el="ershoufang" data-housecode="107104100610" data-is_focus="" data-sl="">满五三房 两房朝南，小区环境好，老式装修可拎包入住</a>
#区域： data-el="ershoufang".*>(.*?)</a>
'''
正则表达式
. 表示通配符（可以匹配任何一个字符）
.*?表示任意多个通配符
(括号里的是被截取的部分，请注意是英文括号)
一般用 (.*?) 选取任意多个字符 (括号里、外也可以写其他特征)
一般把标签和关键属性写上，中间用.*?分隔即可
如 <div class="totalPrice"><span>(.*?)</span>
   标签  属性             相对位置 要的
然后再加入其他结构特征（如上<span>）过滤数据
以免无匹配返回（提示list index out of range）
正则表达式还有很多内容和广泛的用途 可以看看 https://www.runoob.com/python/python-reg-expressions.html
'''
#房间图片
#findImgSrc = re.compile(r'<img.*?class.*?src="(.*?)"',re.S)   #re.S 让换行符包含在字符中
#findImgSrc = re.compile(r'<img.*src="(.*?)"',re.S)   #re.S 让换行符包含在字符中

#房间名字
findTitle = re.compile(r'<a.*?class.*?href=".*?".*?>(.*?)<')
#房间价格
findValue = re.compile(r'<div class="totalPrice"><span>(.*?)</span>')
#房间细节
findJudge = re.compile(r'houseIcon"></span>(.*?)<',re.S)
#房间m^2单价
findVpm2 = re.compile(r'<span>单价(.*?)元/平米</span>')
#大区
findArea = re.compile(r'.*?positionIcon.*?ershoufang.*?target="_blank">(.*?)</a>')
#小区
findCommunity = re.compile(r'.*?positionIcon.*?target="_blank">(.*?)</a>')
#关注人数
findStars = re.compile(r'starIcon"></span>(.*?)人关注 /')
#发布时间
findTime = re.compile(r'starIcon"></span>.*?/ (.*?)</div>')

#一个功能对应一个函数
#爬取网页
def getData(baseurl,u):
    global ipkey
    datalist = []
    global zone
    for i in range(1,pp+1):       #调用获取页面信息的函数#
        url = baseurl +zone[u]+'/pg'+str(i)+'/'
        
        ipkey=ips[random.randint(0,len(ips))-1]#随机化代理ip
        print('以  '+ipkey)
        html = askURL(url)      #保存获取到的网页源码
        print("访问"+url)
         # 2.逐一解析数据
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_="info clear"):     #查找符合要求的字符串，形成列表

#<div class="info clear"><div class="title"><a class="" href="https://sh.lianjia.com/ershoufang/107103961747.html" target="_blank" data-log_index="1" data-el="ershoufang" data-housecode="107103961747" data-is_focus="" data-sl="">虹浦新城南区，简装一房，中间楼层</a><!-- 拆分标签 只留一个优先级最高的标签--><span class="goodhouse_tag tagBlock">必看好房</span></div><div class="flood"><div class="positionInfo"><span class="positionIcon"></span><a href="https://sh.lianjia.com/xiaoqu/5011000014599/" target="_blank" data-log_index="1" data-el="region">虹浦新城南区 </a>   -  <a href="https://sh.lianjia.com/ershoufang/minpu/" target="_blank">闵浦</a> </div></div><div class="address"><div class="houseInfo"><span class="houseIcon"></span>1室1厅 | 55.97平米 | 南 | 简装 | 低楼层(共11层) | 2008年建 | 板楼</div></div><div class="followInfo"><span class="starIcon"></span>29人关注 / 1个月以前发布</div><div class="tag"><span class="subway">近地铁</span><span class="isVrFutureHome">VR看装修</span><span class="taxfree">房本满五年</span><span class="haskey">随时看房</span></div><div class="priceInfo"><div class="totalPrice"><span>246</span>万</div><div class="unitPrice" data-hid="107103961747" data-rid="5011000014599" data-price="43953"><span>单价43953元/平米</span></div></div></div>

            #print(item)   #测试：查看房间item全部信息
            data = []    #保存一个房间的所有信息
            item = str(item)

            #房间详情的链接
            link = re.findall(findLink,item)[0]     #re库用来通过正则表达式查找指定的字符串
            data.append(link)                       #添加链接
            titles = re.findall(findTitle,item)[0]
            data.append(titles)                     #房间名字
            value = re.findall(findValue,item)[0]
            data.append(value)                      #房间价格
            judge = re.findall(findJudge,item)[0]
            data.append(judge)                      #房间细节
            vpm2 = re.findall(findVpm2,item)[0]
            data.append(vpm2)                       #房间m^2单价
            area = re.findall(findArea,item)[0]
            data.append(area)                       #大区
            community = re.findall(findCommunity,item)[0]
            data.append(community)                  #小区
            star=re.findall(findStars,item)[0]
            data.append(star)                       #关注人数
            time=re.findall(findTime,item)[0]
            data.append(time)                       #发布时间
            data.append(zone[u])                    #市区
            datalist.append(data)       #把处理好的一个房间信息放入datalist

    return datalist



#得到指定一个URL的网页内容
def askURL(url):
    head = {"User-Agent": ipkey#"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)" 
    }  #模拟浏览器头部信息，向链家服务器发送消息
    #头部信息：告诉 链家 服务器，我们是什么类型的机器、浏览器（即：我们可以接收什么样的文件内容）
                            #ipkey 用户代理

    request = urllib.request.Request(url,headers=head)  #使用request封装url和头部信息
    html = ""
    #异常处理
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        #print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html




#保存数据
def saveData(datalist,savepath,u):
    global t,q
    print("save..."+str(zone[u])+"...")

    for i in range(0,p):#每市区最多p条
        try:
            print("第%d条" %(i+1))
            print(datalist[i])##数据展示
            data = datalist[i]##数据赋值
            for j in range(len(col)+1):#数据写表 数据len(col)列加上市区1列
                try : #异常处理 避免误覆盖行
                    sheet.write(1+t,j,data[j]) #写表
                except :
                    t+=1     #本行有数据则下移一行，正常不需要
                    sheet.write(1+t,j,data[j])#写表
                q+=1
                #print('本市区写计数'+str(q),end=' ')#可选调试输出
                #print('本市区实写行数'+str(i),end=' ')
                #print('当前总行数'+str(t))
            t+=q//(len(col)+1)#本市区共写了q次，每行写了 len(col)+1 列次，故需下移 q÷[len(col)+1] 行
            q=0#下一个市区，清空写计数q
        except: break
    book.save(savepath)       #保存


# def saveData2DB(datalist,dbpath):
#     init_db(dbpath)
#     conn = sqlite3.connect(dbpath)
#     cur = conn.cursor()
#
#     for data in datalist:
#         for index in range(len(data)):
#             if index == 4 or index == 5:
#                 continue
#             data[index] = '"'+data[index]+'"'
#         sql = '''
#                 insert into movie250 (
#                 info_link,pic_link,cname,ename,score,rated,instroduction,info)
#                 values(%s)'''%",".join(data)
#         print(sql)
#         cur.execute(sql)
#         conn.commit()
#     cur.close()
#     conn.close()
#
#
#
# def init_db(dbpath):
#     sql = '''
#         create table movie250
#         (
#         id integer primary key autoincrement,
#         info_link text,
#         pic_link text,
#         cname varchar,
#         ename varchar,
#         score numeric ,
#         rated numeric ,
#         instroduction text,
#         info text
#         )
#
#     '''  #创建数据表
#     conn = sqlite3.connect(dbpath)
#     cursor = conn.cursor()
#     cursor.execute(sql)
#     conn.commit()
#     conn.close()



if __name__ == "__main__":          #当程序执行时
#调用函数
    main()
    #init_db("movietest.db")
    print("爬取完毕 ~ ")