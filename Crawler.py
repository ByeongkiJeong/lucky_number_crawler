from time import localtime, sleep, strftime

import pandas as pd

from selenium import common, webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class Crawler():
    def __init__(self, webdriver_name="PhantomJS"):
        if webdriver_name == "PhantomJS":
            self.browser = webdriver.PhantomJS(executable_path = './webdriver/phantomjs.exe')
        elif webdriver_name == "Edge":
            self.browser = webdriver.Edge(executable_path='./webdriver/MicrosoftWebDriver.exe')
        elif webdriver_name == "Firefox":
            self.browser = webdriver.Firefox(executable_path='./webdriver/geckodriver.exe')
        else:
            print("Error : Unkonwn webdriver name")

        self.product_group_name = ''
        self.wait_time = 0

    def get_lucky(self, root_url):
        print("Root url : " + root_url)
        
        #get numbers
        print("Gathering...")
        df = pd.DataFrame(columns=["Period", "Number1" , "Number2" , "Number3" , "Number4" , "Number5" , "Number6" , "Number_bonus", "Total sales", "NumOfWinner"])
        page_num = 1
        while(True):
            url = root_url + str(page_num)
            self.get_html(url)
            if page_num % 10 == 0:
                print("Processing %s"%(page_num))
            #http://nlotto.co.kr/gameResult.do?method=byWin&drwNo=1
            Number1 = self.browser.find_element_by_xpath("/html/body/section/article/article/div/div[2]/p/img[1]").get_attribute("alt")
            Number2 = self.browser.find_element_by_xpath("/html/body/section/article/article/div/div[2]/p/img[2]").get_attribute("alt")
            Number3 = self.browser.find_element_by_xpath("/html/body/section/article/article/div/div[2]/p/img[3]").get_attribute("alt")
            Number4 = self.browser.find_element_by_xpath("/html/body/section/article/article/div/div[2]/p/img[4]").get_attribute("alt")
            Number5 = self.browser.find_element_by_xpath("/html/body/section/article/article/div/div[2]/p/img[5]").get_attribute("alt")
            Number6 = self.browser.find_element_by_xpath("/html/body/section/article/article/div/div[2]/p/img[6]").get_attribute("alt")
            Number_bonus = self.browser.find_element_by_xpath("/html/body/section/article/article/div/div[2]/p/span[2]/img").get_attribute("alt")
            Total_sales = self.browser.find_element_by_xpath("/html/body/section/article/article/div/div[3]/ul/li[2]/span[2]").text
            NumOfWinner = self.browser.find_element_by_xpath("/html/body/section/article/article/div/table[1]/tbody/tr[2]/td[3]").text

            if Total_sales == '원':
                break
            row = [page_num, Number1, Number2, Number3, Number4, Number5, Number6, Number_bonus, Total_sales, NumOfWinner]
            df.loc[len(df)] = row
            sleep(self.wait_time)
            page_num = page_num + 1
            
        #save
        df = self.save_df(df)
        print("Finally, we made it!")

    def get_html(self, url):
        self.browser.get(url)
    
    def save_df(self, df):
        file_name = './'+ strftime("%Y%m%d_%H%M%S_", localtime()) + "_lucky.xlsx" 
        self.save_df_to_xlsx(file_name, df)
        return df[0:0]

    def save_df_to_xlsx(self, path, df):
        writer = pd.ExcelWriter(path)
        df.to_excel(writer,'Sheet1')
        writer.save()

if __name__ == "__main__":
    crawler = Crawler()
    crawler.amazon(root_url="http://nlotto.co.kr/gameResult.do?method=byWin&drwNo=")
