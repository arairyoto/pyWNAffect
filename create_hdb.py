# coding: utf-8
import os
import sys
os.environ["NLTK_DATA"] = os.getcwd()

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import *

import sqlite3

def load_hierarchies(corpus):
    tree = ET.parse(corpus)
    root = tree.getroot()

    hierarchies = []

    for elem in root.findall(".//categ"):
        # n#05588321 -> (n, 05588321)
        name = elem.get("name")
        isa = elem.get("isa")
        hierarchies.append((name, isa))

    return hierarchies


if __name__ == '__main__':
    # connect to sqlite database
    dbname = 'wn_affect.db'
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    # activate sql with execute method
    # create table
    try:
        create_table = '''create table hierarchies (NAME, ISA)'''
        c.execute(create_table)
    except:
        print('table already existed')

    hierarchies = load_hierarchies("../WordNet/wn-domains-3.2/wn-affect-1.1/a-hierarchy.xml")

    sql = '''insert into hierarchies (NAME, ISA) values (?,?)'''
    c.executemany(sql, hierarchies)

    sql = '''select NAME from hierarchies where ISA = "root"'''
    res = c.execute(sql)
    print(list(res))


    conn.commit()
    # disconnect to the sqlite database
    conn.close()
