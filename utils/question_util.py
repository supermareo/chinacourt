# coding=utf-8
import os

from utils.file_util import read_lines
from utils.pickle_util import save, load


def process():
    result = {}
    path = os.path.split(os.path.realpath(__file__))[0] + '\question_list.txt'
    lines = read_lines(path)

    question = None
    answer = None
    for line in lines:
        # if '碾压飞石伤路人 总该有' in line:
        #     print('----------------')
        if line.startswith('Q:'):
            if question is not None and answer is not None:
                result[question] = answer
                answer = None
            question = line.strip()[2:]
        else:
            if line.startswith('A:'):
                answer = line.strip()[2:]
            else:
                if answer is not None:
                    answer = answer + '<br>' + line.strip()
    if question is not None and answer is not None:
        result[question] = answer
    save(os.path.split(os.path.realpath(__file__))[0] + '\questions.pkl', result)


def load_questions():
    path = os.path.split(os.path.realpath(__file__))[0] + '\questions.pkl'
    if not os.path.exists(path):
        process()
    return load(path)
