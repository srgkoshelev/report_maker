#! python3

#from textwrap import dedent



from Calculation import *
import subprocess
import os, fnmatch
from wand.image import Image
from wand.color import Color

with open('report.tex', 'w') as file:
	file.write(r"\documentclass[12pt,draft]{article}" "%\n"
				r"\usepackage{graphicx,amsmath,enumitem}" "%\n"
				r"\usepackage[top=1in, bottom = 1.25in, left=0.25in, right=0.25in]{geometry}" "%\n"
				r"\pagestyle{headings}" "%\n"
				)
	file.write("%\n"*3)
	file.write(r"\begin{document}" "%\n")

	file.write("\\section*{{ {0} }}".format(Title))
	file.write('Assumptions\n')
	file.write(r"\begin{enumerate}" "%\n")
	for item in Assumptions:
		file.write(r"\item " + str(item) + "\n")
	file.write(r"\end{enumerate}" "%\n")

	file.write("Piping spool consists of {0} sections:\n".format(len(Piping)))
	file.write(r"\begin{enumerate}" "%\n")
	for pipe in Piping:
		pipe['D'].display_unit = 'inch'
		pipe['L'].display_unit = 'ft'
		file.write(r"\item OD = " + '{0:L}'.format(pipe['D']) + 
					", L = " + '{0:.3L}'.format(pipe['L']) +
					"\n")
	file.write(r"\end{enumerate}" "%\n")
	file.write("Trapped volume condition for " + fluid.capitalize() + " are:" +
			" temperature $" + '{0:.3L}'.format(Temp) + '$'
			" and pressure $" + '{0:.3L}'.format(P_fr) + '$'
			" for relief set at $" + '{0:.3L}'.format(P_set) + '$'
			"\n\n")
	file.write("Considering natural convection for each section:\n")
	file.write(r"\begin{enumerate}[label={Section \arabic*},align=left]" "%\n")
	
	Q_tot = 0*ft**3/min
	for i in range(len(Surfaces)):
		Case = Cases[i]
		Surface = Surfaces[i]
		h = Nu(Air_std, Surface, Case)['h']
		Nuss = Nu(Air_std, Surface, Case)['Nu']	
		A_surf = Surface['Dim']*Surface['Dim_sec']
		q_conv = h*(T_room-Temp) #"W/m^2 convective heat load"
		q_conv.display_unit = 'W/m2'
		q_conv_disp = q_conv*A_surf
		q_conv_disp.display_unit = 'W'
		q_rad = rad_hl(T_hot = T_room, T_cold = Temp)['q0']
		q_rad_disp = q_rad*A_surf
		q_rad_disp.display_unit = 'W'
		U_coef = (q_conv+q_rad)/(T_room-Temp) #convert(W/m^2-K,kJ/hr-m^2-K)
		U_coef.display_unit = 'kJ/(hr*m2*K)'
		Q_a = 0.383*(328*K - Temp)/(922*K-Temp)*G_i*U_coef*A_surf # "m^3/hr of air"
		Q_a.display_unit = 'ft3/min'
		Q_tot += Q_a

		file.write(r'\item '+'\n\\hfill\n'
			'\\begin{itemize}' '\n')		
		file.write(r'\item Nusselt number: $' + '{0:.3}'.format(Nuss) + '$\n'
			r'\item heat transfer coefficient: $' + '{0:.3L}'.format(h) + '$\n'
			r'\item Convective heat load: $' + '{0:.3L}'.format(q_conv_disp) + '$\n'
			r'\item Radiation heat load: $' + '{0:.3L}'.format(q_rad_disp) + '$\n'
			r'\end{itemize}' '\n'
			)
	file.write(r"\end{enumerate}" "%\n\n")

	file.write('Required relief capacity ${0:.3L}$ is less than available ${1:.3L}$ of the relief device. The piping is safe to operate.'.format(Q_tot, Q_avail))
	file.write("\n\n" r"\end{document}%" "\n")


def create_pdf(input_filename):
    process = subprocess.Popen([
        'pdflatex',   # Or maybe 'C:\\Program Files\\MikTex\\miktex\\bin\\latex.exe
        '-quiet', #Remove excess output
        #'-output-format=pdf',
        #'-job-name=' + output_filename,
        input_filename])
    process.wait()

create_pdf ('report.tex')

