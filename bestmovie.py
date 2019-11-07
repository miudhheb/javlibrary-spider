from multiprocessing import Pool, Manager
import multiprocessing
import requests
from bs4 import BeautifulSoup
import time
import re
import scrapy
import cfscrape
import traceback

proxy_url = '127.0.0.1:8123'
proxies = {
    'http': proxy_url,
    'https': proxy_url
}

def useweb1(code):
    '''
    使用https://idope.se/torrent-list/获取对于番号的磁力链
    :param code:
    :return:
    '''
    url_root1 = 'https://idope.se'
    search_url1 = 'https://idope.se/torrent-list/'
    headers ={'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
    r1 = requests.get(search_url1+code,headers=headers, proxies=proxies)
    content1 = r1.text
    soup1 = BeautifulSoup(content1, 'html.parser')
    url_1 = soup1.find('a',href=re.compile(code))['href']
    print(url_root1+url_1)
    r2 = requests.get(url_root1+url_1,headers=headers, proxies=proxies)
    content2 = r2.text
    soup2 = BeautifulSoup(content2, 'html.parser')
    magnet = soup2.find('a', id='mangetinfo')['href']
    if magnet:
        return(magnet)
    return ''


def useweb2(code):
    '''
    使用https://btso.pw/search/来查找番号
    :param code:
    :return:
    '''
    search_url2 = 'https://btso.pw/search/'
    headers ={'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
    r1 = requests.get(search_url2+code,headers=headers,proxies=proxies)
    print(search_url2+code)
    content1  = r1.text
    soup1 = BeautifulSoup(content1, 'html.parser')
    url_1 = soup1.find('a', href=re.compile('/detail/hash/'))['href']
    r2 = requests.get(url_1, headers=headers, proxies=proxies)
    content2 = r2.text
    soup2 = BeautifulSoup(content2, 'html.parser')
    magnet = soup2.find('textarea','magnet-link')
    if magnet:
        return magnet.text
    return ''

def DealCookies(cookie):
    cookies = {}
    for line in cookie.split(';'):  # 按照字符：进行划分读取
        # 其设置为1就会把字符串拆分成2份
        name, value = line.strip().split('=', 1)
        cookies[name] = value  # 为字典cookies添加内容
    return cookies


def GUrl(starturl):
    '''
    生成URL
    '''
    urls = []
    urls.append(starturl)
    for i in range(2,26):
        u = 'http://www.javlibrary.com/cn/vl_bestrated.php?&mode=&page='+str(i)
        urls.append(u)
    return urls

def GetAVcode():
    '''
    从URL中获得每一页的AV code
    '''
    codelist = []
    starturl = 'http://www.javlibrary.com/cn/vl_bestrated.php'
    urls = GUrl(starturl)
    for url in urls:

        cookie = '__cfduid=dde56d6fcc565a88be4e864b5f96277111560354411; timezone=-480; __qca=P0-1781664010-1560354568665; cf_clearance=81727c95cdae53188ea59092b25dbd339e51fa28-1561893594-3600-150; over18=18'
        cookies = DealCookies(cookie)
        scraper = cfscrape.create_scraper()
        r = scraper.get(url, proxies=proxies, cookies=cookies)
        content= r.text
        soup = BeautifulSoup(content, 'html.parser')
        # 找class为id的div
        codes = soup.find_all('div', 'id')
        print(url)
        for code in codes:
            codelist.append(code.text)
            print('Get====='+code.text)
    return codelist

def write(code,con):
    file_path = './study_movie.txt'
    f = open(file_path, 'a+')
    f.write(con+'\n')
    f.close()


def GetAVmagnet(code):
    '''
    通过AV code从磁力搜索引擎上获得磁力链，其中一个获得不到结果，就使用第二个
    '''
    print(code)
    try:
        magnet = useweb1(code)
        if magnet:
            write(code, magnet)
        else:
            magnet = useweb2(code)
            write(code, magnet)
        print(code + '=====over')
    except Exception as e:
        print(e, traceback.print_exc())


if __name__ == '__main__':
    codelist = GetAVcode()
    cpus = multiprocessing.cpu_count()
    p = Pool(8)
    for code in codelist:
        p.apply_async(GetAVmagnet, args=(code,))
    p.close()
    p.join()
