import numpy as np
import scipy
import matplotlib.pyplot as plt
import os
import pandas as pd
import math


def pdyn_to_mp(Pdyn=0.319, equatorial = False, noon_midnight = False, dawn_dusk = False):
	#set dynamic pressure as an entry

	
	deg=180.0 / np.pi
	#create grid
	xdatapts = ((np.arange(5001.0)*0.1 - 250.0)/120.0)
	
	amagp = -0.134 + 0.488*Pdyn**(-.25)
	bmagp = -0.581 - 0.225*Pdyn**(-.25)
	cmagp = -0.186 - 0.016*Pdyn**(-.25)
	dmagp = -0.014 + 0.096*Pdyn
	emagp = -0.814 - 0.811*Pdyn
	fmagp = -0.050 + 0.168*Pdyn


	if equatorial: # z = 0, x = xdatapts, y : E*y**2+(F*x+D)*y + (A + B*x) = 0 
		aplot = emagp
		bplot = dmagp + fmagp*xdatapts
		cplot = amagp + bmagp*xdatapts + cmagp*(xdatapts**2)

	if noon_midnight: # y = 0, x = xdatapts, z : -z**2 + C*x**2 + B *x+ A = 0
		aplot = -1
		bplot = 0
		cplot = bmagp*xdatapts + bmagp*xdatapts + amagp

	if dawn_dusk:# x = 0, y = xdatapts, z : -z**2 + E*y**2+ D*y + A = 0 
		aplot = -1
		bplot = 0
		cplot =  emagp*xdatapts**2 + dmagp*amagp + amagp 


	#split to plot dawn side (0-180) 
	yplotplus = (-1*bplot + np.sqrt((bplot**2) - 4*aplot*cplot))/(2*aplot)
	#and split to make dusk side (180-360)
	yplotminus = (-1*bplot - np.sqrt((bplot**2) - 4*aplot*cplot))/(2*aplot)
	#rescale x and y to jovian radii as the calculations assume R/120
	yplotplused = 120*yplotplus
	yplotminused = 120*yplotminus
	#calculate the radial distance in Rj 0-180, then 180-360 as 2 separate halves of msphere
	xdataptsed = xdatapts*120.

	rad0plus = np.sqrt(xdataptsed*xdataptsed + yplotplused*yplotplused + 0j)
	rad180plus = np.sqrt(xdataptsed*xdataptsed + yplotminused*yplotminused + 0j)
	lt0plus = 180 - (np.arccos(xdataptsed/rad0plus)*deg)
	lt180plus = 180 + (np.arccos(xdataptsed/rad180plus)*deg)
	#put together 2 sides of MP using a dataframe
	rjltdawndf = pd.DataFrame(rad0plus)
	rjltdawndf.columns = ['Rad']
	rjltdawndf['LT']=lt0plus
	rjltduskdf = pd.DataFrame(np.flip(rad180plus))
	rjltduskdf.columns = ['Rad']
	rjltduskdf['LT']=np.flip(lt180plus)
	mprjlt=pd.concat([rjltdawndf,rjltduskdf])
	mprjlt

	standoff = xdataptsed[np.logical_not(np.isnan(yplotplused))][-1]

	#plt.plot(rjltdawndf.LT,rjltdawndf.Rad, '-b')
	#plt.plot(rjltduskdf.LT,rjltduskdf.Rad, '-b')


	return([xdataptsed, xdataptsed],[yplotplused,yplotminused], standoff)
	return
	

#Add Joy model standoffs to dataframe
def pdyn_to_bs(Pdyn=0.319, equatorial = False, noon_midnight = False, dawn_dusk = False):
	#set dynamic pressure as an entry
	deg=180.0 / np.pi
	#create grid
	xdatapts = ((np.arange(5001.0)*0.1 - 250.0)/120.0)
	
	amagp = -1.107 + 1.591*Pdyn**(-.25)
	bmagp = -0.566 - 0.812*Pdyn**(-.25)
	cmagp =  0.048 - 0.059*Pdyn**(-.25)
	dmagp =  0.077 - 0.038*Pdyn
	emagp = -0.874 - 0.299*Pdyn
	fmagp = -0.055 + 0.124*Pdyn
	

	if equatorial: # z = 0, x = xdatapts, y : E*y**2+(F*x+D)*y + (A + B*x) = 0 
		aplot = emagp
		bplot = dmagp + fmagp*xdatapts
		cplot = amagp + bmagp*xdatapts + cmagp*(xdatapts**2)

	if noon_midnight: # y = 0, x = xdatapts, z : -z**2 + C*x**2 + B *x+ A = 0
		aplot = -1
		bplot = 0
		cplot = bmagp*xdatapts + bmagp*xdatapts + amagp

	if dawn_dusk:# x = 0, y = xdatapts, z : -z**2 + E*y**2+ D*y + A = 0 
		aplot = -1
		bplot = 0
		cplot =  emagp*xdatapts**2 + dmagp*amagp + amagp 
	#split to plot dawn side (0-180)
	
	yplotplus = (-1*bplot + np.sqrt((bplot**2) - 4*aplot*cplot))/(2*aplot)
	#and split to make dusk side (180-360)
	
	yplotminus = (-1*bplot - np.sqrt((bplot**2) - 4*aplot*cplot))/(2*aplot)
	#rescale x and y to jovian radii as the calculations assume R/120
	yplotplused = 120*yplotplus
	yplotminused = 120*yplotminus
	#calculate the radial distance in Rj 0-180, then 180-360 as 2 separate halves of msphere
	xdataptsed = xdatapts*120.
	
	rad0plus = np.sqrt(xdataptsed*xdataptsed + yplotplused*yplotplused + 0j)
	rad180plus = np.sqrt(xdataptsed*xdataptsed + yplotminused*yplotminused + 0j)
	lt0plus = 180 - (np.arccos(xdataptsed/rad0plus)*deg)
	lt180plus = 180 + (np.arccos(xdataptsed/rad180plus)*deg)
	#put together 2 sides of MP using a dataframe
	rjltdawndf = pd.DataFrame(rad0plus)
	rjltdawndf.columns = ['Rad']
	rjltdawndf['LT']=lt0plus
	rjltduskdf = pd.DataFrame(np.flip(rad180plus))
	rjltduskdf.columns = ['Rad']
	rjltduskdf['LT']=np.flip(lt180plus)
	mprjlt=pd.concat([rjltdawndf,rjltduskdf])


	standoff = xdataptsed[np.logical_not(np.isnan(yplotplused))][-1]

#	plt.plot(rjltdawndf.LT,rjltdawndf.Rad, '-k')
#	plt.plot(rjltduskdf.LT,rjltduskdf.Rad,'-k')


	return([xdataptsed, xdataptsed],[yplotplused,yplotminused], standoff)



