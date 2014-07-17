from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import IndexLocator, FormatStrFormatter
from lc_functions import phasecalc
'''
Make a nice plot of an RGEB Kepler light curve for a paper.
You'd better run 'makelc.py' and 'ELClcprep.py' first !!

For reference... 
Pretty dark red color is color='#e34a33'
Complementary light yellow color is color='#fdbb84'
'''

# Important starting info
KIC = '9246715'
period = 171.277967
BJD0 = 2455170.514777
infile = 'makelc_out.txt' # must be the file written by 'makelc.py'

# Read in light curve
# The columns in 'infile' are as follows, from 'makelc.py':
# Kepler time, SAP flux, flux err, SAP mag, mag err, CBV flux, CBV mag, CBV model
f = open(infile)
times, mags, merrs = np.loadtxt(f, comments='#', dtype=np.float64, usecols=(0,3,4), unpack=True)
f.close()

# Calculate orbital phases (0-1), and make a 'phase2s' list (1-2).
BJD0_kep = BJD0 - 2454833 
phases = phasecalc(times, period, BJD0_kep)
phase2s = []
for phase in phases: phase2s.append(phase + 1)

# System-specific plot parameters
primary_phasemin = 0.98 #0.48
primary_phasemax = 1.02 #0.52
secondary_phasemin = 0.694 #0.194
secondary_phasemax = 0.734 #0.234
phasemin = 0
phasemax = 2
magdim = 9.54
magbright = 9.20
timemin = 100
timemax = 1600

# Full light curve
ax1 = plt.subplot2grid((3,2),(0,0), colspan=2)
plt.axis([timemin, timemax, magdim, magbright])
plt.tick_params(axis='both', which='major')
plt.plot(times, mags, color='#e34a33', marker='.', ls='None', ms=5, mew=0)
#ax1.set_ylabel('Kepler Magnitude')#, size=18)
ax1.set_xlabel('Time (BJD $-$ 2454833)')
#ax1.set_xticklabels([])

# Folded full light curve
ax2 = plt.subplot2grid((3,2),(1,0), colspan=2)
plt.axis([phasemin, phasemax, magdim, magbright])
plt.plot(phases, mags, color='#e34a33', marker='.', ls='None', ms=5, mew=0)
plt.plot(phase2s, mags, color='#e34a33', marker='.', ls='None', ms=5, mew=0)
plt.axvline(x=0.5, ymin=magdim, ymax=magbright, color='0.75', ls=':')
plt.axvline(x=1.5, ymin=magdim, ymax=magbright, color='0.75', ls=':')
# plot phases of RV observations on top?
#ax2.set_ylabel('Kepler Magnitude')
#ax2.set_xlabel('Orbital Phase')

# Secondary eclipse zoom & offset
# NEED TO ACTUALLY OFFSET !!!
ax3 = plt.subplot2grid((3,2),(2,0))
plt.axis([secondary_phasemin, secondary_phasemax, magdim, magbright])
ax3.xaxis.set_major_locator(IndexLocator(0.01, 0.20))
ax3.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
plt.plot(phases, mags, color='#e34a33', marker='.', ls='None', ms=5, mew=0)

# Primary eclipse zoom & offset
ax4 = plt.subplot2grid((3,2),(2,1))
plt.axis([primary_phasemin, primary_phasemax, magdim, magbright])
ax4.xaxis.set_major_locator(IndexLocator(0.01, 0.49))
ax4.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
plt.plot(phases, mags, color='#e34a33', marker='.', ls='None', ms=5, mew=0)
plt.plot(phase2s, mags, color='#e34a33', marker='.', ls='None', ms=5, mew=0)
ax4.set_yticklabels([])

plt.figtext(0.5, 0.04, 'Orbital Phase', ha='center', va='center', size=25)
plt.figtext(0.05, 0.5, 'Kepler Magnitude', ha='center', va='center', rotation='vertical', size=25)
plt.figtext(0.135, 0.34, 'Secondary \n Eclipse')
plt.figtext(0.525, 0.34, 'Primary \n Eclipse')

plt.show()