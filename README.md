# cnn_qa
cnn实现的qa召回，在学习句子表示的同时得到满足当前业务反馈的word_embedding
# Installation
  pip install gensim  
  python version >= 2.7  
  tensorflow version >=1.0  
# Quick Start 
  1. generate query lda topics with gensim(with train and load test)  
     build: python script/get_sentence_lda.py train data/train/small  
	 load: python script/get_sentence_lda.py load  
  2. qa\_cnn  

# File layout
  * script  
	- all runnable scripts, include gensim lda class and cnn smilarity class
  * model
    - dirctory to save model, include gensim and tf model
  * log
    - include lda\_log and tf_log 
  * data
    - train (with small and middle scale data, contact me with emial if you need all)
	- test (test data after training)
