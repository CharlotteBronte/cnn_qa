#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
@desc:  gensim_lda聚类得到句子的类别 
@time:  2017/07/26 16:25
@author: liuluxin(0_0mirror@sina.com)
@param: $1-训练数据根目录
"""

import codecs
from gensim.models import LdaModel
from gensim.corpora import Dictionary
import sys 
reload(sys)
sys.setdefaultencoding("utf-8")
import gensim

def train_lda(data_root):
    train = []
    stopwords = codecs.open(data_root+"stop_words",'r',encoding='utf8').readlines()
    stopwords = [ w.strip() for w in stopwords ]
    fp = codecs.open(data_root+'query','r',encoding='utf8')
    for line in fp:
        line = line.split("	")
        train.append([ w for w in line if w not in stopwords ])

    dictionary = gensim.corpora.Dictionary(train)
    corpus = [ dictionary.doc2bow(text) for text in train ]
    print corpus
    lda = LdaModel(corpus=corpus, id2word=dictionary, num_topics=5)
    lda.print_topic(1)


if __name__=="__main__":
    if len(sys.argv)!=2:
        print "Useage: python get_sentence_lda.py train_dir"
        exit(0)
    else:
        train_lda(sys.argv[1])
