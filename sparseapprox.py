#This creates a sparse approximation w of a signal X provided a dictionary D.
#||X-Dw||
#Requires mpv2 package: http://www.ux.uis.no/~karlsk/dle/mpv2-class.zip
#Improvements  to come in the next version

from ij import IJ, ImagePlus
from ij.plugin import ImageCalculator
from ij.process import ImageProcessor
from ij.process import FloatProcessor
#import sys
#sys.path.append('Jama.jar')
#from Jama import Matrix
from mpv2 import MatchingPursuit as MP, JamaMatrix as Matrix, SymmetricMatrix as SM

imp2 = IJ.getImage()
IJ.run("32-bit")
imp2 = IJ.getImage()

#path to lighting directions
IJ.run("Text Image... ", "open=")
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
  W = jMP.vsBMP(q,K)   
  w.append(W)

w2 = zip(*w)

Sp = Matrix(w2).getColumnPackedCopy()

#return matrices to images 
ipFloat = FloatProcessor(K, imp2.height*imp2.width, Sp)
impa = ImagePlus("Sp", ipFloat)
impa.show()

#reshape as using montage and reslice commands (need a better way to do this) 
IJ.run(impa,"Montage to Stack...", "images_per_row=1 images_per_column=%d border=0" % imp2.height)
impb = IJ.getImage()
IJ.run("Reslice [/]...", "output=1.000 start=Left avoid")
impc = IJ.getImage()

impa.close()
impb.close()
