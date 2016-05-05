# ZncLogfileConverter

This is a tool for combining and preparing ZNC IRC logfiles.

### Usage:

```
python ZncLogfileConverter.py [logfile1 | logfile2 | ...]
```
or alternatively:

```
chmod +x ZncLogfileConverter.py
```
To set executable permissions. And then run it using:

```
./ZncLogfileConverter.py [logfile1 | logfile2 | ...]
```

### Output:

The lines of the input logfiles are converted and printed to your terminal.

Therefore you probably want to redirect the output to a file in order to save it like this:

```
./ZncLogfileConverter.py *.* > everything.log
```

Loads all logfiles in the current directory and saves the output to *everything.log*.
### Logfilenames:

Only filenames ending in *_YYYYMMDD.log* will be processed where *YYYY* represents a 4-digit year, *MM* the month and *DD* the day, each written as 2-digit numbers.


# SentiWSDataConverter

Converts one or more sentiment data files given in the SentiWS file format:

```
<Word>|<POS tag> \t <Polarity weight> \t <Infl_1>,...,<Infl_k>
```

into a flatfile in the following format:

```
<Polarity weight> <Word1>
<Polarity weight> <Infl1_1>
...
<Polarity weight>, <Infl1_k>
<Polarity weight> <Word2>
<Polarity weight> <Infl2_1>
...
<Polarity weight>, <Infl2_k>
...
```


### Usage:

```
python SentiWSDataConverter.py [file1 | file2 | ... ] > sentiment_flatfile.txt
```

If you don't provide filenames the tool will try to load *SentiWS_v1.8c_Positive.txt* and *SentiWS_v1.8c_Negative.txt*


