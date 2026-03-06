
import os
import shutil
import re

# Paths
source_dir = r'c:\MAINDOMAIN\Portfolio sites\LIFE UPGRADE MOVITATIONS'
dest_dir = r'c:\MAINDOMAIN\Portfolio sites\p5\new_images'

files_to_patch = [
    r'c:\MAINDOMAIN\Portfolio sites\p5\index.html',
    r'c:\MAINDOMAIN\Portfolio sites\p5\profile\index.html',
    r'c:\MAINDOMAIN\Portfolio sites\p5\archive\index.html',
    r'c:\MAINDOMAIN\Portfolio sites\p5\_nuxt\3ac11fa.js',
    r'c:\MAINDOMAIN\Portfolio sites\p5\_nuxt\763368b.js',
    r'c:\MAINDOMAIN\Portfolio sites\p5\_nuxt\842b1ec.js',
    r'c:\MAINDOMAIN\Portfolio sites\p5\_nuxt\9331327.js'
]

# 1. Collect all unique URLs from all files
all_urls = set()
for file_path in files_to_patch:
    if not os.path.exists(file_path):
        print(f"Skipping missing file: {file_path}")
        continue
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    found = re.findall(r'https://res\.cloudinary\.com/[^"\')\s]+', content)
    # Clean them up just in case (e.g. trailing characters that regex might catch if strictly not " or ')
    # The regex [^"\')\s]+ stops at quote, paren, or whitespace. Should be safe for JS and HTML.
    for url in found:
        all_urls.add(url)

unique_urls = sorted(list(all_urls))
print(f"Found {len(unique_urls)} ADDITIONAL unique URLs to replace across {len(files_to_patch)} files.")

if not unique_urls:
    print("No new URLs found.")
    exit()

# 2. Prepare source images
source_images = [f for f in os.listdir(source_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
source_images.sort()

# 3. Create map and copy
# Start from 51 as per previous run
img_counter = 51
replacement_map = {}

os.makedirs(dest_dir, exist_ok=True)

for i, url in enumerate(unique_urls):
    src_img_name = source_images[i % len(source_images)]
    src_img_path = os.path.join(source_dir, src_img_name)
    
    new_img_name = f'img{img_counter}.jpg'
    new_img_path = os.path.join(dest_dir, new_img_name)
    
    shutil.copy2(src_img_path, new_img_path)
    replacement_map[url] = f'/new_images/{new_img_name}'
    img_counter += 1

# 4. Apply replacements
for file_path in files_to_patch:
    if not os.path.exists(file_path):
        continue
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    count_in_file = 0
    for url, new_path in replacement_map.items():
        if url in new_content:
            new_content = new_content.replace(url, new_path)
            count_in_file += 1
            
    if count_in_file > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Patched {file_path} ({count_in_file} replacements)")
    else:
        print(f"No changes in {file_path}")

print("Global update complete.")
