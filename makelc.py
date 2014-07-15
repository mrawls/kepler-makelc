from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import kplr
from lc_functions import *
from astropy.io import fits
'''
Creates a friendly light curve from multiple quarters of Kepler data.
Works for ANY valid KIC target your heart desires (no need to already have the data).
by Meredith Rawls, with some functions originally by Jean McKeever
July 2014

First, the kepcotrend task is used to create a 'detrended' light curve in parallel with
the 'raw' simple aperture photometry light curve. The following operations are then
carried out on BOTH light curves:
- NaN values are deleted
- each quarter is put on the same median flux level
- the gaps between quarters are lined up nicely
Note there is no interpolation---every original timestamp is preserved.

You will get a nice plot and an outfile (.txt), which you can specify below.
It will contain fluxes and magnitudes (normalized to the Kepler magnitude of the target).
It will also contain error values for both flux and magnitude!!!

TO USE THIS PROGRAM:
(1) Be sure you have numpy, matplotlib, kplr, astropy, pyraf, and PyKE installed
--> if you don't, try 'pip install kplr' (for example)
--> PyKE is a bit more complicated: see http://keplergo.arc.nasa.gov/PyKE.shtml
--> you'll want to run 'mkiraf' in the working directory, too
(2) Be sure you have 'lc_functions.py' saved in the same directory as this file
(3) Download ALL the basis vectors and save them in a subdirectory called 'basisvectors'
--> get them here: https://archive.stsci.edu/kepler/cbv.html
(4) Optional: make a mask (e.g., for eclipses) in real BJD units (Kepler time + 2454833)
--> see mask_kepcotrend.txt for an example
--> save the mask file in ~/.kplr/data/lightcurves/KICNUMBERHERE/.
--> if no mask file is found, the program will still work
(5) Optional: tweak the parameters used in the kepcotrend task in 'lc_functions.py'.
--> for more info, see: http://keplergo.arc.nasa.gov/ContributedSoftwareKepcotrend.shtml
(6) Change any settings below as necessary (KIC, home directory, etc.)
(7) Type 'python makelc.py' and watch the magic happen
'''

### SET KIC, HOME DIRECTORY, AND CBV FILE DIRECTORY HERE ###
KIC = '9246715'
homedir = '/Users/Meredith/'
cbvdir = 'basisvectors/'
outfile = 'makelc_out.txt'
maskfile = 'mask_kepcotrend.txt'
plotaxes = [100, 1600, 9.6, 9.0]

# Read in Kepler light curve data from MAST
# For more info, see http://dan.iel.fm/kplr/#
client = kplr.API()
star = client.star(KIC)
lcs = star.get_light_curves(short_cadence=False)
time, flux_cbv, model, flux_sap, ferr, quality, kepmag = [], [], [], [], [], [], []
qtr = 0
for lc in lcs:
	# figure out the basis vector filename corresponding to each quarter (lc)
	if qtr == 15: drnum = '-d20'
	elif qtr == 16: drnum = '-d22'
	elif qtr == 17: drnum = '-d23'
	else: drnum = '-d21'
	if qtr < 10: qtr = '0' + str(qtr)
	else: qtr = str(qtr)
	fullKIC = str(lc)[17:26] #e.g. 009246715
	filenamechunk = str(lc)[27:40] #e.g. 2009131105131
	cbvfile = cbvdir + 'kplr' + filenamechunk + '-q' + qtr + drnum + '_lcbv.fits'
	lcin = homedir + '.kplr/data/lightcurves/' + fullKIC + '/kplr' + fullKIC + '-' + filenamechunk + '_llc.fits'
	lcout = homedir + '.kplr/data/lightcurves/' + fullKIC + '/cbv_kplr' + fullKIC + '-' + filenamechunk + '_llc.fits'
	# check if a maskfile exists. if yes, read it in. if no, don't use a mask.
	try:
		masktest = homedir + '.kplr/data/lightcurves/' + fullKIC + '/' + maskfile
		fmask = open(masktest)
		fullmaskfile = masktest
		mstart, mend = np.loadtxt(fmask, delimiter=',', unpack=True)
		mstart = mstart - 2454833
		mend = mend - 2454833
	except:
		print('No mask file found.')
		fullmaskfile = ''
		mstart = []
		mend = []
	# check if the cbv_filename.fits files already exist. if they don't, run kepcotrend.
	try:
		f = fits.open(lcout)
	except:
		print('Running kepcotrend...')
		kepcotrend(lcin, lcout, cbvfile, fullmaskfile)
		f = fits.open(lcout)
	# read in light curve data
	hdu_data = f[1].data #lc data is in the 1st FITS HDU
	time.append(hdu_data['time'])
	flux_sap.append(hdu_data['sap_flux'])
	model.append(hdu_data['cbvsap_modl'])
	flux_cbv.append(hdu_data['cbvsap_flux'])
	ferr.append(hdu_data['sap_flux_err'])
	quality.append(hdu_data['sap_quality'])
	#kepmag.append(hdu_data['kepmag'])
	kepmag.append(f[0].header['kepmag']) # kepler magnitude from header
	qtr = int(qtr) + 1

# Save the timestamp at the start of each quarter
qtrstart = []
for i in range(0,len(time)): qtrstart.append(time[i][0])

# Get rid of any observation that has NaNs, because we hate NaNs
for i in range(0,len(time)):
	time[i], flux_sap[i], ferr[i], flux_cbv[i], model[i], quality[i]  = nan_delete(
		time[i], flux_sap[i], ferr[i], flux_cbv[i], model[i], quality[i])

# Put data from different quarters on the same median level
flux_sap = normalize_qtr_med(flux_sap)
flux_cbv = normalize_qtr_med(flux_cbv)

# New time arrays for clearer accounting: one for the raw (SAP) flux and one for the
# processed (CBV) flux. These arrays are IDENTICAL.
time_cbv = time
time_sap = time

# Line up the gaps within each quarter
time_cbv, flux_cbv = lineup_qtr_gaps(time_cbv, flux_cbv, mstart, mend)
time_sap, flux_sap = lineup_qtr_gaps(time_sap, flux_sap, mstart, mend)

# Stitch all the quarters together into a single light curve
time_all_cbv = np.concatenate(time_cbv)
time_all_sap = np.concatenate(time_sap)
flux_all_cbv = np.concatenate(flux_cbv)
flux_all_sap = np.concatenate(flux_sap)
model_all = np.concatenate(model)
ferr_all = np.concatenate(ferr)

# Put everything on a magnitude scale
kepmag = np.mean(kepmag) # kepler magnitudes from file headers (should all be the same)
mag_all_sap = -2.5*np.log10(flux_all_sap) + (kepmag - np.median(-2.5*np.log10(flux_all_sap)))
merr_all_sap = 1.0857 * ferr_all / flux_all_sap
mag_all_cbv = -2.5*np.log10(flux_all_cbv) + (kepmag - np.median(-2.5*np.log10(flux_all_cbv)))
merr_all_cbv = 1.0857 * ferr_all / flux_all_cbv

# TODO: REMOVE LONG-TERM TREND OVER ALL THE QUARTERS W/O INTERPOLATING ??
# TODO: SOMEHOW MANUALLY REMOVE THE REMAINING ARTIFACTS/BLIPS ??

# Write out all light curve info to a file
f2 = open(outfile, 'w')
print('# Kepler time, SAP flux, flux err, SAP mag, mag err, CBV flux, CBV mag, CBV model', file=f2)
for i in range(0,len(time_all_sap)):
	print(time_all_sap[i], flux_all_sap[i], ferr_all[i], mag_all_sap[i], 
		merr_all_sap[i], flux_all_cbv[i], mag_all_cbv[i], model_all[i], file=f2)

# Make a plot!
## normalizations if you want to plot fluxes & model on same scale
#nrm1 = len(str(int(np.nanmax(flux_all_sap))))-1
#flux_all_cbv_plot = flux_all_cbv / np.power(10, nrm1) - 0.5
#flux_all_sap_plot = flux_all_sap / np.power(10, nrm1)
#model_all_plot = model_all / np.median(model_all)
#model_all_plot_mag = -2.5*np.log10(model_all+10) + (kepmag - np.median(-2.5*np.log10(model_all+10)))
##
# actually plot stuff already (in magnitudes)
plt.axis(plotaxes)
plt.plot(time_all_cbv, mag_all_cbv-0.2, color='k', linestyle='None', marker='.', label='CBV mag (offset)')
plt.plot(time_all_sap, mag_all_sap, color='r', linestyle='None', marker='.', label='SAP mag') 
#plt.plot(time_all_cbv, model_all_plot_mag-0.25, color='b', linestyle='None', marker='.', label='CBV model')
plt.vlines(qtrstart, 0, 10, colors='k', linestyles='dotted')
plt.xlabel('Time (BJD $-$ 2454833)')
plt.ylabel('Kepler Magnitude')
plt.legend(loc=3, numpoints=1)

plt.show()