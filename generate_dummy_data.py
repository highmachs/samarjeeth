import os

TEMPLATE_FILE = r"c:\MAINDOMAIN\Portfolio sites\p5\profiledat.txt"

# Exact Key Mapping for High Quality Overhaul
# We use the keys found in the file (e.g., 3ac11fa_js__Item_25_Eniola_Korty__y)
# and map them to complete new sentences.

CONTENT_MAP = {
    # LANDING PAGE (763368b.js)
    "763368b_js__Item_3_Profile": "Profile",
    "763368b_js__Item_4_Archive": "Archive",
    "763368b_js__Item_5_credits": "Credits",
    
    # Hero / Intro
    "763368b_js__Item_19_View_Korty_s_Pr": "View Portfolio",
    "763368b_js__Item_20_korty_eo": "ethan_sec",
    "763368b_js__Item_21_FILMAKER__": "CYBERSEC &",
    "763368b_js__Item_22_YOUTUBER": "RESEARCHER",
    "763368b_js__Item_23_Based_in_Lagos_": "Based in New York. Ethan runs a security blog where he posts -",
    "763368b_js__Item_24_these_mostly_go": "vulnerability writeups and zero-day exploits. Highly technical content.",
    "763368b_js__Item_25_She_has_walked_": "He has consulted for Fortune 500 companies on network defense.",
    
    # Hover Links / Menu items
    "763368b_js__Item_7_VL": "CT",
    "763368b_js__Item_8_O": "F",
    "763368b_js__Item_9_GS": "S",
    "763368b_js__Item_10_INTERVIEWS": "WRITEUPS",
    
    "763368b_js__Item_12_VIDE": "BUG",
    "763368b_js__Item_13_O": "S",
    "763368b_js__Item_14_MASHUPS": "BOUNTY",
    
    "763368b_js__Item_16_M": "P",
    "763368b_js__Item_17_O": "EN",
    "763368b_js__Item_18_DELLING": "TESTING",

    # Mobile duplicates (763368b.js continued)
    "763368b_js__Item_26_Profile": "Profile",
    "763368b_js__Item_27_Archive": "Archive",
    "763368b_js__Item_28_korty_eo": "ethan_sec",
    "763368b_js__Item_29_FILMAKER__": "CYBERSEC &",
    "763368b_js__Item_30_YOUTUBER": "RESEARCHER",
    "763368b_js__Item_31_Based_in_Lagos_": "Based in New York. Ethan runs a security blog where he posts -",
    "763368b_js__Item_39_these_mostly_go": "vulnerability writeups and zero-day exploits. Highly technical content.",
    "763368b_js__Item_32_VL": "CT",
    "763368b_js__Item_33_O": "F",
    "763368b_js__Item_34_GS": "S",
    "763368b_js__Item_35_INTERVIEWS": "WRITEUPS",
    "763368b_js__Item_36_VIDE": "BUG",
    "763368b_js__Item_37_O": "S",
    "763368b_js__Item_38_MASHUPS": "BOUNTY",
    "763368b_js__Item_40_M": "P",
    "763368b_js__Item_41_O": "EN",
    "763368b_js__Item_42_DELLING": "TESTING",
    "763368b_js__Item_43_She_has_walked_": "He has consulted for Fortune 500 companies on network defense.",
    "763368b_js__Item_44_View_Korty_s_Pr": "View Portfolio",

    # PROFILE PAGE (3ac11fa.js)
    "3ac11fa_js__Item_3_Close": "Close",
    "3ac11fa_js__Item_4_Archive": "Archive",
    "3ac11fa_js__Item_9_Korty_EO_": "Ethan Hunt.",
    "3ac11fa_js__Item_10_January_23__202": "October 10, 2023",
    "3ac11fa_js__Item_11_by__jag_ubani": "by @defcon_official",
    
    # Hero Title (Eniola Korty Olanrewaju split)
    "3ac11fa_js__Item_12_Eniola": "Ethan",
    "3ac11fa_js__Item_13_Korty": "Nathaniel",
    "3ac11fa_js__Item_14_Olanrewaju": "Hunt",
    "3ac11fa_js__Item_15_Eniola": "Ethan",
    "3ac11fa_js__Item_16_Korty": "Nathaniel",
    "3ac11fa_js__Item_17_Olanrewaju": "Hunt",
    "3ac11fa_js__Item_18_Eniola": "Ethan",
    "3ac11fa_js__Item_19_Korty": "Nathaniel",
    "3ac11fa_js__Item_20_Olanrewaju": "Hunt",
    
    "3ac11fa_js__Item_21_Korty_EO_": "Ethan H.",
    "3ac11fa_js__Item_23_is_a_Lagos_base": "is a NY based Security Researcher & Student",
    "3ac11fa_js__Item_24__in_love_with_m": "—in love with kernels and exploits. On his github; he publishes POCs, tools, and other experimental malware analysis. He has previously worked with some of the best red teams in the world.",
    "3ac11fa_js__Item_25_Eniola_Korty__y": "Ethan Hunt, known online as 'Hunt3r', leaves no room for error when it comes to penetration testing. Ethan has an impressive stack, as he credits being a reverse engineer, cryptographer, network analyst, and now Student. His rigorous and detailed reporting, combined with his ethical approach to disclosure, makes him a trusted asset.",
    
    # Quotes
    "3ac11fa_js__Item_26_Korty_EO____TG_": "Ethan H. & MR. ROBOT",
    "3ac11fa_js__Item_28__The_inspiratio": "“The inspiration behind my work is curiosity. I like to break systems as a hobby because I’m fascinated by how things work. Converting these exploits into safe patches is like solving a puzzle. The thought of a secure web encourages me.”",
    "3ac11fa_js__Item_29___Korty_EO_": "- Ethan H.",
    
    # Story Text
    "3ac11fa_js__Item_31_Korty_left_her_": "Ethan left his university program in CS for a hands-on role after winning a major CTF. Studies were going well, until he got bored and literally said 'sudo rm -rf school'. He is mostly self taught, leveraging the documentation available online. He found more creative freedom in bug bounty hunting.",
    "3ac11fa_js__Item_32_She_later_joine": "He later joined HackTheBox, (a platform to train security professionals) in January 2022 as a Content Lead where he designed retired machines. He soon left to pursue full-time freelance pentesting and independent research.",
    
    # Work Experience / Logos
    "3ac11fa_js__Item_33_Korty_EO_": "Ethan H.",
    "3ac11fa_js__Item_34_March_23__2021_": "Nov 15, 2023 by @null_pointer",
    "3ac11fa_js__Item_35_W": "W",
    "3ac11fa_js__Item_36_O": "O",
    "3ac11fa_js__Item_37_RK": "RK",
    "3ac11fa_js__Item_38_Korty_Eniola_ha": "Ethan has worked across finance, tech and defense industries as a scanner, patcher, auditor, white hat, and now consultant.",
    
    # Projects
    "3ac11fa_js__Item_40_NIKE": "OWASP",
    "3ac11fa_js__Item_41_Collaboration_w": "Collaboration with Core Team for the new Top 10 release.",
    "3ac11fa_js__Item_71_NIKE": "OWASP", # Duplicates probably

    "3ac11fa_js__Item_42_GTBANK": "WIRESHARK",
    "3ac11fa_js__Item_43_Winning_project": "Developed a custom dissector for proprietary protocols.",
    "3ac11fa_js__Item_72_GTBANK": "WIRESHARK",

    "3ac11fa_js__Item_45_EMPAWA": "HACKTHEBOX",
    "3ac11fa_js__Item_44_Worked_as_a_con": "Served as a machine creator, designing 'Insane' difficulty boxes.",
    "3ac11fa_js__Item_73_EMPAWA": "HACKTHEBOX",

    "3ac11fa_js__Item_46_GOOGLE_ARTS": "ZERO DAY",
    "3ac11fa_js__Item_47___CULTURE": "INITIATIVE",
    "3ac11fa_js__Item_48_Worked_on_produ": "Private disclosure of a critical RCE in a major browser engine.",
    "3ac11fa_js__Item_111_3ac11fa_js__Item_78": "ZERO DAY INITIATIVE", # key mismatch in my brain, relying on script match

    "3ac11fa_js__Item_49_ZIKOKO": "KALI LINUX",
    "3ac11fa_js__Item_50_Assistant_Video": "Contributor in 2020, became a Maintainer in 2021",
    "3ac11fa_js__Item_107_ZIK": "KAL",
    "3ac11fa_js__Item_108_O": "I",
    "3ac11fa_js__Item_74_ZIK": "KAL", # check keys later

    "3ac11fa_js__Item_54_COACHELLA": "DEFCON",
    "3ac11fa_js__Item_55_A_documentation": "Winner of the Social Engineering Capture The Flag (SECTF).",
    
    "3ac11fa_js__Item_57_BBNAIJA": "MR. ROBOT",
    "3ac11fa_js__Item_56_At_Zikoko__Kort": "Consulted on technical accuracy for a hacking TV series.",
    
    "3ac11fa_js__Item_58_KEEXS": "NMAP",
    "3ac11fa_js__Item_59_Edited_a_promot": "Wrote a custom NSE script for IoT device discovery.",
    
    "3ac11fa_js__Item_61_PAMANE": "BURP SUITE",
    "3ac11fa_js__Item_60_Photo_modelling": "Created a popular extension for automated auth testing.",
    
    "3ac11fa_js__Item_63_MAKING_FILM_THE": "HACKING THE",
    "3ac11fa_js__Item_64_SLOWER_WAY_": "HARDER WAY,",
    
    # Archive page
    "842b1ec_js__Item_3_This_archive_co": "This archive contains reports, CVEs and POCs related to Ethan and his work. Contact for PGP key.",
}

def main():
    if not os.path.exists(TEMPLATE_FILE):
        print(f"Error: {TEMPLATE_FILE} not found.")
        return

    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    new_lines = []
    
    for line in lines:
        if "=" in line and not line.strip().startswith("#") and not line.strip().startswith("["):
            parts = line.split("=", 1)
            key = parts[0].strip()
            
            # Check if we have a direct override for this key
            if key in CONTENT_MAP:
                new_val = CONTENT_MAP[key]
                # Re-quote
                new_lines.append(f'{key} = "{new_val}"\n')
            else:
                # If not mapped, keep as is
                new_lines.append(line)
        else:
            new_lines.append(line)
            
    # Write back
    with open(TEMPLATE_FILE, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
        
    print("New cybersecurity data injected into profiledat.txt")

if __name__ == '__main__':
    main()
