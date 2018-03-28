# Python version of Plate_MZC
# Reference Matlab code source: http://www.cimne.com/mat-fem/plates.asp 
# 4 Nodes Quadrilateral Thin Plate Element MZC

import time
from pylab import *
from scipy.io import loadmat
from scipy.sparse import lil_matrix
from get_data import *
from b_mat_plate_mzc import *
from stress_plate_mzc import *
from to_gid_plate_mzc import *
from postprocess_plate_mzc import *
from scipy.sparse.linalg import spsolve


# filename prompt
filename = input("Input filename: ")

# Get data in dictionary format from text file
dat = get_data(filename)

# young = Young Modulus
# poiss = Poission Ratio
# thick = Thickness
# denss = Density
# coordinates = [ x , y ] coordinate ndarray nnode x ndime (2)
# elements    = [ inode , jnode , knode , lnode ] element connectivity
#               matrix. Matrix size: nelem x nnode; nnode = 4
# fixnodes    = [ node number , dof , fixed value ] ndarray with Dirichlet
#               restrictions, were dof=1 for vertical displacement,
#               dof=2 for rotation in x and dof=3 for rotation in y
# pointload   = [ node number , dof , load value ] ndarray with
#               nodal loads, were dof=1 for vertical load,
#               dof=2 for x moment and dof=3 for y moment
# uniload     = [ element number, uniform vertical load ]

# Find values from dictionary
young = dat['young']
poiss = dat['poiss']
thick = dat['thick']
denss = dat['denss']
coordinates = dat['coordinates']
elements = dat['elements']
fixnodes = dat['fixnodes']
pointload = dat['pointload']
uniload = dat['uniload']

# Clock started
t1 = time.time()

# Find basic dimensions
npnod = shape(coordinates)[0]        # Number of nodes
nelem = shape(elements)[0]           # Number of elements
nnode = shape(elements)[1]           # Number of nodes per element
dofpn = 3                               # Number of DOF per node
dofpe = nnode*dofpn                     # Number of DOF per element
nndof = npnod*dofpn                     # Number of total DOF


# Sort rows by first columne
elements = elements[elements[:,0].argsort(),]
uniload = uniload[uniload[:,0].argsort(),]

# Dimension the global matrices
StifMat  = lil_matrix((nndof , nndof))  # Create the global stiffness matrix
force    = lil_matrix((nndof , 1))      # Create the global force vector
force1   = lil_matrix((nndof , 1))      # Create the global force vector
reaction = lil_matrix((nndof , 1))      # Create the global reaction vector
u        = lil_matrix((nndof , 1))      # Nodal variables

# Material properties(Constant over the domain)
aux0 = (young*thick**3)/(12*(1-poiss**2))
D_mat = array([[aux0,          poiss*aux0,     0               ],
               [poiss*aux0,    aux0,           0               ],
               [0,             0,              aux0*(1-poiss)/2]])

# Gauss point coordinates
gauss_x = zeros(4)
gauss_y = zeros(4)

gauss_x[0] = -1/sqrt(3)
gauss_y[0] = -1/sqrt(3)

gauss_x[1] =  1/sqrt(3)
gauss_y[1] = -1/sqrt(3)

gauss_x[2] =  1/sqrt(3)
gauss_y[2] =  1/sqrt(3)

gauss_x[3] = -1/sqrt(3)
gauss_y[3] =  1/sqrt(3)

# Element cycle
for ielem in range(nelem):
    if (ielem+1)%1000==0:
        print("Going through element:", ielem+1)
    lnods = elements[ielem,0:nnode]
    lnods = [int(i)-1 for i in lnods]   # python index = element_number - 1
    coor_x = coordinates[lnods, 0]      # Elem.X coordinates
    coor_y = coordinates[lnods, 1]      # Elem.Y coordinatesS

    a = (coor_x[1]-coor_x[0])/2
    a2 = (coor_x[2]-coor_x[3])/2
    b = (coor_y[3]-coor_y[0])/2
    b2 = (coor_y[2]-coor_y[1])/2

    if ((a != a2) or (b != b2)):
        print('WARNING Only rectangular elements allowed')

    if (a == 0):
        a = (coor_x[2]-coor_x[1])/2
        b = (coor_y[0]-coor_y[1])/2
        lnods[0] = int(elements[ielem, 1]) - 1
        lnods[1] = int(elements[ielem, 2]) - 1
        lnods[2] = int(elements[ielem, 3]) - 1
        lnods[3] = int(elements[ielem, 0]) - 1

    elif (a < 0): # Adjust the nodal connectivities
        a = abs(a)
        b = abs(b)
        lnods[0] = int(elements[ielem, 2]) - 1
        lnods[1] = int(elements[ielem, 3]) - 1
        lnods[2] = int(elements[ielem, 0]) - 1
        lnods[3] = int(elements[ielem, 1]) - 1

    K_elem = zeros((dofpe, dofpe))

    for igaus in range(nnode):
        x = gauss_x[igaus]
        y = gauss_y[igaus]

        bmat_b = b_mat_plate_mzc(a, b, x, y)

        K_elem = K_elem + transpose(bmat_b) @ D_mat @ bmat_b * a * b

    f = 4 * (-denss * thick + uniload[ielem, 1]) * a * b

    ElemFor = f * array([1 / 4, a / 12, b / 12, 1 / 4, -a / 12, b / 12,
               1 / 4, -a / 12, -b / 12, 1 / 4, a / 12, -b / 12])

    # Find the equation number list for the i - th element
    eqnum = zeros(dofpe, int)
    for i in range(nnode):
        ii = i * dofpn
        for j in range(dofpn):
            eqnum[ii + j] = lnods[i] * dofpn + j  # Build the eq.number list

    # Assemble the force vector and the stiffnes matrix
    for i in range(dofpe):
        ipos = eqnum[i]
        force[ipos, 0] = force[ipos, 0] + ElemFor[i]
        for j in range(dofpe):
            jpos = eqnum[j]
            StifMat[ipos, jpos] = StifMat[ipos, jpos] + K_elem[i, j]

# Add point load conditions to the force vector
print("Adding point load conditions")
for i in range(shape(pointload)[0]):
    ieqn = (pointload[i,0]-1)*dofpn + pointload[i,1] - 1   # Find eq. number
    force[ieqn,0] = force[ieqn,0] + pointload[i,2]         # and add the force

# Apply the Dirichlet conditions and adjust the right hand side
print("Applying boundary conditions")
fixnodeslen = shape(fixnodes)[0]
fix_indices = zeros(fixnodeslen, int)
for i in range(fixnodeslen):
    ieqn = (fixnodes[i,0]-1)*dofpn + fixnodes[i,1] - 1   # Find equation number
    u[ieqn] = fixnodes[i,2]                              # and store the solution in u
    fix_indices[i] = ieqn                                # and mark the eq. as a fix value

print("Adjusting right hand side with the known values")
force1 = force - StifMat @ u      # Adjust the rhs with the known values

# Compute the solution by solving StifMat * u = force for the remaining
# unknown values of u
# Find the free node list
print("Finding free node list")
FreeNodes = setdiff1d([i for i in range(nndof)], fix_indices)
# and solve for it
print("Solving for displacements")
u[FreeNodes] = spsolve(StifMat[FreeNodes,:][:,FreeNodes].tocsr(), \
                force1[FreeNodes].tocsr()).reshape((np.shape(FreeNodes)[0],1))

# Compute the reactions on the fixed nodes as R = StifMat * u - F
print("Computing reactions on the fixed nodes")
reaction[fix_indices] = StifMat[fix_indices,:] @ u - force[fix_indices]

# Compute the stresses
print("Computing the stresses")
Strnod = stress_plate_mzc(coordinates,elements,D_mat,gauss_x,gauss_y,u)

# Write to gid postprocess file
print("Writing to GID postprocess file")
to_gid_plate_mzc(coordinates,elements,u,reaction,Strnod,filename)

# Postprocess
print("Postprocessing")
postprocess_plate_mzc(young, poiss, thick, denss, coordinates, elements, u, reaction, Strnod, filename)

print("End")

print("\nTime elapsed: {:.2f} seconds".format(time.time()-t1))
