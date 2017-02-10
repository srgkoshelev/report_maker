#Trapped volume relief calculation
#ver 0.0.1

#First test, it is not going to work


from math import *

from pyrefprop import refprop as rp


from natu import config; config.simplification_level=0
from natu.units import *
from natu.units import kPa, uPa, kJ

import sys
sys.path.append(r'D:\Personal\Python repo')
from heat_transfer.functions import *
u=g/mol #numerical equivalent of atomic mass unit




arb_var = 'MMMagic'


Title = 'heat load to the HAB transfer lines'

Assumptions = [
	'Piping consists of horizontal and vertical sections',
	'Vacuum is spoiled by air or fluid vapor',
	'Heat load is calculated in regards to average diameter between inner pipe and vaccum jacket',
	'The piping is considered to be a vessel with cryogenic liquid for maximum 110% overpressure i.e. calculations are based on CGA S-1.3-2008 6.1.3',

]













OD_pipe = 0.75*inch # diameter of the pipe
L_pipe = 5*ft #length
fluid = 'Nitrogen'

#print(A_surf)


P_set = 60*psig #psia, set pressure

#There should be a list of Cases implemented
Case = {'convection':'free', 'body':'cyl_hor'}










A_surf = pi*OD_pipe*L_pipe
P_fr = 1.1*P_set

M_N2 = 28.0134e-3*kg/mol #molar mass - should be handled by refprop
M_air = 28.96e-3*kg/mol

x = [1]
rp.setup('def', fluid)
#If temperature is not set - use saturation temperature
satur = rp.satp(P_fr/kPa, [1]) #K, saturation temp
T = satur ['t']*K
D_liq = satur ['Dliq']*mol/L
D_vap = satur ['Dvap']*mol/L

r = (rp.flsh("PQ",P_fr/kPa,1,x)['h']*J/(mol) - rp.flsh("PQ",P_fr/kPa,0,x)['h']*J/(mol))/M_N2 #J/kg, latent heat


C_coef = 356*(K**0.5*kg/m**3)

#also refprop
Z = 0.856 #Compressibility factor, lol


G_i = 241*(922*K-T)/(C_coef*r)*(Z*T/(M_N2/u))**0.5
G_i.display_unit = 'K*m3/kJ'

T_room = 100*degF #room temperature based on CGA code (need reference)




#print(P_fr, T, r, M_N2/u, G_i)



#Convection calculation






Air_std = {'fluid':'air', 'T' : T_room, 'P':1*atm} 
N2_pipe = {'Dim':OD_pipe, 'T':T}
# print (Pr(Air_stnrd), Gr(Air_stnrd, Nitrogen_pipe), Ra(Air_stnrd, Nitrogen_pipe))
# print("\n")

# print (Nu(Air_stnrd, Nitrogen_pipe, Case) )

# prop = rp.setup('def', 'Air')



# Air_prop = rp.flsh ("TP", T_room/K, 1*atm/kPa, prop['x'])
# D_air = Air_prop['Dvap']*mol/L
# Air_trans_prop = rp.trnprp(T_room/K, D_air/(mol/L), prop['x'])
# mu_air = Air_trans_prop['eta']*uPa*s
# k_air = Air_trans_prop['tcx']*W/(m*K)

# nu_air = mu_air/(D_air*M_air) #for Air!
# nu_air.display_unit = 'm2/s'
# nu_air.display_unit = 'm2/s'
# Pr = mu_air*Air_prop['cp']*(J/(mol*K))/(k_air*M_air)

# beta_exp = 1/(T_room/K)*(1/K) #volumetric thermal expansion coefficient
# Gr = g_0*OD_pipe**3*beta_exp*(T_room-T)/nu_air**2 #Grashof number
# Ra = Gr*Pr #Rayleigh number
# C_l = 0.671/(1+(0.492/Pr)**(9/16))**(4/9) #Handbook of heat transfer, Rohsenow, Hartnet, Cho
# Nu_l = 2*0.8/log(1+2*0.8*0.722*C_l*Ra**(1/4))
# Nu_t = 0.103*Ra**(1/3)
# Nu = (Nu_l**10 + Nu_t**10)**(1/10) #Nu number, Handbook of heat transfer, Rohsenow, Hartnet, Cho

# h = k_air*Nu/OD_pipe #"W/m^2-K, convective heat transfer coefficient"
# h.display_unit = 'W/(m2*K)'
h = Nu(Air_std, N2_pipe, Case)['h']
Nu_1 = Nu(Air_std, N2_pipe, Case)['Nu']
q_conv = h*(T_room-T) #"W/m^2 convective heat load"
q_conv.display_unit = 'W/m2'





# epsilon = 0.55 #"All radiating surfaces are assumed to be made from ground steel"
# q_rad = epsilon/2*5.67*(W/(m**2*K**4))*((T_room/100)**4-(T/100)**4) #"W/m^2; radiative heat load"
# q_rad.display_unit = 'W/m2'

q_rad = rad_hl(T_hot = T_room, T_cold = T)['q0']

U_coef = (q_conv+q_rad)/(T_room-T) #convert(W/m^2-K,kJ/hr-m^2-K)
U_coef.display_unit = 'kJ/(hr*m2*K)'

Q_a = 0.383*(328*K - T)/(922*K-T)*G_i*U_coef*A_surf # "m^3/hr of air"
Q_a.display_unit = 'ft3/min'


#print (Nu_1, h, q_conv, q_rad, U_coef, Q_a)






rp.setup('def', fluid)


N2_pipe = {'Dim':L_pipe, 'T':T, 'Dim_sec':OD_pipe}
# print (Pr(Air_stnrd), Gr(Air_stnrd, Nitrogen_pipe), Ra(Air_stnrd, Nitrogen_pipe))
# print("\n")

Case = {'convection':'free', 'body':'cyl_vert'}
#print(Ra(Air_std, N2_pipe)/1e6)





#print(P_fr, T, r, G_i)










