#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3 
import sys
import numpy as np



def retrieve_collum_between(filename='test.db',column='in1',lower=0.99,upper=1.0)
    con = None
    # the real stuff
    try:
        #connection
        con=sqlite3.connect(filename)
        #cursor
        cur=con.cursor()
        #fetch the rows
        cur.execute('SELECT in1 FROM Points WHERE in1 > {} AND in1<={} '.format(low_edge,high_edge))
        rows=cur.fetchall()
    # Finalise ...
    except sqlite3.Error as e:
        if con:
            con.rollback()
        print('ERROR: {}'.format(e.args[0]))
        sys.exit()
    finally:
        if con:
            con.close()
    return rows
