#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
@desc:  gensim_lda聚类得到句子的类别 
@time:  2017/07/26 16:25
@author: liuluxin(0_0mirror@sina.com)
@param: $1-训练数据根目录 $2-模型的保存地址
"""

import codecs
from gensim.models import LdaModel
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from gensim.models import ldamulticore
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
import gensim
import jieba
import logging
import logging.handlers

MODEL_PATH = "model/lda"
# 配置日志信息
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='lda.log',
                    filemode='w')
# 定义一个Handler打印INFO及以上级别的日志到sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# 设置日志打印格式
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
# 将定义好的console日志handler添加到root logger
logging.getLogger('').addHandler(console)


class LdaClass:
    # @desc: 使用模型路径初始化lda模型
    def __init__(self, model_path):
        self.model_path = model_path + ".model"
        self.dic_path = model_path + ".dic"
        self.logger = logging.getLogger(model_path + ".log")
        self.logger.debug('Init Lda model with model path :{0}'.format(self.model_path))

    # @desc: 从model_path加载已经训练好的model
    def load(self):
        if len(self.model_path) <= 3:
            self.logger.error("Model path {0} unvalid".format(self.model_path))
            exit(-1)
        else:
            self.lda = LdaModel.load(self.model_path)
            self.dictionary = Dictionary.load(self.dic_path)

    # @desc: 从data_root中的数据训练lda，默认设置为10个topic
    def build(self, data_root, topic_num=10):
        train = []
        stopwords = codecs.open(data_root + "stop_words", 'r', encoding='utf8').readlines()
        stopwords = [w.strip() for w in stopwords]
        fp = codecs.open(data_root + 'query', 'r', encoding='utf8')
        for line in fp:
            line = line.split("	")
            train.append([w for w in line if w not in stopwords])

        self.dictionary = gensim.corpora.Dictionary(train)
        corpus = [self.dictionary.doc2bow(text) for text in train]
        tfidf = TfidfModel(corpus)
        corpus_tfidf = tfidf[corpus] 
        #self.lda = LdaModel(corpus=corpus_tfidf,id2word=self.dictionary, num_topics=topic_num)
	self.lda = ldamulticore.LdaMulticore(corpus=corpus_tfidf, num_topics=topic_num, id2word=self.dictionary, workers=10, chunksize=1000000) 

        self.logger.debug(self.lda.print_topic(6))
        self.dictionary.save(self.dic_path)
        self.lda.save(self.model_path)

    # @desc:将输入query进行结巴分词找到最相似的topic
    def get_query_topic(self,query="简单query测试"):
        if len(query) == 0:
            self.logger.error("Empty query")
        else:
	    print self.dictionary
            query_seg = jieba.cut(query, cut_all=False)
            doc_bow = self.dictionary.doc2bow(query_seg)
	    print doc_bow
            print(self.lda[doc_bow])
            print(self.lda.get_document_topics(doc_bow))
	    print self.lda



if __name__ == "__main__":
    if sys.argv[1] == "train":
        lda_model = LdaClass(MODEL_PATH)
        lda_model.build(sys.argv[2], 10000)

    if sys.argv[1] == "load":
        lda_model = LdaClass(MODEL_PATH)
        lda_model.load()
	print(lda_model)
        line = "Build finished, Input your query"
        while True:
            line = raw_input("Input your query:\n")
            if line == "q":
                exit(0)
            lda_model.get_query_topic(line)

    print("Useage: python get_sentence_lda.py (train data_dir)|load")
    exit(0)
