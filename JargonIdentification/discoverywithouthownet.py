from gensim import matutils
import numpy as np
import json
from scipy.spatial.distance import pdist
import OpenHowNet
from tqdm import tqdm
hownet_dict = OpenHowNet.HowNetDict()
hownet_dict.initialize_sememe_similarity_calculation()
hownet_dict_advanced = OpenHowNet.HowNetDict(use_sim=True)

#Dataset A1必须是含有黑话的对比数据集
vocab="vocab.txt"
a_vector_1="a1.txt"
a_vector_2="a2.txt"
b_vector_1="b1.txt"
b_vector_2="b2.txt"
output="./jargon.json"
outputtemp="./jargontemp.json"
dim=200

def compute_A(nowword):
	try:
		res=list()
		res.append(dataset_a_dict_1[nowword])
		res=np.array(res)
		res=normalize(res)
		res2=list()
		res2.append(dataset_a_dict_2[nowword])
		res2=np.array(res2)
		res2=normalize(res2)
		finalresult=np.dot(res[0], res2[0])
		return finalresult
	except:
		return -1

def compute_B(nowword):
	try:
		res=list()
		res.append(dataset_b_dict_1[nowword])
		res=np.array(res)
		res=normalize(res)
		res2=list()
		res2.append(dataset_b_dict_2[nowword])
		res2=np.array(res2)
		res2=normalize(res2)
		finalresult=np.dot(res[0], res2[0])
		return finalresult
	except:
		return -1

    
def compute(vector1,vector2):
	try:
		res=list()
		res.append(vector1)
		res=np.array(res)
		res=normalize(res)
		res2=list()
		res2.append(vector2)
		res2=np.array(res2)
		res2=normalize(res2)
		finalresult=np.dot(res[0], res2[0])
		return finalresult
	except:
		return -1

def normalize(matrix):
	ret = np.zeros(matrix.shape)
	for i in range(matrix.shape[0]):
		ret[i] = matutils.unitvec(matrix[i])
	return ret


#读取准备数据
print("Parpring Data..")
with open(vocab) as f:
    now=f.read()
vocab_json=json.loads(now)
dataset_a_dict_1=dict()
dataset_a_dict_2=dict()

data1,data2=open(a_vector_1).read().split("\n"),open(a_vector_2).read().split("\n")
for piece in data1:
    if len(piece.split(" "))!=dim+1:
        continue
    dataset_a_dict_1[piece.split(" ")[0]]=[float(i) for i in piece.split(" ")[1:]]
for piece in data2:
    if len(piece.split(" "))!=dim+1:
        continue
    dataset_a_dict_2[piece.split(" ")[0]]=[float(i) for i in piece.split(" ")[1:]]

dataset_b_dict_1=dict()
dataset_b_dict_2=dict()

data1,data2=open(b_vector_1).read().split("\n"),open(b_vector_2).read().split("\n")
for piece in data1:
    if len(piece.split(" "))!=dim+1:
        continue
    dataset_b_dict_1[piece.split(" ")[0]]=[float(i) for i in piece.split(" ")[1:]]
for piece in data2:
    if len(piece.split(" "))!=dim+1:
        continue
    dataset_b_dict_2[piece.split(" ")[0]]=[float(i) for i in piece.split(" ")[1:]]


print("Find Jargon Candidate")
print(" ")
#可以调参的参数
ngram=20 #即出现达到多少次才开始记为黑话
lacpart=0.8 #即出现次数中名词出现次数至少为多少次
avgsimi=0.255 #即和近义词的平均相似度要低于多少
distance=0.1 #即两份词向量相似度差值

#输出可疑的Jargon
final_jargon=[]
for word in vocab_json:
    try:
        if vocab_json[word]['bngram']>ngram:
            if vocab_json[word]['blac']>vocab_json[word]['bngram']*lacpart:
                simia=compute_A(word)
                simib=compute_B(word)
                if simia!=-1 and simib!=-1:
                    if abs(simia-simib)>distance:
                    #if simia<0.3 and simib>0.2:
                        if len(word)>1:
                            final_jargon.append(word)
                else:
                    final_jargon.append(word)
    except:
        continue

# #输出结果
finaljson=json.dumps(final_jargon)
with open(output,"w+") as f:
	f.write(finaljson)