#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3 , sys, random, os, argparse
import numpy as np

con = None
def parse_args():
    parser = argparse.ArgumentParser(description='Creating an sql data base')
    parser.add_argument('--n-inputs', dest='n_inputs', action='store',type=int, 
            default=7,  help='Number of input parameters')
    parser.add_argument('--n-outputs', dest='n_outputs', action='store',type=int, 
            default=190,  help='Number of output parameters')
    parser.add_argument('--n-points', '-n',dest='n_points', action='store',type=int, 
            default=10000,  help='Number of points')
    parser.add_argument('--collection-id', dest='collection_id', action='store',type=int, 
            default=1,  help='collection-id')
    parser.add_argument('--output-file','-o', dest='output_file', action='store', 
            default='test.db',  help='Name of output date base file')
    parser.add_argument('--update', dest='update', action='store_true', 
            default=False,  help='Recreate data base, i.e. delete existing file if exists')
    return parser.parse_args()

args= parse_args()

if not args.update:
    try:
        os.remove(args.output_file)
    except FileNotFoundError:
        pass

# the real stuff
try:
    #set numbers
    Ninput=args.n_inputs
    Noutput=args.n_outputs
    Npoints=args.n_points
    collection_id=args.collection_id
    #connection
    con=sqlite3.connect(args.output_file)
    #cursor
    cur=con.cursor()
    input_string=','.join([' in{} REAL '.format(i) for i in range(1,Ninput+1)])
    output_string=','.join([' out{} REAL '.format(i) for i in range(1,Noutput+1)])
    cur.execute('CREATE TABLE IF NOT EXISTS Points(Id INT, CollectionId INT, {},{}) '.format(input_string,output_string))
    many_in_output=tuple([ tuple(np.append([j,collection_id], np.random.rand(Ninput+Noutput))) for j in range(Npoints)])
    questionmarks= ','.join(['?' for i in range(Ninput+Noutput+2)])  # ?, ... , ?
#    cur.execute('INSERT INTO Points VALUES({}) '.format(questionmarks),one_in_output)
    cur.executemany('INSERT INTO Points VALUES({}) '.format(questionmarks),many_in_output)
    con.commit()

# Finalise ...
except sqlite3.Error as e:
    if con:
        con.rollback()
    print('ERROR: {}'.format(e.args[0]))
    sys.exit()
finally:
    if con:
        con.close()
