#!/usr/bin/env python3
import csv
import json
from os import path
from slugify import slugify

base = 'manual/processed'

out = csv.writer(open('sherlock.json.csv', 'w'))

for i, (title, author, _) in enumerate(json.load(open('sherlock.json', 'r'))):
  story_path = path.join(base, '%s-0000-%04d.txt' % (slugify(title + ' by ' + author), i))
  out.writerow([title, author, 'Europe', 'United Kingdom', story_path])


