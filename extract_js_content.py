import re
import os
import glob

NUXT_DIR = r"c:\MAINDOMAIN\Portfolio sites\p5\_nuxt"
OUTPUT_CURRENT = r"c:\MAINDOMAIN\Portfolio sites\p5\currentprofiledata.txt"
OUTPUT_TEMPLATE = r"c:\MAINDOMAIN\Portfolio sites\p5\profiledat.txt"

def main():
    if not os.path.exists(NUXT_DIR):
        print(f"Error: {NUXT_DIR} not found.")
        return

    js_files = glob.glob(os.path.join(NUXT_DIR, "*.js"))
    all_extracted = []

    for js_file in js_files:
        filename = os.path.basename(js_file)
        
        with open(js_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        # Match _v("...") or _v('...')
        # We capture the quote type to handle it correctly
        matches = re.finditer(r'_v\((["\'])(.*?)\1\)', content)
        
        file_extracted = []
        for m in matches:
            quote = m.group(1)
            raw_text = m.group(2)
            
            # Unescape logic
            # If it's single quoted in JS, unescape singles. If double, unescape doubles.
            # Simple approach: standard unescape
            text = raw_text.replace('\\n', ' ').replace('\\t', ' ')
            text = " ".join(text.split())
            
            # Debug specific missing text
            if "jag_ubani" in raw_text:
                print(f"Found jag_ubani in {filename} with raw: {raw_text}")
            
            if len(text) > 0 and text not in [" ", " • ", "(", ")", "+", "|"]:
                 file_extracted.append(text)
        
        if file_extracted:
            all_extracted.append((filename, file_extracted))
            print(f"- {filename}: {len(file_extracted)} items")
        else:
            print(f"- {filename}: 0 items")

    # Write Outputs (Same as before)
    
    with open(OUTPUT_TEMPLATE, 'w', encoding='utf-8') as f:
        f.write("# EDITABLE PROFILE DATA TEMPLATE\n")
        f.write("# Format: FILE_KEY__Item_ID = \"Value\"\n")
        
        for filename, items in all_extracted:
            file_key = filename.replace('.', '_')
            f.write(f"\n[{filename}]\n")
            for i, text in enumerate(items):
                safe_preview = "".join([c if c.isalnum() else "_" for c in text[:15]])
                key = f"{file_key}__Item_{i+1}_{safe_preview}"
                
                # Double check we escape quotes for the python string
                val_escaped = text.replace('"', '\\"')
                f.write(f'{key} = "{val_escaped}"\n')

    print(f"Finished. Scanned {len(js_files)} files.")

if __name__ == '__main__':
    main()
