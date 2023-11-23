# requires: facebook-scraper, facebook-page-scraper, selenium, // webdriver-manager, python-dateutil, selenium-wire
from facebook_page_scraper import Facebook_scraper
from facebook_scraper import get_profile

from selenium import webdriver
from selenium.webdriver.common.by import By

import json
import sys
import re

import requests
import string
from bs4 import BeautifulSoup



def find_likes_objects(text):
    pattern = r'(?<="likes":).*?(?=,|\})'
    likes_objects = re.findall(pattern, text)
    likes_list = [json.loads(f'{{"likes":{obj}}}') for obj in likes_objects]
    return likes_list

def find_comments_objects(text):
    pattern = r'(?<="comments":).*?(?=,|\})'
    comments_objects = re.findall(pattern, text)
    comments_list = [json.loads(f'{{"comments":{obj}}}') for obj in comments_objects]
    return comments_list

#user will be able to input a number of pages to scrape -- hardcoded values for testing purposes
#page_list = ['OfficialJudasPriest', 'Metallica', 'Megadeth', 'Trivium']
page_list = ['https://www.facebook.com/OfficialJudasPriest/', 'https://www.facebook.com/Metallica/']

#page_list = sys.argv[1]


#smartproxy ip 
# (will probably need a paid service to do this for multiple users at a time! use residential IPs -- facebook will block datacenter ips)
proxy_port = 1005

#number of posts to scrape
posts_count = 3

#chrome or firefox
browser = "firefox"

timeout = 600

# set to true once testing is complete
headless = True

pagecounter = 0
page = page_list[pagecounter]

for page in page_list:
    #authentication for smartproxy
    proxy = f'username:password@us.smartproxy.com:{proxy_port}'
    
    #fbwebscraper only takes the page name not full link, so we will strip it down
    pageStripped = page.lstrip("https://www.facebook.com/").rstrip("/")
    print(pageStripped)
    #initialising scraper -- page title, posts count, browser type...
    scraper = Facebook_scraper(pageStripped, posts_count, browser, proxy=proxy, timeout=timeout, headless=headless)
    
    jsonDumps = str
    jsonLoads = str
    
    #printing the json data
    json_data = scraper.scrap_to_json()
    json_str = json.dumps(json_data, indent=4)
    #print(json.loads(json_str))
    jsonLoads = json.loads(json_str)
    
    #print(json.dumps(json_str))
    jsonDumps = json.dumps(json_str)
    
    #change proxy port to avoid facebook's blocking
    proxy_port += 1

    print(page + "'s stats: ")

    totalLikes = 0
    likes = find_likes_objects(jsonLoads)
    comments = find_comments_objects(jsonLoads)
    

    # finding total likes for page
    response = requests.get(page)
    if response.status_code != 200:
        print("Error fetching page")
        exit()
    else:
        content = response.content
        
    soup = BeautifulSoup(response.content, 'html.parser')
    
    content = str(content)
    location = content.find("likes")
    likecount = (content[(location - 11):location]).strip(string.ascii_lowercase).strip(string.ascii_uppercase).strip(".").strip(" ")
    print(pageStripped + "'s total page likes: " + likecount)
    
    
        
    # finding average likes per post
    theSum = 0
    sumLikes = 0
    averageLikes = 0
    for like in likes:
        theSum = like['likes']
        sumLikes += theSum
        averageLikes = int((sumLikes/len(likes)))
    print("Average likes for " + pageStripped + "'s last " + str(posts_count) + " posts: " + str(averageLikes))
    print('\n')
    
    theSum = 0
    sumComments = 0
    averageComments = 0
    for comment in comments:
        theSum = comment['comments']
        sumComments += theSum
        averageLikes = int((sumLikes/len(likes)))
    print("Average number of comments for " + pageStripped + "'s last " + str(posts_count) + " posts: " + str(averageLikes))
    print('\n')
    
    
    #scrape the next requested page
    pagecounter += 1
    
print('\n')
print("Scraped " + str(len(page_list)) + " pages for " + str(posts_count) + " post(s) each")