from bs4 import BeautifulSoup
import os

HTML_FILE = r"c:\MAINDOMAIN\Portfolio sites\p5\index.html"
OUTPUT_CURRENT = r"c:\MAINDOMAIN\Portfolio sites\p5\currentprofiledata.txt"
OUTPUT_TEMPLATE = r"c:\MAINDOMAIN\Portfolio sites\p5\profiledat.txt"

def main():
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # removals
    for tag in soup(['script', 'style', 'noscript', 'svg']):
        tag.decompose()
        
    data_map = []
    
    # Just get everything that looks like content
    # We will try to provide context by finding the nearest parent with a class
    
    for element in soup.find_all(text=True):
        text = element.strip()
        if len(text) > 1 and "{" not in text and "}" not in text: # Avoid JS crumbs
            parent = element.parent
            # Find a parent with a class to use as a section label
            label = "Content"
            curr = parent
            while curr and curr.name != 'html':
                if curr.get('class'):
                    label = ".".join(curr['class'])
                    break
                curr = curr.parent
            
            tag = parent.name
            key = f"[{label}] {tag}"
            data_map.append((key, text))

    # Write
    with open(OUTPUT_CURRENT, 'w', encoding='utf-8') as f:
        f.write("# CURRENT DATA\n")
        f.write("# Reference of all text found in the HTML.\n\n")
        for key, val in data_map:
            f.write(f"{key}: {val}\n")

    with open(OUTPUT_TEMPLATE, 'w', encoding='utf-8') as f:
        f.write("# TEMPLATE\n")
        f.write("# Replace values in quotes.\n\n")
        
        counts = {}
        for key, val in data_map:
            # Create a unique key for the property file format
            # e.g. c-landing_h1
            
            # Clean section name
            clean_section = key.split(']')[0].replace('[','').replace(' ', '_').replace('.', '_')
            tag = key.split(']')[1].strip()
            
            base_key = f"{clean_section}_{tag}"
            if base_key not in counts: counts[base_key] = 0
            counts[base_key] += 1
            
            final_key = f"{base_key}_{counts[base_key]}"
            
            f.write(f"{final_key} = \"{val}\"\n")

    print("Scanned all content.")

if __name__ == '__main__':
    main()
