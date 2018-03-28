from pylab import *
from scipy.sparse import lil_matrix
from b_mat_plate_mzc import *

def stress_plate_mzc(coordinates,elements,D_mat,gauss_x,gauss_y,u):
    """
    Stress Evaluates the stresses at the Gauss points and smooth the values
         to the nodes

    Parameters:
    Input,
       coordinates : Coordinate matrix nnode x ndime (2)
          elements : Element connectivity
           D_mat   : Constitutive matrix
           gauss_x : Local X coordinates of the Gauss points
           gauss_y : Local Y coordinates of the Gauss points
           u       : Nodal displacements

    Output, Strnod the nodal stress matrix (nnode,nstrs)
    """
    # Find basic dimensions
    nelem  = shape(elements)[0]          # Number of elements
    nnode  = shape(elements)[1]          # Number of nodes por element
    npnod  = shape(coordinates)[0]       # Number of nodes
    Strnod = lil_matrix((npnod,nnode))        # Create array for stresses
    dofpn  = 3                              # Number of DOF per node
    dofpe  = dofpn*nnode                    # Number of DOF per element

    # Shape function matrix for stress extrapolation
    aa = 1 + sqrt(3)
    bb = 1 - sqrt(3)
    mstres = array([[aa*aa , aa*bb , bb*bb , aa*bb],
                    [bb*aa , aa*aa , aa*bb , bb*bb],
                    [bb*bb , aa*bb , aa*aa , bb*aa],
                    [aa*bb , bb*bb , bb*aa , aa*aa]])/4

    # Element cycle
    for ielem in range(nelem):
        if (ielem+1)%1000==0:
            print("Going through element:", ielem+1)
        lnods = elements[ielem,0:nnode]
        lnods = [int(i)-1 for i in lnods]   # python index = element_number - 1
        coor_x = coordinates[lnods, 0]      # Elem.X coordinates
        coor_y = coordinates[lnods, 1]      # Elem.Y coordinatesS

        a = (coor_x[1]-coor_x[0])/2
        b = (coor_y[3]-coor_y[0])/2

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

        # Find the equation number list for the i - th element
        eqnum = np.zeros(dofpe, int)
        for i in range(nnode):
            ii = i * dofpn
            for j in range(dofpn):
                eqnum[ii + j] = lnods[i] * dofpn + j  # Build the eq.number list

        # Recover the nodal displacements for the i-th element
        u_elem = u[eqnum]

        Strx = zeros((nnode,1))
        Stry = zeros((nnode,1))
        Strxy = zeros((nnode,1))
        for igaus in range(nnode):
            x = gauss_x[igaus]
            y = gauss_y[igaus]

            bmat = b_mat_plate_mzc(a, b, x, y)
            #print(np.shape(D_mat))
            #print(np.shape(bmat))
            #print(np.shape(np.transpose(u_elem)))
            Str1 = D_mat @ bmat @ u_elem

            Strx[igaus,0]  = Str1[0]
            Stry[igaus,0]  = Str1[1]
            Strxy[igaus,0] = Str1[2]

        Str1 = mstres @ Strx
        Strnod[lnods,0] = Strnod[lnods,0] + Str1
        Str1 = mstres @ Stry
        Strnod[lnods,1] = Strnod[lnods,1] + Str1
        Str1 = mstres @ Strxy
        Strnod[lnods,2] = Strnod[lnods,2] + Str1
        Strnod[lnods,3] = Strnod[lnods,3] + np.ones((nnode,1))

    for i in range(npnod):
        Strnod[i,[0,1,2]] = Strnod[i,[0,1,2]]/Strnod[i,3]

    return Strnod