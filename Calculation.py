#Calculation file for report_maker
#ver 0.0.1


from math import *
from pyrefprop import refprop as rp
from natu import config; config.simplification_level=0
from natu.units import *
from natu.units import kPa, uPa, kJ

import sys
sys.path.append(r'D:\Personal\Python repo')
# from heat_transfer import functions as ht
# from heat_transfer import piping
from heat_transfer import cga, piping
# from heat_transfer.piping import *
u=g/mol #numerical equivalent of atomic mass unit















###Inputs:
#Internal fluid

# fluid = 'Helium'
fluid = 'Nitrogen'
P_set = 60*psig #set pressure

from LN2_spools import * #piping as per convention
# from He_spools import * #piping as per convention


#Air section

T_room = 100*degF #room temperature based on CGA code (need reference)
Convection = 'natural'
Conv_flow = {'fluid':'air', 'T' : T_room, 'P':1*atm} #Flow outside piping for convection and radiation heat load calculation

#Relief section

Q_avail = 157.5*ft**3/min







####Calculation

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
	Temp =  cga.max_theta(P_fr,x)
	D_vap_0 = rp.flsh('TP', Temp/K, P_fr/kPa, x) ['Dvap']*mol/L

Z = rp.therm2(Temp/K, D_vap_0/(mol/L), x)['Z'] #Compressibility factor

Internal_fluid = {'fluid':fluid,
					'P':P_fr,
					'T':Temp
				}

print (Internal_fluid)


for Pipe in Piping:
	Pipe.update({'fluid':Internal_fluid.copy()})


Sections = cga.make_sections(Piping, Section_start)
Q_tot = 0*ft**3/min
for Section in Sections:
	Q_sect = 0*ft**3/min
	for Pipe in Section:
		#Required capacity due to vacuum loss
		Q_sect += cga.Q_vac(Pipe, Conv_flow, P_fr) 

	prop = rp.setup('def', fluid)
	x = prop.get('x', [1])
	M = rp.wmol(x)['wmix']*g/mol
	'''Air condensation is assumed for liquids with normal boiling point below 50 K'''
	if rp.satp(101.325, x)['t'] < 50: 
		Q_air_cond = 0*ft**3/min
		for Pipe in Section:
			Q_air_cond += cga.Q_air(Pipe, Conv_flow, P_fr) #Required capacity due to air condensation (if aplicable)
		Q_sect = max(Q_sect, Q_air_cond)

	Q_tot = max(Q_tot, Q_sect)
	# Q_tot += Q_sect


#Hydraulics and pressure drops


M_dot = cga.from_scfma(Q_tot, Internal_fluid)
M_dot.display_unit = 'kg/s'



print ("Pressure drop for required flow is {:.3g}".format(piping.dP_piping(M_dot, Piping)))

# max_M_dot = piping.calculate_flow(Piping, P_in=67.5*psig, P_out=40*psig, M_dot_0 = 0.74*kg/s, M_step = 1e-3*kg/s)

# Q_max = cga.to_scfma(max_M_dot, Internal_fluid)

# print (max_M_dot, Q_max)






# F_factor = ((P_prv*D_prv)/(P_fr*D_vap_0))**0.5 # _prv -> conditions at the PRV inlet
# if F_factor > 1:
# 	print ("F = {:g}".format(F_factor))
# 	Q_final = Q_tot*F_factor
# else: 
# 	# print ("F = {:g}".format(F_factor))
# 	Q_final = Q_tot



print ("Required relief valve for P_set = {:g} and capacity {:.3g} of standard air.".format(P_set, Q_tot))



#Format results for report document













