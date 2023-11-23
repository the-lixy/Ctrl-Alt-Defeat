'''
import requests
from bs4 import BeautifulSoup

def get_website_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Error:", err)

def seo_audit_tool(url):
    website_data = get_website_data(url)

    if website_data:
        soup = BeautifulSoup(website_data, 'html.parser')

        # Check Title Tag
        title_tag = soup.title
        if title_tag:
            print(f"Title Tag: {title_tag.text.strip()}")
        else:
            print("Title Tag not found.")

        # Check Meta Description
        meta_description = soup.find('meta', attrs={'name': 'description'})
        if meta_description:
            print(f"Meta Description: {meta_description.get('content').strip()}")
        else:
            print("Meta Description not found.")

        # Check H1 Tags
        h1_tags = soup.find_all('h1')
        if h1_tags:
            print("H1 Tags:")
            for h1_tag in h1_tags:
                print(f"- {h1_tag.text.strip()}")
        else:
            print("H1 Tags not found.")

        # Check Images without Alt Text
        img_tags = soup.find_all('img', attrs={'alt': None})
        if img_tags:
            print("Images without Alt Text:")
            for img_tag in img_tags:
                print(f"- {img_tag}")
        else:
            print("All images have Alt Text.")

    else:
        print(f"Failed to retrieve data for {url}")

if __name__ == "__main__":
    website_url = input("Enter the website URL for SEO audit: ")
    seo_audit_tool(website_url)
'''
import requests
import json

def seo():
    url = "https://seo-keyword-research.p.rapidapi.com/keynew.php"

    key = input(str("Enter keyword:"))

    querystring = {"keyword":key,"country":"gb"}

    headers = {
	"X-RapidAPI-Key": "1caf149ecdmsh763a29cd8276b10p11797bjsn2980280a52cb",
	"X-RapidAPI-Host": "seo-keyword-research.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    x = response.json()

    with open('data.json', 'w') as f:
        json.dump(x, f)

def formatting():
    # Your JSON data
    with open("data.json", "r") as file:
        json_data = json.load(file)

    # Convert JSON data to HTML table
    html_table = "<table border='1'><tr><th>Text</th><th>CPC</th><th>Volume</th><th>V</th><th>Competition</th><th>Score</th></tr>"

    for entry in json_data:
        html_table += f"<tr><td>{entry['text']}</td><td>{entry['cpc']}</td><td>{entry['vol']}</td><td>{entry['v']}</td><td>{entry['competition']}</td><td>{entry['score']}</td></tr>"

    html_table += "</table>"

    # Save the HTML table to a file
    with open('output_table.html', 'w') as file:
        file.write(html_table)

    print("HTML table has been generated and saved to output_table.html.")


def main(): 
    #seo()
    formatting()

main()