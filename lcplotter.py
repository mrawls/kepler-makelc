from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import IndexLocator, FormatStrFormatter
from lc_functions import phasecalc
'''
Make a nice plot of an RGEB Kepler light curve for a paper.
You'd better run 'makelc.py' and 'ELClcprep.py' first !!
'''

# Important starting info
KIC = '9246715'
period = 171.277967
BJD0 = 2455170.514777
infile = 'makelc_out.txt' # must be the file written by 'makelc.py'
red = '#e34a33' # RV curve red, star 1
yel = '#fdbb84' # RV curve yellow, star 2

# Read in full light curve
# The columns in 'infile' are as follows, from 'makelc.py':
# Kepler time, SAP flux, flux err, SAP mag, mag err, CBV flux, CBV mag, CBV model
f = open(infile)
times, mags, merrs = np.loadtxt(f, comments='#', dtype=np.float64, usecols=(0,3,4), unpack=True)
f.close()

# Read in light curve chunks
try:
	test = open('ELC_lc0.txt')
	test.close()
	for i in range(0,100):
		try: test = open('ELC_lc'+str(i)+'.txt'); test.close()
		except: cyclecount = i-1; break
except:
	print('Sorry, no chunk files found.')
	cyclecount = 0

# Calculate orbital phases (0-1), and make a 'phase2s' list (1-2).
BJD0_kep = BJD0 - 2454833 
phases = phasecalc(times, period, BJD0_kep)
phase2s = []
for phase in phases: phase2s.append(phase + 1)

# System-specific plot parameters
primary_phasemin = 0.985 #0.48
primary_phasemax = 1.015 #0.52
secondary_phasemin = 0.699 #0.194
secondary_phasemax = 0.729 #0.234
phasemin = 0
phasemax = 2
magdim = 9.54
magdimzoom = 9.74
magbright = 9.205
timemin = 100
timemax = 1600

# Folded full light curve
ax2 = plt.subplot2grid((14,2),(5,0), colspan=2, rowspan=4)
plt.axis([phasemin, phasemax, magdim, magbright])
plt.plot(phases, mags, color=red, marker='.', ls='None', ms=5, mew=0)
plt.plot(phase2s, mags, color=red, marker='.', ls='None', ms=5, mew=0)
ax2.axvline(x=0.5, color='k', ls=':') #vertical lines
ax2.axvline(x=1.5, color='k', ls=':')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.xaxis.set_ticks_position('bottom')
ax2.yaxis.set_ticks_position('left')
# plot phases of RV observations on top? #NOPE, not now, would look too busy
#ax2.set_ylabel('Kepler Magnitude')
#ax2.set_xlabel('Orbital Phase')

# Full light curve
ax1 = plt.subplot2grid((14,2),(0,0), colspan=2, rowspan=4)
plt.axis([timemin, timemax, magdim, magbright])
plt.tick_params(axis='both', which='major')
plt.plot(times, mags, color='#e34a33', marker='.', ls='None', ms=5, mew=0)
#ax1.set_ylabel('Kepler Magnitude')#, size=18)
ax1.set_xlabel('Time (BJD $-$ 2454833)', size=24)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.xaxis.set_ticks_position('bottom')
ax1.yaxis.set_ticks_position('left')
#ax1.set_xticklabels([])

# Secondary eclipse zoom & offset
ax3 = plt.subplot2grid((14,2),(10,0), rowspan=5)
plt.subplots_adjust(wspace = 0.0001, hspace=0.0001)
plt.axis([secondary_phasemin, secondary_phasemax, magdimzoom, magbright])
ax3.xaxis.set_major_locator(IndexLocator(0.01, 0.70))
ax3.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
#ax3.yaxis.set_major_locator(IndexLocator(0.1, 9.8))
offset = 0
for i in range(0, cyclecount):
	f = open('ELC_lc'+str(i)+'.txt')
	times, mags, merrs = np.loadtxt(f, comments='#', usecols=(0,1,2), unpack=True)
	f.close()
	phases = phasecalc(times, period, BJD0_kep)
	phase2s = []
	for phase in phases: phase2s.append(phase + 1)
	plt.plot(phases, mags+offset, color=yel, marker='.', ls='None', ms=5, mew=0)
	offset += 0.03

# Primary eclipse zoom & offset
ax4 = plt.subplot2grid((14,2),(10,1), rowspan=5)
plt.axis([primary_phasemin, primary_phasemax, magdimzoom, magbright])
ax4.xaxis.set_major_locator(IndexLocator(0.01, 0.99))
ax4.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
#ax4.yaxis.set_major_locator(IndexLocator(0.1, 9.8))
offset = 0
for i in range(0, cyclecount):
	f = open('ELC_lc'+str(i)+'.txt')
	times, mags, merrs = np.loadtxt(f, comments='#', usecols=(0,1,2), unpack=True)
	f.close()
	phases = phasecalc(times, period, BJD0_kep)
	phase2s = []
	for phase in phases: phase2s.append(phase + 1)
	plt.plot(phases, mags+offset, color=red, marker='.', ls='None', ms=5, mew=0)
	plt.plot(phase2s, mags+offset, color=red, marker='.', ls='None', ms=5, mew=0)
	offset += 0.03
ax4.set_yticklabels([])

plt.figtext(0.5, 0.04, 'Orbital Phase', ha='center', va='center', size=24)
plt.figtext(0.05, 0.5, 'Kepler Magnitude', ha='center', va='center', rotation='vertical', size=24)
plt.figtext(0.135, 0.13, 'Secondary \n (offset)', size=20)
plt.figtext(0.525, 0.13, 'Primary \n (offset)', size=20)
plt.figtext(0.135, 0.42, 'Folded', size=20)

plt.show()