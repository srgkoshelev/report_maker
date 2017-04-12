#!python3
#Generator of a pweave file for standard/auxillary functions to be included with calculations

import subprocess
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import LatexFormatter
import pweave
import os, fnmatch
from wand.image import Image
from wand.color import Color


import sys
sys.path.append(r'D:\Personal\Python repo')
from heat_transfer import functions as ht


Make_imgs = True
Add_aux_funcs = False


for filename in fnmatch.filter(os.listdir('.'), 'page*.png'): #Remove old .png before starting
	os.remove(filename)


pweave.weave ('body.texw')


Folder = 'D:\Personal\Python repo\heat_transfer'

File_list = ['cga.py', 'functions.py', 'piping.py']


with open('report.tex', 'w') as aux_file:
	####
	with open('preamble.tex', 'r') as preamble:
		aux_file.write(preamble.read())
	aux_file.write("%\n"*3)
	aux_file.write(r"\begin{document}" "%\n")
	with open('body.tex', 'r') as body:
		aux_file.write(body.read())

	if Add_aux_funcs:
		aux_file.write("\\pagebreak")
		aux_file.write("\\section*{Supporting functions}\n\n\n")
		for filename in File_list:
			Path = Folder + '\\' + filename
			aux_file.write("\\subsection*{{From file {0} }}\n\n".format(filename))
			with open(Path, 'r') as input_file:
				aux_file.write (highlight(input_file.read(), PythonLexer(), LatexFormatter(verboptions=r'fontsize=\scriptsize')))

	aux_file.write(r"\end{document}" "%\n")


def create_pdf(input_filename):
    process = subprocess.Popen([
        'pdflatex',   # Or maybe 'C:\\Program Files\\MikTex\\miktex\\bin\\latex.exe
        # '-quiet', #Remove excess output
        #'-output-format=pdf',
        #'-job-name=' + output_filename,
        input_filename])
    process.wait()



create_pdf ('report.tex')

extensions = ['tex', 'aux', 'log'] #Don't delete .pdf if not making images

if Make_imgs:

	with Image(filename='report.pdf', resolution = 200) as img: #converting PDF to png, no changes could be successfully done to images at this point
		with img.convert('png') as converted:
			converted.save(filename = 'page.png')

	extensions = ['tex', 'pdf', 'aux', 'log']

	# for filename in fnmatch.filter(os.listdir('.'), 'page*.png'): #Making changes to each png, e.g. setting white background, rescaling
	# 	with Image(filename = filename) as pngimg:
	# 		with Image(width=pngimg.width, height=pngimg.height, background=Color("white")) as bg: #create background image size of the original, filled with white
	# 			bg.composite(pngimg,0,0) #compose two images and keep as bg
	# 			bg.transform('100%', '60%') #crop too 100%, scale to 50%
	# 			bg.save(filename = 'clean_' + filename)
	# 	os.remove(filename)



os.remove('body.tex')
for filename in ('report.'+x for x in extensions): #deleting garbage
	if os.path.isfile(filename):
		os.remove(filename)
