import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

sites = pd.read_excel('D:\sites.xlsx')


full = list()
for site in sites["WebSite"]:
    r = requests.get(r'http://' + site + '/info_add/teachers_salary/#')
    if r.status_code == 200:        
        driver = webdriver.Chrome()
        a = driver.get(r'http://' + site + '/info_add/teachers_salary/#')
        try:
            driver.find_element_by_class_name("uscl-public_popup-not-show").click()     
        except NoSuchElementException:
            pass
        try:
            driver.find_element_by_partial_link_text("2018/2019").click()
        except NoSuchElementException:
            pass
        else:
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            table = soup.find("table", {"id": "salary"})
            pd.set_option('display.max_columns', None)
            table_rows = table.find_all('tr')
            l = []
            for tr in table_rows:
                td = tr.find_all('td')
                row = [tr.text for tr in td]
                l.append(row)
            try:
                info = pd.DataFrame(l, columns=["Отчетный период", "Численность учителей в отчетном периоде",
                                "Фонд оплаты труда учителей в отчетном периоде",
                                "Средняя начисленная заработная плата учителя в отчетном периоде"]).iloc[1:]
            except:
                pass
            else:
                info["WebSite"] = site
                driver.close()
                full.append(info)
    else:
        pass
df = pd.concat(full, ignore_index=True)
print(df)
df.to_excel("D:/18-19.xlsx",
               sheet_name='18/19')

