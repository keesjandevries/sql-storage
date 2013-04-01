#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3 
import sys
import numpy as np

con = None

lower=0.99
upper=0.992
stepsize=0.001

# the real stuff
try:
    #connection
    con=sqlite3.connect('test.db')
    #cursor
    cur=con.cursor()
    vals=[]
    for low_edge in np.arange(0.9,1.0,0.01): 
        high_edge=low_edge+stepsize
        cur.execute('SELECT in1, in2  FROM Points WHERE in1 > {} AND in1<={} '.format(low_edge,high_edge))
        rows=cur.fetchall()
        print(rows)
        print('==============================')

    print(vals)

# Finalise ...
except sqlite3.Error as e:
    if con:
        con.rollback()
    print('ERROR: {}'.format(e.args[0]))
    sys.exit()
finally:
    if con:
        con.close()
