import json
from bs4 import BeautifulSoup
from slugify import slugify
from os import path, listdir
from tqdm import tqdm
import parser
import gutenberg
import sys

index_path = sys.argv[1] # 'fixed.json'
txt_dir = sys.argv[2] # 'data/raw'
story_dir = sys.argv[3] # 'data/processed'

books = {}
for (continent, country, book_title, url), titles in json.load(open(index_path, encoding='utf8')):
  key = slugify(book_title)
  books[key] = (continent, country, titles)

for filename in tqdm(listdir(txt_dir)):

  key, ext = path.splitext(filename)
  continent, country, titles = books[key]
  text = open(path.join(txt_dir, filename), 'r', encoding='utf8').read()
  
  if ext == '.html':
    soup = BeautifulSoup(text, 'html.parser')

    if titles:
      rows = parser.parse_toc2(text, titles)
    else:
      rows = parser.parse_toc1(text)

    for s, e in zip(rows, rows[1:]):
      title, author, start_href = s
      _, _, end_href = e
      
      start, end = soup.find(id=start_href[1:]), soup.find(id=end_href[1:])
      if start is None:
        start, end = soup.find('a',{'name':start_href[1:]}), soup.find('a',{'name':end_href[1:]})

      if start == end:
        end = start.find_next('a')

      lines = parser.lines_between(start, end)
      story = gutenberg.strip_headers(''.join(lines)).strip()

      open(path.join(story_dir, '%s.txt' % slugify(title)), 'w', encoding='utf8').write(story)
  
  elif ext == '.txt':
    # txt

    stories = parser.parse_text(text, titles)
    if not stories:
      print (filename)
    if len(stories) != len(titles):
      print (filename,  set([title for title, author in titles]) - set([ title for title, author in stories.keys()]) )
    
    for (title, author), lines in stories.items():
      story = '\n'.join(lines).strip()
      if not story:
        print (title, filename)
      open(path.join(story_dir, '%s.txt' % slugify(title)), 'w', encoding='utf8').write(story)
