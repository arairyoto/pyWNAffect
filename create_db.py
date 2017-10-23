# coding: utf-8
import os
import sys
os.environ["NLTK_DATA"] = os.getcwd()

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import *

import nltk
from nltk.corpus import WordNetCorpusReader
from sqlalchemy import *
from xml.dom import minidom
from nltk.corpus import wordnet as wn

import difflib

import sqlite3

#wordnet-1.6 の読み込み
cwd = os.getcwd()
nltk.data.path.append(cwd)
wordnet16_dir="../WordNet/Wordnet-1.6/"
wn16_path = "{0}/dict".format(wordnet16_dir)
WN16 = WordNetCorpusReader(os.path.abspath("{0}/{1}".format(cwd, wn16_path)), nltk.data.find(wn16_path))


# load Wordnet-Affect synsets
# corpus: a-synset.xml
# return: {
#   'noun': {
#     '05586574': { 'categ': 'electricity', 'pos': 'noun', 'offset16': '05586574' }
#   }, ...
# }
def load_asynsets(corpus):
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

    return asynsets

# Merge WordNet-Affect synsets with WordNet-3.0 synsets
def merge_asynset_with_wn(asynsets):
    pos_map = { "noun": "n", "adj": "a", "verb": "v", "adv": "r" }
    # start from "noun" because other pos use noun-synset
    for pos in ["noun", "adj", "verb", "adv"]:
        for offset in asynsets[pos].keys():
            # Get WordNet-1.6 synset
            synset_16 = WN16._synset_from_pos_and_offset(pos_map[pos], int(offset))
            if not synset_16: continue

            synset_30 = _wn30_synsets_from_wn16_synset(synset_16)
            if not synset_30:
                asynsets[pos][offset]["missing"] = 1
            else:
                asynsets[pos][offset]["missing"] = 0
                (word, p, index) = synset_30.name().split(".")
                asynsets[pos][offset]["word"] = word
                asynsets[pos][offset]["synset"] = synset_30.name()
                # db-synset is used to query the japanese wordnet (sqlite)
                asynsets[pos][offset]["db-synset"] = str("%08d-%s" % (synset_30.offset(), p))
                asynsets[pos][offset]["offset"] = str("%08d" % (synset_30.offset()))
                if "noun-offset" in asynsets[pos][offset]:
                    noffset = asynsets[pos][offset]["noun-offset"]
                    asynsets[pos][offset]["noun-synset"] = asynsets["noun"][noffset]["synset"]

    return asynsets

# Get WordNet-3.0 synset
# Similarity is calculated by wup_similarity
def _wn30_synsets_from_wn16_synset(synset):
    (word, p, index) = synset.name().split(".")
    gloss = synset.definition()
    # ADJ_SAT -> ADJ: DO NOT EXIST ADJ_SAT in wordnet.POS_LIST
    if p == 's':
        p = 'a'
    synsets = wn.synsets(word, p)
    if len(synsets) == 0:
        return

    synset_sims = {}

    #定義文の文字列類似度でソート
    for i in range(len(synsets)):
        synset_sims[i] = difflib.SequenceMatcher(None, gloss, synsets[i].definition()).ratio()

    # Most similar synset index
    index = sorted(synset_sims.items(), key=lambda x:x[1], reverse=True)[0][0]

    return synsets[index]

# def asynsets_to_syn_dictionary(asynsets):
#     dictionary = {}
#     for pos in ["noun", "adj", "verb", "adv"]:
#         for offset in asynsets[pos].keys():
#             if asynsets[pos][offset]["missing"]==1:
#                 continue
#             else:
#                 print(asynsets[pos][offset]["synset"])
#                 dictionary[asynsets[pos][offset]["synset"]]=asynsets[pos][offset]["categ"]
#
#
#                 #似ているsynsetに拡張
#                 synsets = wn.synset(asynsets[pos][offset]["synset"]).similar_tos()
#                 for synset in synsets:
#                     dictionary[synset.name()] = asynsets[pos][offset]["categ"]
#
#     return dictionary

def asynsets_to_syn_dictionary(asynsets):
    dictionary = []
    for pos in ["noun", "adj", "verb", "adv"]:
        for offset in asynsets[pos].keys():
            if asynsets[pos][offset]["missing"]==1:
                continue
            else:
                dictionary.append((asynsets[pos][offset]["synset"],asynsets[pos][offset]["categ"]))

                #似ているsynsetに拡張
                # synsets = wn.synset(asynsets[pos][offset]["synset"]).similar_tos()
                # for synset in synsets:
                #     dictionary[synset.name()] = asynsets[pos][offset]["categ"]

    return dictionary

if __name__ == '__main__':
    # connect to sqlite database
    dbname = 'wn_affect.db'
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    # activate sql with execute method
    # create table
    create_table = '''create table asynsets (SYNSET, CATEGORY)'''
    # c.execute(create_table)

    #wn_affectを{word:categ}の辞書化し，それをpickleファイル化
    asynsets_16 = load_asynsets("../WordNet/wn-domains-3.2/wn-affect-1.1/a-synsets.xml")
    asynsets = merge_asynset_with_wn(asynsets_16)
    dic = asynsets_to_syn_dictionary(asynsets)

    sql = '''insert into asynsets (SYNSET, CATEGORY) values (?,?)'''
    c.executemany(sql, dic)

    conn.commit()
    # disconnect to the sqlite database
    conn.close()
