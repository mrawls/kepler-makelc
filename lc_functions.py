import numpy as np
from pyraf import iraf
from pyraf.iraf import kepler
'''
Useful functions for Kepler light curve processing
Use this with the program 'makelc.py'
Originally by Jean McKeever
Edited and improved by Meredith Rawls
'''

# calculate orbital phase
# times must be a list of observation times in the same units as BJD0
# it returns 'phases': orbital phases from 0 to 1
# it also returns 'phasedoubles': twice as long as 'phases' and now from 0 to 2
def phasecalc(times, period=100, BJD0=2454833):
	phases = []
	cycles = []
	for i in range(0, len(times)):
		fracP = (times[i] - BJD0) / period
		if fracP < 0:
			phases.append(fracP % 1)
			cycles.append(int(fracP))
		else:
			phases.append(fracP % 1)
			cycles.append(int(fracP) + 1)
		#print(fracP, phases[i])
	return phases

# remove long-term trends
# uses a simple 3rd-order polynomial by default
# operates on one array at a time (e.g., after all quarters have been combined)
def long_detrend(t, flux, order=3):
    model = np.polyfit(t, flux, order)
    fit = np.zeros(len(t))
    # apply the model coefficients to create the fit
    for i in range(0, order+1):
        fit += model[i]*np.power(t, (order-i))
    #flux = flux/fit*1e6 - 1e6 # put it in ppm >:(
    flux = flux/fit*np.median(flux) # don't put it in ppm, because ppm is annoying
    return t, flux

# Delete any observation that has one or more NaN values.
# Assumes there are six parallel arrays... use dummy arrays if you don't have 6
# columns of interest to operate on (sorry).
# Operates on one quarter at a time
def nan_delete(time, flux, ferr, other1, other2, other3):
	a = []
	a = [time, flux, ferr, other1, other2, other3]
	atrans = np.transpose(a)
	newatrans = []
	newa = []
	for row in atrans:
		# only save rows that DON'T contain a NaN value
		if np.isnan(row).any() != True:
			newatrans.append(row)
	newa = np.transpose(newatrans)
	newtime = newa[0]
	newflux = newa[1]
	newferr = newa[2]
	newother1 = newa[3]
	newother2 = newa[4]
	newother3 = newa[5]
	return newtime, newflux, newferr, newother1, newother2, newother3
		
# Put data from different quarters on the same AVERAGE level
# operates on a list of arrays (multiple quarters) all at once
# DON'T USE THIS ONE
# def normalize_qtr_avg(flux):
# 	sumflux = 0
# 	npts = 0
# 	for arr in flux:
#    	sumflux += np.nansum(arr)
#     	npts += len(arr[arr>0])
# 	avgflux = sumflux/npts # overall average for all quarters
# 	for arr in flux:
#     	avg_arr = np.mean(arr[arr>0]) # average for an individual quarter
#     	arr += avgflux - avg_arr
# 	return flux

# Put data from different quarters on the same MEDIAN level
# operates on a list of arrays (multiple quarters) all at once
def normalize_qtr_med(flux):
	sumflux = 0
	npts = 0
	for arr in flux:
		sumflux += np.nansum(arr)
		npts += len(arr)
	avgflux = sumflux/npts # overall average for all quarters
	for arr in flux:
		med_arr = np.median(arr) # median for an individual quarter
		arr += avgflux - med_arr
	return flux

# Line up the gaps within each quarter
# operates on a list of arrays (multiple quarters) all at once
def lineup_qtr_gaps(time, flux, maskstart, maskend):
	diffs = np.zeros(len(time) - 1)
	for i in range(0,len(time) - 1): # loop through quarters
	# calculate differences between flux points at quarter start/end
		start = 0
		end = -1
		for idx, mask in enumerate(maskstart):
			while (time[i][end] > maskstart[idx] and time[i][end] < maskend[idx]):
				#print('end', end, time[i][end], maskstart[idx], maskend[idx])
				end -= 1
			while (time[i+1][start] > maskstart[idx] and time[i+1][start] < maskend[idx]):
				#print('start', start, time[i+1][start], maskstart[idx], maskend[idx])
				start += 1
		diffs[i] = (flux[i][end] - flux[i+1][start])
	# maxi will find the point with the largest change in flux
	maxi = lambda z: np.where(max(abs(z)) == abs(z))[0][0]
	cntr = 0 # counter
	max_val = max(abs(diffs))
	while max_val > 100: #original value here was 100
		# this is the index of the largest change in flux, so it needs adjusting
		ind = maxi(diffs)
		# this is the actual change in flux associated with that index
		diff = diffs[ind]
		# adjust the flux at this spot and its neighbor so they meet
		flux[ind] = flux[ind] - diff/2.0
		flux[ind+1] = flux[ind+1] + diff/2.0
		diffs = np.zeros(len(time) - 1)
		for i in range(0, len(time) - 1):
		# calculate differences between flux points at quarter start/end, again
			start = 0
			end = -1
			for idx, mask in enumerate(maskstart):
				while time[i][end] > maskstart[idx] and time[i][end] < maskend[idx]:
					#print('end', end, time[i][end], maskstart[idx], maskend[idx])
					end -= 1
				while time[i+1][start] > maskstart[idx] and time[i+1][start] < maskend[idx]:
					#print('start', start, time[i+1][start], maskstart[idx], maskend[idx])
					start += 1
			diffs[i] = (flux[i][end] - flux[i+1][start])
		cntr += 1 # count how many times this while-loop happens
		max_val = max(abs(diffs))
#		print(max_val, cntr)
	return time, flux

# performs detrending with cotrending basis vectors (cbvs)
# lcin and lcout must both be FITS filenames
def kepcotrend(lcin, lcout, cbvfile, maskfile=''):
	iraf.kepcotrend(infile=lcin, outfile=lcout, cbvfile=cbvfile, 
		vectors='1 2', method='simplex', fitpower=1, iterate='yes', sigmaclip=2.0, 
		maskfile=maskfile, scinterp='None', plot='no', clobber='yes', verbose='no')	
	return