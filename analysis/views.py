from django.shortcuts import render
from main.models import JDCommentDetail,JDCommodity
import jieba.posseg as pseg #词性标注
import jieba.analyse
import jieba
from gensim import corpora,models
import pandas as pd
from pandas import DataFrame,Series
from datetime import datetime,timezone
from collections import namedtuple





# Create your views here.
def analysis(request,*args,**kwargs):
    if request.method == "POST":

        commodityId = request.POST.get("uniqueId")

        name = JDCommodity.objects.get(uniqueId=commodityId).name
        print("-"*100)
        print(commodityId,name)
        print("-"*100)
        filtered_positive_data, filtered_negative_data, filtered_general_data = preprocess(commodityId)


        positive_topics, positive_keywords = commentProcess(filtered_positive_data)
        negative_topics, negative_keywords = commentProcess(filtered_negative_data)
        general_topics, general_keywords = commentProcess(filtered_general_data)

        context = {"positive":{'topics':positive_topics,'keywords':positive_keywords},
                   "negative":{'topics':negative_topics,'keywords':negative_keywords},
                   "general":{'topics':general_topics,'keywords':general_keywords}}
        return render(request,"analysis/analysisPage.html",context=context)

def preprocess(commodityId):
    total_data = JDCommentDetail.objects.filter(commodityId=commodityId).all()
    positive_data_idx, negative_data_idx, general_data_idx = partition(total_data)
    filtered_positive_data = effectivenessFilter(total_data, positive_data_idx)
    filtered_negative_data = effectivenessFilter(total_data, negative_data_idx)
    filtered_general_data = effectivenessFilter(total_data, general_data_idx)
    return filtered_positive_data,filtered_negative_data,filtered_general_data

def partition(data):
    # 划分好中差评
    positive_data_idx = []
    negative_data_idx = []
    general_data_idx = []
    for i, d in enumerate(data):
        if d.score == 5:
            positive_data_idx.append(i)
        elif d.score >= 3:
            general_data_idx.append(i)
        else:
            negative_data_idx.append(i)
    return positive_data_idx,negative_data_idx,general_data_idx

def effectivenessFilter(total_data, idx_list):
    data = [total_data[i] for i in idx_list]

    Val = namedtuple("Val", "effectiveness days idx")
    valid_data = []
    for i, d in enumerate(data):
        effectiveness = 0
        effectiveness += 1 if len(d.content) > 20 else 0
        effectiveness += 1 if int(d.picNum) > 0 else 0
        effectiveness += 1 if int(d.videoNum) > 0 else 0
        effectiveness += 1 if int(d.replyNum) > 0 else 0
        effectiveness += int(d.isTop)
        days = (datetime.now(timezone.utc) - d.creationTime).days
        if d.userLevelName == "金牌会员" or d.userLevelName == "钻石会员" or d.userLevelName == "白金会员" or d.userLevelName == "PLUS会员":
            effectiveness += 1
        effectiveness += int(d.usefulVoteCount)
        valid_data.append(Val(effectiveness, days, i))

    valid_data = sorted(valid_data, key=lambda x: (x.effectiveness, -x.days), reverse=True)
    valid_data_after_cut = valid_data[:len(valid_data)//4*3]
    return [total_data[d.idx] for d in valid_data_after_cut]

def commentProcess(data):
    # 对判定有效的所有评论进行分词分析
    jieba.analyse.set_stop_words('./analysis/stopwords-master/哈工大停用词表.txt')
    document = ""
    texts = []
    for d in data:
        texts.append(jieba.analyse.extract_tags(d.content,20,allowPOS=("n","v")))
        document += d.content + "\n"
    keywords = jieba.analyse.extract_tags(document, 3, allowPOS=("n","v"))

    dictionary = corpora.Dictionary(texts)
    # #Dictionary该字典的词袋模型
    bow_corpus = [dictionary.doc2bow(text) for text in texts]
    # doc2bow获得在该字典下，text的向量化表示[（i,j）,......]   i代表词的index，j代表词出现的次数
    lda = models.LdaModel(bow_corpus, num_topics=3, id2word=dictionary)
    tmp = lda.show_topics()
    topics = ''.join(tmp[0][1]).split('+')
    return topics, keywords

def genLDA(comments):
    # texts = pd.DataFrame(comments,columns=["content"])
    dictionary = corpora.Dictionary(comments)
    bow_corpus = [dictionary.doc2bow(text) for text in comments]
    lda = models.LdaModel(bow_corpus, num_topics=3, id2word=dictionary)
    topics = lda.show_topics()
    return topics




