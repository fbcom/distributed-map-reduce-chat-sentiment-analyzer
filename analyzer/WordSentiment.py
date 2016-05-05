#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Author: Florian Buetow
# Copyright: Copyright (C) 2016 by Florian Buetow
# License: MIT License
# Source: https://github.com/fbcom/distributed-map-reduce-chat-sentiment-analyzer
#

from mrjob.job import MRJob
from mrjob.step import MRStep
from nltk.tokenize import RegexpTokenizer


class MRWordSentiment(MRJob):

    def load_sentiment_data(self):
        self.sentiment_dict = {}
        with open("sentiments.txt") as filehandle:
            lines = filehandle.readlines()
            for line in lines:
                (word, weight, postag) = line.split(' ')
                word = word.lower()
                self.sentiment_dict[word] = float(weight.strip('0'))

    def get_sentiment(self, word):
        word = word.lower()
        return self.sentiment_dict[word] if word in self.sentiment_dict else 0.0

    def steps(self):
        return [
            MRStep(
                mapper_init=self.load_sentiment_data,
                mapper=self.mapper,
                reducer=self.reducer
            )
        ]

    def mapper(self, _, line):
        token = line.split(' ')
        (timestamp, userid, text) = token[:2]+[" ".join(token[2:])]
        tokenizer = RegexpTokenizer(r'\w+')
        for word in tokenizer.tokenize(text.decode("utf8")):
            sentiment = self.get_sentiment(word)
            if not sentiment != 0:
                yield word, float(sentiment)

    def reducer(self, word, sentiment):
        print "reducer"
        sentiment_sum = round(sum(sentiment), 4)
        if sentiment_sum != 0:
            yield word, sentiment_sum

if __name__ == '__main__':
    MRWordSentiment.run()
