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
#infile = 'makelc_out.txt' # typically the file written by 'makelc.py'
infile = 'ELC_lcall_Patrick.txt'
instub = 'ELC_Patrick_lc'
red = '#e34a33' # red, star 1
yel = '#fdbb84' # yellow, star 2

# Read in full light curve
# The columns in 'infile' are as follows, from 'makelc.py':
# Kepler time, SAP flux, flux err, SAP mag, mag err, CBV flux, CBV mag, CBV model
f = open(infile)
#times, mags, merrs = np.loadtxt(f, comments='#', dtype=np.float64, usecols=(0,3,4), unpack=True)
times, mags, merrs = np.loadtxt(f, comments='#', dtype=np.float64, usecols=(0,1,2), unpack=True)
f.close()

# Read in light curve chunks	
try:
	test = open(instub+'0.txt')
	test.close()
	for i in range(0,100):
		try: test = open(instub+str(i)+'.txt'); test.close()
		except: cyclecount = i; break
except:
	print('Sorry, no chunk files found.')
	cyclecount = 0

# Calculate orbital phases (0-1), and make a 'phase2s' list (1-2).
BJD0_kep = BJD0 - 2454833 
phases = phasecalc(times, period, BJD0_kep)
phase2s = []
for phase in phases: phase2s.append(phase + 1)

# System-specific plot parameters
primary_phasemin = 0.97 #0.985 #0.48
primary_phasemax = 1.03 #1.015 #0.52
secondary_phasemin = 0.683 #0.699 #0.194
secondary_phasemax = 0.743 #0.729 #0.234
phasemin = 0.5
phasemax = 1.5
magdim = 9.54
magdimzoom = 9.78
magbright = 9.205
magbrightzoom = 9.24
timemin = 100
timemax = 1600

# Folded full light curve
ax2 = plt.subplot2grid((14,2),(5,0), colspan=2, rowspan=4)
plt.axis([phasemin, phasemax, magdim, magbright])
plt.plot(phases, mags, color=red, marker='.', ls='None', ms=5, mew=0)
plt.plot(phase2s, mags, color=red, marker='.', ls='None', ms=5, mew=0)
#ax2.axvline(x=0.5, color='k', ls=':') #dotted vertical lines
#ax2.axvline(x=1.5, color='k', ls=':')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.xaxis.set_ticks_position('bottom')
ax2.yaxis.set_ticks_position('left')
ax2.axvline(x=primary_phasemin, color='k', ls=':') # vertical lines showing zoom extent
ax2.axvline(x=primary_phasemax, color='k', ls=':')
ax2.axvline(x=secondary_phasemin, color='k', ls=':')
ax2.axvline(x=secondary_phasemax, color='k', ls=':')
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
plt.axis([secondary_phasemin, secondary_phasemax, magdimzoom, magbrightzoom])
ax3.xaxis.set_major_locator(IndexLocator(0.01, 0.68))
ax3.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
ax3.spines['top'].set_visible(False)
ax3.xaxis.set_ticks_position('bottom')
#ax3.yaxis.set_major_locator(IndexLocator(0.1, 9.8))
offset = 0
for i in range(0, cyclecount):
	f = open(instub+str(i)+'.txt')
	times, mags, merrs = np.loadtxt(f, comments='#', usecols=(0,1,2), unpack=True)
	f.close()
	phases = phasecalc(times, period, BJD0_kep)
	phase2s = []
	for phase in phases: phase2s.append(phase + 1)
	plt.plot(phases, mags+offset, color=yel, marker='.', ls='None', ms=5, mew=0)
	offset += 0.03
# Little circles
plt.scatter(0.73, 9.61, s=4000, facecolors=red, edgecolors=red)
plt.scatter(0.73, 9.67, s=2000, facecolors=yel, edgecolors=yel)

# Primary eclipse zoom & offset
ax4 = plt.subplot2grid((14,2),(10,1), rowspan=5)
plt.axis([primary_phasemin, primary_phasemax, magdimzoom, magbrightzoom])
ax4.xaxis.set_major_locator(IndexLocator(0.01, 0.98))
ax4.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
ax4.spines['top'].set_visible(False)
ax4.xaxis.set_ticks_position('bottom')
#ax4.yaxis.set_major_locator(IndexLocator(0.1, 9.8))
offset = 0
for i in range(0, cyclecount):
	f = open(instub+str(i)+'.txt')
	times, mags, merrs = np.loadtxt(f, comments='#', usecols=(0,1,2), unpack=True)
	f.close()
	phases = phasecalc(times, period, BJD0_kep)
	phase2s = []
	for phase in phases: phase2s.append(phase + 1)
	plt.plot(phases, mags+offset, color=red, marker='.', ls='None', ms=5, mew=0)
	plt.plot(phase2s, mags+offset, color=red, marker='.', ls='None', ms=5, mew=0)
	offset += 0.03
ax4.set_yticklabels([])
# Little circles
plt.scatter(1.02, 9.61, s=2000, facecolors=yel, edgecolors=yel)
plt.scatter(1.02, 9.67, s=4000, facecolors=red, edgecolors=red)


plt.figtext(0.5, 0.04, 'Orbital Phase', ha='center', va='center', size=28)
plt.figtext(0.05, 0.5, 'Kepler Magnitude', ha='center', va='center', rotation='vertical', size=28)
plt.figtext(0.135, 0.13, 'Secondary \n (offset)', size=24)
plt.figtext(0.525, 0.13, 'Primary \n (offset)', size=24)
plt.figtext(0.135, 0.40, 'Folded', size=24)
plt.figtext(0.135, 0.685, 'Unfolded', size=24)
#plt.scatter(0.4, 0.1, s=np.pi*(np.power(0.5,2)), c='#e34a33')
#plt.Circle((0.4, 0.1), 0.1, ec='#e34a33', fc='#e34a33')

plt.show()