from os import path, listdir
import json


data_dir = path.join('sherlock' ,'processed')

footer = '''     ----------
     This text is provided to you "as-is" without any warranty. No
     warranties of any kind, expressed or implied, are made to you as to
     the text or any medium it may be on, including but not limited to
     warranties of merchantablity or fitness for a particular purpose.

     This text was formatted from various free ASCII and HTML variants.
     See http://sherlock-holm.es for an electronic form of this text and
     additional information about it.

     This text comes from the collection's version 3.1.'''

for filename in listdir(data_dir):

  story_path = path.join(data_dir, filename)

  text = open(story_path, 'r', encoding='utf8').read()
  text = text.replace(footer, '').strip()
  
  open(story_path, 'w', encoding='utf8').write(text)
