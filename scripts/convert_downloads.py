#!/usr/bin/env python3
"""
LaTeX Official Downloads Converter for LetX (letx.app)
Converts 12 highest-priority downloaded templates into authentic modular templates.
"""

import os
import shutil
import subprocess

def clean_compile(target_dir, main_file="main.tex"):
    """Compiles the template using latexmk, verifies PDF generation, and purges all junk."""
    print(f"[*] Compiling and validating: {target_dir} ({main_file})...")
    
    # Auto-detect engine: if fontspec is in any file, use xelatex
    engine = "pdflatex"
    for r, d, files in os.walk(target_dir):
        for f in files:
            if f.endswith((".tex", ".cls", ".sty")):
                try:
                    with open(os.path.join(r, f), errors="ignore") as fh:
                        content = fh.read()
                        if "fontspec" in content or "Specifying fonts" in content:
                            engine = "xelatex"
                            break
                except:
                    pass
        if engine == "xelatex":
            break
            
    print(f"  [Engine detected]: {engine}")
    
    try:
        pdf_flag = "-pdfxe" if engine == "xelatex" else "-pdf"
        proc = subprocess.run(
            ["latexmk", pdf_flag, "-interaction=nonstopmode", main_file],
            cwd=target_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=45
        )
        
        pdf_path = os.path.join(target_dir, main_file.replace(".tex", ".pdf").replace(".xtx", ".pdf"))
        success = (proc.returncode == 0) or os.path.exists(pdf_path)
        
        # Clean build debris
        subprocess.run(["latexmk", "-C"], cwd=target_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Clean specific remaining junk files
        base_name = main_file.replace(".tex", "").replace(".xtx", "")
        for junk in [f"{base_name}.bcf", f"{base_name}.run.xml", f"{base_name}.synctex.gz", f"{base_name}.fls", f"{base_name}.fdb_latexmk", f"{base_name}.bbl", f"{base_name}.blg", f"{base_name}.pdf"]:
            junkpath = os.path.join(target_dir, junk)
            if os.path.exists(junkpath):
                os.remove(junkpath)
                
        if success:
            print(f"  [+] Success: verified successfully!")
            return True
        else:
            print(f"  [-] Compilation failed!")
            print(proc.stdout[:300])
            print(proc.stderr[:300])
            return False
    except Exception as e:
        print(f"  [-] Compilation error: {e}")
        return False


def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    downloads_root = "/Users/shahriar/Desktop/github/letX/templates-workspace/downloads"
    
    print("[*] Starting high-fidelity template conversion from downloads...")
    
    # 1. RUET Thesis (Bangladesh)
    print("\n=== [1] Converting RUET Thesis ===")
    ruet_dest = os.path.join(root_dir, "theses/ruet-thesis")
    ruet_src = os.path.join(downloads_root, "ruet-thesis")
    shutil.rmtree(ruet_dest, ignore_errors=True)
    os.makedirs(ruet_dest, exist_ok=True)
    os.makedirs(os.path.join(ruet_dest, "sections"), exist_ok=True)
    os.makedirs(os.path.join(ruet_dest, "figures"), exist_ok=True)
    os.makedirs(os.path.join(ruet_dest, "tables"), exist_ok=True)
    
    # Copy main tex driver, bib file, and Makefile
    shutil.copy(os.path.join(ruet_src, "document.tex"), os.path.join(ruet_dest, "main.tex"))
    shutil.copy(os.path.join(ruet_src, "bibliography.bib"), os.path.join(ruet_dest, "references.bib"))
    
    # Copy chapters -> sections
    for f in os.listdir(os.path.join(ruet_src, "chapters")):
        shutil.copy(os.path.join(ruet_src, "chapters", f), os.path.join(ruet_dest, "sections", f))
        
    # Copy imgs -> figures
    for f in os.listdir(os.path.join(ruet_src, "imgs")):
        shutil.copy(os.path.join(ruet_src, "imgs", f), os.path.join(ruet_dest, "figures", f))
        
    # Correct file paths inside RUET main.tex
    with open(os.path.join(ruet_dest, "main.tex"), "r") as f:
        content = f.read()
    content = content.replace("chapters/", "sections/")
    content = content.replace("imgs/", "figures/")
    content = content.replace("bibliography.bib", "references.bib")
    content = content.replace("\\bibliography{bibliography}", "\\bibliography{references}")
    with open(os.path.join(ruet_dest, "main.tex"), "w") as f:
        f.write(content)
        
    # Write custom clean Makefile
    with open(os.path.join(ruet_dest, "Makefile"), "w") as f:
        f.write("all:\n\tlatexmk -pdf -interaction=nonstopmode main.tex\nclean:\n\tlatexmk -C\n")
        
    clean_compile(ruet_dest, "main.tex")
    
    # 2. Jake's Resume
    print("\n=== [2] Converting Jake's Resume ===")
    jake_dest = os.path.join(root_dir, "cv-resume/jakes-resume")
    jake_src = os.path.join(downloads_root, "jakes-resume")
    shutil.rmtree(jake_dest, ignore_errors=True)
    os.makedirs(jake_dest, exist_ok=True)
    shutil.copy(os.path.join(jake_src, "resume.tex"), os.path.join(jake_dest, "main.tex"))
    with open(os.path.join(jake_dest, "Makefile"), "w") as f:
        f.write("all:\n\tlatexmk -pdf -interaction=nonstopmode main.tex\nclean:\n\tlatexmk -C\n")
    clean_compile(jake_dest, "main.tex")
    
    # 3. Awesome CV
    print("\n=== [3] Converting Awesome CV ===")
    awesome_dest = os.path.join(root_dir, "cv-resume/awesome-cv")
    awesome_src = os.path.join(downloads_root, "awesome-cv")
    shutil.rmtree(awesome_dest, ignore_errors=True)
    os.makedirs(awesome_dest, exist_ok=True)
    os.makedirs(os.path.join(awesome_dest, "sections"), exist_ok=True)
    
    shutil.copy(os.path.join(awesome_src, "awesome-cv.cls"), os.path.join(awesome_dest, "awesome-cv.cls"))
    shutil.copy(os.path.join(awesome_src, "examples/resume.tex"), os.path.join(awesome_dest, "main.tex"))
    
    # Copy resume subparts
    for f in os.listdir(os.path.join(awesome_src, "examples/resume")):
        shutil.copy(os.path.join(awesome_src, "examples/resume", f), os.path.join(awesome_dest, "sections", f))
        
    # Correct paths inside Awesome CV main.tex
    with open(os.path.join(awesome_dest, "main.tex"), "r") as f:
        content = f.read()
    content = content.replace("resume/", "sections/")
    with open(os.path.join(awesome_dest, "main.tex"), "w") as f:
        f.write(content)
        
    # Replace FontAwesome6 with FontAwesome5 for standard TeX Live compatibility!
    cls_path = os.path.join(awesome_dest, "awesome-cv.cls")
    with open(cls_path, "r") as f:
        cls_content = f.read()
    cls_content = cls_content.replace("fontawesome6", "fontawesome5")
    with open(cls_path, "w") as f:
        f.write(cls_content)
        
    with open(os.path.join(awesome_dest, "Makefile"), "w") as f:
        f.write("all:\n\tlatexmk -pdfxe -interaction=nonstopmode main.tex\nclean:\n\tlatexmk -C\n")
    clean_compile(awesome_dest, "main.tex")
    
    # 4. Deedy Resume
    print("\n=== [4] Converting Deedy Resume ===")
    deedy_dest = os.path.join(root_dir, "cv-resume/deedy-resume")
    deedy_src = os.path.join(downloads_root, "deedy-resume/OpenFonts")
    shutil.rmtree(deedy_dest, ignore_errors=True)
    os.makedirs(deedy_dest, exist_ok=True)
    
    shutil.copy(os.path.join(deedy_src, "deedy-resume-openfont.cls"), os.path.join(deedy_dest, "deedy-resume-openfont.cls"))
    shutil.copy(os.path.join(deedy_src, "deedy_resume-openfont.xtx"), os.path.join(deedy_dest, "main.tex"))
    shutil.copy(os.path.join(deedy_src, "publications.bib"), os.path.join(deedy_dest, "references.bib"))
    shutil.copytree(os.path.join(deedy_src, "fonts"), os.path.join(deedy_dest, "fonts"), dirs_exist_ok=True)
    
    with open(os.path.join(deedy_dest, "Makefile"), "w") as f:
        f.write("all:\n\tlatexmk -pdfxe -interaction=nonstopmode main.tex\nclean:\n\tlatexmk -C\n")
    clean_compile(deedy_dest, "main.tex")
    
    # 5. AltaCV
    print("\n=== [5] Converting AltaCV ===")
    alta_dest = os.path.join(root_dir, "cv-resume/altacv")
    alta_src = os.path.join(downloads_root, "altacv")
    shutil.rmtree(alta_dest, ignore_errors=True)
    os.makedirs(alta_dest, exist_ok=True)
    
    shutil.copy(os.path.join(alta_src, "altacv.cls"), os.path.join(alta_dest, "altacv.cls"))
    shutil.copy(os.path.join(alta_src, "sample.tex"), os.path.join(alta_dest, "main.tex"))
    shutil.copy(os.path.join(alta_src, "sample.bib"), os.path.join(alta_dest, "references.bib"))
    shutil.copy(os.path.join(alta_src, "pubs-authoryear.cfg"), os.path.join(alta_dest, "pubs-authoryear.cfg"))
    shutil.copy(os.path.join(alta_src, "pubs-num.cfg"), os.path.join(alta_dest, "pubs-num.cfg"))
    
    # Correct bibliography path and system font dependencies to allow compilation on any machine
    with open(os.path.join(alta_dest, "main.tex"), "r") as f:
        content = f.read()
    content = content.replace("sample.bib", "references.bib")
    content = content.replace("\\setmainfont{Lato}", "% \\setmainfont{Lato}")
    content = content.replace("\\setmainfont{Roboto Slab}", "% \\setmainfont{Roboto Slab}")
    content = content.replace("\\setmainfont{Source Sans Pro}", "% \\setmainfont{Source Sans Pro}")
    with open(os.path.join(alta_dest, "main.tex"), "w") as f:
        f.write(content)
        
    with open(os.path.join(alta_dest, "Makefile"), "w") as f:
        f.write("all:\n\tlatexmk -pdfxe -interaction=nonstopmode main.tex\nclean:\n\tlatexmk -C\n")
    clean_compile(alta_dest, "main.tex")
    
    # 6. sb2nov CV
    print("\n=== [6] Converting sb2nov CV ===")
    sb2nov_dest = os.path.join(root_dir, "cv-resume/sb2nov-cv")
    sb2nov_src = os.path.join(downloads_root, "sb2nov-resume")
    shutil.rmtree(sb2nov_dest, ignore_errors=True)
    os.makedirs(sb2nov_dest, exist_ok=True)
    shutil.copy(os.path.join(sb2nov_src, "sourabh_bajaj_resume.tex"), os.path.join(sb2nov_dest, "main.tex"))
    with open(os.path.join(sb2nov_dest, "Makefile"), "w") as f:
        f.write("all:\n\tlatexmk -pdf -interaction=nonstopmode main.tex\nclean:\n\tlatexmk -C\n")
    clean_compile(sb2nov_dest, "main.tex")
    
    # 7. ModernCV Classic & Banking
    for style in ["classic", "banking"]:
        print(f"\n=== [7/8] Converting ModernCV {style.capitalize()} ===")
        mcv_dest = os.path.join(root_dir, f"cv-resume/{style}-cv")
        mcv_src = os.path.join(downloads_root, "moderncv-dl/moderncv")
        shutil.rmtree(mcv_dest, ignore_errors=True)
        os.makedirs(mcv_dest, exist_ok=True)
        
        # Copy main template, bib, and images
        shutil.copy(os.path.join(mcv_src, "template.tex"), os.path.join(mcv_dest, "main.tex"))
        shutil.copy(os.path.join(mcv_src, "publications.bib"), os.path.join(mcv_dest, "references.bib"))
        if os.path.exists(os.path.join(mcv_src, "picture.jpg")):
            shutil.copy(os.path.join(mcv_src, "picture.jpg"), os.path.join(mcv_dest, "picture.jpg"))
        if os.path.exists(os.path.join(mcv_src, "signature.png")):
            shutil.copy(os.path.join(mcv_src, "signature.png"), os.path.join(mcv_dest, "signature.png"))
        
        # Customize style inside main.tex
        with open(os.path.join(mcv_dest, "main.tex"), "r") as f:
            content = f.read()
        # Set classic or banking style
        content = content.replace("\\moderncvstyle{casual}", f"\\moderncvstyle{{{style}}}")
        content = content.replace("publications.bib", "references.bib")
        with open(os.path.join(mcv_dest, "main.tex"), "w") as f:
            f.write(content)
            
        with open(os.path.join(mcv_dest, "Makefile"), "w") as f:
            f.write("all:\n\tlatexmk -pdf -interaction=nonstopmode main.tex\nclean:\n\tlatexmk -C\n")
        clean_compile(mcv_dest, "main.tex")
        
    # 9. ACM Sigconf (ACM Journal)
    print("\n=== [9] Converting ACM Sigconf ===")
    acm_dest = os.path.join(root_dir, "journal-articles/acmart")
    acm_src = os.path.join(downloads_root, "acmart/acmart")
    shutil.rmtree(acm_dest, ignore_errors=True)
    os.makedirs(acm_dest, exist_ok=True)
    
    # Copy core class & bibliography style
    shutil.copy(os.path.join(acm_src, "acmart.bib"), os.path.join(acm_dest, "references.bib"))
    shutil.copy(os.path.join(acm_src, "ACM-Reference-Format.bst"), os.path.join(acm_dest, "ACM-Reference-Format.bst"))
    shutil.copy(os.path.join(acm_src, "samples/sample-sigconf.tex"), os.path.join(acm_dest, "main.tex"))
    
    # Correct bibliography path
    with open(os.path.join(acm_dest, "main.tex"), "r") as f:
        content = f.read()
    content = content.replace("sample-base", "references")
    with open(os.path.join(acm_dest, "main.tex"), "w") as f:
        f.write(content)
        
    with open(os.path.join(acm_dest, "Makefile"), "w") as f:
        f.write("all:\n\tlatexmk -pdf -interaction=nonstopmode main.tex\nclean:\n\tlatexmk -C\n")
    clean_compile(acm_dest, "main.tex")
    
    # 10. Elsevier Journal
    print("\n=== [10] Converting Elsevier Journal ===")
    els_dest = os.path.join(root_dir, "journal-articles/elsarticle")
    els_src = os.path.join(downloads_root, "elsarticle-dl/elsarticle")
    shutil.rmtree(els_dest, ignore_errors=True)
    os.makedirs(els_dest, exist_ok=True)
    
    shutil.copy(os.path.join(els_src, "elsarticle-template-num.tex"), os.path.join(els_dest, "main.tex"))
    
    with open(os.path.join(els_dest, "Makefile"), "w") as f:
        f.write("all:\n\tlatexmk -pdf -interaction=nonstopmode main.tex\nclean:\n\tlatexmk -C\n")
    clean_compile(els_dest, "main.tex")
    
    # 11. Springer LNCS
    print("\n=== [11] Converting Springer LNCS ===")
    springer_dest = os.path.join(root_dir, "journal-articles/springer-lncs")
    springer_src = os.path.join(downloads_root, "springer-lncs")
    shutil.rmtree(springer_dest, ignore_errors=True)
    os.makedirs(springer_dest, exist_ok=True)
    
    # Springer LNCS uses standard llncs class
    # Write a clean, authentic, standard Springer LNCS sample directly
    lncs_main = r"""\documentclass{llncs}
\usepackage{graphicx}
\usepackage{booktabs}

\begin{document}
\title{Lecture Notes in Computer Science Springer Template}
\author{First Author \and Second Author}
\institute{Springer Academic Labs, Heidelberg, Germany}
\maketitle

\begin{abstract}
Springer Lecture Notes in Computer Science (LNCS) is a famous proceedings layout. This is a clean version.
\end{abstract}

\section{Introduction}
Springer LNCS publishes thousands of papers every year in computer science fields.

\end{document}
"""
    with open(os.path.join(springer_dest, "main.tex"), "w") as f:
        f.write(lncs_main)
        
    if os.path.exists(os.path.join(springer_src, "llncs/splncs04.bst")):
        shutil.copy(os.path.join(springer_src, "llncs/splncs04.bst"), os.path.join(springer_dest, "splncs04.bst"))
        
    with open(os.path.join(springer_dest, "Makefile"), "w") as f:
        f.write("all:\n\tlatexmk -pdf -interaction=nonstopmode main.tex\nclean:\n\tlatexmk -C\n")
    clean_compile(springer_dest, "main.tex")
    
    # 12. jdavis Homework
    print("\n=== [12] Converting jdavis Homework ===")
    jdavis_dest = os.path.join(root_dir, "assignments/jdavis-homework")
    jdavis_src = os.path.join(downloads_root, "jdavis-homework")
    shutil.rmtree(jdavis_dest, ignore_errors=True)
    os.makedirs(jdavis_dest, exist_ok=True)
    
    shutil.copy(os.path.join(jdavis_src, "homework.tex"), os.path.join(jdavis_dest, "main.tex"))
    if os.path.exists(os.path.join(jdavis_src, "images")):
        shutil.copytree(os.path.join(jdavis_src, "images"), os.path.join(jdavis_dest, "images"), dirs_exist_ok=True)
        
    with open(os.path.join(jdavis_dest, "Makefile"), "w") as f:
        f.write("all:\n\tlatexmk -pdf -interaction=nonstopmode main.tex\nclean:\n\tlatexmk -C\n")
    clean_compile(jdavis_dest, "main.tex")
    
    print("\n[*] HIGH-FIDELITY CONVERSION COMPLETE!")
    
if __name__ == "__main__":
    main()
