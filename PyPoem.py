import bs4
from bs4 import BeautifulSoup
import requests
import time


class PyPoem:

    def __init__(self):
        self.poem = ""
        self.poet = ""
        self.title = ""

        name = input('Poem name?\n')

        print('Connecting to server...')
        self.getPoem(name)
        beg = '*' * 50 + '\n'
        end = '\n'+'*'*50

        with open('hello.poem', 'w') as file:
            #file.write(self.title)
            file.write(beg+self.poem+end)
        print('Successful. Extracted to file hello.poem')

    def getPoem(self, poem_query):
        poem_url = self.getPoemURL(poem_query)
        poem_html_page = self.fetchPage(poem_url)
        poem_soup = BeautifulSoup(poem_html_page.content, 'html.parser')

        self.title = self.getPoemTitle(poem_soup)
        self.poet = self.getPoetName(poem_soup)
        self.poem = self.getPoemContents(poem_soup)

        return self.poem

    def getPoemTitle(self, poem_soup):
        pass

    def getPoemContents(self, poem_page):
        poem_div = poem_page.find('div', {'class': ['o-poem', 'isActive']})
        poem_contents = self.formatPoem(poem_div)

        return poem_contents

    def formatPoem(self, poem_div):
        poem_contents = ""
        for child in poem_div.children:
            if child.name == 'div':
                for string in child.stripped_strings:
                    poem_contents += string
                poem_contents += "\n"
        print(poem_contents)

        return poem_contents

    def getPoetName(self, page_content):
        poet_name_div = page_content.find(
            'div', {'class': ['c-feature-sub', 'c-feature-sub_vast']})

        poet_name = poet_name_div.div.span.text.replace('By', '').strip()
        return poet_name

    def getPoemURL(self, poem_title):
        url = self.fetchPage(query=poem_title)
        soup = BeautifulSoup(url.content, 'html.parser')
        poem_url = soup.find('h2', {'class': ['c-hdgSans', 'c-hdgSans_2']})

        return poem_url.a['href']

    def fetchPage(self, url="https://www.poetryfoundation.org/", query=None):
        if (query == None):
            # print("Fetching Page ", url)
            return requests.get(url)

        query = query.replace(' ', '+')
        url = url+"search?query=%s" % query
        # print("Fetching Page ", url)
        return requests.get(url)


load = PyPoem()
