import scrapy
from scrapy_playwright.page import PageMethod
from urllib.parse import urlencode
from ..items import InfoActItem
import time

class BankruptsSpider(scrapy.Spider):
    name = "bankrupts"
    url = "https://bankrot.fedresurs.ru/bankrupts"

    def start_requests(self): 
        yield scrapy.Request(url=self.url,
        meta=dict(
            playwright_include_page=True,
            playwright=True,
            playwright_page_methods=[
                PageMethod("wait_for_selector", selector=".u-tab__content"),
                ]
            ),
            callback=self.parse_start_page,)

    async def parse_start_page(self, response):
        page = response.meta["playwright_page"]
        await page.click("li.tab__li:nth-of-type(2)")
        context = page.context
        url_arr = []
        i = 1
        while(True):
            start_time = time.time()
            button = await page.query_selector("el-tab.selected button.btn.btn_load_more")
            if button is None:
                break
            else:
                await page.click("el-tab.selected button.btn.btn_load_more")
                await page.wait_for_timeout(1000) 
                
            end_time = time.time() 
            execution_time = end_time - start_time
            print(execution_time, i)
            i += 1
        
        

        yield None