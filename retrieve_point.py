#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3 , sys, random, os, argparse
import numpy as np


def parse_args():
    parser = argparse.ArgumentParser(description='Fill points randomly for the moment')
    parser.add_argument('--input-file','-i', dest='input_file', action='store', 
            default='test.db',  help='Name of input date base file')
    return parser.parse_args()


# FIXME: this function is now duplicated from fill_points. Will and up in something lite mc_sql_tools.py
def get_columns_and_observable_ids(con,cur):
    cur.execute('select point_column, obs_id_field1 , obs_id_field2 from obs_id_lookup')
    obs_id_lookup=cur.fetchall()
    columns=[]
    oids={}
    for col, id1, id2 in obs_id_lookup:
        columns.append(col)
        oids[col]=(id1,id2)
    return columns, oids

def query_points_table(con,cur,query_condition):
    #Here starts the niceness!
    obs_columns, mc_obs_ids = get_columns_and_observable_ids(con,cur)
#    all_columns=','.join(obs_columns)
    
    cur.execute('select * from points where {}'.format( query_condition))
    rows=cur.fetchall()
    points=[]
    for row in rows:
        point={mc_obs_ids[col]: val for col, val in zip(obs_columns, row[2:]) } #FIXME: we may want to replace this with row_factory
        points.append(point)
    return points


if __name__=="__main__" :
    con = None
    args= parse_args()
    # the real stuff
    try:
        #connection and cursor
        con=sqlite3.connect(args.input_file)
        cur=con.cursor()
        #retrieve a point
        m0=query_points_table(con,cur,'obs0 > 10')[0][('MINPAR','M0')]
    
    # Finalise ...
    except sqlite3.Error as e:
        if con:
            con.rollback()
        print('ERROR: {}'.format(e.args[0]))
        sys.exit()
    finally:
        if con:
            con.close()

