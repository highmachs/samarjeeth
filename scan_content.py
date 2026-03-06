from bs4 import BeautifulSoup
import os
import re

HTML_FILE = r"c:\MAINDOMAIN\Portfolio sites\p5\index.html"
OUTPUT_CURRENT = r"c:\MAINDOMAIN\Portfolio sites\p5\currentprofiledata.txt"
OUTPUT_TEMPLATE = r"c:\MAINDOMAIN\Portfolio sites\p5\profiledat.txt"

def get_identifier(element):
    """Generates a readable identifier for an element based on class or ID."""
    if element.get('id'):
        return element['id']
    if element.get('class'):
        # Filter out utility classes if possible, but taking the first meaningful one helps
        # returning the most specific class often helps context
        return ".".join(element['class'])
    return element.name

def main():
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # removals
    for tag in soup(['script', 'style', 'noscript', 'svg']):
        tag.decompose()

    data_map = [] # List of (Section, Text) tuples
    
    # We will look for specific major containers to group things
    # Based on previous CSS analysis: .c-landing, .c-profile, .c-footer, .c-archive__main
    
    sections = {
        "Preloader": soup.select_one('.c-preloader'),
        "Landing (Home)": soup.select_one('.c-landing'),
        "Profile (Main)": soup.select_one('.c-profile'),
        "Footer": soup.select_one('.c-footer'),
        "Archive": soup.select_one('.c-archive__main'),
        "Modal/Menu": soup.select_one('.c-modal')
    }

    # Helper to traverse and extract text
    def extract_text_from_section(section_name, root_element):
        if not root_element: return
        
        # recursive text extraction with context
        # We want deep strings but we don't want to break simple sentences split by spans
        # Actually simple .get_text(separator=' ', strip=True) on block elements might be better
        # Let's iterate over block children
        
        # Strategy: Find all child elements that contain text directly or are leaf nodes
        for elem in root_element.find_all(text=True):
            text = elem.strip()
            if len(text) > 1: # Ignore single chars like punctuation often active in spans
                # Parent context
                parent = elem.parent
                
                # Check if this text is already captured (BS4 find_all(text=True) gives all nodes)
                # We'll just append it.
                
                # Construct a key: Section_Tag_Class
                tag = parent.name
                cls = "_".join(parent.get("class", []))
                if not cls: cls = "text"
                
                key = f"{section_name} | {tag}.{cls}"
                value = text
                
                data_map.append((key, value))

    # 1. Process defined sections
    for name, element in sections.items():
        if element:
            extract_text_from_section(name, element)
            # Remove from soup to avoid double counting if we switched to a global scan later
            # element.decompose() # actually let's not decompose, just trust the selector
    
    # 2. Write Current Data
    with open(OUTPUT_CURRENT, 'w', encoding='utf-8') as f:
        f.write("# CURRENT WEBSITE DATA CONTENT\n")
        f.write("# This file lists the actual text found on the site for reference.\n\n")
        
        last_section = ""
        for key, val in data_map:
            section = key.split('|')[0].strip()
            if section != last_section:
                f.write(f"\n--- {section} ---\n")
                last_section = section
            
            # Clean key for readability
            clean_key = key.split('|')[1].strip()
            f.write(f"{clean_key} = {val}\n")

    # 3. Write Template Data
    with open(OUTPUT_TEMPLATE, 'w', encoding='utf-8') as f:
        f.write("# EDITABLE PROFILE DATA TEMPLATE\n")
        f.write("# Replace the text inside the quotes \" \" to change the website content.\n")
        f.write("# NOTE: This file is a template. You must manually apply these changes to index.html.\n\n")
        
        last_section = ""
        seen_keys = set()
        
        for key, val in data_map:
            section = key.split('|')[0].strip()
            item_key = key.split('|')[1].strip().replace(' ', '_').replace('.', '_')
            
            if section != last_section:
                f.write(f"\n[{section}]\n")
                last_section = section
            
            # Deduplicate generic keys slightly by appending content snippet if needed, 
            # but simple list is better for user blindly filling
            # Let's just output nice key-value pairs
            
            # Heuristic to name keys better?
            # e.g. h1.details-title -> Heading
            
            full_key_str = f"{item_key}"
            # Ensure unique key if multiple items have same class in same section
            count = 1
            base_key = full_key_str
            while f"{section}_{full_key_str}" in seen_keys:
                count += 1
                full_key_str = f"{base_key}_{count}"
            seen_keys.add(f"{section}_{full_key_str}")
            
            f.write(f"{full_key_str} = \"{val}\"\n")

    print("Scanned and created data files.")

if __name__ == '__main__':
    main()
