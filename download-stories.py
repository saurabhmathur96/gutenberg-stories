#!/usr/bin/env python3
import sys
from os import path
import requests, json
from slugify import slugify
import csv
from tqdm import tqdm
import gutenberg

filename = sys.argv[1] 
data_dir = sys.argv[2] 

footer = '''     ----------
     This text is provided to you "as-is" without any warranty. No
     warranties of any kind, expressed or implied, are made to you as to
     the text or any medium it may be on, including but not limited to
     warranties of merchantablity or fitness for a particular purpose.

     This text was formatted from various free ASCII and HTML variants.
     See http://sherlock-holm.es for an electronic form of this text and
     additional information about it.

     This text comes from the collection's version 3.1.'''


stories = json.load(open(filename, 'r', encoding='utf8'))
out = csv.writer(open('%s.csv' % filename, 'w'))

for i, (continent, country, title, author, url) in tqdm(enumerate(stories), total=len(stories)):
  
  text = requests.get(url).content.decode('utf8')
  text = text.replace(footer, '').strip()
  text =  gutenberg.strip_headers(text).strip()

  write_path = path.join(data_dir, '%s-0000-%04d.txt' % (slugify(title + ' by ' + author), i))
  
  out.writerow([title, author, continent, country, write_path])
  open(write_path, 'w', encoding='utf8').write(text)
