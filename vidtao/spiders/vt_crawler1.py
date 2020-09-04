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
    name='vt1'
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

        email.send_keys("Randomvidtao1@mailinator.com")
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
        up_desc=self.driver.find_element_by_xpath('/html/body/jms-root/jms-layout/main/jms-module-instance/jms-instance-overview/div[2]/st-e-is-table/section/div/mat-card/mat-card-content/div/table/thead/tr/th[3]/div/div/div[1]')
        up_desc.click()
        time.sleep(10)
        self.driver.save_screenshot('image1.png')
        while True:
            try:
                html.send_keys(Keys.END)
                time.sleep(WAIT)
                for ids in Selector(text=self.driver.page_source).xpath('//img[@class="ng-star-inserted"]/ @alt').getall():
                    youtube_id.add(ids)
    
                    if ids == "NMj-FtLkp2E":
                        break
                        print("[!][!][!][!]       Ads Ended        [!][!][!][!]")

                for i in youtube_id:
                    if i not in helper:
                        yield {
                            'YouTube ID':i
                        }
                    helper.append(i)
                count+=1
                print(f"#########################   Crawler : 1     {count}    {len(youtube_id)}    ########################")
            except Exception as e:
                print(e)
                break
                
                
# "-vXPyvNoyOo"
        # ad_id=Selector(text=self.driver.page_source).xpath('//img[@class="ng-star-inserted"]/ @alt').getall()
        # for i in ad_id:

        #     yield {
        #         "Youtube ID":i
        #     }

# 
        # with open("vidscript.html",'w') as f:
        #     f.write(self.driver.page_source)
                
        
    # def scrape_ads(self,response):
            # title,up_date,view_count,yesterday,monthly,length=[],[],[],[],[],[]
    #     print(response.text)
        # ad_id=response.xpath('//img[@class="ng-star-inserted"]/ @alt').getall()
        # for i in ad_id:
        #     yield{
        #         "Youtube ID":i
        #     }



                # all_data=response.xpath('//div[@class="column-inner ng-star-inserted"]/ text()').getall()
                # channel_name=response.xpath('//span[@class="link pointer"]/ text()').getall()
                # for i in range(0,len(all_data)//6):
                #     a=all_data[count:count1]
                #     title.append(a[0])
                #     up_date.append(a[1])
                #     view_count.append(a[2])
                #     yesterday.append(a[3])
                #     monthly.append(a[4])
                #     length.append(a[5])
                #     count=count1
                #     count1+=6

                # zipped=zip(ad_id,title,up_date,view_count,yesterday,monthly,length,channel_name)
                # for i in zipped:
                #     if i:
                #         yield{
                #             'youtube id':i[0],
                #             'title':i[1],
                #             'upload date':i[2],
                #             'view count':i[3],
                #             'yesterday':i[4],
                #             'monthly':i[5],
                #             'length':i[6],
                #             'channel name':i[7],
                #         }
                
            
            
        


        # with open("vidscript.txt",'w') as f:
        #     f.write(self.driver.page_source)



       