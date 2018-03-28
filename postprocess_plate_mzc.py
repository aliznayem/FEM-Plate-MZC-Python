from pyevtk.hl import gridToVTK
from pylab import *
from report_generation_plate_mzc import *
from scipy.interpolate import griddata as gd


def postprocess_plate_mzc(young, poiss, thick, denss, coordinates, elements, u, reaction, Strnod, file_name):
    """
    :param young : Young's modulus
    :param poiss : Poisson's ration
    :param thick : Plate thickness
    :param denss : Plate material density
    :param coordinates:  Coordinate matrix nnode x ndime (2)
    :param u: Nodal displacements
    :param reaction: Nodal reactions
    :param Strnod: Nodal stresses
    :param file_name: Save file name
    :return: Void
    """

    file_name = "analysis_output/"+file_name

    # Number of nodes
    npnod = shape(coordinates)[0]
    nelem = shape(elements)[0]

    # Coordinates
    x = coordinates[:, 0].flatten()
    y = coordinates[:, 1].flatten()

    # Find plate length, width
    xmin = min(x)
    xmax = max(x)
    ymin = min(y)
    ymax = max(y)
    length = xmax - xmin
    width = ymax - ymin

    # Find grid coordinates
    dim = 500
    xc = linspace(xmin, xmax, num=dim)
    yc = linspace(ymin, ymax, num=dim)

    # Displacements
    uz = []  # Z-Displacement
    xtheta = []  # X-Rotation
    ytheta = []  # Y-Rotation
    for i in range(npnod):
        uz.append(u[i * 3, 0])
        xtheta.append(u[i * 3 + 1, 0])
        ytheta.append(u[i * 3 + 2, 0])

    # Stresses
    mx = Strnod[:, 0].toarray().flatten()
    my = Strnod[:, 1].toarray().flatten()
    mxy = Strnod[:, 2].toarray().flatten()

    # Reaction forces
    zf = []  # Z-Force
    xm = []  # X-Moment
    ym = []  # Y-Moment
    for i in range(npnod):
        zf.append(reaction[i * 3, 0])
        xm.append(reaction[i * 3 + 1, 0])
        ym.append(reaction[i * 3 + 2, 0])

    # Griddata genetarion
    inter = 'linear'    # Interpolation method
    uzc = gd((x, y), uz, (xc[None,:], yc[:,None]), method=inter)
    xthetac = gd((x, y), xtheta, (xc[None, :], yc[:, None]), method=inter)
    ythetac = gd((x, y), ytheta, (xc[None, :], yc[:, None]), method=inter)
    mxc = gd((x, y), mx, (xc[None, :], yc[:, None]), method=inter)
    myc = gd((x, y), my, (xc[None, :], yc[:, None]), method=inter)
    mxyc = gd((x, y), mxy, (xc[None, :], yc[:, None]), method=inter)
    zfc = gd((x, y), zf, (xc[None, :], yc[:, None]), method=inter)
    xmc = gd((x, y), xm, (xc[None, :], yc[:, None]), method=inter)
    ymc = gd((x, y), ym, (xc[None, :], yc[:, None]), method=inter)

    # pylab griddata : don't have cubic interpolation method
    #uzc = griddata(x, y, uz, xc, yc, interp='linear')
    #xthetac = griddata(x, y, xtheta, xc, yc, interp='linear')
    #ythetac = griddata(x, y, ytheta, xc, yc, interp='linear')
    #mxc = griddata(x, y, mx, xc, yc, interp='linear')
    #myc = griddata(x, y, my, xc, yc, interp='linear')
    #mxyc = griddata(x, y, mxy, xc, yc, interp='linear')
    #zfc = griddata(x, y, zf, xc, yc, interp='linear')
    #xmc = griddata(x, y, xm, xc, yc, interp='linear')
    #ymc = griddata(x, y, ym, xc, yc, interp='linear')

    # export .vtk
    gridToVTK(file_name, xc, yc, np.array([0]), pointData={"Z-Displacement": uzc.reshape((dim, dim, 1)),
                                                           "X-Rotation": xthetac.reshape((dim, dim, 1)),
                                                           "Y-Rotation": ythetac.reshape((dim, dim, 1)),
                                                           "Mx-Stress": mxc.reshape((dim, dim, 1)),
                                                           "My-Stress": myc.reshape((dim, dim, 1)),
                                                           "Mxy-Stress": mxyc.reshape((dim, dim, 1)),
                                                           "Z-ReactionForce":zfc.reshape((dim, dim, 1)),
                                                           "X-ReactionMoment":xmc.reshape((dim, dim, 1)),
                                                           "Y-ReactionMoment":ymc.reshape((dim, dim, 1))})

    print(".VTK file write success")

    # Report generation
    figure(num=None, dpi=150, facecolor='w', edgecolor='k')
    contourf(xc, yc, uzc)
    title("Vertical Displacement")
    colorbar()
    savefig("figures/zdisp.png")
    figure(num=None, dpi=150, facecolor='w', edgecolor='k')
    contourf(xc, yc, xthetac)
    title("X-Rotation")
    colorbar()
    savefig("figures/xrot.png")
    figure(num=None, dpi=150, facecolor='w', edgecolor='k')
    contourf(xc, yc, ythetac)
    title("Y-Rotation")
    colorbar()
    savefig("figures/yrot.png")
    figure(num=None, dpi=150, facecolor='w', edgecolor='k')
    contourf(xc, yc, mxc)
    title("Mx-Stress")
    colorbar()
    savefig("figures/mx.png")
    figure(num=None, dpi=150, facecolor='w', edgecolor='k')
    contourf(xc, yc, myc)
    title("My-Stress")
    colorbar()
    savefig("figures/my.png")
    figure(num=None, dpi=150, facecolor='w', edgecolor='k')
    contourf(xc, yc, mxyc)
    title("Mxy-Stress")
    colorbar()
    savefig("figures/mxy.png")
    figure(num=None, dpi=150, facecolor='w', edgecolor='k')
    contourf(xc, yc, zfc)
    title("Vetical Reaction Force")
    colorbar()
    savefig("figures/zf.png")
    figure(num=None, dpi=150, facecolor='w', edgecolor='k')
    contourf(xc, yc, xmc)
    title("X-Reaction Moment")
    colorbar()
    savefig("figures/xm.png")
    figure(num=None, dpi=150, facecolor='w', edgecolor='k')
    contourf(xc, yc, ymc)
    title("Y-Reaction Moment")
    colorbar()
    savefig("figures/ym.png")

    # Report generation
    print("Generating report")
    report_generation_plate_mzc(length, width, thick, young, poiss, denss, npnod, nelem, uz, xtheta, ytheta, zf, xm, ym,
                                mx, my, mxy, file_name)
