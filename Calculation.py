#Calculation file for report_maker
#ver 0.0.1


from math import *
from pyrefprop import refprop as rp
from natu import config; config.simplification_level=0
from natu.units import *
from natu.units import kPa, uPa, kJ

import sys
sys.path.append(r'D:\Personal\Python repo')
from heat_transfer import functions as ht
from heat_transfer import piping
from auxillary import *
# from heat_transfer.piping import *
u=g/mol #numerical equivalent of atomic mass unit

#These globals variables will be used in LaTeX file 
Title = 'Trapped volume relief calculation for HAB Transfer lines'

Assumptions = [
	'Piping consists of horizontal and vertical sections',
	'Flex hoses on the top are considered to be vertical',
	'Vacuum is spoiled by air or fluid vapor',
	#'Heat load is calculated in regards to average diameter between inner pipe and vaccum jacket',
	'The piping is considered to be a vessel with cryogenic liquid for maximum 110\% overpressure i.e. calculations are based on CGA S-1.3-2008 6.2.2',
]













###Inputs:
#Internal fluid

fluid = 'Helium'
# fluid = 'Nitrogen'
P_set = 60*psig #set pressure

# from LN2_spools import Piping #piping as per convention
from He_spools import Piping #piping as per convention


#Air section

T_room = 100*degF #room temperature based on CGA code (need reference)
Convection = 'natural'
Conv_flow = {'fluid':'air', 'T' : T_room, 'P':1*atm} #Flow outside piping for convection and radiation heat load calculation

#Relief section

Q_avail = 5*ft**3/min









P_fr = 1.1*P_set

prop = rp.setup('def', fluid)
x = prop.get('x', [1])
M = rp.wmol(x)['wmix']*g/mol

#If temperature is not set - use saturation temperature
P_crit = rp.critp(x)['pcrit']*kPa #Critical pressure; If supercritical flow need to use specific input calculation
if P_fr <= P_crit:
	satur = rp.satp(P_fr/kPa, x) #K, saturation temp
	Temp = satur ['t']*K
	# r = (rp.flsh("PQ",P_fr/kPa,1,x)['h']*J/(mol) - rp.flsh("PQ",P_fr/kPa,0,x)['h']*J/(mol))/M #J/kg, latent heat
	D_vap_0 = satur ['Dvap']*mol/L
else:
	Temp =  max_theta(P_fr,x)
	D_vap_0 = rp.flsh('TP', Temp/K, P_fr/kPa, x) ['Dvap']*mol/L

Z = rp.therm2(Temp/K, D_vap_0/(mol/L), x)['Z'] #Compressibility factor

Internal_fluid = {'fluid':fluid,
					'P':P_fr,
					'T':Temp
				}

print (Internal_fluid)



for Pipe in Piping:
	Pipe.update({'fluid':Internal_fluid.copy()})



Q_tot = 0*ft**3/min
for Pipe in Piping:
	Q_tot += Q_vac(Pipe, Conv_flow, P_fr)

prop = rp.setup('def', fluid)
x = prop.get('x', [1])
M = rp.wmol(x)['wmix']*g/mol
if rp.satp(101.325, x)['t'] < 50:
	Q_air_cond = 0*ft**3/min
	for Pipe in Piping:
		Q_air_cond += Q_air(Pipe, Conv_flow, P_fr)
	if Q_tot > Q_air_cond:
		Danger = 'Vacuum loss'
	else:
		Q_tot = Q_air_cond
		Danger = 'Air condensation'




#Hydraulics and pressure drops


M_dot = Q_tot*D_vap_0*M
M_dot.display_unit = 'kg/s'



sections = len (Piping)

for sec_num, Pipe in enumerate (Piping):
	P = Pipe['fluid']['P']
	if 'h' in Pipe['fluid']:
		h = Pipe['fluid']['h']
		T = rp.flsh('PH', P/kPa, h/(J/mol), x)['t']*K
		Pipe['fluid'].update({'T':T})
		# print('h->T')
	else:
		T = Pipe['fluid']['T']
		h = rp.flsh('TP',T/K, P/kPa, x)['h']*(J/mol)
		Pipe['fluid'].update({'h':h})
		# print('T->h')
	delta_P = piping.dp_pipe(M_dot, Pipe, Pipe['fluid'])
	if sec_num < sections - 1:
		if Pipe['Corrugated'] == False and Piping[sec_num+1]['Corrugated'] == False:
			delta_P += piping.dp_elbow(M_dot, Pipe, Pipe['fluid'])
		P_next = P-delta_P
		h_next = h
		Piping[sec_num+1]['fluid'].update({'P':P_next, 'h':h_next})
	else:
		P_prv = P-delta_P
		Delta_P = P_fr - P_prv
		Delta_P.display_unit = 'psi'
		D_prv = rp.flsh('PH', P_prv/kPa, h/(J/mol), x)['Dvap']*(mol/L)

print("Pressure drop for the piping is {:g}.".format(Delta_P))
if Delta_P/P_set <= 0.03:
	dP_negligible = True
else:
	dP_negligible = False
	print ('Delta_p/P_fr > 3%, additional consideration required')


F_factor = ((P_prv*D_prv)/(P_fr*D_vap_0))**0.5 # _prv -> conditions at the PRV inlet
if F_factor > 1:
	print ("F = {:g}".format(F_factor))
	Q_final = Q_tot*F_factor
else: 
	# print ("F = {:g}".format(F_factor))
	Q_final = Q_tot



print ("Required relief valve for P_set = {:g} and capacity {:g} of standard air.".format(P_set, Q_final))



#Format results for report document













