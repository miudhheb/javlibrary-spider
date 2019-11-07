# javlibrarycrawler
javlibrary评分最高影片磁力链爬虫

先爬取javlibrary最高评分影片的番号

获得番号后在通过磁力链搜索引擎搜索该番号对应影片的磁力链


### 开始

``` bash

git@github.com:ericjjj/javlibrary-spider.git


# 使用 shadowsocks 代理， 端口默认1080
brew install polipo
polipo socksParentProxy=localhost:1080


# 安装依赖, 需要有nodejs环境如果没有， brew install node
pip3 install scrapy
pip3 install bs4
pip3 install cfscrape


python3 bestmovie.py

# enjoy~
```
