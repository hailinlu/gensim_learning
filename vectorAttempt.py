import logging
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO)

from gensim import corpora

documents = [
    "Human machine interface for lab abc computer applications",
    "A survey of user opinion of computer system response time",
    "The EPS user interface management system",
    "System and human system engineering testing of EPS",
    "Relation of user perceived response time to error measurement",
    "The generation of random binary unordered trees",
    "The intersection graph of paths in trees",
    "Graph minors IV Widths of trees and well quasi ordering",
    "Graph minors A survey"
]

stopList = set('for a of the and to in'.split())
texts = [[word for word in document.lower().split() if word not in stopList]
        for document in documents]

# print(texts)

from collections import defaultdict
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1

texts = [[token for token in text if frequency[token] > 1]
         for text in texts]

from pprint import pprint
# pprint(texts)

# directory = corpora.Dictionary(texts)
# directory.save('./tmp/deerwester.dict')
# print(directory.token2id)


directory = corpora.Dictionary(line.lower().split() for line in open('./tmp/mycorpus.txt'))
stop_ids = [directory.token2id[stopword] for stopword in stopList if stopword in directory.token2id]
once_ids = [tokenid for tokenid, docfreq in directory.dfs.items() if docfreq == 1]
directory.filter_tokens(stop_ids+once_ids)
directory.compactify()

directory.save('./tmp/deerwester.dict')

print(directory.token2id)

new_doc = "Human computer interaction"
new_vec = directory.doc2bow(new_doc.lower().split())
# print(new_vec)

corpus = [directory.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('./tmp/deerwester.mm', corpus)
# pprint(corpus)

'''一个百万数量级文档的语料库，我们不可能将整个语料库全部存入内存'''


class MyCorpus(object):
    def __iter__(self):
        for line in open('./tmp/mycorpus.txt'):
            yield directory.doc2bow(line.lower().split())


corpus_memory_friendly = MyCorpus()
print(corpus_memory_friendly)

for vector in corpus_memory_friendly:
    print(vector)

# corpus = corpora.MmCorpus("./tmp/deerwester.mm")
# print(list(corpus))
