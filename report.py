#! python3

from Calculation import *
import subprocess
import os, fnmatch
from wand.image import Image
from wand.color import Color

def quantistr (Quant):
	try:
		return '${0:.3L}$'.format(Quant)
	except ValueError:
		try: 
			return '{0:.3g}'.format(Quant)
		except ValueError:
			return str(Quant)





with open('report.tex', 'w') as file:
	file.write(r"\documentclass[12pt,draft]{article}" "%\n"
				r"\usepackage{graphicx,amsmath,enumitem,multicol}" "%\n"
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

	# file.write("Piping spool consists of {0} sections:\n".format(len(Piping)))
	# max_rows = 5
	# if len(Piping) > max_rows:
	# 	file.write("\\begin{{multicols}}{{ {0} }} \n".format(ceil(len(Piping)/max_rows)))
	# 	multicol = True
	# file.write(r"\begin{enumerate}" "%\n")
	# for pipe in Piping:
	# 	pipe['OD'].display_unit = 'inch'
	# 	pipe['L'].display_unit = 'ft'
	# 	file.write(r"\item OD = " + '{0:L}'.format(pipe['D']) + 
	# 				", L = " + '{0:.3L}'.format(pipe['L']) +
	# 				"\n")
	# file.write(r"\end{enumerate}" "%\n")
	# if multicol: file.write("\\end{multicols} \n")


	file.write("Trapped volume condition for " + fluid.capitalize() + " piping are:\n")
	file.write("\\begin{itemize}\n")
	file.write("\\item " + "Relief set pressure: $" + '{0:.3L}'.format(P_set) + '$\n')
	file.write("\\item " + "Flow rating pressure: $P_{{fr}} = 1.1\\times P_{{set}} = {0:.3L} $ \n".format(P_fr))
	file.write("\\item " + "Temperature for flow capacity calculation (CGA S-1.3 2008, 6.1.3): $" + '{0:.3L}'.format(Temp) + '$\n')
	file.write("\\end{itemize}")
	# if F_factor == 1:
	# 	file.write("Pressure drop through the piping is assumed negligible, i.e. F = 1.\n")

	file.write("Calculation results for natural convection for horizontal and vertical convection (Handbook of Heat Transfer, Rohsenow, Hartnet, Cho, 1998):\n\n\\medskip\n\n")

	keys = [('OD', 1*inch), ('L', 1*ft), ('Orientation', )] #Icouldn't find a way to transform 'ft' string into unit ft

	if Danger == 'Vacuum loss':
		keys.append([('q_conv', 1*W), ('q_rad', 1*W)])

	elif Danger == 'Air condensation':
		keys.append(('q_cond', 1*W))
	Header = ['Section']
	for key in keys:
		tex_key = key[0]
		if '_' in key[0]:
			tex_key = '$' + tex_key.split('_')[0] + '_{' + ','.join(tex_key.split('_')[1:]) + '}$'
		if len(key) > 1:
			tex_key += ',' + '{0:L}'.format(key[1])[3:] #Dirty hack - i remove 3 symbols '1.0' from the line
		Header.append(tex_key)


	file.write("\\begin{center}\n")
	file.write(r"\begin{tabular}{ |"+"c|"*len(Header) + " }\n")
	file.write("\\hline \n")
	file.write(' & '.join(Header) + r'\\''\n')
	file.write("\\hline \n")
	for number, Pipe in enumerate (Piping):
		table_line = [str(number + 1)]
		for key in keys:
			if len(key) == 1:
				table_line.append(str(Pipe[key[0]]))
			else:
				table_line.append('{:.4g}'.format(Pipe[key[0]]/key[1]))
		file.write(' & '.join(table_line) + r'\\' '\n')
		file.write("\\hline \n")
	file.write("\\end{tabular}\n\n")
	file.write("\\end{center}\n")





	# file.write("\\begin{center}\n")
	# file.write(r"\begin{tabular}{ |"+"c|"*len(Results) + " }\n")
	# file.write("\\hline \n")
	# Header = []
	# order = list(Results[0].keys())
	# order.sort()
	# for key in order:
	# 	if '_' in key:
	# 		key = '$' + key.split('_')[0] + '_{' + ','.join(key.split('_')[1:]) + '}$'
	# 	Header.append(key)
	# # print(Header)
	# file.write(' & '.join(Header) + r'\\''\n')
	# file.write("\\hline \n")
	# for section in Results[1:]:
	# 	file.write(' & '.join([quantistr(section[x]) for x in order]) + r'\\''\n')
	# 	file.write("\\hline \n")
	# file.write("\\end{tabular}\n\n")
	# file.write("\\end{center}\n")

	file.write("\\medskip\n\n")

	file.write("\\begin{itemize}\n")
	file.write("\\item Required relief capacity ${0:.3L}< {1:.3L}$  of available capacity \n".format(Q_tot, Q_avail))
	file.write("\\item Pressure drop for all piping: ${0:.3L} <$ 3\\% of set pressure. According to 5.4.1.1 API 520 2014, this pressure drop can be ingored.\n".format(Delta_P))
	file.write("\\end{itemize}")

	file.write("For the most dangerous case of {}, the required relief capacity is below avilable capacity of a used relief device. The piping is safe.".format(Danger.lower()))
 

	file.write("\n\n" r"\end{document}%" "\n")


def create_pdf(input_filename):
    process = subprocess.Popen([
        'pdflatex',   # Or maybe 'C:\\Program Files\\MikTex\\miktex\\bin\\latex.exe
        # '-quiet', #Remove excess output
        #'-output-format=pdf',
        #'-job-name=' + output_filename,
        input_filename])
    process.wait()

create_pdf ('report.tex')


with Image(filename='report.pdf', resolution = 300) as img: #converting PDF to png, no changes could be successfully done to images at this point
	with img.convert('png') as converted:
		converted.save(filename = 'page.png')

for filename in fnmatch.filter(os.listdir('.'), 'page*[0-9].png'): #Making changes to each png, e.g. setting white background, rescaling
	with Image(filename = filename) as pngimg:
		with Image(width=pngimg.width, height=pngimg.height, background=Color("white")) as bg: #create background image size of the original, filled with white
			bg.composite(pngimg,0,0) #compose two images and keep as bg
			bg.transform('100%', '50%') #crop too 100%, scale to 50%
			bg.save(filename = 'clean_'+filename)
	os.remove(filename)



extensions = ['tex', 'pdf', 'aux', 'log']
for filename in ('report'+x for x in extensions): #deleting garbage
	if os.path.isfile(filename):
		os.remove(filename)

