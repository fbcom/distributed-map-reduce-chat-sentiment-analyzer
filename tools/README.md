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

Therefore you probably want to redirect the output to a file in order to save it.

```
./ZncLogfileConverter.py *.* > everything.log
```

### Logfilenames:

Only filenames ending in *_YYYYMMDD.log* will be loaded and save the converted lines of all logfiles to *everything.log*.

Where *YYYY* represents a 4-digit year, *MM* the month and *DD* the day, each written as 2-digit numbers.
