#!python3
from math import *
from pyrefprop import refprop as rp
from natu import config; config.simplification_level=0
from natu.units import *
from natu.units import kPa, uPa, kJ

import sys
sys.path.append(r'D:\Personal\Python repo')
from heat_transfer import functions as ht
from heat_transfer.piping import *
u=g/mol #numerical equivalent of atomic mass unit



#To be moved to another place
def max_theta(P, x, step = 0.1):
	T_start = rp.satp(101.325,x)['t'] #Starting temperature - liquid temperature for atmospheric pressure. Vacuum should be handled separately
	T_end = 300 #K
	theta = 0
	T = T_start
	T_max = 0
	while T <= T_end:
		D_vap = rp.flsh('TP', T, P/kPa, x)['Dvap']
		theta_sq_v = rp.therm3(T, D_vap, x)['spht']*(D_vap)**0.5
		if theta_sq_v > theta:
			theta = theta_sq_v
			T_max = T
		T += step
	return T_max*K


def Q_vac (Pipe, External, P_fr):
	fluid = Pipe['fluid']['fluid']
	prop = rp.setup('def', fluid)
	x = prop.get('x', [1])
	M = rp.wmol(x)['wmix']*g/mol
	P = Pipe['fluid']['P']
	P_crit = rp.critp(x)['pcrit']*kPa #Critical pressure; If supercritical flow need to use specific input calculation
	T = Pipe['fluid']['T']

	C_coef = 356*(K**0.5*kg/m**3)
	if P <= P_crit:
		D_vap = rp.satp(P_fr/kPa, x)['Dvap']*mol/L
		Z = rp.therm2(T/K, D_vap/(mol/L), x)['Z'] #Compressibility factor
		r = (rp.flsh("PQ",P/kPa,1,x)['h']*J/(mol) - rp.flsh("PQ",P/kPa,0,x)['h']*J/(mol))/M # latent heat
		G_i = 241*(922*K-T)/(C_coef*r)*(Z*T/(M/u))**0.5

	else:
		D_vap = rp.flsh('TP', T/K, P/kPa, x)['Dvap']*mol/L
		Z = rp.therm2(T/K, D_vap/(mol/L), x)['Z'] #Compressibility factor
		theta = (rp.therm3(T/K, D_vap/(mol/L), x)['spht']*J/mol)/M
		G_i = 241*(922*K-T)/(C_coef*theta)*(Z*T/(M/u))**0.5
	G_i.display_unit = 'K*m3/kJ'

	Surface = make_surface(Pipe)
	if Pipe['Orientation'] == 'Horizontal': #make it a proper function in future
		Case = {'convection':'free', 'body':'cyl_hor'}
	elif Pipe['Orientation'] == 'Vertical':
		Case = {'convection':'free', 'body':'cyl_vert'}
	h = ht.Nu(External, Surface, Case)['h']
	Nuss = ht.Nu(External, Surface, Case)['Nu']
	A_surf = Surface['Dim']*Surface['Dim_sec']
	T_ext = External['T']
	q_conv = h*(T_ext-T) #"W/m^2 convective heat load"
	q_conv.display_unit = 'W/m2'
	q_conv_disp = q_conv*A_surf
	q_conv_disp.display_unit = 'W'
	q_rad = ht.rad_hl(T_hot = T_ext, T_cold = T)['q0']
	q_rad_disp = q_rad*A_surf
	q_rad_disp.display_unit = 'W'
	U_coef = (q_conv+q_rad)/(T_ext-T) #convert(W/m^2-K,kJ/hr-m^2-K)
	U_coef.display_unit = 'kJ/(hr*m2*K)'
	Q_a = 0.383*(328*K - T)/(922*K-T)*G_i*U_coef*A_surf # "m^3/hr of air"
	Q_a.display_unit = 'ft3/min'

	Pipe.update({'q_rad':q_rad_disp, 'q_conv':q_conv_disp})

	return Q_a


def Q_air (Pipe, External, P_fr): #Required relief capacity due to air condensation
	Diam = OD(Pipe)
	L = Pipe['L']

	fluid = Pipe['fluid']['fluid']
	prop = rp.setup('def', fluid)
	x = prop.get('x', [1])
	M = rp.wmol(x)['wmix']*g/mol
	P = Pipe['fluid']['P']
	P_crit = rp.critp(x)['pcrit']*kPa #Critical pressure; If supercritical flow need to use specific input calculation
	T = Pipe['fluid']['T']

	C_coef = 356*(K**0.5*kg/m**3)
	if P <= P_crit:
		D_vap = rp.satp(P_fr/kPa, x)['Dvap']*mol/L
		Z = rp.therm2(T/K, D_vap/(mol/L), x)['Z'] #Compressibility factor
		r = (rp.flsh("PQ",P/kPa,1,x)['h']*J/(mol) - rp.flsh("PQ",P/kPa,0,x)['h']*J/(mol))/M # latent heat
		G_i = 241*(922*K-T)/(C_coef*r)*(Z*T/(M/u))**0.5

	else:
		D_vap = rp.flsh('TP', T/K, P/kPa, x)['Dvap']*mol/L
		Z = rp.therm2(T/K, D_vap/(mol/L), x)['Z'] #Compressibility factor
		theta = (rp.therm3(T/K, D_vap/(mol/L), x)['spht']*J/mol)/M
		G_i = 241*(922*K-T)/(C_coef*theta)*(Z*T/(M/u))**0.5
	G_i.display_unit = 'K*m3/kJ'


	A_surf = pi*Diam*L
	flux = 0.6*W/cm**2 #Heat flux for  MLI insulated LHe tank from Lehman, Zahn
	q_cond = A_surf*flux
	q_cond.display_unit = 'W'
	T_cold = rp.satp(5*psig/kPa, x)['t']*K#Temperature of the cold surface used for air condensation. The heat will be deposited to liquid at presssure close to atmospheric (assumed 5 psig)
	T_ext = External['T']
	U_coef = flux/(T_ext-T_cold) #convert(W/m^2-K,kJ/hr-m^2-K)
	U_coef.display_unit = 'kJ/(hr*m2*K)'

	Q_a = 0.383*(328*K - T)/(922*K-T)*G_i*U_coef*A_surf # "m^3/hr of air"
	Q_a.display_unit = 'ft3/min'

	Pipe.update({'q_cond':q_cond, })

	return Q_a