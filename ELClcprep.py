from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
from lc_functions import phasecalc
'''
by Meredith Rawls
July 2014

Takes light curve data written by 'makelc.py' and makes a set of text files
that will work with ELC.
ELC is Jerry Orosz's "Eclipsing Light Curve" code for EBs. It is a Fortran black box
of doom, but it does amazing things if you feed and care for it.

Two main results: (1) a file with all the light curve data, and (2) a set of files
with light curve data containing one primary and one secondary eclipse each. The
last of these 'chunk' files will be empty because loops are annoying (sorry).
Also it makes a plot, because plots.
Everything is done in magnitudes.
We assume the BJD0 corresponds to the midpoint of the primary (deepest) eclipse.

You need to customize some variables below for your favorite KIC star.
This assumes you have previously run 'makelc.py' or otherwise have a textfile light curve.
'''

##### SET IMPORTANT THINGS HERE #####
KIC = '9246715'
period = 171.277967
BJD0 = 2455170.514777
# Choose PHASEMIN and PHASEMAX so that a primary & secondary eclipse fall neatly near
# the center of this range.
# You MUST choose phasemin < 1 and phasemax > 1; you likely want phasemax = phasemin + 1.
phasemin = 0.6
phasemax = 1.6
#infile = 'makelc_out.txt' # typically the file written by 'makelc.py'
infile = 'KIC_9246715_201408_Patrick.txt' # (or not)
plotaxes = [phasemin, phasemax, 9.4, 8.4]
#bigoutfile = 'ELC_lcall.txt'
bigoutfile = 'ELC_lcall_Patrick.txt'
outstub = 'ELC_Patrick_lc'

# Read in light curve
# The columns in 'infile' are as follows, from 'makelc.py':
# Kepler time, SAP flux, flux err, SAP mag, mag err, CBV flux, CBV mag, CBV model
f = open(infile)
if infile == 'makelc_out.txt': # assume special makelc.py column assignments
	times, mags, merrs = np.loadtxt(f, comments='#', dtype=np.float64, usecols=(0,3,4), unpack=True)
else: # assume time, mag, merr are in first three columns
	times, mags, merrs = np.loadtxt(f, comments='#', dtype=np.float64, usecols=(0,1,2), unpack=True)
f.close()

# Write the full light curve to an ELC-useable file
f = open(bigoutfile, 'w')
for time, mag, merr in zip(times, mags, merrs):
	print(time, mag, merr, file=f)
f.close()

# Calculate orbital phases (0-1), and make a 'phase2s' list (1-2).
BJD0_kep = BJD0 - 2454833 
phases = phasecalc(times, period, BJD0_kep)
phase2s = []
for phase in phases: phase2s.append(phase + 1)

# If the 'chunk' files already exist, skip ahead and make a plot.
# If the 'chunk' files don't exist yet, create them.
try:
	test = open(outstub+'0.txt')
	test.close()
	print('\''+outstub+'0.txt\' exists! Skipping ahead to plot this and the other chunks.')
	for i in range(0,100):
		try: test = open(outstub+str(i)+'.txt'); test.close()
		except: cyclecount = i-1; break
except:
	print('\''+outstub+'0.txt\' does not exist. Creating files...')
	# The 'cycle' variable keeps track of the filename for each 'chunk.'
	# We assume that phasemin < 1 and phasemax > 1. If not... good luck.
	## loop through phases 0-1
	cycle = 0
	f = open(outstub+'0.txt', 'a') #append, don't overwrite. this is important.
	for i, (phase, time, mag, merr) in enumerate(zip(phases[:-1], times[:-1], mags[:-1], merrs[:-1])):
		if phase > phasemin: print(time, mag, merr, file=f)
		if phases[i+1] < phase: #if we go from 0.999 back to 0.000, we're done
			f.close()
			cycle += 1
			f = open(outstub+str(cycle)+'.txt', 'a')
	f.close()
	## loop through phases 1-2
	if phase2s[0] > phasemax: cycle = -1 #nothing here, move along
	else: cycle = 0 #actually start here
	f = open(outstub+'0.txt', 'a')
	for i, (phase2, time, mag, merr) in enumerate(zip(phase2s[:-1], times[:-1], mags[:-1], merrs[:-1])):
		if phase2 < phasemax: print(time, mag, merr, file=f)
		if phase2s[i+1] < phase2: #if we go from 1.999 back to 1.000, we're done
			f.close()
			cycle += 1
			f = open(outstub+str(cycle)+'.txt', 'a')
	f.close()
	cyclecount = cycle

# Option to plot the ENTIRE folded light curve on top of itself instead of the chunks
#phasedoubles = np.concatenate((phases, phase2s))
#cycledoubles = np.concatenate((cycles, cycles))
#timedoubles = np.concatenate((times, times))
#magdoubles = np.concatenate((mags, mags))
#merrdoubles = np.concatenate((merrs, merrs))
#plt.plot(phasedoubles, magdoubles, color='k', linestyle='None', marker='.')

# Plot each chunk with an offset in magnitude to see the data we'll be working with
plt.axis(plotaxes)
yoffset = 0
for idx in range(0, cyclecount):
	f = open(outstub+str(idx)+'.txt')
	times, mags, merrs = np.loadtxt(f, comments='#', usecols=(0,1,2), unpack=True)
	f.close()
	phases = phasecalc(times, period, BJD0_kep)
	phase2s = []
	for phase in phases: phase2s.append(phase + 1)
	phasedoubles = np.concatenate((phases, phase2s))
	magdoubles = np.concatenate((mags, mags))
	plt.plot(phasedoubles, magdoubles-yoffset, color='r', linestyle='None', marker='.')
	yoffset += 0.1

plt.xlabel('Orbital Phase')
plt.ylabel('Kepler Magnitude')

plt.show()