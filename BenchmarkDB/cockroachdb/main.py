"""
DB Benchmarking Application
===========================

This file handles all interactions with CockroachDB during the benchmarking
process.

"""
from __future__ import absolute_import

import os

import psycopg2
from .local import *

#from benchmark_template import BenchmarkDatabase
from six.moves import range
import random


class Benchmark():

    def __init__(self, collection, setup=False, trials=0, testcase=1):

        self.trials = trials
        self.split_points = {}
        self.test_number = testcase
        self.connections = {}
        self.cursors = {}

        print("Running test case: " + str(testcase))

        self.insert_statement_oringal = """
INSERT INTO test (
  gIndex, column1, column2, column3, column4, column5, column6, column7, column8, column9,
  column10, column11, column12, column13, column14, column15, column16, column17, column18,
  column19, column20, column21, column22, column23, column24, column25, column26, column27,
  column28, column29, column30, column31, column32, column33, column34, column35, column36,
  column37, column38, column39, column40
) VALUES (
  {Index},
  {column1!r},
  {column2!r},
  {column3!r},
  {column4!r},
  {column5!r},
  {column6!r},
  {column7!r},
  {column8!r},
  {column9!r},
  {column10!r},
  {column11!r},
  {column12!r},
  {column13!r},
  {column14!r},
  {column15!r},
  {column16!r},
  {column17!r},
  {column18!r},
  {column19!r},
  {column20!r},
  {column21},
  {column22},
  {column23},
  {column24},
  {column25},
  {column26},
  {column27},
  {column28},
  {column29},
  {column30},
  {column31},
  {column32},
  {column33},
  {Index},
  {Index},
  {Index},
  {Index},
  {Index},
  {Index},
  {Index}
);
         """

        self.insert_statement = """
INSERT INTO test (
  gIndex, column1, column2, column3, column4, column5, column6, column7, column8, column9,
  column10, column11, column12, column13, column14, column15, column16, column17, column18,
  column19, column20, column21, column22, column23, column24, column25, column26, column27,
  column28, column29, column30, column31, column32, column33, column34, column35, column36,
  column37, column38, column39, column40
) VALUES (
  {Index},
  {Info!r},
  {Info!r},
  {Info!r},
  {Info!r},
  {Info!r},
  {Info!r},
  {Info!r},
  {Info!r},
  {Info!r},
  {Info!r},
  {Info!r},
  {Info!r},
  {Info!r},
  {Info!r},
  {Info!r},
  {Info!r},
  {Info!r},
  {Info!r},
  {Info!r},
  {Info!r},
  {Number},
  {Number},
  {Number},
  {Number},
  {Number},
  {Number},
  {Number},
  {Number},
  {Number},
  {Number},
  {Number},
  {Number},
  {Number},
  {Index},
  {Index},
  {Index},
  {Index},
  {Index},
  {Index},
  {Index}
);
         """


        self.delete_statement = 'DROP TABLE IF EXISTS {table} CASCADE'

        if self.test_number in (1,2):
            self.create_statement = """
CREATE TABLE IF NOT EXISTS test (
  gindex   INT8 PRIMARY KEY,
  column1  STRING,
  column2  STRING,
  column3  STRING,
  column4  STRING,
  column5  STRING,
  column6  STRING,
  column7  STRING,
  column8  STRING,
  column9  STRING,
  column10 STRING,
  column11 STRING,
  column12 STRING,
  column13 STRING,
  column14 STRING,
  column15 STRING,
  column16 STRING,
  column17 STRING,
  column18 STRING,
  column19 STRING,
  column20 STRING,
  column21 INT8,
  column22 INT8,
  column23 INT8,
  column24 INT8,
  column25 INT8,
  column26 INT8,
  column27 INT8,
  column28 INT8,
  column29 INT8,
  column30 INT8,
  column31 INT8,
  column32 INT8,
  column33 INT8,
  column34 INT8,
  column35 INT8,
  column36 INT8,
  column37 INT8,
  column38 INT8,
  column39 INT8,
  column40 INT8
);
            """
        elif self.test_number in (3,4,5):
            self.create_statement = """
CREATE TABLE IF NOT EXISTS test (
  gindex   INT8 PRIMARY KEY,
  column1  STRING,
  column2  STRING,
  column3  STRING,
  column4  STRING,
  column5  STRING,
  column6  STRING,
  column7  STRING,
  column8  STRING,
  column9  STRING,
  column10 STRING,
  column11 STRING,
  column12 STRING,
  column13 STRING,
  column14 STRING,
  column15 STRING,
  column16 STRING,
  column17 STRING,
  column18 STRING,
  column19 STRING,
  column20 STRING,
  column21 INT8,
  column22 INT8,
  column23 INT8,
  column24 INT8,
  column25 INT8,
  column26 INT8,
  column27 INT8,
  column28 INT8,
  column29 INT8,
  column30 INT8,
  column31 INT8,
  column32 INT8,
  column33 INT8,
  column34 INT8,
  column35 INT8,
  column36 INT8,
  column37 INT8,
  column38 INT8,
  column39 INT8,
  column40 INT8,
  CONSTRAINT index40 UNIQUE (column40 ASC),
  CONSTRAINT index39 UNIQUE (column39 ASC),
  CONSTRAINT index38 UNIQUE (column38 ASC),
  CONSTRAINT index37 UNIQUE (column37 ASC),
  CONSTRAINT index36 UNIQUE (column36 ASC),
  CONSTRAINT index35 UNIQUE (column35 ASC)
);
            """

        if self.test_number in (1,3):
            self.select_statement = 'SELECT * FROM test WHERE gIndex = {index};'
        elif self.test_number in (2,4):
            self.select_statement = 'SELECT * FROM test WHERE column40 = {index};'
        elif self.test_number in (0,5):
            self.select_statement = 'SELECT * FROM test WHERE column34 = {index};'

        if setup:
            self.setup(collection)

    def setup(self, collection):
        """ This function will set up the connection with the DB.  The options
        used here are all configured in the config file.

        :param collection: The collection that all benchmark writes will happen
                    with

        """
        # #TODO - fix how the collection is used here

        import ipdb
        # ipdb.set_trace()

        lock_file = '.sql_{node}.lock'
        dir = 'cockroachdb'
        file_list = os.listdir(dir)
        split_number = self.trials / NUMBER_OF_NODES

        for node in range(1, NUMBER_OF_NODES + 1):
            current_host = COCKROACH_NODES[
                'COCKROACH_{node}'.format(node=node)
            ]
            current_port = COCKROACH_PORTS[
                'COCKROACH_{node}'.format(node=node)
            ]
            current_conn = psycopg2.connect(
                host=current_host,
                port=current_port,
                user=COCKROACH_USER,
                password=COCKROACH_PASSWORD,
                dbname="defaultdb"
                #dbname=collection
                #sslmode='require'
            )

            current_conn.autocommit = False
            self.connections[node] = current_conn
            current_cursor = self.connections[node].cursor()
            self.cursors[node] = current_cursor
            self.split_points[node] = split_number * node

        firstNode = 1
        delete = self.delete_statement.format(table=collection)
        self.cursors[firstNode].execute(delete)
        self.commit(firstNode)

        self.cursors[firstNode].execute(self.create_statement)
        self.commit(firstNode)

    def write(self, data):
        """ The function handles all writes with MongoDB.  It takes a single
        parameter (a dict of sample data) and then writes it to the DB.

        :param data: An incoming dict that will be written to the DB

        """

        trial = data['Index']
        #print("GGG: " + str(trial))
        node = self.node_select(trial)

        print("Node: " + str(node) + "- Trial: " + str(trial))
        #print(data)
        insert = self.insert_statement.format(**data)
        #print("INSER IS: " + str(insert))

        self.cursors[node].execute(insert)
        self.commit(node)

    def read(self, index):
        """ This function handles all reads from MongoDB.  It takes a single
        parameter (index) which determines which record to retrieve from the DB.

        :param index: The index of the record to be retrieved from the DB

        :return read_entry: the entry retrieved from the DB

        """
        node = self.node_select(index)
        select = self.select_statement.format(index=index)
        self.cursors[node].execute(select)
        return self.cursors[node].fetchone()

    def node_select(self, trial):
        """

        :param trial:
        :return:
        """

        node = 1
        for n in range(1, NUMBER_OF_NODES + 1):
            split = self.split_points.get(n)
            if split and trial <= split:
                return n
        return node

    def commit(self, node):
        """ Commits the current transaction.  This function is ONLY USED FOR
        SQL-TYPE DATABASES.

        :return:
        """

        #self.cursors[node].execute('commit;')
        self.connections[node].commit()
