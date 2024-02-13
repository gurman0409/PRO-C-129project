from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv

START_URL = "https://en.wikipedia.org/wiki/Lists_of_stars"
browser = webdriver.Chrome("/path/to/chromedriver")
browser.get(START_URL)
time.sleep(10)
star_data = []
headers = ["Name","Distance","Mass","Radius"]

def scrape():
    for i in range(1,5):
        while True:
            time.sleep(2)

            soup = BeautifulSoup(browser.page_source, "html.parser")

            # Check page number    
            current_page_num = int(soup.find_all("input", attrs={"class", "page_num"})[0].get("value"))

            if current_page_num < i:
                browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            elif current_page_num > i:
                browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()
            else:
                break

        for ul_tag in soup.find_all("ul", attrs={"class", "exoplanet"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []
            for index, li_tag in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")

            # Get Hyperlink Tag
            hyperlink_li_tag = li_tags[0]

            temp_list.append("https://en.wikipedia.org/wiki/Lists_of_stars"+ hyperlink_li_tag.find_all("a", href=True)[0]["href"])
           
            star_data.append(temp_list)

        browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()

        print(f"Page {i} scraping completed")

# Calling Method
scrape()

new_star_data = []

def scrape_more_data(hyperlink):
    try:
        page = request.get(hyperlink)
        soup = BeautifulSoup(page.content,"html.parser")
        temp_list = []
        for tr_tag in soup.find_all("tr",attrs = {"class":"facthttps://en.wikipedia.org/wiki/Lists_of_stars_row"}):
            td_tag = tr_tag.find_all("td")
            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div",attrs = {"class":"value"})[0].contents[0])
                except:
                    temp_list.append("")
            new_star_data.append(temp_list)
    except:
        time.sleep(1)
        scrape_more_data(hyperlink)

for index,data in enumerate(star_data):
    scrape_more_data(data[5])

print(new_star_data[0:10])

final_star_data = []

for index,data in enumerate(star_data):
    new_star_data_element = new_star_data[index]
    new_star_data_element = [elem.replace("\n","") for elem in new_star_data_element]
    new_star_data_element = new_star_data_element[:7]
    final_star_data.append(data+new_star_data_element)

with open ("final.csv" , "w") as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(headers)
    csvwriter.rightrows(final_star_data)