import paddlehub as hub
import os
import json
import six
from tqdm import tqdm
import threading
#import multiprocessing

os.environ["CUDA_VISIBLE_DEVICES"] = "1"

class BadThread (threading.Thread):
    def __init__(self, threadid,bad_lines,startline,endline,windowsize):
        threading.Thread.__init__(self)
        self.threadid = threadid
        self.bad_lines = bad_lines
        self.startline = startline
        self.endline = endline
        self.windowsize = windowsize
    def run(self):
        deal_with_file_bad(self.threadid,self.bad_lines,self.startline,self.endline,self.windowsize)

def deal_with_file_bad(threadid,bad_lines,startline,endline,windowsize,use_gpu=True):
    lac = hub.Module(name="lac")
#def deal_with_file_bad(threadid,bad_lines,startline,endline,windowsize,word_frequency,word_frequency_bad,word_frequency_bad_window,word_frequency_bad_n,use_gpu=False):
    bad_lines=bad_lines[startline:endline]
    print("Bad Thread "+str(threadid))
    for line in tqdm(bad_lines):
        line = line.strip().split(' ')
        #送入LAC模型处理
        linestr="".join(line)
        linestr=[linestr]
        lacinputs = {"text": linestr}
        lacresults = lac.lexical_analysis(data=lacinputs, use_gpu=use_gpu, batch_size=10)[0]
        for nowid,w in enumerate(line):
            try:
                word_frequency_bad[w] += 1
            except:
                word_frequency_bad[w] = 1  
            
            try:
                word_frequency[w] += 1
            except:
                word_frequency[w] = 1
            if w in lacresults["word"]:
                if lacresults["tag"][lacresults["word"].index(w)]=="n":
                    try:
                        word_frequency_bad_n[w] += 1
                    except:
                        word_frequency_bad_n[w] = 1   
                else:
                    try:
                        temp = word_frequency_bad_n[w]
                    except:
                        word_frequency_bad_n[w]=0                               
            else:
                try:
                    word_frequency_bad_n[w] += 1
                except:
                    word_frequency_bad_n[w] = 1
            if nowid>windowsize and nowid+windowsize<len(line)-1:
                nowwindow=list()
                for i in range(nowid-windowsize,nowid+windowsize):
                    nowwindow.append(line[i])
                try:
                    failtag=0
                    nowhistory=word_frequency_bad_window[w]
                    for item in nowhistory:
                        if len(set(nowwindow).difference(set(item)))<len(nowwindow):
                            failtag=1
                            break
                    if failtag==0:
                        word_frequency_bad_window[w].append(nowwindow)
                except:
                    word_frequency_bad_window[w]=list()
                    word_frequency_bad_window[w].append(nowwindow)
            else:
                try:
                    word_frequency_bad_window[w].append(list())
                except:
                    word_frequency_bad_window[w]=list()
                    word_frequency_bad_window[w].append(list())

def get_words(file_name_bad,vocab_file,windowsize,threadnum,use_gpu=True):
    input_file_bad = open(file_name_bad, encoding="UTF-8")
    global word_frequency
    global word_frequency_bad
    global word_frequency_bad_window
    global word_frequency_bad_n    
    word_frequency = dict()
    word_frequency_bad = dict()
    word_frequency_bad_window = dict()
    word_frequency_bad_n = dict()
    bad_lines=input_file_bad.readlines()

    print("Dealing with Bad File")
    print(" ")
    print(" ")
    badthreads = []
    #创建线程
    singlethread=int(len(bad_lines)/threadnum)
    lastpoint=0
    for threadid in range(0,threadnum):
        if threadid<threadnum-1:
            #nowthread = multiprocessing.Process(target=deal_with_file_bad,args=(threadid,bad_lines,lastpoint,lastpoint+singlethread,windowsize,word_frequency,word_frequency_bad,word_frequency_bad_window,word_frequency_bad_n))
            nowthread = BadThread(threadid,bad_lines,lastpoint,lastpoint+singlethread,windowsize)
            lastpoint+=singlethread
        else:
            #nowthread = multiprocessing.Process(target=deal_with_file_bad,args=(threadid,bad_lines,lastpoint,len(bad_lines)-1,windowsize,word_frequency,word_frequency_bad,word_frequency_bad_window,word_frequency_bad_n))
            nowthread = BadThread(threadid,bad_lines,lastpoint,len(bad_lines)-1,windowsize)
        nowthread.start()
        badthreads.append(nowthread)

    # 等待所有线程完成
    for t in badthreads:
        t.join()

    print("Output Result")
    outputjson=dict()
    for key,value in word_frequency_bad.items():
        nowword=key
        try:
            temp=outputjson[nowword]["bcn"]
        except:
            outputjson[nowword]=dict()
            outputjson[nowword]["gcn"]=0
            outputjson[nowword]["gngram"]=0
            outputjson[nowword]["cn"]=word_frequency[nowword]
        outputjson[nowword]["bcn"]=value
        outputjson[nowword]["bngram"]=len(word_frequency_bad_window[nowword])
        outputjson[nowword]["blac"]=word_frequency_bad_n[nowword]
    outputjsonstr=json.dumps(outputjson)
    with open(vocab_file,'w+') as file_handle:
        file_handle.write(outputjsonstr)

get_words("bad.txt","./vocab.txt",5,1)
