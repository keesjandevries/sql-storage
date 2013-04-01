#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3 , argparse, sys
import numpy as np


def parse_args():
    parser = argparse.ArgumentParser(description='Quering an sql database')
    parser.add_argument('--input-file','-i', dest='input_file', action='store', 
            default='test.db',  help='Name of output date base file')
    return parser.parse_args()

args=parse_args()

filename=args.input_file

con = None
# the real stuff
try:
    #connection
    con=sqlite3.connect(filename)
    #cursor
    cur=con.cursor()
    #fetch the rows
#    cur.execute('SELECT COUNT(*) FROM Points  ')
    cur.execute('SELECT * FROM points where CollectionId=5 and in1 <0.5 and in1> 0.3 and in2<0.001')
    print(cur.fetchmany(size=5))

# Finalise ...
except sqlite3.Error as e:
    if con:
        con.rollback()
    print('ERROR: {}'.format(e.args[0]))
    sys.exit()
finally:
    if con:
        con.close()
