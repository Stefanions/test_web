import scrapy
from scrapy_playwright.page import PageMethod
from urllib.parse import urlencode
from ..items import InfoActItem


class BargainingNewSpider(scrapy.Spider):
    name = "bargaining_new"
    # url = "https://fedresurs.ru/biddings"


    def __init__(self, param=None, *args, **kwargs):
        super(BargainingNewSpider, self).__init__(*args, **kwargs)
        self.url = param
        self.results = []

    def start_requests(self): 
        #Параметры для запроса
        # params = {
        #     "tradeType": "all",
        #     "price": "null",
        #     "tradePeriod": "null",#'{"endJsDate":"2023-02-11T21:00:00.000Z"}',
        #     "bankrupt": "null",
        #     "onlyAvailableToParticipate": "false",
        #     "regionNumber": "all",
        #     "limit": "15"Ф
        # }
        # url = self.url + '?' + urlencode(params)
        yield scrapy.Request(url=self.url,
        meta=dict(
            playwright_include_page=True,
            playwright=True,
            playwright_page_methods=[
                PageMethod("wait_for_selector", selector=".u-card-result"),
                ]
            ),
            callback=self.parse_start_page,
        )

    async def parse_start_page(self, response):
        page = response.meta["playwright_page"]
        date_mas = []
        context = page.context
        url_arr = []
        #Раскрытие всего списка торгов, нажатие на кнопку загрузить ещё много раз
        count = response.xpath("//div[@class = 'tab__btn tab__btn_active']//*[@class = 'tab__count']//text()").get().strip().replace(">", "").replace(" ", "")
        count = (int(count)//15)
        idx = 0
        while(True):
            button = await page.query_selector("div.more_btn")
            if button is None:
                break
            else:
                await page.click("div.more_btn")
                idx += 1
                if(idx != count):
                    await page.wait_for_selector('div.more_btn')  
                else:
                    break


        #Получение ссылок на все торги в отдельности
        while(True):
            elem = await page.query_selector("el-tab.selected div.u-card-result:not(.u-card-result_opacity) div.info-link-container")
            if elem is None:
                break
            else:
                async with context.expect_page() as new_page_info:
                    #Сохранение даты
                    container_date = await page.query_selector("xpath=//el-tab//div[@class='u-card-result']//div[@class='period-text']")
                    if container_date:
                        text_date = await container_date.text_content()
                        date_mas.append(text_date)

                    await page.click("el-tab.selected div.u-card-result:not(.u-card-result_opacity) div.info-link-container")        
                    # await page.wait_for_timeout(1000)
                new_page = await new_page_info.value
                await new_page.wait_for_load_state()
                url_arr.append(new_page.url)
                await new_page.close()
        page.close

        #Вызов запросов на парсинг лотов в каждой карточке
        for i, el in enumerate(url_arr):
            yield scrapy.Request(url = el + "/lots",
                meta=dict(
                playwright=True,
                playwright_page_methods=[
                    PageMethod("wait_for_selector", selector=".header-wrapper"),
                    ],
                additional_info={'date': date_mas[i]}
                ),
                callback=self.parse_one_auc,
                errback=self.handle_error
            )
        yield None

    def parse_one_auc(self, response):
        item = InfoActItem()
        additional_info = response.meta.get('additional_info', {})
        date = additional_info['date']
        for lot_html in response.css("bidding-lot-card").getall():
            #Парсим дескрипшн
            lot = scrapy.Selector(text=lot_html)
            item['trade_id'] = response.css("div.headertext::text").get()
            item['url'] = (response.url).rstrip('/lots')
            item['start_price'] = lot.css("div.lot-item-description div.info-item-name:contains('Начальная цена') + div.info-item-value::text").get()
            item['classifier'] = lot.xpath("//div[@class='lot-item-classifiers-element']/text()").get()
            item['description'] = lot.xpath("//div[@class='lot-item-tradeobject']//text()").get()
            item['final_price'] = lot.css("div.lot-item-description div.info-item-name:contains('Итоговая цена') + div.info-item-value::text").get()
            item['winner'] = ' '.join(lot.xpath("//div[contains(text(), 'Победитель')]//following-sibling::div[contains(@class, 'info-item-value')][1]//text()").getall())
            item['justification'] = lot.xpath("//div[contains(text(), 'Обоснование итогового решения')]//following-sibling::div[contains(@class, 'info-item-value')][1]//text()").get()
            item['date'] = date
            yield item
        

    def handle_error(self, failure):
        yield None
