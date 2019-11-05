#!/usr/bin/env python3
import sys
from os import path
import requests, json
from slugify import slugify

filename = sys.argv[1] 
data_dir = sys.argv[2] 

stories = json.load(open(filename, 'r', encoding='utf8'))

for i, (title, author, url) in enumerate(stories):
  
  text = requests.get(url).content.decode('utf8')
  write_path = path.join(data_dir, '%s-0000-%04d.txt' % (slugify(title + ' by ' + author), i))
  open(write_path, 'w', encoding='utf8').write(text)
