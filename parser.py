import gutenberg
import bs4

def lines_between(cur, end):
  while cur and cur != end:
    if isinstance(cur, bs4.NavigableString) and cur.parent.name != 'a':
      text = str(cur)
      if cur.parent.name in ('i', 'b', 'strong'):
        text = text.strip()

      if len(text):
        yield text
    cur = cur.next_element
    
    
def parse_toc(text):
  soup = BeautifulSoup(text, 'html.parser')
  table = soup.find('table')
  toc = []
  for tr in table.find_all('tr'):
    cells = [td for td in tr.find_all('td')]
    if len(cells) < 3: continue
    toc.append((cells[0].text, cells[1].text, int(cells[2].text), cells[2].find('a').attrs['href'] ))
  return toc


def parse_text(text, titles):
  lines = gutenberg.strip_headers(text).strip().splitlines()
  stories = {}
  key = None
  authors = [author for _, author in titles]
  
  for line in lines:
    if not line or line in authors:
      continue
    for title, author in titles:
      cond1 = line.replace('_', ' ').strip() == title
      cond2 = line.replace('_', ' ').strip().startswith(title.upper())
      if cond1 or cond2:
        key = (title, author)
        stories[key] = []
        line = ''
        break
    if key:
      stories[key].append(line)

  return stories
