#! python3

#from textwrap import dedent

from Calculation import *

with open('report.tex', 'w') as file:
	file.write("\\documentclass[12pt,draft]{article}%\n"
				"\\usepackage{graphicx,amsmath}%\n"
				"\\usepackage[top=1in, bottom = 1.25in, left=0.25in, right=0.25in]{geometry}%\n"
				"\\pagestyle{headings}%\n"
				)
	file.write("%\n"*3)
	file.write("\\begin{document}%\n")

	file.write("\\subsection*{{Calculation of {0} }}".format(Title))













	file.write("\n\n\\end{document}%\n")
