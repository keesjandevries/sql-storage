#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3 , sys, random, os, argparse

Ninput=5
Noutput=50
Npoints=10000

con = None
def parse_args():
    parser = argparse.ArgumentParser(description='Creating an sql data base')
    parser.add_argument('--output-file','-o', dest='output_file', action='store', 
            default='test.db',  help='Name of output date base file')
    parser.add_argument('--recreate', dest='recreate', action='store_true', 
            default=False,  help='Recreate data base, i.e. delete existing file if exists')
    return parser.parse_args()

args= parse_args()

if args.recreate:
    os.remove()

# the real stuff
try:
    #connection
    con=sqlite3.connect(args.output_file)
    #cursor
    cur=con.cursor()
    input_string=','.join([' in{} REAL '.format(i) for i in range(1,Ninput+1)])
    output_string=','.join([' out{} REAL '.format(i) for i in range(1,Noutput+1)])
    cur.execute('CREATE TABLE IF NOT EXISTS Points(Id INT, CollectionId INT, {},{}) '.format(input_string,output_string))
    many_in_output=tuple([ tuple([1,2]+[ random.random() for i in range(Ninput+Noutput)]) for j in range(Npoints)])
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
