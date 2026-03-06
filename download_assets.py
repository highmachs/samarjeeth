import os
import re
import json
import urllib.request
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import ssl

# Ignore SSL errors for scraping
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

BASE_URL = "https://kortyeo.madebynull.com/profile"
LOCAL_DIR = r"c:\MAINDOMAIN\Portfolio sites\p5"
HTML_FILE = os.path.join(LOCAL_DIR, "index.html")

def download_file(url, local_path):
    try:
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        if not os.path.exists(local_path):
            print(f"Downloading {url} to {local_path}")
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, context=ctx) as response, open(local_path, 'wb') as out_file:
                out_file.write(response.read())
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

def main():
    if not os.path.exists(HTML_FILE):
        print(f"File not found: {HTML_FILE}")
        return

    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # 1. Scripts and Links (CSS/JSON/JS in _nuxt)
    # Process <script src="...">
    for script in soup.find_all('script'):
        src = script.get('src')
        if src and src.startswith('/_nuxt/'):
            full_url = urljoin(BASE_URL, src)
            local_rel_path = src.lstrip('/') # _nuxt/...
            local_abs_path = os.path.join(LOCAL_DIR, local_rel_path.replace('/', os.sep))
            
            download_file(full_url, local_abs_path)
            script['src'] = f"./{local_rel_path}"

    # Process <link href="...">
    for link in soup.find_all('link'):
        href = link.get('href')
        if href and (href.startswith('/_nuxt/') or href.startswith('/favicon')):
            full_url = urljoin(BASE_URL, href)
            local_rel_path = href.lstrip('/')
            local_abs_path = os.path.join(LOCAL_DIR, local_rel_path.replace('/', os.sep))
            
            download_file(full_url, local_abs_path)
            link['href'] = f"./{local_rel_path}"

    # 2. Images in <img> tags
    image_map = {} # url -> local_filename
    img_counter = 1

    for img in soup.find_all('img'):
        src = img.get('src')
        if src:
            if src.startswith('http'):
                ext = os.path.splitext(urlparse(src).path)[1]
                if not ext: ext = '.jpg'
                local_name = f"image_{img_counter}{ext}"
                local_rel = f"images/{local_name}"
                local_abs = os.path.join(LOCAL_DIR, "images", local_name)
                
                download_file(src, local_abs)
                img['src'] = f"./{local_rel}"
                image_map[src] = local_rel
                img_counter += 1
            elif src.startswith('/'):
                full_url = urljoin(BASE_URL, src)
                local_rel_path = src.lstrip('/')
                local_abs_path = os.path.join(LOCAL_DIR, local_rel_path.replace('/', os.sep))
                download_file(full_url, local_abs_path)
                img['src'] = f"./{local_rel_path}"

    # 3. Images in inline CSS
    style_tags = soup.find_all('style')
    for style in style_tags:
        if not style.string: continue
        css = style.string
        
        urls = re.findall(r'url\((.*?)\)', css)
        new_css = css
        for url in urls:
            url_clean = url.strip('\'"')
            if url_clean.startswith('data:'): continue
            
            if url_clean.startswith('http'):
                if url_clean in image_map:
                    new_rel = image_map[url_clean]
                    new_css = new_css.replace(url, f"url(./{new_rel})")
                else:
                    ext = os.path.splitext(urlparse(url_clean).path)[1]
                    if not ext: ext = '.jpg'
                    local_name = f"bg_image_{img_counter}{ext}"
                    local_rel = f"images/{local_name}"
                    local_abs = os.path.join(LOCAL_DIR, "images", local_name)
                    
                    download_file(url_clean, local_abs)
                    new_css = new_css.replace(url, f"url(./{local_rel})")
                    image_map[url_clean] = local_rel
                    img_counter += 1
            elif url_clean.startswith('/'):
               full_url = urljoin(BASE_URL, url_clean)
               local_rel_path = url_clean.lstrip('/')
               local_abs_path = os.path.join(LOCAL_DIR, local_rel_path.replace('/', os.sep))
               download_file(full_url, local_abs_path)
               new_css = new_css.replace(url, f"url(./{local_rel_path})")
               
        style.string.replace_with(new_css)

    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    print("HTML and assets saved.")

    # 4. Generate Text Templates
    texts = []
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc:
        texts.append(f"Meta Description: {meta_desc['content']}")
        
    title = soup.title.string if soup.title else ""
    texts.append(f"Page Title: {title}")

    for element in soup.body.find_all(text=True):
        t = element.strip()
        if len(t) > 2 and element.parent.name not in ['script', 'style']:
            texts.append(f"[{element.parent.name}]: {t}")

    with open(os.path.join(LOCAL_DIR, "currentprofiledata.txt"), 'w', encoding='utf-8') as f:
        f.write("\n".join(texts))

    template_content = """[Profile Information]
Name = "Korty Eniola"
Title = "Filmmaker & YouTuber"
Bio = "Eniola Korty Olanrewaju is a Lagos based freelance filmmaker & youtuber..."

[Contact]
Email = "example@email.com"
Social_Instagram = "@kortyeo"
Social_Twitter = "@korty_eo"
Social_YouTube = "Korty EO"

[Sections]
Intro_Headline = "I AM A FILMMAKER"
Work_Heading = "SELECTED WORK"
Footer_Text = "Thanks for visiting"

[Images]
# Instructions:
# 1. Go to the 'p5/images' folder.
# 2. You will see images like 'image_1.jpg', 'bg_image_2.jpg', etc.
# 3. To replace an image, delete the existing one and put your new image there with the EXACT SAME NAME.
# 4. Refresh the page to see changes.
"""
    with open(os.path.join(LOCAL_DIR, "profiledat.txt"), 'w', encoding='utf-8') as f:
        f.write(template_content)

    print("Templates created.")

if __name__ == '__main__':
    main()
