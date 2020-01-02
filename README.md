# Matching-Pursuit-for-Fiji
Python script for Fiji based on sparse weights, **w**, given an image **X** and a dictionary **D** following this cost function **min||X-Dw||**. 

This script wraps java libraries for sparse modeling written by Karl Skretting:  For more infomation see http://www.ux.uis.no/~karlsk/dle/doc/index.html

1) Download the following class file: http://www.ux.uis.no/~karlsk/dle/mpv2-class.zip. Extract it, rename as mpv, and install in plugins folder. 
2) Download and install sparseapprox.py in the plugins folder
2) Create an over complete dictionary D with atoms constructed from the hyperspectral measurement of pure pigments or through the extraction of endmembers. Ensure that the atoms in D and the image X are normalized (0 min, 1 max).
3) Save D as a text file with the spectra arranged in columns.

The script has a GUI that prompts the user to select the dictionary file and then which greedy algorithm they want ti employ: MP (basic matching pursuit), OMP (orthogonal matching pursuit), or ORMP (order recursive matching pursuit). Also used as an input is the number of non-zero elements desired in the **w** matrix.
