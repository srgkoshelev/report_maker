#Calculation file for report_maker
#ver 0.0.1


from math import *

from pyrefprop import refprop as rp


from natu import config; config.simplification_level=0
from natu.units import *
from natu.units import kPa, uPa, kJ

import sys
sys.path.append(r'D:\Personal\Python repo')
from heat_transfer.functions import *
u=g/mol #numerical equivalent of atomic mass unit

#These globals variables will be used in LaTeX file 
Title = 'Trapped volume relief calculation for HAB Transfer lines'

Assumptions = [
	'Piping consists of horizontal and vertical sections',
	'Flex hoses on the top are considered to be vertical',
	'Vacuum is spoiled by air or fluid vapor',
	#'Heat load is calculated in regards to average diameter between inner pipe and vaccum jacket',
	'The piping is considered to be a vessel with cryogenic liquid for maximum 110\% overpressure i.e. calculations are based on CGA S-1.3-2008 6.1.3',
]

#Piping section

OD_pipe = 0.75*inch # diameter of the pipe
L_pipe = 5*ft #length
fluid = 'Nitrogen'
P_set = 60*psig #psia, set pressure
P_fr = 1.1*P_set



prop = rp.setup('def', fluid)
x = prop.get('x', [1])
M = rp.wmol(x)['wmix']*g/mol

#If temperature is not set - use saturation temperature
satur = rp.satp(P_fr/kPa, x) #K, saturation temp
Temp = satur ['t']*K
r = (rp.flsh("PQ",P_fr/kPa,1,x)['h']*J/(mol) - rp.flsh("PQ",P_fr/kPa,0,x)['h']*J/(mol))/M #J/kg, latent heat
D_vap = satur ['Dvap']*mol/L
Z = rp.therm2(Temp/K, D_vap/(mol/L), x)['Z'] #Compressibility factor

Sections = [(OD_pipe, 13*ft+5*inch, 'hor'), 
			(OD_pipe, 14*ft+10*inch, 'hor'), 
			(OD_pipe, 19*ft, 'vert'), 
			(OD_pipe, 70*inch, 'hor'), 
			(OD_pipe, 6*ft, 'hor'), 
			(OD_pipe, 177*inch, 'vert'), 
]



#Air section




T_room = 100*degF #room temperature based on CGA code (need reference)
Convection = 'natural'
Air_std = {'fluid':'air', 'T' : T_room, 'P':1*atm} 


Surfaces = []
Cases = []
Piping = []
for section in Sections:
	Surfaces.append(dict([('T', Temp)]))
	Piping.append(dict([('D', section[0]), ('L', section[1])]))
	Cases.append({'convection':Convection, 'body':'cyl_'+section[2]})
	if section[2] =='hor':
		Surfaces[-1].update([('Dim', section[0]), ('Dim_sec', section[1])])
	if section[2] =='vert':
		Surfaces[-1].update([('Dim', section[1]), ('Dim_sec', section[0])])




C_coef = 356*(K**0.5*kg/m**3)
G_i = 241*(922*K-Temp)/(C_coef*r)*(Z*Temp/(M/u))**0.5
G_i.display_unit = 'K*m3/kJ'



Q_avail = 5*ft**3/min



















