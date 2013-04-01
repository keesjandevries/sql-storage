#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pylab
def plotBars(intervals,width,Npoints):
    ind = pylab.array(intervals)    # the x locations for the groups

    pylab.subplot(121)
    p1 = pylab.bar(ind, Npoints, width, color='r')
    #pylab.bar(ind, Npoints, width=0.8, bottom=0)

    pylab.ylabel(r'# of points in "in1"')
    pylab.xlabel(r'Interval in in1')

    pylab.subplot(122)

    p1 = pylab.hist(Npoints)
    pylab.show()



