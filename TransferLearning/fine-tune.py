import csv
import numpy as np
from collections import Counter
from mittens import GloVe, Mittens
from sklearn.feature_extraction.text import CountVectorizer

n_dims=200
def glove2dict(glove_filename):
    with open(glove_filename, encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=' ', quoting=csv.QUOTE_NONE)
        embed = {line[0]: np.array(list(map(float, line[1:])))
                for line in reader}
    return embed

old_glove_path = "vectors1.txt" # get it from https://nlp.stanford.edu/projects/glove
pre_glove = glove2dict(old_glove_path)

sw = []
train_data=[]
with open("second.txt", "r", encoding="utf-8") as f:
    for s in f.readlines():
        s=s.split(" ")
        for item in s:
            train_data.append(item.replace("\n",""))
train_nonstop = [token for token in train_data if (token not in sw)]
#oov = [token for token in train_nonstop if token not in pre_glove.keys()]
oov=train_nonstop

corp_vocab = list(set(oov))
brown_doc = [' '.join(train_nonstop)]

cv = CountVectorizer(ngram_range=(1,1), vocabulary=corp_vocab)
X = cv.fit_transform(brown_doc)
Xc = (X.T * X)
Xc.setdiag(0)
coocc_ar = Xc.toarray()

mittens_model = Mittens(n=n_dims, max_iter=5000)

new_embeddings = mittens_model.fit(
    coocc_ar,
    vocab=corp_vocab,
    initial_embedding_dict= pre_glove)

newglove = dict(zip(corp_vocab, new_embeddings))

#Vector写入文件中
f=open("vectors2.txt","w+",encoding="utf-8")
# s=str(len(corp_vocab))+" "+str(n_dims)+"\n"
# f.write(s)
for i in newglove:
    f.write(i)
    for item in newglove[i]:
        f.write(" ")
        f.write(str(item))
    f.write("\n")
f.close()

# f = open("repo_glove.pkl","wb")
# pickle.dump(newglove, f)
# f.close()