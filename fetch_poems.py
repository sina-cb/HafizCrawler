import requests
from BeautifulSoup import BeautifulSoup
import random

__author__ = 'Sina Solaimanpour'

responses = {
    'MajorTests Tricky Words': 'http://www.vocabulary.com/lists/682592#view=notes',
    'Official GRE Verbal': 'http://www.vocabulary.com/lists/700826#view=notes',
    'Magoosh Tricky Words': 'http://www.vocabulary.com/lists/687078#view=notes'
}


def read_data(urlStr):
    page = requests.get(urlStr).text
    soup = BeautifulSoup(page)

    node = soup.find('ol', {"id": "wordlist"})

    dictionary = {}
    for row in node.findAll("li"):
        des = row.find('div', {"class": "description"})

        if des is None:
            dictionary[row.attrs[3][1]] = (row.find('div', {"class": "definition"}).text, 'No Description')
        else:
            dictionary[row.attrs[3][1]] = (row.find('div', {"class": "definition"}).text, des.text)

    return dictionary


def randomize(dictionary):
    keys = dictionary.keys()
    random.shuffle(keys)

    randomized_d = {}
    for key in keys:
        randomized_d[key] = (dictionary[key][0], dictionary[key][1])

    return randomized_d


def write_to_file(list, dictionary):
    f = open(list + '.txt', 'w')
    keys = dictionary.keys()
    for key in keys:
        f.write(key + "\t" + dictionary[key][0] + "\t" + dictionary[key][1] + "\n")
    f.close()

    f = open(list+'_index.txt', 'w')
    f.write('0')
    f.close()

def main():
    responses_key = responses.keys()
    list = responses_key[0]
    print("Reading data from " + responses[list])
    dictionary = read_data(responses[list])

    dictionary_r = randomize(dictionary)

    write_to_file(list, dictionary_r)


if __name__ == "__main__": main()
