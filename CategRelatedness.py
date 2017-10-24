# coding: utf-8
import os
import sys

import networkx as nx
import matplotlib.pylab as plt

class WSLObject:
    def __init__(self, name, attribute, lang = None):
        self.name = name
        self.attribute = attribute
        self.lang = lang

class CategRelatedness:
    def __init__(self, folder, langs):
        # loading word vectors
        self.mwv = MultilingualWordVector(folder, langs)
        # loading hierarchical structure of some kind; in this case WordNetAffect
        self.wna = WNAffect()

    def categ_relatedness(self, target, categ):
        result = 0
        # total number of a-synsets and categs dirive from the categ inputed
        N = len(self.wna.asynsets(categ))+len(self.wna.hypo(categ))

        for s in self.wna.asynsets(categ):
            o = WSLObject(s, 'synset')
            result += (1+self.mwv.relatedness(target, o))/(2*N)

        for c in self.wna.hypo(categ):
            result += self.categ_relatedness(target, c)/N

        return result

    def show_categ_tree(self, target, categ):
        G = nx.Graph()
        G.add_node(categ, weight=1000*self.categ_relatedness(target,categ))
        for c in self.wna.hypo(categ):
            G.add_node(c, weight=1000*self.categ_relatedness(target,c))
            G.add_edge(categ, c)
        pos = nx.spring_layout(G)

        node_size = [d['weight'] for (n,d) in G.nodes(data=True)]
        nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color="w")
        nx.draw_networkx_edges(G, pos, width=1)
        nx.draw_networkx_labels(G, pos ,font_size=16, font_color="b")

        plt.xticks([])
        plt.yticks([])
        plt.show()

if __name__=='__main__':
    G = nx.Graph()
    G.add_node("a", weight=1000)
    G.add_node("b", weight=400)
    G.add_node("c", weight=800)

    G.add_edge("a","c",weight=3)
    G.add_edge("b","c",weight=5)

    pos = nx.spring_layout(G)
    edge_labels = {("a","c"):3,("b","c"):5}

    node_size = [d['weight'] for (n,d) in G.nodes(data=True)]
    nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color="r")
    nx.draw_networkx_edges(G, pos, width=1)
    nx.draw_networkx_edge_labels(G, pos,edge_labels)
    nx.draw_networkx_labels(G, pos ,font_size=16, font_color="b")

    plt.xticks([])
    plt.yticks([])
    plt.show()
