#!/usr/bin/env python3
import sys
from os import path
import requests, json
from slugify import slugify

filename = sys.argv[1] 
data_dir = sys.argv[2] 

stories = json.load(open(filename, 'r', encoding='utf8'))

for title, author, url in stories:
  
  text = requests.get(url).content.decode('utf8')
  write_path = path.join(data_dir, '%s.txt' % slugify(title + ' by ' + author))
  open(write_path, 'w', encoding='utf8').write(text)
