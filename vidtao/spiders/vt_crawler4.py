import scrapy 
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from scrapy.selector import Selector
# from scrapy.http import Response 
# from scrapy.http import HtmlResponse
import time

class vidtao_ads(scrapy.Spider):
    name='vt4'
    allowed_domains=['vidtao.com']

    def start_requests(self):
        start_urls=['https://dashboard.vidtao.com/login']
    
        yield SeleniumRequest(
            url=start_urls[0],
            callback=self.parse,
            wait_time=10,
            screenshot=True
            )

    def parse(self,response):
        self.driver = response.request.meta['driver']
        email=self.driver.find_element_by_id('mat-input-0')
        password=self.driver.find_element_by_id('mat-input-1')
        login = self.driver.find_elements_by_css_selector("button")

        email.clear()
        password.clear()

        email.send_keys("Randomvidtao4@mailinator.com")
        password.send_keys("password")
        login[1].click()
        
        WebDriverWait(self.driver,20).until( EC.presence_of_element_located((By.CLASS_NAME, "pointer")))
        
        yield SeleniumRequest(
            url="https://dashboard.vidtao.com/m/videos/overview",
            wait_time=20,
            wait_until= EC.presence_of_element_located((By.ID, "zADj0k0waFY")),
            callback=self.vt_scrape,
            screenshot=True
            )

    def vt_scrape(self,response):
        WAIT=0.5
        count=0
        youtube_id=set()
        helper=[]
        html = self.driver.find_element_by_tag_name('html')
        up_desc=self.driver.find_element_by_xpath('/html/body/jms-root/jms-layout/main/jms-module-instance/jms-instance-overview/div[2]/st-e-is-table/section/div/mat-card/mat-card-content/div/table/thead/tr/th[4]/div/div/div[1]')
        up_desc.click()
        up_desc.click()
        time.sleep(10)
        self.driver.save_screenshot('image4.png')
        while True:
            try:
                html.send_keys(Keys.END)
                time.sleep(WAIT)
                for ids in Selector(text=self.driver.page_source).xpath('//img[@class="ng-star-inserted"]/ @alt').getall():
                    youtube_id.add(ids)
                    if ids == "-vXPyvNoyOo":
                        break
                        print("[!][!][!][!]       Ads Ended        [!][!][!][!]")

                for i in youtube_id:
                    if i not in helper:
                        yield {
                            'YouTube ID':i
                        }
                    helper.append(i)
                count+=1
                print(f"#########################    Crawler : 4    {count}    {len(youtube_id)}    ########################")
            except Exception as e:
                print(e)
                break