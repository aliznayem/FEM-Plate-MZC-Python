# Extracts input data from file
from pylab import *

def get_data(filename):
    """

    :param file_name: Data file name
    :return: Variable dictionary
    """

    f = open(filename, 'r')

    datadic = {}     # return data dictionary
    vin = False      # value extraction mode
    dtype = ''       # float or ndarray
    vname = ''       # variable name
    varray = []      # list array

    for line in f:
        ec = '\n,;[]'                                             # remove extra characters
        for c in ec:
            line = line.replace(c, ' ')
        line = line.strip()
        if line == '':                                            # ignore blank lines
            continue
        elif line[0]=='#':                                        # ignore comments
            continue

        if not vin:
            line = line.split()

            if len(line)>=2:
                if line[1]=='float':
                    vin = True
                    dtype = 'float'
                    vname = line[0]
                elif line[1]=='ndarray':
                    vin = True
                    dtype = 'ndarray'
                    vname = line[0]
        else:
            if dtype=='float':
                datadic[vname] = float(line)
                vin = False
            elif dtype=='ndarray':
                if line=='end':
                    datadic[vname] = array(varray)
                    varray = []
                    vin = False
                else:
                    varray.append([float(val) for val in line.split()])

    return datadic
