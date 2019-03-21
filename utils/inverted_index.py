# coding=utf-8
# 倒排索引
import os
import re
from collections import Counter

import jieba

from utils import pickle_util


def count_in_str(source, target=[]):
    # 去掉标点符号等
    line = re.sub("[.!//_,$&%^*()<>+\"'?@#-|:~{} ]+|[——！\\\\，。=？、：“”‘’《》【】￥……（） ]+", '', source)
    # 分词
    words = list(jieba.cut_for_search(line))
    # 仅选取要处理的单词
    if target is not None and len(target) > 0:
        words = list(filter(lambda s: s in target, words))
    # 统计单词数量
    counter = dict(Counter(words))
    return counter


# 获取倒排索引，如果不存在返回None
def get_inverted_index(path):
    path = os.path.split(os.path.realpath(__file__))[0] + '/' + path
    if os.path.exists(path):
        return pickle_util.load(path)
    return None


# 生成倒排索引，保存到本地，并返回
def generate_inverted_index(path, lines):
    inverted_index = {
    }
    for question in lines:
        one_line_data = count_in_str(question)
        for word, count in one_line_data.items():
            if not word in inverted_index:
                inverted_index[word] = {}
            inverted_index[word][question] = count
    pickle_util.save(path, inverted_index)
    return inverted_index


if __name__ == '__main__':
    # lines = read_lines('question_list.txt')
    # # 筛选出所有以Q:开头的行
    # lines = list(filter(lambda l: l.startswith('Q:'), lines))
    # # 对所有筛选出的行，去掉Q:
    # lines = list(map(lambda l: l.strip()[2:], lines))
    # # 使用这部分数据生成倒排索引
    # generate_inverted_index('inverted_index.pkl', lines)
    # print(pickle_util.load('inverted_index.pkl'))
    pass
