#coding:utf-8
from URLManager import UrlManager
from HtmlDownloader import HtmlDownloader
from HtmlParser import HtmlParser

from DataOutput import DataOutput


class SpiderMan(object):
    def __init__(self):
        self.manager = UrlManager()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.output = DataOutput()
    def crawl(self,root_url):
        #添加入口URL
        self.manager.add_new_url(root_url)  #先添加第一个链接到为处理的列表中
        #判断url管理器中是否有新的url，同时判断抓取了多少个url
        while(self.manager.has_new_url() and self.manager.old_url_size()<100): #第一个页面爬出来的链接已经占用了70多个，导致循环后面获取的链接无法被使用过，n为循环次数，m为一个页面爬出的链接，爬出所有的内容=n*m；需要优化，应该每个页面爬出所有链接后，循环爬出那些链接的内容，然后进行下一个循环，即为二次循环才能满足
            try:
                #从URL管理器获取新的url
                new_url = self.manager.get_new_url()
                print(new_url)
                #HTML下载器下载网页
                html = self.downloader.download(new_url)  #下载整个列表的html内容
                #HTML解析器抽取网页数据
                new_urls,data = self.parser.parser(new_url,html) #解析每个html页面的内容，获取所有的链接，还有一段内容
                print(new_urls)
                print(len(new_urls))    #每次解析html的url列表都很多，都插入到未处理的url集合里面，但是只循环100次，导致后面循环爬到的url未被使用过
                print(data)
                #将抽取到url添加到URL管理器中
                self.manager.add_new_urls(new_urls) #新的url集合插入未处理的url里面
                #数据存储器储存文件
                self.output.store_data(data)        #data插入显示的文件

                print ("已经抓取%s个链接"%self.manager.old_url_size())

            except Exception as e:
                print (e)
                print ("crawl failed")
            #数据存储器将文件输出成指定格式
        self.output.output_html()

if __name__=="__main__":
    spider_man = SpiderMan()
    spider_man.crawl("http://baike.baidu.com/view/284853.htm")
    #spider_man.crawl("https://baike.baidu.com/item/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB")
