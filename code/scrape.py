import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

pages = [
    'fest3.html',
    '4fest.html',
    '6fest.html',
    '7fest.html',
    '8fest.html',
    '9fest.html',
    '10fest.html',
]

for week in pages:
    out = os.path.join('out/', week)
    url = urljoin('http://www.ccs.neu.edu/home/matthias/4500-f18/', week)
    page = requests.get(url).text
    soup = BeautifulSoup(page)

    grade_table = soup.find(class_='maincolumn').table

    rows = grade_table.findAll('tr')[1:]

    print(week)
    for row in rows:
        group = row.findAll('td')[0].p.text
        links = [a.get('href') for a in row.findAll('a')]

        dl_dir = os.path.join(out, group)
        os.makedirs(dl_dir, exist_ok=True)

        print('\t' + group, end=' ')
        for link in links:
            print(link, end=' ')
            content = requests.get(urljoin(url, link)).text
            open(os.path.join(dl_dir, link), 'w').write(content)
        print()
