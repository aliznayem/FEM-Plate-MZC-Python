# FEM-Plate-MZC-Python
Melosh and Zienkiewicz and Cheung developed a popular 4-noded plate rectangle which is known as MZC plate element. [MAT-fem](http://www.cimne.com/mat-fem/plates.asp) developed a Matlab program for FEM analysis of thin plate with the MZC element.

I just converted the Matlab code into Python and added some features.

## Added features in Python version
* Generates a PDF report file. The PDF file consists of results summary and contour plots.
* Generates .vtk post-process file which can be opened by ParaView, a open-source data analysis and visualization application.

## Future improvement
* At present there is no preprocessor for the FEM analysis. Program is getting input data from a text file. Need to work on preprocessor software integration to the python program or to build its own.
