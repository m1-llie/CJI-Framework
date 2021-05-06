# CJI-Framework (Chinese Jargon Identification Framework)

 

This is a code release of `CJI-Framework` proposed in Conference paper `A Novel Framework of Identifying Chinese Jargons for Telegram Underground Markets` and in Journal paper `What Exactly are You Concealing? Identifying Dark Jargons in Chinese Online Underground Markets`.

Our code is composed of four parts

`VectorProjection` Part is an implementation of Vector Projection mentioned in paper. You can modify parameters in `run.sh` to use the code. This Part require you have two pre-trained vectors as input.

`TransferLearning` Part is an implementation of Transfer Learning mentioned in paper. You need to prepare a corpus and a source vector as input (We used the public Tencent Vectors). Then run `fine-tune.py` to get embedding of your corpus.

`TCDBuilding` Part can use BaiduLAC to build TCD mentioned in paper.

`VectorGeneration` is GloVe, you can also download it from the offical website of it.

`JargonIdentification` contains feature calculation and jargon identification. You need to input the TCD and two groups of vectors to get the final result.

