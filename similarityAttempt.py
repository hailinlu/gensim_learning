import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim import corpora, models, similarities
directory = corpora.Dictionary.load('./tmp/deerwester.dict')
corpus = corpora.MmCorpus("./tmp/deerwester.mm")

lsi = models.LsiModel(corpus, id2word=directory, num_topics=2)
doc = "Human computer interaction"
vec_bow = directory.doc2bow(doc.lower().split())
vec_lsi = lsi[vec_bow]

# print(vec_lsi)

index = similarities.MatrixSimilarity(lsi[corpus])
index.save('./tmp/deerwester.index')

sims = index[vec_lsi]
# print(list(enumerate(sims)))

sims = sorted(enumerate(sims),key=lambda item: -item[1])
print(sims)