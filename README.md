kepler-makelc
=============

Basic light curve 'detrending' for all your KIC EB needs.

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
1. Be sure you have numpy, matplotlib, kplr, astropy, pyraf, and PyKE installed
  --> if you don't, try 'pip install kplr' (for example)
  --> PyKE is a bit more complicated: see http://keplergo.arc.nasa.gov/PyKE.shtml
2. Be sure you have 'lc_functions.py' saved in the same directory as this file
3. Download ALL the basis vectors and save them in a subdirectory called 'basisvectors'
  --> get them here: https://archive.stsci.edu/kepler/cbv.html
4. Optional: make a mask (e.g., for eclipses) in real BJD units (Kepler time + 2454833)
  --> see mask_kepcotrend.txt for an example
  --> save the mask file in ~/.kplr/data/lightcurves/KICNUMBERHERE/.
  --> if no mask file is found, the program will still work
5. Optional: tweak the parameters used in the kepcotrend task in 'lc_functions.py'.
  --> for more info, see: http://keplergo.arc.nasa.gov/ContributedSoftwareKepcotrend.shtml
6. Change any settings below as necessary (KIC, home directory, etc.)
7. Type 'python makelc.py' and watch the magic happen
