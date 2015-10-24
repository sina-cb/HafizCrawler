import requests
from BeautifulSoup import BeautifulSoup
import re

__authors__ = 'Sina Solaimanpour, Shervin Shahryari'


def read_links(urlStr):
    page = requests.get(urlStr).text
    soup = BeautifulSoup(page)

    links = []
    for node in soup.findAll('td'):

        node = node.find('font')
        if node != None:
            node = node.find('font')
            if node != None:
                node = node.find('a')
                if node != None:
                    links.insert(len(links), node.attrs[0][1])

    return links


def read_poems(urlStr):
    page = requests.get(urlStr).text
    soup = BeautifulSoup(page)

    node = soup.find('blockquote')
    node = node.find('blockquote')

    poem = []
    for paragraph in node.findAll('p'):
        paragraph = paragraph.find('font').find('strong')

        index = 0
        if paragraph != None:
            for content in paragraph.contents:
                if index % 2 == 0:
                    line = content.replace("\r\n", "")
                    line = line.replace("&amp;", "&")
                    line = line.replace("&nbsp;", "")
                    line = line.replace("&#146;", "'")
                    line = line.replace("&quot;", '"')
                    line = re.sub("\s\s+", " ", line)
                    poem.insert(len(poem), line.strip())
                index = index + 1

            poem.insert(len(poem), "\n")

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
    baseUrl = 'http://www.rumionfire.com/shams/'
    f = open_file("Divan-e-Shams - Rumi")

    links = read_links(baseUrl + "index.htm")

    index = 1
    for link in links:
        temp_url = baseUrl + link
        print(temp_url)
        text = read_poems(temp_url)
        write_to_file(text, f)

    close_file(f)

if __name__ == "__main__": main()
