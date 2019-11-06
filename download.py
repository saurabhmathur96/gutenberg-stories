#!/usr/bin/env python3
import sys
from os import path
import requests, json
from bs4 import BeautifulSoup
from slugify import slugify
from tqdm import tqdm

filename = sys.argv[1] 
data_dir = sys.argv[2] 

books = json.load(open(filename, 'r', encoding='utf8'))
for (continent, country, book_title, url), titles in tqdm(books):
  
  text = requests.get(url).content.decode('utf8')
  
  soup = BeautifulSoup(text, 'html.parser')
  a = soup.find(lambda tag: tag.name=="a" and "html" in tag.text.lower())
  if 'generated' not in a.text.lower():  

    text = requests.get('http://gutenberg.org'+a.attrs['href']).content.decode('utf8', 'ignore')
    open(path.join(data_dir, '%s.html' % slugify(book_title)), 'w', encoding='utf8').write(text)

  else:

    a = soup.find(lambda tag: tag.name=="a" and "text" in tag.text.lower())
    text = requests.get('http://gutenberg.org'+a.attrs['href']).content.decode('utf8', 'ignore')


    
    open(path.join(data_dir, '%s.txt' % slugify(book_title)), 'w', encoding='utf8').write(text)

