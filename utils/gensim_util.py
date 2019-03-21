# coding=utf-8
import re

from gensim import corpora, models, similarities
from jieba import posseg as pseg


def tokenization(content):
    content = re.sub("[.!//_,$&%^*()<>+\"'?@#-|:~{} ]+|[——！\\\\，。=？、：“”‘’《》【】￥……（） ]+", '', content)
    words = pseg.cut(content)
    return [word for word, flag in words]


# dest 要对比的文本-用户输入的问题
# src  相当于词典文本-爬取的问题列表
def similarity(dest, src):
    texts = [tokenization(content) for content in src]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    new_doc = dest
    new_vec = dictionary.doc2bow(tokenization(new_doc))
    tfidf = models.TfidfModel(corpus)  # 建立tf-idf模型
    index = similarities.MatrixSimilarity(tfidf[corpus], num_features=len(dictionary))  # 对整个语料库进行转换并编入索引，准备相似性查询
    sims = index[tfidf[new_vec]]  # 查询每个文档的相似度
    sims = list(enumerate(sims))
    result = []
    for index, weight in sims:
        # 去掉相似度为0的
        if weight == 0:
            continue
        result.append({
            'sentence': src[index],
            'similarity': weight
        })
    result.sort(key=lambda k: k.get('similarity', 0), reverse=True)
    return result

# if __name__ == '__main__':
#     print(similarity('可以', ['哈哈哈，可以吗', '好吧', '不行的', '不可以']))
