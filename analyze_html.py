from bs4 import BeautifulSoup
import re
import os
import json

def analyze():
    with open(r'c:\MAINDOMAIN\Portfolio sites\p5\index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # Assets
    scripts = [s['src'] for s in soup.find_all('script') if s.get('src')]
    links = [l['href'] for l in soup.find_all('link') if l.get('href')]
    images = [i['src'] for i in soup.find_all('img') if i.get('src')] + \
             [l['href'] for l in soup.find_all('link', rel='icon')]

    # Extract text content for templates
    # This is heuristic. We want meaningful text.
    # We'll traverse and find text nodes > 3 chars?
    texts = []
    for element in soup.find_all(['h1', 'h2', 'h3', 'p', 'span', 'a']):
        text = element.get_text(strip=True)
        if text and len(text) > 2:
            texts.append(text)

    # Output
    result = {
        'scripts': scripts,
        'links': links,
        'images': images,
        'texts': texts[:20]  # Just a sample for now to see
    }
    
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    try:
        analyze()
    except Exception as e:
        print(e)
