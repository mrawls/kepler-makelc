from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import IndexLocator, FormatStrFormatter, ScalarFormatter
from lc_functions import phasecalc
'''
Makes a nice plot of an RGEB Kepler light curve for a paper.
You will want to run 'ELClcprep.py' first.
'''

# Important starting info
#infile = 'makelc_out.txt'  # often the file written by 'makelc.py'
#instub = 'ELC_lc'          # beginning part of each of the 'chunk' files
pristarcirclesize = 4000; secstarcirclesize = 500
red = '#e34a33' # red, star 1
yel = '#fdbb84' # yellow, star 2

# 946715
#KIC = '9246715'; period = 171.277967; BJD0 = 2455170.514777
#infile = '../../RG_light_curves/9246715/KIC_9246715_201408_Patrick.txt'
#instub = '../../RG_light_curves/9246715/ELC_Patrick_lc'
#primary_phasemin = 0.97; primary_phasemax = 1.03
#secondary_phasemin = 0.685; secondary_phasemax = 0.745
#phasemin = 0.5; phasemax = 1.5
#magdim = 9.54; magbright = 9.21
#magdimzoom = 9.79; magbrightzoom = 9.21
#timemin = 100; timemax = 1600
#pristarcirclesize = 4000; secstarcirclesize = 4000
#zoommagspace = 0.03

# 8702921
KIC = '8702921'; period = 19.38446; BJD0 = 2454970.2139
infile = '../../RG_light_curves/8702921/KIC_8702921_LC_mag_Q017.txt'
instub = '../../RG_light_curves/8702921/lcchunk'
primary_phasemin = 0.935; primary_phasemax = 1.075
secondary_phasemin = 0.37; secondary_phasemax = 0.51
phasemin = 0.2; phasemax = 1.2
magdim = 11.986; magbright = 11.979
magdimzoom = 12.06; magbrightzoom = 11.979
timemin = 100; timemax = 1600
zoommagspace = 0.001

# 9291629
#KIC = '9291629'; period = 20.68639; BJD0 = 2454966.882
#infile = '../../RG_light_curves/9291629/KIC_9291629_LC_mag_Q017.txt'
#instub = '../../RG_light_curves/9291629/lcchunk'
#primary_phasemin = 0.91; primary_phasemax = 1.09
#secondary_phasemin = 0.41; secondary_phasemax = 0.59
#phasemin = 0.2; phasemax = 1.2
#magdim = 14.17; magbright = 13.93
#magdimzoom = 14.85; magbrightzoom = 13.93
#timemin = 100; timemax = 1600
#zoommagspace = 0.01

# 3955867
#KIC = '3955867'; period = 33.65685; BJD0 = 2454960.8989
#infile = '../../RG_light_curves/3955867/KIC_3955867-phot_transit_only.txt'
#instub = '../../RG_light_curves/3955867/lcchunk'
#primary_phasemin = 0.94; primary_phasemax = 1.06
#secondary_phasemin = 0.435; secondary_phasemax = 0.575
#phasemin = 0.2; phasemax = 1.2
#magdim = 13.605; magbright = 13.541
#magdimzoom = 14.05; magbrightzoom = 13.541
#timemin = 100; timemax = 1600
#zoommagspace = 0.01

# 10001167
#KIC = '10001167'; period = 120.3903; BJD0 = 2454957.682
#infile = '../../RG_light_curves/10001167/KIC_10001167-phot_transit_only.txt'
#instub = '../../RG_light_curves/10001167/lcchunk'
#primary_phasemin = 0.95; primary_phasemax = 1.05
#secondary_phasemin = 0.535; secondary_phasemax = 0.635
#phasemin = 0.2; phasemax = 1.2
#magdim = 10.080; magbright = 10.045
#magdimzoom = 10.5; magbrightzoom = 10.045
#timemin = 100; timemax = 1600
#zoommagspace = 0.03

# 5786154
#KIC = '5786154'; period = 197.9182; BJD0 = 2455162.6140
#infile = '../../RG_light_curves/5786154/KIC_5786154_LC_mag_Q017.txt'
#instub = '../../RG_light_curves/5786154/lcchunk'
#primary_phasemin = 0.97; primary_phasemax = 1.03
#secondary_phasemin = 0.255; secondary_phasemax = 0.315
#phasemin = 0.2; phasemax = 1.2
#magdim = 13.635; magbright = 13.52
#magdimzoom = 13.9; magbrightzoom = 13.52
#timemin = 100; timemax = 1600
#zoommagspace = 0.03

# 7037405
#KIC = '7037405'; period = 207.1082; BJD0 = 2455112.7655
#infile = '../../RG_light_curves/7037405/KIC_7037405-phot_transit_only.txt'
#instub = '../../RG_light_curves/7037405/ELC_Patrick_lc'
#primary_phasemin = 0.97; primary_phasemax = 1.03
#secondary_phasemin = 0.368; secondary_phasemax = 0.428
#phasemin = 0.2; phasemax = 1.2
#magdim = 11.967; magbright = 11.862
#magdimzoom = 12.19; magbrightzoom = 11.85
#timemin = 100; timemax = 1600
#zoommagspace = 0.03

# 9970396
#KIC = '9970396'; period = 235.300; BJD0 = 2455190.539
#infile = '../../RG_light_curves/9970396/KIC_9970396_LC_mag_Q017.txt'
#instub = '../../RG_light_curves/9970396/lcchunk'
#primary_phasemin = 0.97; primary_phasemax = 1.03
#secondary_phasemin = 0.385; secondary_phasemax = 0.445
#phasemin = 0.2; phasemax = 1.2
#magdim = 11.53; magbright = 11.43
#magdimzoom = 11.75; magbrightzoom = 11.43
#timemin = 100; timemax = 1600
#zoommagspace = 0.03


# Read in full light curve
# The columns in 'infile' are as follows, from 'makelc.py':
# Kepler time, SAP flux, flux err, SAP mag, mag err, CBV flux, CBV mag, CBV model
f = open(infile)
#times, mags, merrs = np.loadtxt(f, comments='#', dtype=np.float64, usecols=(0,3,4), unpack=True)
times, mags, merrs = np.loadtxt(f, comments='#', dtype=np.float64, usecols=(0,1,2), unpack=True)
f.close()

# Read in light curve chunks
# This assumes you have chunk0 - chunkN with no gaps  
try:
    test = open(instub+'0.txt')
    test.close()
    for i in range(0,100):
        try: test = open(instub+str(i)+'.txt'); test.close()
        except: cyclecount = i; break
except:
    print('Skipping chunk files, no chunk0 file found.')
    cyclecount = 0

# Calculate orbital phases (0-1), and make a 'phase2s' list (1-2).
BJD0_kep = BJD0 - 2454833 
phases = phasecalc(times, period, BJD0_kep)
phase2s = []
for phase in phases: phase2s.append(phase + 1)

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
ax2.ticklabel_format(useOffset=False)
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
ax1.ticklabel_format(useOffset=False)
#ax1.set_xticklabels([])

# Option to plot vertical lines at certain timestamps
# (to visually isolate one spacecraft orientation, for instance)
#plt.axvline(169)
#plt.axvline(257)
#plt.axvline(538)
#plt.axvline(628)
#plt.axvline(906)
#plt.axvline(999)
#plt.axvline(1273)
#plt.axvline(1370)

# Secondary eclipse zoom & offset
ax3 = plt.subplot2grid((14,2),(10,0), rowspan=5)
plt.subplots_adjust(wspace = 0.0001, hspace=0.0001)
plt.axis([secondary_phasemin, secondary_phasemax, magdimzoom, magbrightzoom])
#ax3.xaxis.set_major_locator(IndexLocator(0.01, 0.37))
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
    plt.plot(phases, mags+offset, color=yel, marker='.', ls='None', ms=5, mew=0) ###
    offset += zoommagspace
plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)
# Little circles
#plt.scatter(secondary_phasemax-0.01, magdimzoom-0.17, s=pristarcirclesize, facecolors=red, edgecolors=red)
#plt.scatter(secondary_phasemax-0.01, magdimzoom-0.11, s=secstarcirclesize, facecolors=yel, edgecolors=yel)

# Primary eclipse zoom & offset
ax4 = plt.subplot2grid((14,2),(10,1), rowspan=5)
plt.axis([primary_phasemin, primary_phasemax, magdimzoom, magbrightzoom])
#ax4.xaxis.set_major_locator(IndexLocator(0.01, 0.98))
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
    plt.plot(phases, mags+offset, color=red, marker='.', ls='None', ms=5, mew=0) ###
    plt.plot(phase2s, mags+offset, color=red, marker='.', ls='None', ms=5, mew=0) ###
    offset += zoommagspace
ax4.set_yticklabels([])
# Little circles
#plt.scatter(primary_phasemax-0.01, magdimzoom-0.17, s=secstarcirclesize, facecolors=yel, edgecolors=yel)
#plt.scatter(primary_phasemax-0.01, magdimzoom-0.11, s=pristarcirclesize, facecolors=red, edgecolors=red)


plt.figtext(0.5, 0.05, 'Orbital Phase', ha='center', va='center', size=28)
plt.figtext(0.04, 0.5, 'Kepler Magnitude', ha='center', va='center', rotation='vertical', size=28)
plt.figtext(0.135, 0.12, 'Secondary \n (offset)', size=24)
plt.figtext(0.525, 0.12, 'Primary \n (offset)', size=24)
plt.figtext(0.135, 0.40, 'Folded', size=24)
plt.figtext(0.135, 0.685, 'Unfolded', size=24)

plt.show()