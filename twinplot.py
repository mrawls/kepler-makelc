import numpy as np
import matplotlib.pyplot as plt
'''
Meredith Rawls, 2015
(inspired by Paul Beck)

Makes a plot of two stars' oscillation spectra. Presumably the two stars are nearly
'twins,' i.e. they have similar oscillation patterns but one is noisier than the other
so you want to use the better-characterized one to inform an analysis of the noisy one.

Input: two text files with two columns each (frequency and power)
Output: pretty plot with one oscillation spectrum on top axis and one on bottom axis
'''
target_infile = '../../Rawls_etal_2015/seismicTwin/KIC9246715_smoothed_50.txt'
twin_infile = '../../Rawls_etal_2015/seismicTwin/KIC11725564_SiB_comparison_50.txt'

target_freq, target_amp = np.loadtxt(target_infile, usecols=(0,1), unpack=True)
twin_freq, twin_amp = np.loadtxt(twin_infile, usecols=(0,1), unpack=True)

red = '#e34a33'
gray = '#808080'
fig, ax2 = plt.subplots(1, figsize=(15,7))
plt.xlabel('Frequency ($\mu$Hz)')
plt.ylabel('Smoothed Power Density (ppm$^2$ $\mu$Hz$^{-1}$)')

ax2.set_xlim([61,149])
ax2.set_ylim([0,850])
ax1 = ax2.twinx()
ax1.set_xlim([61,149])
ax1.set_ylim([0,850])
ax1.xaxis.set_label_position('top')
ax1.xaxis.set_ticks_position('top')
ax1.yaxis.set_label_position('right')
ax1.yaxis.set_ticks_position('right')

ax1.stackplot(twin_freq, twin_amp, edgecolor='None', colors=(gray,))
ax2.stackplot(target_freq, target_amp, edgecolor='None', colors=(red,))

ax1.invert_yaxis()
plt.show()