#! python3
import pweave
import subprocess
import os, fnmatch
from wand.image import Image
from wand.color import Color

def create_pdf(input_filename):
    process = subprocess.Popen([
        'pdflatex',   # Or maybe 'C:\\Program Files\\MikTex\\miktex\\bin\\latex.exe
        # '-quiet', #Remove excess output
        #'-output-format=pdf',
        #'-job-name=' + output_filename,
        input_filename])
    process.wait()


Report_file = 'Calc_report'

pweave.weave(file = Report_file + '.texw', output = Report_file + '.tex')
create_pdf (Report_file + '.tex')


# with Image(filename=Report_file + '.pdf', resolution = 300) as img: #converting PDF to png, no changes could be successfully done to images at this point
# 	with img.convert('png') as converted:
# 		converted.save(filename = 'page.png')

# for filename in fnmatch.filter(os.listdir('.'), 'page*[0-9].png'): #Making changes to each png, e.g. setting white background, rescaling
# 	with Image(filename = filename) as pngimg:
# 		with Image(width=pngimg.width, height=pngimg.height, background=Color("white")) as bg: #create background image size of the original, filled with white
# 			bg.composite(pngimg,0,0) #compose two images and keep as bg
# 			bg.transform('100%', '50%') #crop too 100%, scale to 50%
# 			bg.save(filename = 'clean_'+filename)
# 	os.remove(filename)



# extensions = ['tex', 'pdf', 'aux', 'log']
# for filename in (Report_file+'.'+x for x in extensions): #deleting garbage
# 	if os.path.isfile(filename):
# 		os.remove(filename)



