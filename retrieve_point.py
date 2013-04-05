#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3 , sys, random, os, argparse
import numpy as np


def parse_args():
    parser = argparse.ArgumentParser(description='Fill points randomly for the moment')
    parser.add_argument('--input-file','-i', dest='input_file', action='store', 
            default='test.db',  help='Name of input date base file')
    return parser.parse_args()


def get_columns_and_observable_ids(con,cur):
    cur.execute('select point_column, obs_id_field1 , obs_id_field2 from obs_id_lookup')
    obs_id_lookup=cur.fetchall()
    columns=[]
    oids={}
    for col, id1, id2 in obs_id_lookup:
        columns.append(col)
        oids[col]=(id1,id2)
    return columns, oids

def mc_points_to_rows(con,cur,points,collection_id=1):
    #Here starts the niceness!
    obs_columns, mc_obs_ids = get_columns_and_observable_ids(con,cur)
    rows=[]
    for point in points:
        #The following checks whether
        #   the point contains all the information in the lookup table, 
        #   the lookup table is complete
        try:
            observables=[point[mc_obs_ids[col]] for col in obs_columns]
        except KeyError:
            #This crashes if the KeyError was caused in calling mc_obs_ids[col], which should not happend
            print("WARNING: presumably point does not contain key {}".format(mc_obs_ids[col]))
        if len(point) > len(obs_columns):
            print("WARNING: DATABASE IS MISSING COLUMNS")
            print("         FIXME: A function is needed to take care of this")

        #Et voila: le point :D :D
        rows.append(tuple([collection_id]+observables))
    return rows

#def make_some_random_rows(con,cur):
#    #count number of columns
#    cur.execute("pragma table_info(points)")
#    n_columns=len(cur.fetchall())
#    rows=[]
#    for i in range(args.n_points):
#        rows.append(tuple(np.append([2], np.random.rand(n_columns-2)))) 
#    return rows


if __name__=="__main__" :
    con = None
    args= parse_args()
    # the real stuff
    try:
        #connection and cursor
        con=sqlite3.connect(args.input_file)
        cur=con.cursor()
        #dump one point
#        rows=make_some_random_rows(con,cur)
        rows=mc_points_to_rows(con,cur,[one_point])
        dump_rows(con,cur,rows)
    
    # Finalise ...
    except sqlite3.Error as e:
        if con:
            con.rollback()
        print('ERROR: {}'.format(e.args[0]))
        sys.exit()
    finally:
        if con:
            con.close()

