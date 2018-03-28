from pylab import *

def to_gid_plate_mzc(coordinates,elements,u,reaction,Strnod,file_name):
    """
    ToGiD Writes the postprocess files

    Parameters:

        Input, coordinates : Coordinate matrix nnode x ndime (2)
               elements    : Element connectivity
               u           : Nodal displacements
               reaction    : Nodal reactions
               Strnod      : Nodal stresses
               filename    : Output file name

    Output, none
    """
    # Find basic dimensions
    nelem  = shape(elements)[0]          # Number of elements
    nnode  = shape(elements)[1]          # Number of nodes por element
    npnod  = shape(coordinates)[0]       # Number of nodes

    eletyp = 'Quadrilateral'

    msh_file = "analysis_output/"+file_name+'.flavia.msh'
    res_file = "analysis_output/"+file_name+'.flavia.res'

    # Mesh File
    f = open(msh_file, 'w')
    f.write('### \n')
    f.write('# MAT-fem Plate MZC v1.4 \n')
    f.write('# \n')
    f.write('MESH dimension {:d}   Elemtype {:s}   Nnode {:d} \n \n'.format(2, eletyp, nnode))
    f.write('coordinates \n')

    for i in range(npnod):
        f.write('{:6d} {:13.5f} {:13.5f} \n'.format(i+1, coordinates[i, 0], coordinates[i, 1]))

    f.write('end coordinates \n \n')
    f.write('elements \n')

    for i in range(nelem):
        f.write('{:6d} {:6.0f} {:6.0f} {:6.0f} {:6.0f} 1 \n'.format(i+1, elements[i,0], elements[i,1], elements[i,2], elements[i,3]))

    f.write('end elements \n \n')

    f.close()

    # Results File
    f = open(res_file, 'w')
    f.write('Gid Post Results File 1.0 \n')
    f.write('### \n')
    f.write('# MAT-fem Plate MZC v1.4 \n')
    f.write('# \n')

    # Displacement
    f.write('Result "Displacement" "Load Analysis"  1  Vector OnNodes \n')
    f.write('ComponentNames "X-Displ", "Y-Displ", "Z-Displ" \n')
    f.write('Values \n')
    for i in range(npnod):
        f.write('{:6d} 0.0 0.0 {:13.7g} \n'.format(i+1, u[i*3,0]))

    f.write('End Values \n')
    f.write('# \n')

    # Rotation
    f.write('Result "Rotation" "Load Analysis"  1  Vector OnNodes \n')
    f.write('ComponentNames "X-Rot", "Y-Rot", "Z-Rot" \n')
    f.write('Values \n')

    for i in range(npnod):
        f.write('{:6d} {:13.7g} {:13.7g} 0.0 \n'.format(i+1,u[i*3+1,0],u[i*3+2,0]))

    f.write('End Values \n')
    f.write('# \n')

    # Reaction
    f.write('Result "Reaction" "Load Analysis"  1  Vector OnNodes \n')
    f.write('ComponentNames "Z-Force", "X-Moment", "Y-Moment" \n')
    f.write('Values \n')

    for i in range(npnod):
        f.write('{:6d} {:13.7g} {:13.7g} {:13.7g} \n'.format(i+1,reaction[i*3,0],reaction[i*3+1,0],reaction[i*3+2,0]))

    f.write('End Values \n')
    f.write('# \n')

    # Moment
    f.write('Result "Moment" "Load Analysis"  1  Vector OnNodes \n')
    f.write('ComponentNames "Mx", "My", "Mxy" \n')
    f.write('Values \n')

    for i in range(npnod):
        f.write('{:6d} {:13.7g} {:13.7g} {:13.7g} \n'.format(i+1,Strnod[i,0],Strnod[i,1],Strnod[i,2]))

    f.write('End Values \n')

    f.close()

    print("GID postprocess file write success")