
import re

file_path = r'c:\MAINDOMAIN\Portfolio sites\p5\_nuxt\30d1d07.js'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find all cloudinary URLs
urls = re.findall(r'https://res\.cloudinary\.com/[^"\']+', content)
unique_urls = sorted(list(set(urls)))

print(f"Found {len(unique_urls)} unique URLs.")
for url in unique_urls:
    print(url)
