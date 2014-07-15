kepler-makelc
=============

These programs are intended for folks who care about Eclipsing Binaries observed by _Kepler_. They may be applicable to a wider set of situations, but that is the original use.

### makelc.py

Deletes NaNs, puts SAP flux data from multiple quarters onto the same median level, and nicely lines up gaps between quarters. Does NOT use any interpolation.

Additionally runs kepcotrend to get a detrended flux, and performs the operations listed above on that, too. So you can use whichever you prefer.

The full light curve (all quarters, and both SAP and detrended (CBV) data) is written to a large text file. Both flux and magnitude units are calculated, and both have error bars.

Works for ANY valid KIC target your heart desires (no need to already have the data)!

### ELClcprep.py

Breaks light curves into 'chunks' for use with Jerry Orosz's modeling program ELC. You need to specify some details about your star in the code before running this program.

### lc_functions.py

Some handy functions that are used in both programs above.




