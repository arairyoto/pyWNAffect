# coding: utf-8
import os
import sys

import sqlite3

DBNAME = 'wn_affect.db'
TABLENAMEs = {}
TABLENAMEs['as'] = 'asynsets'
TABLENAMEs['hi'] = 'hierarchies'

class WNAffect:
    def __init__(self):
        # connect to db
        self.dbname = DBNAME
        conn = sqlite3.connect(self.dbname)
        self.c = conn.cursor()

    def all_categories(self):
        sql = 'select NAME from '+TABLENAMEs['hi']
        names = set([row[0] for row in self.c.execute(sql)])
        sql = 'select ISA from '+TABLENAMEs['hi']
        isas = set([row[0] for row in self.c.execute(sql)])
        all_categories = names | isas

        return list(all_categories)

    def all_asynsets(self):
        sql = 'select SYNSET from '+TABLENAMEs['as']

        return list(set([row[0] for row in self.c.execute(sql)]))


    def hype_categs(self, categ, n=1):
        sql = 'select ISA from '+TABLENAMEs['hi']+' where NAME='+'"'+categ+'"'
        return list(set([row[0] for row in self.c.execute(sql)]))

    def hypo_categs(self, categ, n=1):
        sql = 'select NAME from '+TABLENAMEs['hi']+' where ISA='+'"'+categ+'"'
        return list(set([row[0] for row in self.c.execute(sql)]))

    def asynsets(self, categ):
        sql = 'select SYNSET from '+TABLENAMEs['as']+' where CATEGORY='+'"'+categ+'"'
        return list(set([row[0] for row in self.c.execute(sql)]))

    def categs(self, synset):
        sql = 'select CATEGORY from '+TABLENAMEs['as']+' where SYNSET='+'"'+synset+'"'
        return list(set([row[0] for row in self.c.execute(sql)]))

if __name__=='__main__':
    wna = WNAffect()
    print(wna.all_asynsets())
