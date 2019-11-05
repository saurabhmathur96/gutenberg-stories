import gutenberg
import bs4
from bs4 import BeautifulSoup
from operator import itemgetter

def lines_between(cur, end):
  while cur and cur not in end:
    if isinstance(cur, bs4.NavigableString) and cur.parent.name != 'a':
      text = str(cur)
      if cur.parent.name in ('i', 'b', 'strong'):
        text = text.strip()

      if len(text):
        yield text
    cur = cur.next_element
    
    
def parse_toc1(text):
  soup = BeautifulSoup(text, 'html.parser')
  table = soup.find('table')
  toc = []
  for tr in table.find_all('tr'):
    cells = [td for td in tr.find_all('td')]
    if len(cells) < 3: continue
    toc.append((cells[0].text, cells[1].text, int(cells[2].text), cells[2].find('a').attrs['href'] ))
  toc = [(text, author, href) for text, author, _, href in sorted(toc, key=itemgetter(2))]
  return toc

def parse_toc2(text, titles):
  toc = []
  soup = BeautifulSoup(text, 'html.parser')
  for a in soup.find_all('a', href=True):
    for text, author in titles:
      if a.text.strip().lower().startswith(text.lower()):
        toc.append((text, author, a.attrs['href']))
        break
  return toc

def parse_toc3(text, titles):
  toc = []
  soup = BeautifulSoup(text, 'html.parser')
  for text, author in titles:
    for a in soup.find_all('a', href=True):
      if a.text.strip().lower().startswith(text.lower()):
        toc.append((text, author, a.attrs['href']))
        break
  return toc


def parse_text(text, titles):
  lines = gutenberg.strip_headers(text).strip().splitlines()
  i = -1
  for index, line in enumerate(lines):
    if line.strip() == 'INDEX':
      i = index
  lines = lines[:i]
  stories = {}
  key = None
  authors = [author for _, author in titles]
  
  for line in lines:
    if not line or line in authors:
      continue
    for title, author in titles:
      cond1 = line.replace('_', ' ').replace('[1]', '').rstrip('*').strip() == title
      cond2 = line.replace('_', ' ').strip().startswith(title.upper())
      if cond1 or cond2:
        key = (title, author)
        stories[key] = []
        line = ''
        break
    if key:
      stories[key].append(line)

  return stories
