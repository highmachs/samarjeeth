import re
import os
import shutil

NUXT_DIR = r"c:\MAINDOMAIN\Portfolio sites\p5\_nuxt"
TEMPLATE_FILE = r"c:\MAINDOMAIN\Portfolio sites\p5\profiledat.txt"

def main():
    if not os.path.exists(TEMPLATE_FILE):
        print(f"Error: {TEMPLATE_FILE} not found.")
        return

    # 1. Parse Template
    file_changes = {}
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#") and not line.startswith("["):
                parts = line.split("=", 1)
                full_key = parts[0].strip()
                val_raw = parts[1].strip()
                
                if "__Item_" in full_key:
                    file_key_part, rest = full_key.split("__Item_", 1)
                    
                    if file_key_part.endswith("_js"):
                        filename = file_key_part[:-3] + ".js"
                    else:
                        continue
                    
                    idx_match = re.match(r'^(\d+)', rest)
                    if idx_match:
                        index = int(idx_match.group(1)) - 1
                        
                        # Handle potential quoted value properly
                        # If first and last chars are quotes, strip them
                        if len(val_raw) >= 2 and val_raw[0] in ['"', "'"] and val_raw[-1] == val_raw[0]:
                            val = val_raw[1:-1]
                            # Unescape \" to " if strictly needed? 
                            # The file has escaped quotes: "foo \"bar\""
                            val = val.replace('\\"', '"') 
                            
                            if filename not in file_changes:
                                file_changes[filename] = {}
                            file_changes[filename][index] = val

    # 2. Patch
    for filename, changes in file_changes.items():
        js_path = os.path.join(NUXT_DIR, filename)
        if not os.path.exists(js_path):
            continue
            
        print(f"Patching {filename}...")
        
        # Backup
        bak_path = js_path + ".bak"
        if not os.path.exists(bak_path):
            shutil.copy(js_path, bak_path)
            
        with open(js_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # EXACT REGEX from extract_js_content.py
        matches = list(re.finditer(r'_v\((["\'])(.*?)\1\)', content))
        
        valid_matches = []
        for m in matches:
            quote = m.group(1)
            raw_text = m.group(2)
            
            # EXACT FILTERING
            text = raw_text.replace('\\n', ' ').replace('\\t', ' ')
            text = " ".join(text.split())
            
            if len(text) > 0 and text not in [" ", " • ", "(", ")", "+", "|"]:
                valid_matches.append(m)
                
        sorted_indices = sorted(changes.keys(), reverse=True)
        
        new_content = content
        for idx in sorted_indices:
            if idx < len(valid_matches):
                match = valid_matches[idx]
                new_text = changes[idx]
                
                # Check original quote style to preserve valid JS? 
                # Actually we can just force double quotes and escape content.
                # _v("new_text")
                
                safe_new_text = new_text.replace('"', '\\"').replace('\n', '\\n')
                replacement = f'_v("{safe_new_text}")'
                
                start, end = match.span()
                new_content = new_content[:start] + replacement + new_content[end:]
                # print(f"  Applied Item {idx+1} to {filename}")
            else:
                 print(f"  Error: Index {idx+1} out of bounds for {filename}")

        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
    print("All files patched. Refresh localhost.")

if __name__ == '__main__':
    main()
