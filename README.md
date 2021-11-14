# CJI-Framework (Chinese Jargons Identification Framework)

 

This is a code release of paper `Identification of Chinese Dark Jargons in Telegram Underground Markets Using Context-Oriented and Linguistic Features` (Under Review).

Our code is composed of four parts.

`TCDBuilding` Part can use BaiduLAC to build the TCD mentioned in our paper.

`VectorGeneration` is the GloVe tool, you can also download it from the offical website of it.

`TransferLearning` Part is an implementation of Transfer Learning method mentioned in the paper. You need to prepare a corpus and a source vector as input (we used the public Tencent Vectors). Then run `fine-tune.py` to get embedding of your corpus.

`VectorProjection` Part is an implementation of Vector Projection mentioned in the paper. You can modify parameters in `run.sh` to use the code. This Part requires that you have two pre-trained vectors as the input.

`JargonIdentification` contains feature calculation and jargon identification. You need to input the TCD and two groups of vectors to get the final result.

We will give more details once the paper is published.
