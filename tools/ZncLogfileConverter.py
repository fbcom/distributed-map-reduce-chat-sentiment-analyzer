#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This is a tool for combining and preparing ZNC IRC logfiles.
#
# (C) 2016 by Florian Buetow
#
# Usage:
#   python ZncLogfileConverter.py [logfile | logfile2 | ...]
#
# Or:
#
#   chmod +x ZncLogfileConverter.py
#   ./ZncLogfileConverter.py [logfile1 | logfile2 | ...]
#
# Output:
#   Converted logfile lines are printed to your terminal. You probably want to redirect the output to a file.
#
# Example:
#   python ZncLogfileConverter *.* > everything.log
#
# Note:
#   The tool will automatically filter provided filenames so that they end in *_YYYYMMDD.log
#   where YYYY is a 4-digit year, MM the month and DD the day both with 2 digits each.
#
# Sourcecode: https://github.com/fbcom/distributed-map-reduce-chat-sentiment-analyzer
#

import re
import sys
import time
import datetime


class LinebasedLogfileReader:

    def __init__(self, filename):
        self.filename = filename
        self.filehandle = open(self.filename, "r")

    def nextLine(self):
        line = self.filehandle.readline()
        if line:
            return line
        else:
            self.filehandle.close()
        return None


class ZncLogfileConverter():

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
        Expects a line of a znc logfile and returns a better formated version of it

        Sample input: [11:23:23] <userid> text with spaces and all
        Sample output: 1422300092 userid text with spaces and all
        """
        line = line.strip()
        token = line.split(" ")
        (timestamp, userid, text) = token[:2] + [" ".join(token[2:])]
        del token

        timestamp = str(self.cleanupTimestamp(timestamp))
        if not timestamp:
            return ""  # unknown line format

        userid = self.cleanupUserid(userid)
        if not userid:
            return ""  # unknown line format

        return " ".join([timestamp, userid, text])

    def cleanupUserid(self, userid):
        userid_regex = re.compile(r"^<(.*)>$")  # = expected format in znc logfile
        match = userid_regex.match(userid)
        if match:
            return match.groups()[0]
        return None

    def cleanupTimestamp(self, timestamp):
        YMD = self.getYMDFromFilename(self.filename)
        hms = self.getHMSFromTimestamp(timestamp)
        if not YMD or not hms:
            return None
        YMDhms = list(YMD) + list(hms)
        return self.createUnixTimestamp(*YMDhms)

    def getHMSFromTimestamp(self, timestamp):
        timestamp_regex = re.compile(r"^\[(\d{2}):(\d{2}):(\d{2})\]$")  # = expected format in znc logfile
        match = timestamp_regex.match(timestamp)
        if match:
            return map(int, match.groups())  # [hour, minute, second]
        return None

    def getYMDFromFilename(self, filename):
        filename_regex = re.compile(r".*(\d{4})(\d{2})(\d{2})\.log$")
        match = filename_regex.match(filename)
        if match:
            (year, month, day) = map(int, match.groups())
            return (year, month, day)

        raise Exception("Cannot extract YearMonthDay from filename of unknown pattern")

    def createUnixTimestamp(self, Y, M, D, h, m, s):
        dt = datetime.datetime(year=Y, month=M, day=D, hour=h, minute=m, second=s)
        return int(time.mktime(dt.timetuple()))

if __name__ == '__main__':
    for filename in sys.argv[1:]:
        converter = ZncLogfileConverter(filename)
        while True:
            line = converter.nextLine()
            if line:
                print line
            if line == None:
                break
