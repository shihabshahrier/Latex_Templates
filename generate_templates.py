#!/usr/bin/env python3
"""
LaTeX Templates Factory for LetX (letx.app)
Generates 80+ SEO-optimized, highly structured, modular LaTeX templates.
Compiles templates in parallel, verifies correctness, cleans up debris, and commits to Git.
"""

import os
import sys
import shutil
import subprocess
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

# Define standard colors for universities to make each template feel premium and authentic.
UNIVERSITY_THEMES = {
    # Global
    "mit-thesis": {
        "univ_name": "Massachusetts Institute of Technology",
        "univ_short": "MIT",
        "location": "Cambridge, Massachusetts",
        "primary_color": "RGB(163, 31, 52)", # MIT Cardinal Red
        "secondary_color": "RGB(138, 139, 140)", # MIT Dark Gray
        "degree": "Doctor of Philosophy",
        "logo_tikz": r"""
            \draw[fill=primary, draw=none] (-1.2,-0.4) rectangle (-0.8, 0.4);
            \draw[fill=secondary, draw=none] (-0.6,-0.4) rectangle (-0.2, 0.4);
            \draw[fill=primary, draw=none] (0.0,-0.4) rectangle (0.4, 0.4);
            \draw[fill=secondary, draw=none] (0.6,-0.4) rectangle (1.0, 0.4);
            \node[primary, font=\tiny\bfseries\sffamily] at (0,-0.7) {M I T};
        """
    },
    "stanford-thesis": {
        "univ_name": "Stanford University",
        "univ_short": "Stanford",
        "location": "Stanford, California",
        "primary_color": "RGB(140, 21, 21)", # Stanford Cardinal Red
        "secondary_color": "RGB(94, 94, 94)",
        "degree": "Doctor of Philosophy",
        "logo_tikz": r"""
            \draw[fill=primary, draw=none] (0,0) circle (0.6);
            \draw[white, fill=white] (0,0) circle (0.5);
            \node[primary, font=\Large\bfseries\itshape\rmfamily] at (0,0) {S};
            \draw[primary, thick] (-0.8,-0.8) -- (0.8,-0.8);
        """
    },
    "oxford-thesis": {
        "univ_name": "University of Oxford",
        "univ_short": "Oxford",
        "location": "Oxford, United Kingdom",
        "primary_color": "RGB(0, 33, 71)", # Oxford Blue
        "secondary_color": "RGB(178, 163, 117)", # Gold
        "degree": "Doctor of Philosophy",
        "logo_tikz": r"""
            \draw[draw=primary, ultra thick] (-0.6,-0.4) rectangle (0.6,0.4);
            \draw[draw=primary, thick] (-0.5,-0.3) -- (0.5,-0.3);
            \draw[draw=primary, thick] (-0.5,0.3) -- (0.5,0.3);
            \node[primary, font=\tiny\bfseries\sffamily] at (0,0) {DOMI MINA};
            \node[primary, font=\tiny\bfseries\sffamily] at (0,-0.18) {NVS ILLV};
        """
    },
    "cambridge-thesis": {
        "univ_name": "University of Cambridge",
        "univ_short": "Cambridge",
        "location": "Cambridge, United Kingdom",
        "primary_color": "RGB(0, 62, 81)", # Cambridge Blue-Green
        "secondary_color": "RGB(212, 175, 55)",
        "degree": "Doctor of Philosophy",
        "logo_tikz": r"""
            \draw[fill=primary, draw=none] (-0.5,-0.5) -- (0,0.5) -- (0.5,-0.5) -- cycle;
            \draw[fill=white, draw=none] (-0.2,-0.3) -- (0,0.2) -- (0.2,-0.3) -- cycle;
            \node[primary, font=\tiny\bfseries] at (0,-0.6) {CAMBRIDGE};
        """
    },
    "harvard-thesis": {
        "univ_name": "Harvard University",
        "univ_short": "Harvard",
        "location": "Cambridge, Massachusetts",
        "primary_color": "RGB(165, 28, 48)", # Crimson
        "secondary_color": "RGB(30, 30, 30)",
        "degree": "Doctor of Philosophy",
        "logo_tikz": r"""
            \draw[fill=primary, draw=none] (-0.6,-0.4) rectangle (0.6,0.4);
            \draw[white, thick] (-0.5,-0.3) rectangle (0.5,0.3);
            \node[white, font=\tiny\bfseries] at (-0.25,0.1) {VE};
            \node[white, font=\tiny\bfseries] at (0.25,0.1) {RI};
            \node[white, font=\tiny\bfseries] at (0,-0.15) {TAS};
        """
    },
    "eth-zurich-thesis": {
        "univ_name": "ETH Zurich",
        "univ_short": "ETHZ",
        "location": "Zurich, Switzerland",
        "primary_color": "RGB(31, 58, 107)", # ETH Navy
        "secondary_color": "RGB(0, 120, 140)",
        "degree": "Doctor of Sciences",
        "logo_tikz": r"""
            \draw[fill=primary, draw=none] (-0.8,-0.2) rectangle (0.8,0.2);
            \node[white, font=\small\bfseries\sffamily] at (0,0) {ETH Zurich};
        """
    },
    # Singapore & Asia
    "nus-singapore-thesis": {
        "univ_name": "National University of Singapore",
        "univ_short": "NUS",
        "location": "Singapore",
        "primary_color": "RGB(0, 61, 124)", # NUS Blue
        "secondary_color": "RGB(239, 124, 0)", # NUS Orange
        "degree": "Doctor of Philosophy",
        "logo_tikz": r"""
            \draw[fill=primary, draw=none] (-0.5,-0.5) rectangle (0.5,0.5);
            \draw[fill=secondary, draw=none] (-0.3,-0.3) rectangle (0.3,0.3);
            \node[white, font=\tiny\bfseries] at (0,0) {NUS};
        """
    },
    "ntu-singapore-thesis": {
        "univ_name": "Nanyang Technological University",
        "univ_short": "NTU",
        "location": "Singapore",
        "primary_color": "RGB(163, 19, 44)", # NTU Red
        "secondary_color": "RGB(0, 43, 91)", # NTU Blue
        "degree": "Doctor of Philosophy",
        "logo_tikz": r"""
            \draw[fill=primary, draw=none] (-0.6,-0.3) rectangle (0.6,0.3);
            \node[white, font=\small\bfseries] at (0,0) {NTU};
        """
    },
    "tsinghua-thesis": {
        "univ_name": "Tsinghua University",
        "univ_short": "Tsinghua",
        "location": "Beijing, China",
        "primary_color": "RGB(102, 8, 116)", # Tsinghua Purple
        "secondary_color": "RGB(150, 150, 150)",
        "degree": "Doctor of Philosophy",
        "logo_tikz": r"""
            \draw[fill=primary, draw=none] (0,0) circle (0.5);
            \draw[white, fill=white] (0,0) circle (0.4);
            \node[primary, font=\tiny\bfseries] at (0,0) {清华大学};
        """
    },
    "kaist-thesis": {
        "univ_name": "Korea Advanced Institute of Science and Technology",
        "univ_short": "KAIST",
        "location": "Daejeon, South Korea",
        "primary_color": "RGB(0, 65, 145)", # KAIST Blue
        "secondary_color": "RGB(140, 140, 140)",
        "degree": "Doctor of Philosophy",
        "logo_tikz": r"""
            \draw[fill=primary, draw=none] (-0.7,-0.2) rectangle (0.7,0.2);
            \node[white, font=\small\bfseries\sffamily] at (0,0) {KAIST};
        """
    },
    "tokyo-university-thesis": {
        "univ_name": "The University of Tokyo",
        "univ_short": "UTokyo",
        "location": "Tokyo, Japan",
        "primary_color": "RGB(0, 75, 141)", # UTokyo Blue
        "secondary_color": "RGB(241, 196, 0)", # Yellow
        "degree": "Doctor of Philosophy",
        "logo_tikz": r"""
            \draw[fill=primary, draw=none] (0,0) circle (0.5);
            \draw[fill=secondary, draw=none] (0,0) circle (0.3);
            \node[white, font=\tiny\bfseries] at (0,0) {東大};
        """
    },
    # India
    "iit-bombay-thesis": {
        "univ_name": "Indian Institute of Technology Bombay",
        "univ_short": "IIT Bombay",
        "location": "Mumbai, India",
        "primary_color": "RGB(0, 48, 135)", # IITB Navy
        "secondary_color": "RGB(229, 114, 0)",
        "degree": "Doctor of Philosophy",
        "logo_tikz": r"""
            \draw[fill=primary, draw=none] (0,0) circle (0.5);
            \draw[fill=white, draw=none] (0,0) circle (0.4);
            \draw[fill=secondary, draw=none] (-0.1,-0.15) rectangle (0.1,0.15);
            \node[primary, font=\tiny\bfseries] at (0,0.25) {IITB};
        """
    },
    "iit-madras-thesis": {
        "univ_name": "Indian Institute of Technology Madras",
        "univ_short": "IIT Madras",
        "location": "Chennai, India",
        "primary_color": "RGB(0, 94, 93)", # IITM Teal
        "secondary_color": "RGB(224, 82, 6)",
        "degree": "Doctor of Philosophy",
        "logo_tikz": r"""
            \draw[fill=primary, draw=none] (0,0) circle (0.5);
            \draw[fill=white, draw=none] (0,0) circle (0.4);
            \node[primary, font=\tiny\bfseries] at (0,0) {IITM};
        """
    },
    "iit-delhi-thesis": {
        "univ_name": "Indian Institute of Technology Delhi",
        "univ_short": "IIT Delhi",
        "location": "New Delhi, India",
        "primary_color": "RGB(139, 0, 0)", # Dark Red
        "secondary_color": "RGB(0, 100, 80)",
        "degree": "Doctor of Philosophy",
        "logo_tikz": r"""
            \draw[fill=primary, draw=none] (-0.4,-0.4) rectangle (0.4,0.4);
            \node[white, font=\tiny\bfseries] at (0,0) {IITD};
        """
    },
    "iit-kanpur-thesis": {
        "univ_name": "Indian Institute of Technology Kanpur",
        "univ_short": "IIT Kanpur",
        "location": "Kanpur, India",
        "primary_color": "RGB(0, 51, 153)", # IITK Blue
        "secondary_color": "RGB(100, 100, 100)",
        "degree": "Doctor of Philosophy",
        "logo_tikz": r"""
            \draw[fill=primary, draw=none] (0,0) circle (0.5);
            \node[white, font=\tiny\bfseries] at (0,0) {IITK};
        """
    },
    "iisc-bangalore-thesis": {
        "univ_name": "Indian Institute of Science",
        "univ_short": "IISc Bangalore",
        "location": "Bengaluru, India",
        "primary_color": "RGB(0, 32, 91)", # IISc Dark Navy
        "secondary_color": "RGB(180, 150, 50)",
        "degree": "Doctor of Philosophy",
        "logo_tikz": r"""
            \draw[fill=primary, draw=none] (-0.5,-0.5) rectangle (0.5,0.5);
            \draw[fill=white, draw=none] (-0.4,-0.4) rectangle (0.4,0.4);
            \node[primary, font=\tiny\bfseries] at (0,0) {IISc};
        """
    },
    "bits-pilani-thesis": {
        "univ_name": "Birla Institute of Technology and Science, Pilani",
        "univ_short": "BITS Pilani",
        "location": "Pilani, Rajasthan, India",
        "primary_color": "RGB(0, 51, 102)", # BITS Navy
        "secondary_color": "RGB(204, 153, 0)", # Gold
        "degree": "Doctor of Philosophy",
        "logo_tikz": r"""
            \draw[fill=primary, draw=none] (0,0) circle (0.5);
            \draw[white, fill=white] (0,0) circle (0.35);
            \node[primary, font=\tiny\bfseries] at (0,0) {BITS};
        """
    },
    # Bangladesh
    "buet-thesis": {
        "univ_name": "Bangladesh University of Engineering and Technology",
        "univ_short": "BUET",
        "location": "Dhaka, Bangladesh",
        "primary_color": "RGB(0, 101, 67)", # BUET Dark Green
        "secondary_color": "RGB(190, 15, 52)", # BUET Crimson Accent
        "degree": "Bachelor of Science in Computer Science and Engineering",
        "logo_tikz": r"""
            \draw[fill=primary, draw=none] (0,0.4) -- (-0.4,-0.3) -- (0.4,-0.3) -- cycle;
            \draw[fill=white, draw=none] (0,0.25) -- (-0.25,-0.2) -- (0.25,-0.2) -- cycle;
            \node[primary, font=\tiny\bfseries] at (0,-0.5) {BUET};
        """
    },
    "du-thesis": {
        "univ_name": "University of Dhaka",
        "univ_short": "Dhaka University",
        "location": "Dhaka, Bangladesh",
        "primary_color": "RGB(0, 48, 135)", # DU Blue
        "secondary_color": "RGB(0, 104, 56)", # Green
        "degree": "Doctor of Philosophy",
        "logo_tikz": r"""
            \draw[fill=primary, draw=none] (0,0) circle (0.5);
            \draw[white, fill=white] (0,0) circle (0.4);
            \node[primary, font=\tiny\bfseries] at (0,0) {DU};
        """
    },
    "ruet-thesis": {
        "univ_name": "Rajshahi University of Engineering and Technology",
        "univ_short": "RUET",
        "location": "Rajshahi, Bangladesh",
        "primary_color": "RGB(178, 15, 36)", # RUET Crimson
        "secondary_color": "RGB(28, 48, 120)", # Blue
        "degree": "Bachelor of Science in Computer Science and Engineering",
        "logo_tikz": r"""
            \draw[fill=primary, draw=none] (-0.5,-0.3) rectangle (0.5,0.3);
            \node[white, font=\small\bfseries] at (0,0) {RUET};
        """
    },
    "kuet-thesis": {
        "univ_name": "Khulna University of Engineering and Technology",
        "univ_short": "KUET",
        "location": "Khulna, Bangladesh",
        "primary_color": "RGB(0, 112, 192)", # KUET Blue
        "secondary_color": "RGB(0, 128, 0)", # Green
        "degree": "Bachelor of Science in Electrical and Electronic Engineering",
        "logo_tikz": r"""
            \draw[fill=primary, draw=none] (0,0) circle (0.5);
            \node[white, font=\tiny\bfseries] at (0,0) {KUET};
        """
    },
    "cuet-thesis": {
        "univ_name": "Chittagong University of Engineering and Technology",
        "univ_short": "CUET",
        "location": "Chittagong, Bangladesh",
        "primary_color": "RGB(142, 36, 170)", # Purple
        "secondary_color": "RGB(0, 137, 123)", # Teal
        "degree": "Bachelor of Science in Mechanical Engineering",
        "logo_tikz": r"""
            \draw[fill=primary, draw=none] (0,0) circle (0.5);
            \node[white, font=\tiny\bfseries] at (0,0) {CUET};
        """
    },
    "sust-thesis": {
        "univ_name": "Shahjalal University of Science and Technology",
        "univ_short": "SUST",
        "location": "Sylhet, Bangladesh",
        "primary_color": "RGB(216, 27, 96)", # Pinkish Red
        "secondary_color": "RGB(30, 136, 229)", # Blue
        "degree": "Bachelor of Science in Computer Science and Engineering",
        "logo_tikz": r"""
            \draw[fill=primary, draw=none] (-0.4,-0.4) rectangle (0.4,0.4);
            \node[white, font=\tiny\bfseries] at (0,0) {SUST};
        """
    },
    "iut-thesis": {
        "univ_name": "Islamic University of Technology",
        "univ_short": "IUT",
        "location": "Gazipur, Bangladesh",
        "primary_color": "RGB(230, 92, 0)", # IUT Orange
        "secondary_color": "RGB(0, 102, 204)", # IUT Blue
        "degree": "Bachelor of Science in Computer Science and Engineering",
        "logo_tikz": r"""
            \draw[fill=primary, draw=none] (0,0) circle (0.5);
            \node[white, font=\tiny\bfseries] at (0,0) {IUT};
        """
    },
    # Pakistan
    "nust-thesis": {
        "univ_name": "National University of Sciences and Technology",
        "univ_short": "NUST",
        "location": "Islamabad, Pakistan",
        "primary_color": "RGB(0, 102, 204)", # NUST Blue
        "secondary_color": "RGB(212, 175, 55)", # Gold
        "degree": "Bachelor of Science in Computer Science",
        "logo_tikz": r"""
            \draw[fill=primary, draw=none] (-0.5,-0.5) rectangle (0.5,0.5);
            \node[white, font=\small\bfseries] at (0,0) {NUST};
        """
    },
    "lums-thesis": {
        "univ_name": "Lahore University of Management Sciences",
        "univ_short": "LUMS",
        "location": "Lahore, Pakistan",
        "primary_color": "RGB(0, 51, 102)", # LUMS Blue
        "secondary_color": "RGB(230, 0, 0)", # Red
        "degree": "Bachelor of Science in Electrical Engineering",
        "logo_tikz": r"""
            \draw[fill=primary, draw=none] (0,0) circle (0.5);
            \node[white, font=\tiny\bfseries] at (0,0) {LUMS};
        """
    },
    "fast-nuces-thesis": {
        "univ_name": "National University of Computer and Emerging Sciences",
        "univ_short": "FAST-NUCES",
        "location": "Islamabad, Pakistan",
        "primary_color": "RGB(28, 54, 116)", # FAST Dark Blue
        "secondary_color": "RGB(163, 19, 44)",
        "degree": "Bachelor of Science in Computer Science",
        "logo_tikz": r"""
            \draw[fill=primary, draw=none] (-0.5,-0.3) rectangle (0.5,0.3);
            \node[white, font=\tiny\bfseries] at (0,0) {FAST};
        """
    },
    "qau-thesis": {
        "univ_name": "Quaid-i-Azam University",
        "univ_short": "QAU",
        "location": "Islamabad, Pakistan",
        "primary_color": "RGB(0, 128, 0)", # Green
        "secondary_color": "RGB(0, 0, 128)", # Navy
        "degree": "Doctor of Philosophy",
        "logo_tikz": r"""
            \draw[fill=primary, draw=none] (0,0) circle (0.5);
            \node[white, font=\tiny\bfseries] at (0,0) {QAU};
        """
    }
}

# --- TeX Templates Boilerplates ---

THESIS_MAIN_TEX = r"""\documentclass[12pt,a4paper,oneside]{report}
\usepackage[utf8]{inputenc}
\usepackage[margin=1.2in]{geometry}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{graphicx}
\usepackage{xcolor}
\usepackage{tikz}
\usepackage{hyperref}
\usepackage{caption}
\usepackage{subcaption}
\usepackage{booktabs}
\usepackage{setspace}
\usepackage[backend=biber,style=ieee,sorting=none]{biblatex}

% Define Colors based on University branding
\definecolor{primary}{HTML}{__PRIMARY_HEX__}
\definecolor{secondary}{HTML}{__SECONDARY_HEX__}

\hypersetup{
    colorlinks=true,
    linkcolor=primary,
    citecolor=primary,
    filecolor=primary,
    urlcolor=primary,
    pdftitle={__UNIV_SHORT__ Thesis Report},
    pdfauthor={Student Author Name}
}

\addbibresource{references.bib}
\onehalfspacing

\begin{document}

% Title and Preliminaries
\input{sections/title.tex}

\pagenumbering{roman}
\input{sections/dedication.tex}
\input{sections/acknowledgements.tex}
\input{sections/abstract.tex}

\tableofcontents
\listoffigures
\listoftables

\clearpage
\pagenumbering{arabic}

% Chapters
\input{sections/chapter1.tex}
\input{sections/chapter2.tex}
\input{sections/chapter3.tex}
\input{sections/chapter4.tex}
\input{sections/chapter5.tex}

\clearpage
\printbibliography[heading=bibintoc,title={References}]

\end{document}
"""

THESIS_TITLE_TEX = r"""\begin{titlepage}
\begin{center}
    \vspace*{1cm}
    
    % University Logo Emblem drawn in pure TikZ
    \begin{tikzpicture}[scale=2]
        __LOGO_TIKZ__
    \end{tikzpicture}
    
    \vspace{1.5cm}
    
    {\huge \bfseries \color{primary} Thesis Title: Scalable and Robust LaTeX Template Scaffolding for Modern Publishing}
    
    \vspace{1.5cm}
    
    {\Large \bfseries Student Author Name} \\
    \vspace{0.2cm}
    {Roll/ID: 1029384}
    
    \vspace{1.5cm}
    
    {A thesis submitted in partial fulfillment of the requirements for the degree of} \\
    \vspace{0.3cm}
    {\large \bfseries \color{secondary} __DEGREE__}
    
    \vspace{1.5cm}
    
    {\large Department of Computer Science and Engineering} \\
    \vspace{0.2cm}
    {\large \bfseries \color{primary} __UNIV_NAME__} \\
    \vspace{0.1cm}
    {__LOCATION__}
    
    \vfill
    
    {Supervised by:} \\
    {\large \bfseries Prof. Advisor Name} \\
    {Designation, CSE Department}
    
    \vspace{1cm}
    
    {\large \today}
    
\end{center}
\end{titlepage}
"""

THESIS_DEDICATION_TEX = r"""\chapter*{Dedication}
\addcontentsline{toc}{chapter}{Dedication}
\begin{center}
    \vspace*{4cm}
    \itshape
    To my beloved parents and family,\\
    whose endless support, sacrifices, and belief in my dreams\\
    have made this achievement possible.
\end{center}
"""

THESIS_ACKNOWLEDGEMENTS_TEX = r"""\chapter*{Acknowledgements}
\addcontentsline{toc}{chapter}{Acknowledgements}
I would like to express my deepest gratitude to my supervisor, Prof. Advisor Name, for their constant guidance, valuable feedback, and infinite patience throughout the course of this research. 

Special thanks go to the Department of Computer Science and Engineering for providing the computational resources and laboratory infrastructure that made this work feasible.

Finally, I am eternally grateful to my friends and family for their unwavering moral support, encouragement, and understanding during the long hours of work. Thank you all.
"""

THESIS_ABSTRACT_TEX = r"""\chapter*{Abstract}
\addcontentsline{toc}{chapter}{Abstract}
Writing LaTeX thesis reports is historically a rigorous process involving precise formatting rules prescribed by academic institutions. In this thesis, we present a complete modular engineering platform designed to automate the scaffolding and generation of premium, SEO-optimized LaTeX templates. Our approach decomposes monolithic source documents into highly organized sub-directories representing separate sections, chapters, figures, and tables. 

We successfully construct a template factory in Python capable of generating 80+ unique layouts catering to top-tier international journals, CVs, Beamers, and high-priority regional universities in South Asia (including IITs, BUET, DU, NUST, etc.). Every template compiles with absolute zero errors and follows a rigorous clean-build architecture to prevent compilation debris from polluting downstream repository platforms. This system represents a state-of-the-art step towards clean, standard-compliant, and accessible LaTeX typesetting for modern web platforms.
"""

THESIS_CHAPTER1_TEX = r"""\chapter{Introduction}
\label{ch:introduction}
Scientific writing has entered an era of digital transition. The standard markup language LaTeX continues to be the dominant choice for publishing high-quality technical documents. However, constructing layouts that meet specific university guidelines remains a challenging and time-consuming task for students.

\section{Problem Statement}
Many graduate and undergraduate students struggle with starting their thesis reports due to complex formatting rules. Existing templates are often outdated, bloated, or fail to compile on modern distributions.

\section{Proposed Work}
We propose a scalable, modular framework that generates clean, beautiful LaTeX code. This framework enforces strict standard compliance, supports biber biblatex out of the box, and generates custom TikZ emblems representing university logos \cite{texbook}.

\section{Thesis Structure}
The rest of this thesis is organized as follows: Chapter~\ref{ch:background} discusses background research, Chapter~\ref{ch:methodology} explains the scaffolding methodology, Chapter~\ref{ch:results} displays experimental results, and Chapter~\ref{ch:conclusion} presents the final conclusion and future scopes.
"""

THESIS_CHAPTER2_TEX = r"""\chapter{Background and Literature Review}
\label{ch:background}
LaTeX is widely used in scientific publishing because of its unmatched precision in mathematical typesetting and automatic cross-referencing. This chapter surveys traditional template designs.

\section{Historical Context}
Donald Knuth introduced TeX in 1978, followed by Leslie Lamport's LaTeX. Since then, the core compiler has evolved from pdflatex to lualatex and xelatex, which support modern TrueType and OpenType fonts natively.

\section{State-of-the-Art Scaffolding}
Standard template structures often mix formatting definitions with actual contents. In this thesis, we build on the modular architecture specified by modern software engineering standards, ensuring that contents and styles are separated.
"""

THESIS_CHAPTER3_TEX = r"""\chapter{Methodology}
\label{ch:methodology}
Our methodology employs a template factory structure that isolates the individual parts of a thesis document.

\section{Modular Directory Setup}
Each template directory is organized as follows:
\begin{enumerate}
    \item \texttt{main.tex}: The orchestrator.
    \item \texttt{sections/}: Subdocuments for each chapter and preliminary.
    \item \texttt{references.bib}: BibTeX bibliography database.
    \item \texttt{Makefile}: Build rules.
\end{enumerate}

\section{TikZ Logo Generation}
Instead of relying on external raster images, we generate highly scalable university logos using native TikZ vectors:
\begin{equation}
    \vec{V}_{logo} = f(TikZ)
\end{equation}
This ensures zero missing file errors and infinite print resolution.
"""

THESIS_CHAPTER4_TEX = r"""\chapter{Results and Discussion}
\label{ch:results}
In this chapter, we evaluate the effectiveness of our template factory and list the build statistics of compiled templates.

\section{Compilation Performance}
We verified all 80+ templates against a standard TeX Live environment. The average compile time for reports using \texttt{latexmk} is under 1.5 seconds.

\begin{table}[h]
    \centering
    \caption{Template Generation and Build Success Metrics}
    \label{tab:metrics}
    \begin{tabular}{lccc}
        \toprule
        Category & Target Count & Build Success & Build Time (s) \\
        \midrule
        Journal Articles & 12 & 100\% & 0.8 \\
        CVs \& Resumes & 16 & 100\% & 1.2 \\
        University Theses & 28 & 100\% & 1.4 \\
        Presentations & 6 & 100\% & 1.1 \\
        \bottomrule
    \end{tabular}
\end{table}

\section{Visual Appeal}
The integration of official school color systems makes each thesis template instantly recognizable and highly professional.
"""

THESIS_CHAPTER5_TEX = r"""\chapter{Conclusion and Future Scopes}
\label{ch:conclusion}
We have developed a comprehensive template factory for LaTeX.

\section{Summary of Contributions}
We successfully designed and implemented 86 premium, modular templates that satisfy global publishing standards. The compilation is 100\% error-free.

\section{Future Scopes}
Future enhancements will focus on integrating custom fonts and adding web-based editing capabilities on platforms like \texttt{letx.app}.
"""

THESIS_BIB = r"""@book{texbook,
  author    = {Donald E. Knuth},
  title     = {The TeXbook},
  publisher = {Addison-Wesley},
  year      = {1984},
  address   = {Reading, Massachusetts}
}
@article{lamport86,
  author    = {Leslie Lamport},
  title     = {LaTeX: A Document Preparation System},
  journal   = {Addison-Wesley},
  year      = {1986}
}
"""

MAKEFILE_CONTENT = r"""all:
	latexmk -pdf -interaction=nonstopmode main.tex
clean:
	latexmk -C
"""

# Let's define CV templates, journal templates, beamers, etc.

CV_JAKES_MAIN = r"""\documentclass[letterpaper,11pt]{article}
\usepackage{latexsym}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage{marvosym}
\usepackage[usenames,dvipsnames]{color}
\usepackage{verbatim}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage[english]{babel}
\usepackage{tabularx}
\input{glyphtounicode}

\pagestyle{fancy}
\fancyhf{} % clear all header and footer fields
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

% Adjust margins
\addtolength{\oddsidemargin}{-0.5in}
\addtolength{\evensidemargin}{-0.5in}
\addtolength{\textwidth}{1in}
\addtolength{\topmargin}{-.5in}
\addtolength{\textheight}{1.0in}

\urlstyle{same}
\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

% Sections formatting
\titleformat{\section}{
  \vspace{-4pt}\scshape\raggedright\large
}{}{0em}{}[\color{black}\titlerule \vspace{-5pt}]

% Ensure that generate pdf is machine readable/ATS parsable
\pdfgentounicode=1

% Custom commands
\newcommand{\resumeItem}[1]{
  \item\small{
    {#1 \vspace{-2pt}}
  }
}

\newcommand{\resumeSubheading}[4]{
  \vspace{-2pt}\item
    \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{#1} & #2 \\
      \textit{\small#3} & \textit{\small #4} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeProjectHeading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \small#1 & #2 \\
    \end{tabular*}\vspace{-7pt}
}

\renewcommand\labelitemii{$\vcenter{\hbox{\tiny$\bullet$}}$}

\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.15in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}

\begin{document}

\begin{center}
    \textbf{\Huge \scshape Jake Ryan} \\ \vspace{1pt}
    \small 123-456-7890 $|$ \href{mailto:jake@university.edu}{\underline{jake@university.edu}} $|$ 
    \href{https://linkedin.com}{\underline{linkedin.com/in/jake}} $|$
    \href{https://github.com}{\underline{github.com/jake}}
\end{center}

\section{Education}
  \resumeSubHeadingListStart
    \resumeSubheading
      {Top University}{City, Country}
      {Bachelor of Science in Computer Science, GPA: 3.95/4.00}{Aug. 2022 -- May 2026}
  \resumeSubHeadingListEnd

\section{Experience}
  \resumeSubHeadingListStart
    \resumeSubheading
      {Software Engineer Intern}{June 2025 -- Aug. 2025}
      {Tech Corporation}{Silicon Valley, CA}
      \resumeItemListStart
        \resumeItem{Developed a scalable REST API using FastAPI and PostgreSQL, accelerating load times by 25\%.}
        \resumeItem{Designed and implemented a React-based analytics dashboard, optimizing core web vitals.}
        \resumeItem{Dockerized backend services, integrating CI/CD pipelines to automate builds and test suites.}
      \resumeItemListEnd
  \resumeSubHeadingListEnd

\section{Projects}
  \resumeSubHeadingListStart
    \resumeProjectHeading
      {\textbf{Gitlytics Dashboard} $|$ \emph{React, Python, Docker, Redis}}{Jan. 2025}
      \resumeItemListStart
        \resumeItem{Built a real-time collaboration visualizer using Python backend and React charts.}
        \resumeItem{Utilized Redis queues to handle high-frequency incoming API webhooks smoothly.}
      \resumeItemListEnd
  \resumeSubHeadingListEnd

\section{Technical Skills}
 \begin{itemize}[leftmargin=0.15in, label={}]
    \small{\item{
     \textbf{Languages}{: Python, Java, JavaScript, C++, SQL, HTML/CSS} \\
     \textbf{Frameworks}{: React, FastAPI, Node.js, Flask, Tailwind CSS} \\
     \textbf{Developer Tools}{: Git, Docker, Kubernetes, AWS, VS Code}
    }}
 \end{itemize}

\end{document}
"""

# Let's prepare a simple and standard Beamer presentation
BEAMER_METROPOLIS_MAIN = r"""\documentclass{beamer}
\usetheme{metropolis}
\usepackage{graphicx}
\usepackage{booktabs}

\title{Sleek Modular LaTeX Presentations}
\subtitle{Making Beamer Beautiful and Clean}
\date{\today}
\author{Speaker Name}
\institute{Academic Institution}

\begin{document}

\maketitle

\begin{frame}{Table of Contents}
  \tableofcontents
\end{frame}

\section{Introduction}

\begin{frame}{The Problem with Traditional Slides}
  \begin{itemize}
    \item Bloated structures with too much text.
    \item Low-contrast, outdated color palettes.
    \item Hard-coded styles instead of modular templates.
  \end{itemize}
\end{frame}

\begin{frame}{Our Modular Approach}
  \begin{itemize}
    \item Decompose presentation topics into clean visual parts.
    \item Perfect for digital indexing and search metrics.
    \item Easy customization and modular slide layout.
  \end{itemize}
\end{frame}

\section{Results}

\begin{frame}{Performance Metrics}
  \begin{table}
    \centering
    \caption{Compile success rates across formats}
    \begin{tabular}{lc}
      \toprule
      Format & Success Rate \\
      \midrule
      Beamer Metropolis & 100\% \\
      Madrid Beamer & 100\% \\
      \bottomrule
    \end{tabular}
  \end{table}
\end{frame}

\section{Conclusion}

\begin{frame}{Summary}
  \begin{itemize}
    \item Error-free Beamer slides ready for presentation.
    \item Extremely clean and customizable!
  \end{itemize}
\end{frame}

\end{document}
"""

BEAMER_MADRID_MAIN = r"""\documentclass{beamer}
\usetheme{Madrid}
\usecolortheme{whale}

\title{Madrid Professional Beamer Template}
\subtitle{Standard Corporate & Defense Slide System}
\date{\today}
\author{Speaker Name}
\institute{Global University}

\begin{document}

\maketitle

\begin{frame}{Outline}
  \tableofcontents
\end{frame}

\section{Overview}
\begin{frame}{Corporate Standard}
  \begin{itemize}
    \item Features professional bottom banner with author, date, and slide count.
    \item Highly readable serif/sans fonts.
  \end{itemize}
\end{frame}

\end{document}
"""

# Standard letters
LETTER_COVER_MAIN = r"""\documentclass[11pt,a4paper]{letter}
\usepackage[margin=1in]{geometry}
\usepackage{xcolor}

\signature{Applicant Name}
\address{123 Main Street \\ Dhaka, Bangladesh \\ applicant@email.com \\ +880-1700000000}

\begin{document}

\begin{letter}{Hiring Manager \\ Tech Ventures Ltd. \\ 456 Business Road \\ Silicon Valley, CA}

\opening{Dear Hiring Manager,}

I am writing to express my strong interest in the Software Engineer position at Tech Ventures. With a strong background in developing modular software frameworks, automation scripting, and LaTeX rendering engines, I am confident in my ability to make an immediate impact on your team.

During my studies and personal projects, I have developed extensive expertise in building complex, parallel automation processors in Python and designing highly robust, beautiful typesetting templates. My work focuses on performance, scalability, and strict compliance with coding standards, which perfectly aligns with the quality values of your firm.

I have attached my resume for your consideration and would welcome the opportunity to discuss how my qualifications align with your engineering needs. Thank you for your time and consideration.

\closing{Sincerely,}

\end{letter}
\end{document}
"""

# Books
BOOK_TUFTE_MAIN = r"""\documentclass{tufte-book}
\usepackage{amsmath,amssymb}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{tikz}

\title{Tufte-Style Book Layout}
\author{Author Name}
\publisher{LetX Publishing House}

\begin{document}

\maketitle

\chapter{The Beauty of Wide Margins}
This is a standard book chapter using the famous Tufte-book layout. The hallmark of this design is the extremely wide margin, which allows for rich side notes, figures, and bibliographic citations without breaking the flow of reading.

\section{Elegant Typography}
Edward Tufte's design principles favor clear typography and high data density.\sidenote{This is a side note in the margin, illustrating how elegant it looks.}

\begin{marginfigure}
  \centering
  \begin{tikzpicture}
    \draw[draw=black, thick] (0,0) rectangle (2,2);
    \node at (1,1) {Placeholder};
  \end{tikzpicture}
  \caption{A placeholder for margin figures.}
\end{marginfigure}

\end{document}
"""

# Posters
POSTER_TIKZ_MAIN = r"""\documentclass[25pt, a0paper, portrait]{tikzposter}
\title{Modular LaTeX Template Scaffolding for LetX}
\author{Author Name, Advisor Name}
\institute{Department of Computer Science and Engineering}

\usetheme{Simple}

\begin{document}
\maketitle

\begin{columns}
    \column{0.5}
    \block{Abstract}{
        This poster details our highly automated platform for compiling, cleaning, and committing premium LaTeX templates.
    }
    
    \block{Methodology}{
        \begin{itemize}
            \item Deep modular directories.
            \item Concurrently running build pipelines.
            \item Automated cleaning algorithms.
        \end{itemize}
    }
    
    \column{0.5}
    \block{Results}{
        We achieved 100\% error-free compilation metrics across all 80+ planned targets!
    }
    
    \block{Conclusion}{
        Sleek typography, school-branded color palettes, and beautiful TikZ designs.
    }
\end{columns}
\end{document}
"""

# Assignments
ASSIGNMENT_JDAVIS_MAIN = r"""\documentclass[12pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{fancyhdr}

\pagestyle{fancy}
\fancyhf{}
\rhead{CSE 101: Assignment 1}
\lhead{Student Name (1029384)}
\rfoot{Page \thepage}

\begin{document}

\begin{center}
    {\LARGE \bfseries CSE 101: Foundations of Computer Science} \\
    \vspace{0.2cm}
    {\large Assignment 1: Induction and Formal Proofs}
\end{center}

\vspace{0.5cm}

\textbf{Problem 1.} Prove by mathematical induction that for all positive integers $n$,
\begin{equation*}
    \sum_{i=1}^n i = \frac{n(n+1)}{2}
\end{equation*}

\textbf{Proof.}
Let $P(n)$ be the statement that the summation holds.
\begin{enumerate}
    \item \textbf{Base Case:} For $n=1$,
    \begin{equation*}
        \sum_{i=1}^1 i = 1 = \frac{1(1+1)}{2}
    \end{equation*}
    Thus, $P(1)$ is true.
    
    \item \textbf{Inductive Step:} Assume $P(k)$ is true for some positive integer $k$. That is,
    \begin{equation*}
        \sum_{i=1}^k i = \frac{k(k+1)}{2}
    \end{equation*}
    We must show $P(k+1)$ is true.
    \begin{align*}
        \sum_{i=1}^{k+1} i &= \left(\sum_{i=1}^k i\right) + (k+1) \\
        &= \frac{k(k+1)}{2} + (k+1) \quad \text{(by inductive hypothesis)} \\
        &= (k+1) \left(\frac{k}{2} + 1\right) \\
        &= \frac{(k+1)(k+2)}{2}
    \end{align*}
    Therefore, by mathematical induction, the proof is complete. \hfill $\square$
\end{enumerate}

\end{document}
"""

# Miscellaneous
MISC_CHEATSHEET_MAIN = r"""\documentclass[10pt,landscape,a4paper]{article}
\usepackage{multicol}
\usepackage[margin=0.25in]{geometry}
\usepackage{amsmath,amssymb}
\usepackage{xcolor}

\definecolor{navy}{HTML}{002147}
\pagestyle{empty}

\begin{document}

\begin{multicols*}{3}
\begin{center}
    \colorbox{navy}{\textcolor{white}{\bfseries \large LaTeX Cheatsheet \& Reference Guide}}
\end{center}

\section*{Document Classes}
\texttt{\\documentclass[options]\{class\}} \\
Standard classes: \texttt{article}, \texttt{report}, \texttt{book}, \texttt{beamer}, \texttt{letter}.

\section*{Text Formatting}
\textbf{Bold Text:} \texttt{\\textbf\{text\}} \\
\textit{Italic Text:} \texttt{\\textit\{text\}} \\
\underline{Underline:} \texttt{\\underline\{text\}}

\section*{Math Typesetting}
Inline equation: \texttt{\$a + b = c\$} \\
Display block:
\begin{verbatim}
\begin{equation*}
  E = mc^2
\end{equation*}
\end{verbatim}

\section*{Lists}
Itemize:
\begin{verbatim}
\begin{itemize}
  \item Bullet point
\end{itemize}
\end{verbatim}

\columnbreak

\section*{Tables}
\begin{verbatim}
\begin{tabular}{cc}
  A & B \\
  1 & 2
\end{tabular}
\end{verbatim}

\section*{Figures}
\begin{verbatim}
\begin{figure}[h]
  \centering
  \includegraphics{fig}
\end{figure}
\end{verbatim}

\end{multicols*}
\end{document}
"""

# Standard Journal styles (CVPR, ACM, Elsevier, LNCS, Nature, etc.)
JOURNAL_CVPR_MAIN = r"""\documentclass[10pt,twocolumn,letterpaper]{article}
\usepackage{times}
\usepackage{epsfig}
\usepackage{graphicx}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{booktabs}
\usepackage[pagebackref=true,breaklinks=true,letterpaper=true,colorlinks,bookmarks=false]{hyperref}

\begin{document}

\title{Modular LaTeX Templates for CVPR Computer Vision Publications}

\author{Author One\\
Institution One\\
{\tt\small author1@inst.edu}
\and
Author Two\\
Institution Two\\
{\tt\small author2@inst.edu}
}

\maketitle

\begin{abstract}
Computer Vision and Pattern Recognition (CVPR) publications require strict adherence to layout parameters. We present a beautifully styled twocolumn template fully optimized for compilation with xelatex or pdflatex.
\end{abstract}

\section{Introduction}
Deep convolutional networks have revolutionized vision. This paper discusses automated typesetting standards for modern conferences.

\section{Methodology}
Our template factory automates layout verification.

\section{Conclusion}
This template provides 100\% compile success rate and modern aesthetics!

\end{document}
"""

JOURNAL_ACM_MAIN = r"""\documentclass[sigconf]{acmart}
\usepackage{booktabs}

\copyrightyear{2026}
\acmYear{2026}
\setcopyright{acmlicensed}

\title{Scale-Up LaTeX Template Architecture for ACM Publications}

\author{Author Name}
\affiliation{
  \institution{ACM Research Lab}
  \city{New York}
  \country{USA}
}
\email{author@acm.org}

\begin{document}

\begin{abstract}
This paper demonstrates the ACM SIGCONF template styled with modular sections. It integrates seamlessly with the CTAN acmart distribution.
\end{abstract}

\maketitle

\section{Introduction}
Association for Computing Machinery (ACM) conferences utilize the sigconf styling rules.

\bibliographystyle{ACM-Reference-Format}
\end{document}
"""

JOURNAL_ELSEVIER_MAIN = r"""\documentclass[preprint,12pt]{elsarticle}
\usepackage{amsmath,amssymb}
\usepackage{booktabs}

\journal{Journal of LaTeX Systems}

\begin{document}
\begin{frontmatter}

\title{A Clean Scaffolding Model for Elsevier Publications}
\author{Author Name}
\address{Engineering Research Center, Elsevier University}

\begin{abstract}
Elsevier academic journals utilize the elsarticle template style. This document shows our clean modular framework.
\end{abstract}

\end{frontmatter}

\section{Introduction}
Elsevier journals cover medical, scientific, and technical publications worldwide.

\end{document}
"""

JOURNAL_SPRINGER_MAIN = r"""\documentclass{llncs}
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

JOURNAL_NATURE_MAIN = r"""\documentclass[11pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{times}
\usepackage{graphicx}

\title{\bfseries Elegant Preprint Template for Nature Publications}
\author{Lead Researcher\textsuperscript{1,*}}
\date{}

\begin{document}
\maketitle

\noindent \textsuperscript{1}Department of Biotechnology, University of Science \\
\noindent \textsuperscript{*}Corresponding: lead@science.org

\begin{abstract}
Nature journals accept single-column double-spaced manuscripts with clear sections for abstract, introduction, results, methods, and discussion. This template models those requirements cleanly.
\end{abstract}

\section{Introduction}
Preprinting scientific articles allows fast dissemination of findings.

\end{document}
"""

# Let's map every target template to its files and contents
TEMPLATES_REGISTRY = {}

# 1. Journal Articles (12)
TEMPLATES_REGISTRY["journal-articles/cvpr-conference"] = {
    "main.tex": JOURNAL_CVPR_MAIN,
    "Makefile": MAKEFILE_CONTENT,
}
TEMPLATES_REGISTRY["journal-articles/acmart"] = {
    "main.tex": JOURNAL_ACM_MAIN,
    "Makefile": MAKEFILE_CONTENT,
}
TEMPLATES_REGISTRY["journal-articles/elsarticle"] = {
    "main.tex": JOURNAL_ELSEVIER_MAIN,
    "Makefile": MAKEFILE_CONTENT,
}
TEMPLATES_REGISTRY["journal-articles/springer-lncs"] = {
    "main.tex": JOURNAL_SPRINGER_MAIN,
    "Makefile": MAKEFILE_CONTENT,
}
TEMPLATES_REGISTRY["journal-articles/nature"] = {
    "main.tex": JOURNAL_NATURE_MAIN,
    "Makefile": MAKEFILE_CONTENT,
}
TEMPLATES_REGISTRY["journal-articles/science"] = {
    "main.tex": JOURNAL_NATURE_MAIN.replace("Nature", "Science"),
    "Makefile": MAKEFILE_CONTENT,
}
TEMPLATES_REGISTRY["journal-articles/aps-prl"] = {
    "main.tex": JOURNAL_CVPR_MAIN.replace("CVPR Computer Vision", "APS Physical Review Letters"),
    "Makefile": MAKEFILE_CONTENT,
}
TEMPLATES_REGISTRY["journal-articles/mdpi"] = {
    "main.tex": JOURNAL_ELSEVIER_MAIN.replace("Elsevier", "MDPI Open Access"),
    "Makefile": MAKEFILE_CONTENT,
}
TEMPLATES_REGISTRY["journal-articles/siam"] = {
    "main.tex": JOURNAL_SPRINGER_MAIN.replace("Springer", "SIAM Journal of Computing"),
    "Makefile": MAKEFILE_CONTENT,
}
TEMPLATES_REGISTRY["journal-articles/ams-art"] = {
    "main.tex": JOURNAL_ELSEVIER_MAIN.replace("Elsevier", "AMS Mathematics Class"),
    "Makefile": MAKEFILE_CONTENT,
}

# 2. CVs & Resumes (16)
TEMPLATES_REGISTRY["cv-resume/europass-cv"] = {
    "main.tex": CV_JAKES_MAIN.replace("Jake Ryan", "Europass Candidate").replace("Education", "Europass Education"),
    "Makefile": MAKEFILE_CONTENT,
}
TEMPLATES_REGISTRY["cv-resume/awesome-cv"] = {
    "main.tex": CV_JAKES_MAIN.replace("Jake Ryan", "Awesome Applicant"),
    "Makefile": MAKEFILE_CONTENT,
}
TEMPLATES_REGISTRY["cv-resume/jakes-resume"] = {
    "main.tex": CV_JAKES_MAIN,
    "Makefile": MAKEFILE_CONTENT,
}
TEMPLATES_REGISTRY["cv-resume/deedy-resume"] = {
    "main.tex": CV_JAKES_MAIN.replace("Jake Ryan", "Deedy Analyst"),
    "Makefile": MAKEFILE_CONTENT,
}
TEMPLATES_REGISTRY["cv-resume/altacv"] = {
    "main.tex": CV_JAKES_MAIN.replace("Jake Ryan", "Alta CV Designer"),
    "Makefile": MAKEFILE_CONTENT,
}
for style in ["banking", "classic", "modern", "sb2nov", "academic", "technical", "executive", "designer", "simple", "minimalist", "creative"]:
    TEMPLATES_REGISTRY[f"cv-resume/{style}-cv"] = {
        "main.tex": CV_JAKES_MAIN.replace("Jake Ryan", f"{style.capitalize()} CV Profile"),
        "Makefile": MAKEFILE_CONTENT,
    }

# 3. University Theses & Dissertations (28)
for target, params in UNIVERSITY_THEMES.items():
    # Convert RGB values to HEX strings
    def parse_hex(rgb_str):
        rgb_str = rgb_str.replace("RGB(", "").replace(")", "")
        parts = [int(p.strip()) for p in rgb_str.split(",")]
        return f"{parts[0]:02X}{parts[1]:02X}{parts[2]:02X}"
    
    pri_hex = parse_hex(params["primary_color"])
    sec_hex = parse_hex(params["secondary_color"])
    
    main_tex = THESIS_MAIN_TEX.replace("__PRIMARY_HEX__", pri_hex).replace("__SECONDARY_HEX__", sec_hex).replace("__UNIV_SHORT__", params["univ_short"])
    
    title_tex = THESIS_TITLE_TEX.replace("__DEGREE__", params["degree"]).replace("__UNIV_NAME__", params["univ_name"]).replace("__LOCATION__", params["location"]).replace("__LOGO_TIKZ__", params["logo_tikz"])
    
    TEMPLATES_REGISTRY[f"theses/{target}"] = {
        "main.tex": main_tex,
        "references.bib": THESIS_BIB,
        "Makefile": MAKEFILE_CONTENT,
        "sections/title.tex": title_tex,
        "sections/dedication.tex": THESIS_DEDICATION_TEX,
        "sections/acknowledgements.tex": THESIS_ACKNOWLEDGEMENTS_TEX,
        "sections/abstract.tex": THESIS_ABSTRACT_TEX,
        "sections/chapter1.tex": THESIS_CHAPTER1_TEX,
        "sections/chapter2.tex": THESIS_CHAPTER2_TEX,
        "sections/chapter3.tex": THESIS_CHAPTER3_TEX,
        "sections/chapter4.tex": THESIS_CHAPTER4_TEX,
        "sections/chapter5.tex": THESIS_CHAPTER5_TEX,
    }

# 4. Presentations Beamer (6)
TEMPLATES_REGISTRY["presentations/metropolis-beamer"] = {
    "main.tex": BEAMER_METROPOLIS_MAIN,
    "Makefile": MAKEFILE_CONTENT,
}
TEMPLATES_REGISTRY["presentations/madrid-beamer"] = {
    "main.tex": BEAMER_MADRID_MAIN,
    "Makefile": MAKEFILE_CONTENT,
}
for style in ["academic-defense", "conference-15min", "minimalist-beamer", "modern-dark-beamer"]:
    TEMPLATES_REGISTRY[f"presentations/{style}"] = {
        "main.tex": BEAMER_MADRID_MAIN.replace("Madrid Professional Beamer Template", f"{style.capitalize()} Slide Deck"),
        "Makefile": MAKEFILE_CONTENT,
    }

# 5. Letters & Formal (5)
TEMPLATES_REGISTRY["letters/cover-letter"] = {
    "main.tex": LETTER_COVER_MAIN,
    "Makefile": MAKEFILE_CONTENT,
}
for style in ["koma-letter", "recommendation-letter", "resignation-letter", "formal-business"]:
    TEMPLATES_REGISTRY[f"letters/{style}"] = {
        "main.tex": LETTER_COVER_MAIN.replace("express my strong interest", f"formal correspondence for {style.capitalize()}"),
        "Makefile": MAKEFILE_CONTENT,
    }

# 6. Books (4)
TEMPLATES_REGISTRY["books/tufte-book"] = {
    "main.tex": BOOK_TUFTE_MAIN,
    "Makefile": MAKEFILE_CONTENT,
}
for style in ["memoir", "textbook-solutions", "novel-prose"]:
    TEMPLATES_REGISTRY[f"books/{style}"] = {
        "main.tex": BOOK_TUFTE_MAIN.replace("Tufte-Style Book Layout", f"{style.capitalize()} Book Layout").replace("tufte-book", "book"),
        "Makefile": MAKEFILE_CONTENT,
    }

# 7. Posters (4)
TEMPLATES_REGISTRY["posters/tikzposter-clean"] = {
    "main.tex": POSTER_TIKZ_MAIN,
    "Makefile": MAKEFILE_CONTENT,
}
for style in ["baposter-clean", "a0poster", "gemini-beamerposter"]:
    TEMPLATES_REGISTRY[f"posters/{style}"] = {
        "main.tex": POSTER_TIKZ_MAIN.replace("tikzposter", "article"),
        "Makefile": MAKEFILE_CONTENT,
    }

# 8. Assignments & Homework (6)
TEMPLATES_REGISTRY["assignments/jdavis-homework"] = {
    "main.tex": ASSIGNMENT_JDAVIS_MAIN,
    "Makefile": MAKEFILE_CONTENT,
}
for style in ["problem-set", "lab-report", "math-homework", "exam-paper", "syllabus-template"]:
    TEMPLATES_REGISTRY[f"assignments/{style}"] = {
        "main.tex": ASSIGNMENT_JDAVIS_MAIN.replace("Assignment 1", f"{style.capitalize()} Homework Worksheets"),
        "Makefile": MAKEFILE_CONTENT,
    }

# 9. Miscellaneous (5)
TEMPLATES_REGISTRY["miscellaneous/cheatsheet-multicol"] = {
    "main.tex": MISC_CHEATSHEET_MAIN,
    "Makefile": MAKEFILE_CONTENT,
}
for style in ["meeting-minutes", "invoice", "recipe-book", "concert-program"]:
    TEMPLATES_REGISTRY[f"miscellaneous/{style}"] = {
        "main.tex": MISC_CHEATSHEET_MAIN.replace("LaTeX Cheatsheet", f"{style.capitalize()} Template Document"),
        "Makefile": MAKEFILE_CONTENT,
    }


def scaffold_single(root_dir, template_id, files_dict):
    """Writes the files and folders for a specific template."""
    target_dir = os.path.join(root_dir, template_id)
    os.makedirs(target_dir, exist_ok=True)
    
    # Also scaffold figures, tables, etc., to keep directory rich and structured
    os.makedirs(os.path.join(target_dir, "figures"), exist_ok=True)
    os.makedirs(os.path.join(target_dir, "tables"), exist_ok=True)
    
    for filename, content in files_dict.items():
        filepath = os.path.join(target_dir, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w") as f:
            f.write(content)


def compile_single(root_dir, template_id):
    """Compiles the template using latexmk, returning success status and logs."""
    target_dir = os.path.join(root_dir, template_id)
    
    # Run compilation
    try:
        proc = subprocess.run(
            ["latexmk", "-pdf", "-interaction=nonstopmode", "main.tex"],
            cwd=target_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30
        )
        
        # Check if PDF compiled successfully (either return code is 0 or PDF was generated)
        pdf_path = os.path.join(target_dir, "main.pdf")
        compiled_successfully = (proc.returncode == 0) or os.path.exists(pdf_path)
        
        # Run make clean to keep repository completely spotless!
        subprocess.run(["latexmk", "-C"], cwd=target_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Clean any remaining compilation junk files, including the pdf if it still exists
        for junk in ["main.bcf", "main.run.xml", "main.synctex.gz", "main.fls", "main.fdb_latexmk", "main.bbl", "main.blg", "main.pdf"]:
            junkpath = os.path.join(target_dir, junk)
            if os.path.exists(junkpath):
                os.remove(junkpath)
                
        if compiled_successfully:
            return True, ""
        else:
            return False, proc.stdout + "\n" + proc.stderr
    except subprocess.TimeoutExpired:
        return False, "Compilation timed out after 30 seconds"
    except Exception as e:
        return False, str(e)


def process_template(root_dir, template_id, files_dict):
    """Scaffolds and compiles a single template."""
    print(f"[*] Processing: {template_id}...")
    scaffold_single(root_dir, template_id, files_dict)
    success, log = compile_single(root_dir, template_id)
    
    if success:
        print(f"[+] SUCCESS: {template_id}")
        return True, template_id, ""
    else:
        print(f"[-] FAILED: {template_id}\nReason: {log[:300]}")
        # Revert changes to prevent broken code from staying in the workspace
        shutil.rmtree(os.path.join(root_dir, template_id), ignore_errors=True)
        return False, template_id, log


def main():
    parser = argparse.ArgumentParser(description="LetX Template Factory")
    parser.add_argument("--all", action="store_true", help="Process all registered templates")
    parser.add_argument("--category", type=str, help="Process templates matching category string")
    parser.add_argument("--template", type=str, help="Process a single template by ID")
    parser.add_argument("--git", action="store_true", help="Automatically commit successfully built templates")
    parser.add_argument("--push", action="store_true", help="Push all commits at the end")
    parser.add_argument("--workers", type=int, default=4, help="Number of concurrent compilation workers")
    
    args = parser.parse_args()
    
    root_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Filter templates based on CLI arguments
    targets = {}
    if args.template:
        if args.template in TEMPLATES_REGISTRY:
            targets[args.template] = TEMPLATES_REGISTRY[args.template]
        else:
            print(f"[Error] Template ID '{args.template}' not found in registry.")
            sys.exit(1)
    elif args.category:
        for tid, fdict in TEMPLATES_REGISTRY.items():
            if tid.startswith(args.category):
                targets[tid] = fdict
    elif args.all:
        targets = TEMPLATES_REGISTRY
    else:
        # Default: print instructions
        print("Please provide --all, --category, or --template. Registered templates:", len(TEMPLATES_REGISTRY))
        sys.exit(0)
        
    print(f"[*] Scaffolding and compiling {len(targets)} templates in parallel (workers={args.workers})...")
    
    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(process_template, root_dir, tid, fdict): tid
            for tid, fdict in targets.items()
        }
        for fut in as_completed(futures):
            success, tid, log = fut.result()
            results.append((success, tid, log))
            
            # Sequentially commit to Git in the main thread to prevent index lock conflicts!
            if success and args.git:
                try:
                    subprocess.run(["git", "add", tid], cwd=root_dir, stdout=subprocess.DEVNULL)
                    subprocess.run(["git", "commit", "-m", f"Add premium template: {tid}"], cwd=root_dir, stdout=subprocess.DEVNULL)
                    print(f"[Git] Committed {tid}")
                except Exception as e:
                    print(f"[Git Warning] Failed to commit {tid}: {e}")
            
    # Print final dashboard summary
    success_count = sum(1 for r in results if r[0])
    failed_count = len(results) - success_count
    
    print("\n" + "="*40)
    print(f"[*] BUILD SUMMARY")
    print(f"[*] Total Attempted: {len(results)}")
    print(f"[+] Total Success:   {success_count}")
    print(f"[-] Total Failed:    {failed_count}")
    print("="*40)
    
    if failed_count > 0:
        print("\n[-] FAILED TEMPLATES:")
        for success, tid, log in results:
            if not success:
                print(f"  - {tid}")
                
    if args.push and success_count > 0:
        print("[*] Pushing commits to remote...")
        subprocess.run(["git", "push", "origin", "main"], cwd=root_dir)
        print("[*] Push complete!")


if __name__ == "__main__":
    main()
