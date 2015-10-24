import requests
from BeautifulSoup import BeautifulSoup
import re

__authors__ = 'Sina Solaimanpour, Shervin Shahryari'


def read_links(urlStr):
    page = requests.get(urlStr).text
    soup = BeautifulSoup(page)

    node = soup.find('ul')

    links = []
    for row in node.findAll("li"):
        row = row.find('a')
        links.insert(len(links), row.attrs[0][1].encode('ascii','ignore'))

    return links


def read_poems(urlStr):
    page = requests.get(urlStr).text
    soup = BeautifulSoup(page)

    node = soup.find('div', {"id": "Main"})
    node = node.find('div', {"id": "Eng"})
    node = node.find('p')

    poem = []
    index = 0
    for content in node.contents:
        if index % 2 == 0:
            line = content.replace("\r\n", "")
            line = line.replace("&amp;", "&")
            line = line.replace("&nbsp;", "")
            line = line.replace("&#146;", "'")
            line = line.replace("&quot;", '"')
            line = re.sub("\s\s+", " ", line)
            poem.insert(len(poem), line.strip())
        index = index + 1

    return poem


def open_file(path):
    f = open(path + '.txt', 'w')
    return f


def write_to_file(text, f):
    for line in text:
        f.write(line.encode('ascii','ignore') + "\n")
    f.write("\n")


def close_file(file):
    file.close()


def main():
    baseUrl = 'http://www.hafizonlove.com/divan/'
    f = open_file("Ghazals - Hafiz")

    links = read_links(baseUrl + "index.htm")

    index = 1
    for sub_url in links:
        links_to_poems = read_links(baseUrl + sub_url)

        for poem_url in links_to_poems:
            temp_url = baseUrl + str(index).zfill(2) + "/" + poem_url
            print(temp_url)
            text = read_poems(temp_url)
            write_to_file(text, f)
        index = index + 1

    close_file(f)

if __name__ == "__main__": main()
