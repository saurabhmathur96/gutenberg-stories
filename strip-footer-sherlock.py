from os import path
import json

from slugify import slugify

stories = json.load(open('sherlock.json', 'r', encoding='utf8'))
data_dir = path.join('manual' ,'processed')

footer = '''     ----------
     This text is provided to you "as-is" without any warranty. No
     warranties of any kind, expressed or implied, are made to you as to
     the text or any medium it may be on, including but not limited to
     warranties of merchantablity or fitness for a particular purpose.

     This text was formatted from various free ASCII and HTML variants.
     See http://sherlock-holm.es for an electronic form of this text and
     additional information about it.

     This text comes from the collection's version 3.1.'''

for title, author, url in stories:

  story_path = path.join(data_dir, '%s.txt' % slugify(title + ' by ' + author))

  text = open(story_path, 'r', encoding='utf8').read()
  text = text.replace(footer, '').strip()
  
  open(story_path, 'w', encoding='utf8').write(text)
