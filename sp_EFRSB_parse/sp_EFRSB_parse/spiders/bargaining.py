import scrapy
from scrapy_playwright.page import PageMethod

class BargainingSpider(scrapy.Spider):
    name = "bargaining"
    url = "https://old.bankrot.fedresurs.ru/TradeList.aspx"
   
    def start_requests(self): 
        yield scrapy.Request(self.url, meta=dict(
            playwright=True,
            # playwright_include_page=True,
            playwright_page_methods=[
                PageMethod("wait_for_timeout", timeout=100000),
                PageMethod("wait_for_selector", selector="table.bank"),
                # PageMethod("select_option", selector="#ctl00_cphBody_ucTradeStatus_ddlBoundList", value="6"),
                # PageMethod("wait_for_timeout", timeout=100000),
                # PageMethod("screenshot", path="screenshot.png", full_page=True)
                ],
            ),
            callback=self.parse_start_page,
        )
        
    async def parse_start_page(self, response):
        with open("rez.html", "w") as file:
            file.write(response.text)
            # file.write(response.css('#ctl00_cphBody_ucTradeType_ddlBoundList'))
        yield "ASD"
        