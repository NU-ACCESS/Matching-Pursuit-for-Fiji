# Matching-Pursuit-for-Fiji
Python script for Fiji based on sparse weights, w, given an image X and a dictionary D following this cost function ||X-Dw||. 

Based on these java libraries for sparse modeling: http://www.ux.uis.no/~karlsk/dle/mpv2-class.zip. 

1) Download zipfile, extract it, rename as mpv, and install in plugins folder. 
2) Create an over complete dictionary D with atoms constructed from the hyperspectral measurement of pure pigments (e.g., from the pigment boards we have in the lab). Make sure the atoms are normalized (0 min, 1 max). Make sure the image X is also normalized in the same way.
save these atoms in a text file with the spectra arranged in columns.

This code is still experimental... more to come
