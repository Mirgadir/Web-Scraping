import os
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from selenium import webdriver  
import requests as req
import pandas as pd


def scrape():
    #import required libraries


    #Chromedriver execute
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)
    #visit first url
    url="https://mars.nasa.gov/news/"
    browser.visit(url)
    #save html and assign parser
    html=browser.html
    soup = bs(html, "html.parser" )
    #get first title from the url
    news_title = soup.find('li',class_="slide").find('div', class_="content_title").text
    # get first paragraph under first title
    news_p = soup.find('li',class_="slide").find('div', class_="article_teaser_body").text

    # url2
    url2 = "https://www.jpl.nasa.gov/spaceimages/"
    #visit url2 click on full image button, wait for a response
    browser.visit(url2)
    browser.find_by_id('full_image').click()
    time.sleep(5)

    #find and click on more info button
    browser.links.find_by_partial_text('more info').click()

    #get an image url
    featured_image_url = browser.find_by_xpath("//img[@class='main_image']")._element.get_attribute("src")
    
    #time.sleep(10)
    #url3 for mars weather 
    url3 = "https://twitter.com/marswxreport?lang=en"
    #visit url save html and close

    # splinter didn't give me expected result, so I switched to selenium
    # browser.visit(url3)
    # browser.url
    # html = browser.html

    driver = webdriver.Chrome()
    driver.get(url3)
    html = driver.page_source
    driver.close()

    #scrap tweets into a list
    soup = bs(html, 'html.parser')
    tweets = soup.find_all('div', class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")

    #time.sleep(15)
    #find required tweet with weather info
    mars_weather = tweets[0].text

    # url4 mars facts
    url4 = "https://space-facts.com/mars/"

    # use pandas to find all tables on website
    df_list = pd.read_html(url4)
    #pick first table
    table_df = df_list[0]
    #rename columns
    table_df = table_df.rename(columns={0: 'Parameter', 1: 'Value'})

    html_table = table_df.to_html()
    
    
    browser.visit(url4)
    html = browser.html
    soup = bs(html, "html.parser")
    tables = soup.findChildren('table')
    table_data=[]
    my_table = tables[0]
    rows = my_table.findChildren(['th', 'tr'])   

    for row in rows:
        title = row.find('td', class_="column-1").text.strip()
        value = row.find('td', class_="column-2").text.strip()
        table_data.append({'title': title, 'value': value})

    #url5 mars hemispheres
    url5 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser.visit(url5)
    browser.url
    html = browser.html
    #assign parser, scrap list of images
    soup = bs(html, "html.parser")
    images = soup.find_all('div', class_="description")
    #use link as f-string
    link = f"https://astrogeology.usgs.gov"

    time.sleep(10)
    # loop thorugh images list, pick href and add it to link, visit new link, scrap for image url and title, append to a list:
    hemisphere_image_urls = []
    for image in images:
        img_link = f"{link}{image.find('a')['href']}"
        browser.visit(img_link)
        img_url = browser.find_by_xpath("//img[@class='wide-image']")._element.get_attribute("src")
        title = browser.find_by_xpath("//h2[@class='title']").text
        title = title.rstrip('Enhanced')
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    
    hemisphere_image_urls

    time.sleep(10)
    #create a dictionary for DB
    mars_website_dict={
    'news_title': news_title, 'news_paragraph': news_p, 'featured_image_url': featured_image_url, 
    'mars_weather': mars_weather, 'row1_title': table_data[0]['title'], 'row1_value': table_data[0]['value'], 'row2_title': table_data[1]['title'], 'row2_value': table_data[1]['value'], 'row3_title': table_data[2]['title'], 'row3_value': table_data[2]['value'], 'row4_title': table_data[3]['title'], 'row4_value': table_data[3]['value'], 'row5_title': table_data[4]['title'], 'row5_value': table_data[4]['value'], 'row6_title': table_data[5]['title'], 'row6_value': table_data[5]['value'], 'row7_title': table_data[6]['title'], 'row7_value': table_data[6]['value'], 'row8_title': table_data[7]['title'], 'row8_value': table_data[7]['value'], 'row9_title': table_data[8]['title'], 'row9_value': table_data[8]['value'], 
    'url1_title': hemisphere_image_urls[0]['title'], 'url1_img': hemisphere_image_urls[0]['img_url'],
    'url2_title': hemisphere_image_urls[1]['title'], 'url2_img': hemisphere_image_urls[1]['img_url'],
    'url3_title': hemisphere_image_urls[2]['title'], 'url3_img': hemisphere_image_urls[2]['img_url'],
    'url4_title': hemisphere_image_urls[3]['title'], 'url4_img': hemisphere_image_urls[3]['img_url']              
    }
    browser.quit()
    
    return mars_website_dict

