#!/usr/bin/env python3
import requests, json
from bs4 import BeautifulSoup

res = requests.get('https://www.gutenberg.org/wiki/Short_Stories_(Bookshelf)')
soup = BeautifulSoup(res.text, 'html.parser')
from urllib.parse import urljoin

books = []
h3, h4 = '', ''
for tag in soup.find(class_='mw-parser-output').children:
  if not tag.name: continue


  if tag.name == 'h3':
    h3 = str(tag.text)
  
  elif tag.name == 'h4':
    h4 = str(tag.text)

  
  if tag.name == 'ul':
    li = tag.find('li')
    a = li.find('a')
    title = a.text
    url = 'http:' + a.attrs['href']
    heading = (h3, h4, title, url)
    
    links = []
    for item in li.find_all('li'):
      parts = item.text.split(' by ')
      title = ''.join(parts[:-1])
      author = parts[-1]
      links.append((title.strip(), author.strip()))
    
    books.append((heading, links))

print (json.dumps(books, indent=2))
