import requests
from bs4 import BeautifulSoup


# Request the html page and parse it
r = requests.get("https://butterfly-conservation.org/uk-butterflies/a-to-z")
soup = BeautifulSoup(r.text)

# Find all hyper link tags in parsed text and print them out
links = soup.find_all("a")
for link in links:
    print(link.attrs.get('href'))

# Make a list of links using list comprehension
hrefs = [link.attrs.get('href') for link in links]

# Skip over links that do not direct to butterfly pages
butterfly_pages = hrefs[39:100]

# Use list comprehension to generate full urls
urls = ["https://butterfly-conservation.org/" + page for page in butterfly_pages]