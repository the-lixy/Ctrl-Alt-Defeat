# requires: facebook_page_scraper, selenium, webdriver-manager, python-dateutil, selenium-wire
from facebook_page_scraper import Facebook_scraper

#user will be able to input a number of pages to scrape -- hardcoded values for testing purposes
page_list = ['Drekavacmusic', 'Metallica', 'Megadeth', 'Trivium']

#smartproxy ip 
# (will probably need a paid service to do this for multiple users at a time! use residential IPs -- facebook will block datacenter ips)
proxy_port = 10001

#number of posts to scrape
posts_count = 1

#chrome or firefox
browser = "firefox"

timeout = 600

# set to true once testing is complete
headless = False

pagecounter = 0
page = page_list[pagecounter]

for page in page_list:
    #authentication for smartproxy
    proxy = f'username:password@us.smartproxy.com:{proxy_port}'
  
    #initialising scraper -- page title, posts count, browser type...
    scraper = Facebook_scraper(page, posts_count, browser, proxy=proxy, timeout=timeout, headless=headless)
    
    #printing the json data
    json_data = scraper.scrap_to_json()
    print(json_data)
    
    #change proxy port to avoid facebook's blocking
    proxy_port += 1
    
    #scrape the next requested page
    pagecounter += 1
    
print("Scraped " + str(len(page_list)) + " pages for " + str(posts_count) + " post(s) each")