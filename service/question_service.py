# coding=utf-8

from utils.gensim_util import tokenization, similarity
from utils.inverted_index import get_inverted_index
from utils.question_util import load_questions


def search(question):
    # 分词
    words = tokenization(content=question)
    # 获取倒排索引
    inverted_index = get_inverted_index('inverted_index.pkl')
    # 从倒排索引中过滤出words中数据
    real_questions = []
    for word in words:
        if word in inverted_index:
            for q in inverted_index[word].keys():
                real_questions.append(q)
    # 去重
    real_questions = list(set(real_questions))
    # 计算相似度
    question_similarities = similarity(question, real_questions)
    question_similarities = list(map(lambda m: {
        'sentence': m['sentence'],
        'similarity': str(m['similarity'])
    }, question_similarities))
    # # 找到真正的问答详情
    # question_details = load_questions()
    return question_similarities


def question_search(question):
    questions = load_questions()
    if question in questions:
        return {
            'question': question,
            'detail': questions[question]
        }
    return {
        'question': question,
        'detail': '没有找到'
    }


# if __name__ == '__main__':
    #     print(search('结婚一年提出离婚，男方能否要求返还彩礼？'))
    # print(question_search('结婚一年提出离婚，男方能否要求返还彩礼？'))
