import requests
import re
import csv
from bs4 import BeautifulSoup


# Task 1: Produce a list of all butterfly profile links


# Request the html page and parse it
r = requests.get("https://butterfly-conservation.org/uk-butterflies/a-to-z")
soup = BeautifulSoup(r.text)

# Find all hyper link tags in parsed text and print them out
links = soup.find_all("a")
for link in links:
    print(link.attrs.get('href'))

# Make a list of links using list comprehension
hrefs = [link.attrs.get('href') for link in links]

# Skip over links that do not direct to butterfly pages or are not consistent
butterfly_pages = hrefs[39:100]

# Use list comprehension to generate full urls
urls = ["https://butterfly-conservation.org/" + page for page in butterfly_pages]


# Task 2: Parse a single butterfly page


def get_butterfly(url):
    """Request and parse a single butterfly profile page, return a dict of data."""

    r = requests.get(url)
    soup = BeautifulSoup(r.text)

    try:
        h1 = soup.find("h1")

        name = h1.text
        name = name.strip()      # strip off whitespace at end of name

        family = soup.find("li", text=re.compile(r'Family:*'))
        size = soup.find("li", text=re.compile(r'Size:*'))
        wing_span = soup.find("li", text=re.compile(r'Wing Span*'))

        return {
            'name': name, 
            'family': peel_data_from_element(family),
            'size': peel_data_from_element(size),
            'wing span': peel_data_from_element(wing_span),
            'url': url
            }

    except:
        print('Inconsistent format: ', url)
        
        return {
            'name': ' ', 
            'family': ' ',
            'size': ' ',
            'wing span': ' ',
            'url': url
        }


def peel_data_from_element(element):
    """ Helper function to separate the label from the HTML element. """

    just_text = element.text
    return just_text.split(':')[1]


# Task 3: Produce a CSV of butterfly data


def process_each_link(list):
    """ Function to pass the list of links generated in Task 1 to the processing function from Task 2. """

    all_data = []

    for url in list:
        all_data.append(get_butterfly(url))

    return all_data


def write_csv(data):
    """ Function that writes all butterfly data to csv file. """

    fields = ['name', 'url', 'family', 'wing span', 'size']
    filename = 'butterfly_data.csv'

    with open(filename, 'w') as csvfile:
        
        # Create a csv dict writer object
        writer = csv.DictWriter(csvfile, fieldnames=fields)

        # Write header
        writer.writeheader()

        # Write data rows
        writer.writerows(data)


# Invoke function for one butterfly page
data = get_butterfly("https://butterfly-conservation.org/butterflies/green-veined-white")
print(data)

# Invoke functions for all butterfly pages
data_list = process_each_link(urls)
write_csv(data_list)