#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Author: Florian Buetow
# Copyright: Copyright (C) 2016 by Florian Buetow
# License: MIT License
# Source: https://github.com/fbcom/distributed-map-reduce-chat-sentiment-analyzer
#

import re
import sys
import time
import datetime


class LinebasedLogfileReader:

    def __init__(self, filename):
        self.filename = filename
        self.filehandle = open(self.filename, 'r')

    def nextLine(self):
        line = self.filehandle.readline()
        if line:
            return line
        else:
            self.filehandle.close()
        return None


class SentiWSDataConverter():

    def __init__(self, filename):
        self.filename = filename
        self.logfileReader = LinebasedLogfileReader(self.filename)

    def nextLine(self):
        line = self.logfileReader.nextLine()
        if line:
            return self.convertLine(line)
        return None

    def convertLine(self, line):
        """
        Sample input: <Word>|<POS tag> \t <Polarity weight> \t <Infl_1>,...,<Infl_k>
        Sample output: ["<Polarity weight>  <Word>", "<Polarity weight> <Infl_1>", ... "<Polarity weight>, <Infl_k>"]
        """

        # extract word
        (word, token) = line.strip().split('|')

        # extract postag and weight
        token = token.split('\t')
        if len(token) == 2:
            token.append([])  # dummy, for when there are no inflections

        (postag, weight, token) = token[:2] + token[2:]
        weight = float(weight)

        # extract inflections
        inflections = []
        if token:
            inflections = token.split(',')

        ret = []
        for w in [word] + inflections:
            tmp = "%f %s %s" % (weight, w, postag)
            tmp = "%s %f %s" % (w, weight, postag)
            ret.append(tmp)

            w2 = w
            for (umlaut, replacement) in [('ä','ae'),('ö','oe'),('ü','ue'),('Ä','Ae'),('Ö','Oe'),('Ü','ue'),('ß','ss')]:
                w2 = w2.replace(umlaut,replacement)

            tmp2 = "%s %f %s" % (w2, weight, postag)
            if tmp2 != tmp:
                ret.append(tmp2)
        return ret


if __name__ == '__main__':
    filenames = sys.argv[1:]
    if not filenames:
        # use these if none were provided
        filenames = [
            'SentiWS_v1.8c_Positive.txt',
            'SentiWS_v1.8c_Negative.txt'
        ]
    for filename in filenames:
        converter = SentiWSDataConverter(filename)
        while True:
            lines = converter.nextLine()
            if lines:
                for line in lines:
                    print line
            if lines == None:
                break
