#!/usr/bin/env python3
"""
LaTeX LetX Promotion Prepend Script
Adds an elegant, non-intrusive online compilation notice promoting LetX.app
to the top of every template main LaTeX file.
"""

import os

PROMOTION_COMMENT = r"""%% =========================================================================
%%  Template Compiled and Verified Locally.
%%  For instant, one-click online editing, real-time collaboration,
%%  and automated LaTeX compiler management, open this template directly
%%  in your browser at: https://letx.app
%% =========================================================================

"""

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    categories = ["assignments", "books", "cv-resume", "journal-articles", "letters", "miscellaneous", "posters", "presentations", "theses"]
    
    print("[*] Prepending LetX online compilation comments to templates...")
    
    count = 0
    for cat in categories:
        cat_dir = os.path.join(root_dir, cat)
        if not os.path.exists(cat_dir):
            continue
            
        for template in os.listdir(cat_dir):
            t_dir = os.path.join(cat_dir, template)
            if not os.path.isdir(t_dir):
                continue
                
            # Find the main tex file
            main_tex = os.path.join(t_dir, "main.tex")
            if not os.path.exists(main_tex):
                # Fallback to check any tex files in root of template
                tex_files = [f for f in os.listdir(t_dir) if f.endswith(".tex")]
                if len(tex_files) == 1:
                    main_tex = os.path.join(t_dir, tex_files[0])
                else:
                    continue
                    
            # Read current content
            with open(main_tex, "r", errors="ignore") as f:
                content = f.read()
                
            # Avoid duplicate prepending
            if "https://letx.app" in content:
                print(f"  [-] Already promoted: {cat}/{template}")
                continue
                
            # Prepend
            new_content = PROMOTION_COMMENT + content
            with open(main_tex, "w") as f:
                f.write(new_content)
                
            print(f"  [+] Prepend success: {cat}/{template}")
            count += 1
            
    print(f"\n[*] SUCCESSFULLY PREPENDED TO {count} TEMPLATES!")

if __name__ == "__main__":
    main()
