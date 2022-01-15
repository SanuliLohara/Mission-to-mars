from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests
import time
from webdriver_manager.chrome import ChromeDriverManager
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def nasa(browser):

    #Connecting to NASA site
    url = "https://redplanetscience.com"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # get the title
    element = soup.select_one("section.image_and_description_container")
    title = element.find("div", class_="content_title").get_text()

    # get the paragraph
    para = element.find("div", class_="article_teaser_body").get_text()

    return title,para

def images(browser):
    # featured image
    # go to image site
    url = "https://spaceimages-mars.com"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # find image link
    featured_image_url = soup.find("img",class_= "headerimage")
    featured_image_url = featured_image_url["src"]

    return url+"/"+featured_image_url



# mars facts
# go to facts site
url = "https://galaxyfacts-mars.com"


# find table data
facts_table = pd.read_html(url)[0]

# give column appropriate names
facts_table.columns = ["Measurements","Mars","Earth"]
facts_table=facts_table.drop(0).reset_index()
facts_table= facts_table.drop('index',axis = 1)
facts_html = facts_table.to_html()
    

def hem(browser):
    # mars hemispheres
    # go to hemispheres site
    url = "https://marshemispheres.com"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hem_info = []

    # find the links
    links = browser.find_by_css("a.product-item h3")

    for link in range(len(links)-1):
        hem = {}

        # click link
        browser.find_by_css("a.product-item h3")[link].click()

        # find the title
        hem["title"] = browser.find_by_css("h2.title").text


        # find the url
        pic_link = browser.find_link_by_text("Sample")
        hem["url"] = pic_link["href"]

        # add to dictionary
        hem_info.append(hem)

        #go back in browser
        browser.back()

    return hem_info

def scrape():
    print("Starting web scraping...")
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    title, para = nasa(browser)
    image_url = images(browser)
    table_facts = facts_html
    hemisphere = hem(browser)

    data = {
        "title": title,
        "para": para,
        "image_url":image_url,
        "table_facts": table_facts,
        "hemisphere": hemisphere
    }

    browser.quit()
    print("Finished scarping.")
    return data
    
if __name__ == "__main__":
    scrape()