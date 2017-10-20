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

    asynsets = {}
    for pos in ["noun", "adj", "verb", "adv"]:
        asynsets[pos] = {}
        for elem in root.findall(".//%s-syn-list//%s-syn" % (pos, pos)):
            # n#05588321 -> (n, 05588321)
            (p, offset) = elem.get("id").split("#")
            if not offset: continue

            asynsets[pos][offset] = { "offset16": offset, "pos": pos };
            if elem.get("categ"):
                asynsets[pos][offset]["categ"] = elem.get("categ")
            if elem.get("noun-id"):
                # n#05588321 -> 05588321
                noun_offset = elem.get("noun-id").replace("n#", "", 1)
                asynsets[pos][offset]["noun-offset"] = noun_offset
                asynsets[pos][offset]["categ"] = asynsets["noun"][noun_offset]["categ"]
            if elem.get("caus-stat"):
                asynsets[pos][offset]["caus-stat"] = elem.get("caus-stat")

    return hierarchies


if __name__ == '__main__':
    # connect to sqlite database
    dbname = 'wn_affect.db'
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    # activate sql with execute method
    # create table
    create_table = '''create table hierarchies (HTPE, HYPO)'''
    c.execute(create_table)

    #wn_affectを{word:categ}の辞書化し，それをpickleファイル化
    hierarchies = load_hierarchies("/Users/arai9814/WordNet/wn-domains-3.2/wn-affect-1.1/a-hierarchies.xml")

    sql = '''insert into hierarchies (HYPE, HYPO) values (?,?)'''
    c.executemany(sql, hierarchies)

    conn.commit()
    # disconnect to the sqlite database
    conn.close()
