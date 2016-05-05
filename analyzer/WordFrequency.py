#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Author: Florian Buetow
# Copyright: Copyright (C) 2016 by Florian Buetow
# License: MIT License
# Source: https://github.com/fbcom/distributed-map-reduce-chat-sentiment-analyzer
#

from mrjob.job import MRJob
from nltk.tokenize import RegexpTokenizer

class MRWordFrequency(MRJob):

    def mapper(self, _, line):
        token = line.split(' ')
        (timestamp, userid, text) = token[:2]+[" ".join(token[2:])]
        tokenizer = RegexpTokenizer(r'\w+')
        for word in tokenizer.tokenize(text.decode("utf8")):
            yield word, 1


    def reducer(self, key, value):
        count = "%010d" % (sum(value))
        yield count, word

if __name__ == '__main__':
    MRWordFrequency.run()

