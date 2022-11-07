import numpy

import numpy.polynomial.polynomial as nppol

def ms_boundaries_to_pdyn(x,y,z,magnetopause = False, bow_shock = False):
	
	#Inputs:
	#(x, y, z): JSE coordinates of the magnetopause or bow shock in planetary radius 

	#Ouput:
	# Pdyn (dynamic pressure) in nPa


	# In order to reduce numerical errors associated
	# with the least squares fitting process all lengths were scaled
	# by 120 (RJ /120).
	x/=120
	y/=120
	z/=120

	# Joy et al., 2002's equation:
	# A(Pdyn) + B(Pdyn)*x + C(Pdyn)*x**2 + D(Pdyn) * y + E(Pdyn)* y **2 + F(Pdyn)*x*y - z**2 = 0
	if bow_shock:
		#A = -1.107 + 1.591*Pdyn**(-.25)
		A_0 = -1.107
		A_1 = 1.591
		#B = -0.566 - 0.812*Pdyn**(-.25)
		B_0 = -0.566
		B_1 = - 0.812
		#C =  0.048 - 0.059*Pdyn**(-.25)
		C_0 =  0.048
		C_1 = - 0.059
		#D =  0.077 - 0.038*Pdyn
		D_0 = 0.077
		D_1 = - 0.038
		#E = -0.874 - 0.299*Pdyn
		E_0 = -0.874
		E_1 = - 0.299
		#F = -0.055 + 0.124*Pdyn
		F_0 = -0.055
		F_1 = + 0.124


	if magnetopause:
		#A = -0.134 + 0.488*Pdyn**(-.25)
		A_0 = -0.134
		A_1 = 0.488
		#B = -0.581 - 0.225*Pdyn**(-.25)
		B_0 = -0.581
		B_1 = - 0.225
		#C = -0.186 - 0.016*Pdyn**(-.25)
		C_0 = -0.186
		C_1 = - 0.016
		#D = -0.014 + 0.096*Pdyn
		D_0 = -0.014
		D_1 = 0.096
		#E = -0.814 - 0.811*Pdyn
		E_0 = -0.814
		E_1 = - 0.811
		#F = -0.050 + 0.168*Pdyn
		F_0 = -0.050
		F_1 = 0.168


	#Joy et al., 2020's equation with Pdyn being the unkown:
#		0 =
#		A_0 + B_0*x + C_0*x**2 + D_0*y +E_0 * y**2 +F_0* x * y - z**2
#		+  Pdyn**(-.25)*(A_1 + B_1*x + C_1*x**2) +
#		+ Pdyn*(F_1*x*y + D_1**y + E_1*y**2) 

# 		with P_tmp = Pdyn**(-1/4)
#		0 = 
#		(A_0 + B_0*x + C_0*x**2 + D_0*y +E_0 * y**2 +F_0* x * y - z**2)
#		+ P_tmp * (A_1 + B_1*x + C_1*x**2) +
#		+ P_tmp**(-4) (F_1*x*y + D_1*y + E_1*y**2)

#		0 = 
#		P_tmp**4 (A_0 + B_0*x + C_0*x**2 + D_0*y +E_0 * y**2 +F_0* x * y - z**2)
#		+ P_tmp**5 * (A_1 + B_1*x + C_1*x**2) +
#		+ (F_1*x*y + D_1*y + E_1*y**2)

#		a * P_tmp**5 + b * P_tmp**4 + f = 0

	b = A_0 +B_0*x + C_0*x**2 + D_0*y + E_0 * y**2 + F_0* x * y - z**2
	a = (A_1 + B_1*x + C_1*x**2)
	f = (F_1*x*y + D_1*y + E_1*y**2)

	solution = nppol.Polynomial([f,0,0,0,b,a])


	roots = solution.roots()

	roots = roots[(numpy.isreal(roots)) & (numpy.isreal(roots) > 0)]
	roots = roots.real
	#	P_tmp = Pdyn**(-1/4) --> Pdyn = tmp**(-4)
	roots = roots**(-4)

	return(roots)
	



#	#Joy et al., 2002's equation:
#	A + B*x + C*x**2 + D*y + E*y**2 + F*x*y - z**2 = 0
#
#	# 
#	if bow_shock:
#		A = -1.107 + 1.591*Pdyn**(-.25)
#		B = -0.566 - 0.812*Pdyn**(-.25)
#		C =  0.048 - 0.059*Pdyn**(-.25)
#		D =  0.077 - 0.038*Pdyn
#		E = -0.874 - 0.299*Pdyn
#		F = -0.055 + 0.124*Pdyn
#
#	if magnetopause:
#		A = -0.134 + 0.488*Pdyn**(-.25)
#		B = -0.581 - 0.225*Pdyn**(-.25)
#		C = -0.186 - 0.016*Pdyn**(-.25)
#		D = -0.014 + 0.096*Pdyn
#		E = -0.814 - 0.811*Pdyn
#		F = -0.050 + 0.168*Pdyn
#
#	# Pdyn is the only unkown:
#	<=> 0 = -1.107 + 1.591*Pdyn**(-.25) 
#		+ (-0.566 - 0.812*Pdyn**(-.25)) *x
#		+ (0.048 - 0.059*Pdyn**(-.25)) *x**2
#		+ (0.077 - 0.038*Pdyn) * y
#		+ (-0.874 - 0.299*Pdyn) * y**2
#		+ (-0.055 + 0.124*Pdyn) * x * y
#		- z**2
#
#
#
#		0 = 
#		- 1.107 -0.566*x + 0.048*x**2 + 0.077*y - 0.874 * y**2 - 0.055* x * y - z**2
#		+ 1.591*Pdyn**(-.25) 
#		- 0.812*Pdyn**(-.25)*x
#		- 0.059*Pdyn**(-.25) *x**2
#		- 0.038*Pdyn * y
#		- 0.299*Pdyn * y**2
#	    + 0.124*Pdyn * x * y
#		
#		
#	<=> 0 =
#		- 1.107 -0.566*x + 0.048*x**2 + 0.077*y - 0.874 * y**2 - 0.055* x * y - z**2
#		+  Pdyn**(-.25)*(1.591 - 0.812*x - 0.059*x**2) + Pdyn*(0.124*x*y - 0.038**y - 0.299*y**2) 
#	
#	then if:
#	b = - 1.107 -0.566*x + 0.048*x**2 + 0.077*y - 0.874 * y**2 - 0.055* x * y - z**2
#	a = (1.591 - 0.812*x - 0.059*x**2)
#	c = (0.124*x*y - 0.038**y - 0.299*y**2)
#	
#	<=> b + a* Pdyn**(-1/4)  + c* Pdyn = 0
#	
#	if P_tmp = Pdyn**(-1/4) <=> P_tmp = 1/Pdyn**(1/4) <=> P_tmp**4 = 1/Pdyn <=> Pdyn = P_tmp**-4 
#	
#	<=> b + a* P_tmp  + c* P_tmp**-4 = 0	
#	<=> b*P_tmp**4 + a* P_tmp*P_tmp**4  + c* P_tmp**-4 * P_tmp**4 = 0
#	<=> b*P_tmp**4 + a* P_tmp**5  + c = 0
#	
#	<=> a* P_tmp**5 + b*P_tmp**4 + c = 0
#	a = a & b = b & f = c
#	<=>
#	# Using the Tschirnhaus transformation: P = Y -b/a --> Y = P + b/a
#	Y**5 + p*Y**3 + q*Y**2 + r*Y +s = 0
#
#	with:
#	p = (- 2 b**2)/5a**2
#	q = (4*b**3)/25*a**2
#	r = (- 3b**4)/125*a**4
#	s = (3125*a**4*f + 4b**5)/3125a**5
#



