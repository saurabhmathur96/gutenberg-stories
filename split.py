#!/usr/bin/env python3
import json
from bs4 import BeautifulSoup
from slugify import slugify
from os import path, listdir
from tqdm import tqdm
import parser
import gutenberg
import sys
import csv

index_path = sys.argv[1] # 'fixed.json'
txt_dir = sys.argv[2] # 'data/raw'
story_dir = sys.argv[3] # 'data/processed'


parse_toc = parser.parse_toc3
'''
if len(sys.argv) == 4:
  parse_toc = parser.parse_toc2
else:
  parse_toc = parser.parse_toc3
'''

books = {}
for (continent, country, book_title, url), titles in json.load(open(index_path, encoding='utf8')):
  key = slugify(book_title)
  books[key] = (continent, country, titles)


story_index = open('%s.csv' % index_path, 'w', encoding='utf8')
out = csv.writer(story_index)

filenames = listdir(txt_dir)
for index, filename in tqdm(enumerate(filenames), total=len(filenames)):

  key, ext = path.splitext(filename)
  continent, country, titles = books[key]
  text = open(path.join(txt_dir, filename), 'r', encoding='utf8').read()
  
  if ext == '.html':
    soup = BeautifulSoup(text, 'html.parser')

    if titles:
      rows = parse_toc(text, titles)
    else:
      rows = parser.parse_toc1(text)


    ends = []
    for row in rows:
      try:
        title, author, href = row
        end = soup.find(id=href[1:])
        if end is None:
          end = soup.find('a',{'name':href[1:]})
        ends.append(end)

      except ValueError:
        print (filename)
        pass

    for i, start in enumerate(rows):
      try:
        title, author, start_href = start
      except ValueError:
        print (filename)
        break
      
      start = soup.find(id=start_href[1:])
      if start is None:
        start = soup.find('a',{'name':start_href[1:]})

      lines = parser.lines_between(start, [e for e in ends if e != start])
      story = gutenberg.strip_headers(''.join(lines)).strip()
      write_path = path.join(story_dir, '%s-%04d-%04d.txt' % (slugify(title + ' by ' + author), index, i))
      out.writerow([title, author, continent, country, write_path])
      open(write_path, 'w', encoding='utf8').write(story)
  
  elif ext == '.txt':
    # txt

    stories = parser.parse_text(text, titles)
    if not stories:
      print (filename)
    if len(stories) != len(titles):
      print (filename,  set([title for title, author in titles]) - set([ title for title, author in stories.keys()]) )
    
    i = 0
    for (title, author), lines in stories.items():
      i += 1
      story = '\n'.join(lines).strip()
      if not story:
        print (title, filename)
      write_path = path.join(story_dir, '%s-%04d-%04d.txt' % (slugify(title + ' by ' + author), index, i))
      out.writerow([title, author, continent, country, write_path])
      open(write_path, 'w', encoding='utf8').write(story)
