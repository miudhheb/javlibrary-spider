import scrapy

class MimvpSpider(scrapy.spiders.Spider):
    name = "mimvp"
    # allowed_domains = ["mimvp.com"]
    start_urls = [
        "http://proxy.mimvp.com/exist.php",
        "https://proxy.mimvp.com/exist.php",
    ]

    ## 代理设置方式1：直接在代理里设置
    def start_requests(self):
        urls = [
            "http://www.javlibrary.com/cn/vl_bestrated.php",
        ]
        for url in urls:
            meta_proxy = ""
            if url.startswith("http://"):
                meta_proxy = "http://127.0.0.1:8123"           # http代理
            elif url.startswith("https://"):
                meta_proxy = "http://127.0.0.1:8123"      # https代理
            cookie = '__cfduid=dde56d6fcc565a88be4e864b5f96277111560354411; timezone=-480; __qca=P0-1781664010-1560354568665; cf_clearance=81727c95cdae53188ea59092b25dbd339e51fa28-1561893594-3600-150; over18=18'
            cookies = {
                '__cfduid': 'dde56d6fcc565a88be4e864b5f96277111560354411',
                'timezone': -480,
                '__qca': 'P0-1781664010-1560354568665',
                'cf_clearance': '81727c95cdae53188ea59092b25dbd339e51fa28-1561893594-3600-150',
                'over18': 18,
            }
            yield scrapy.Request(url=url, cookies=cookies, callback=self.parse,dont_filter=True, meta={'proxy': meta_proxy})


    def parse(self, response):
        mimvp_url = response.url                    # 爬取时请求的url
        body = response.body                        # 返回网页内容

        print("mimvp_url : " + str(mimvp_url))
        print("body : " + str(body))
