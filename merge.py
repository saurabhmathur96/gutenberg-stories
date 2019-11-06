import sys, csv, json
from tqdm import tqdm

outfile = sys.argv[1]
stories = []
for filename in sys.argv[2:]:
  for row in tqdm(csv.reader(open(filename, encoding='utf8'))):
    stories.append({
      'title': row[0],
      'author': row[1],
      'area': row[2],
      'subarea': row[3],
      'url': row[4]
    })

json.dump(stories, open(outfile, 'w', encoding='utf8'))