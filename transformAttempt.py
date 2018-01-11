import logging
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO)
from pprint import pprint


from gensim import corpora, models, similarities
directory = corpora.Dictionary.load('./tmp/deerwester.dict')
corpus = corpora.MmCorpus('./tmp/deerwester.mm')

# pprint(list(corpus))

tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
# for doc in corpus_tfidf:
#     pprint(doc)
