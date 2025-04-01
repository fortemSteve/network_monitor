#!/usr/bin/python3 


import csv as _csv
import numpy as _np

def csvread(fname):
    csvfile = open(fname)
    r = _csv.reader(csvfile)
    rows = list(r)
    colnames = rows[0]
    rows = rows[1:]
    y = {}
    for icol, key in enumerate(colnames):
        try:
            y[key] = _np.array([float(x[icol]) for x in rows])
        except:
            y[key] = [x[icol] for x in rows]
    return y
