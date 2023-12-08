# CJI-Framework (Chinese Jargons Identification Framework)

This is a code release of paper [`Identification of Chinese Dark Jargons in Telegram Underground Markets Using Context-Oriented and Linguistic Features`](https://doi.org/10.1016/j.ipm.2022.103033) ([IP&M](https://www.sciencedirect.com/journal/information-processing-and-management), 2022).

Our code is composed of four parts.

The `TCDBuilding` Part can use BaiduLAC to build the TCD mentioned in our paper.

`VectorGeneration` is the GloVe tool; you can also download it from the official website of it.

The `TransferLearning` Part implements the Transfer Learning method mentioned in the paper.
It would be best to prepare a corpus and a source vector as input (we used the public Tencent Vectors).
Then, run `fine-tune.py` to get the embedding of your corpus.

The `VectorProjection` Part implements the Vector Projection mentioned in the paper.
You can modify parameters in `run.sh` to use the code.
This Part requires that you have two pre-trained vectors as the input.

`JargonIdentification` contains feature calculation and jargon identification.
You need to input the TCD and two groups of vectors to get the final result.


## Dataset
We built [the Telegram Underground Market Chinese Corpus, TUMCC](https://github.com/m1-llie/TUMCC).

28,749 sentences, including 804,971 characters, from 19,821 Telegram users of 12 Telegram groups were collected when we built TUMCC.
We had finished data screening and word segmentation before we released this corpus.
So it might be easier for you to use.
After cleaning, TUMCC contains 3,863 sentences (100,000 characters) from 3,139 Telegram users.

Feel free to use it to convince your research!


## Citation
```
@article{hou2022identification,
  title={Identification of Chinese dark jargons in Telegram underground markets using context-oriented and linguistic features},
  author={Hou, Yiwei and Wang, Hailin and Wang, Haizhou},
  journal={Information Processing \& Management},
  volume={59},
  number={5},
  pages={103033,1--20},
  year={2022},
  publisher={Elsevier}
}
```
