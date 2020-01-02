#This creates a sparse approximation w of a signal X provided a dictionary D.
#||X-Dw||
#Requires mpv2 package: http://www.ux.uis.no/~karlsk/dle/mpv2-class.zip
#Improvements  to come in the next version

from ij import IJ, ImagePlus
from ij.plugin import ImageCalculator
from ij.process import ImageProcessor
from ij.process import FloatProcessor
from fiji.util.gui  import GenericDialogPlus
from mpv2 import MatchingPursuit as MP, JamaMatrix as Matrix, SymmetricMatrix as SM

#Input parameters
gd = GenericDialogPlus("Sparse Approximation, Input Parameters")  
gd.addDirectoryOrFileField("Select dictionary D","")
gd.addChoice("Greedy algorithm type", ["MP","OMP","ORMP"], "OMP")
gd.addNumericField("Number of non-zero elements in w", 3, 0)  # show 3 decimals
gd.showDialog()

directory_w = gd.getNextString()
t_w = int(gd.getNextNumber()) 
Rt = gd.getNextChoice()

imp2 = IJ.getImage()
IJ.run("32-bit")
imp2 = IJ.getImage()

#path to lighting directions
IJ.run("Text Image... ", "open="+str(directory_w))
imp = IJ.getImage()
imp.setTitle("Dictionary Atoms")

# making a jython nested list for constructing dictionary atom matrix
m = imp.getProcessor().getPixels()
m2 = [val for val in m]
K = imp.width
L = [m2[i:i+K] for i in range(0, len(m2), K)]

imp.close()

# reshape image stack as an n x m matrix
n_slices = imp2.getStack().getSize()
I =[]
for i in range(1, n_slices+1):
  imp2.setSlice(i) 
  n = imp2.getProcessor().getPixels()   
  n2 = [val for val in n]
  I.append(n2)

  
# construct matrices and create symmetric dictionary
x = zip(*I)#transpose I
p = len(x)# numb of pixels in image
jD = Matrix(L)
jDD = SM(K,K).eqInnerProductMatrix(jD)
jMP = MP(jD,jDD)



# matching pursuit to create a sparse appoximation

w =[]
for i in range(0, p):
	q = x[i]
	if Rt == "OMP":
		W = jMP.vsOMP(q,t_w)
	elif Rt == "MP":
		W = jMP.vsBMP(q,t_w)
	else: 
		W = jMP.vsORMP(q,t_w)
	w.append(W)
		
w2 = zip(*w)

Sp = Matrix(w2).getColumnPackedCopy()

#return matrices to images 
ipFloat = FloatProcessor(K, imp2.height*imp2.width, Sp)
impa = ImagePlus("Sp", ipFloat)
impa.show()
IJ.run("Montage to Stack...", "columns=1 rows="+str(imp2.height)+" border=0")
imp3=IJ.getImage()
IJ.run("Reslice [/]...", "output=1.000 start=Left avoid")
impa.close()
imp3.close()
