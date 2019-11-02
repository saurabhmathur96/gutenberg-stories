#!/usr/bin/env python3
import csv
import json
from os import path
from slugify import slugify

base = 'manual/processed'

out = csv.writer(open('story-index.csv', 'a'))

for title, author, _ in json.load(open('sherlock.json', 'r')):
  story_path = path.join(base, '%s.txt' % slugify(title + ' by ' + author))
  out.writerow([title, author, 'Europe', 'United Kingdom', story_path])


for (continent, country, book_title, url), titles in json.load(open('manual.json', 'r')):
  for title, author in titles:
     story_path = path.join(base, '%s.txt' % slugify(title + ' by ' + author))
     out.writerow([title, author, continent, country, story_path])