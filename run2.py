from os import listdir
from os import walk
from os import stat
from datetime import datetime, timezone
from os.path import isfile, join
import os.path
import time
from PIL import Image
import piexif
import os
import exifread
import numpy as np
import argparse
import os
import platform
import json
import sys
import codecs
import ftfy

# path = 'D:\\'
#path = 'C:\\Temp\\facebook-mattiasliljenzin\\messages\\'
#path = 'C:\\Temp\\facebook-mattiasliljenzin\\posts'
path = 'C:\\Temp\\facebook-mattiasliljenzin\\'
MISSING_DATE = '0000-00-00 12:00:00'
START_DATE = datetime(2013, 2, 1, 0, 0).timestamp()
STOP_DATE = datetime(2013, 3, 1, 0, 0).timestamp()
count = 0


def getFiles(directory):

    files = []

    for (dirpath, dirnames, filenames) in walk(directory):

        for file in filenames:
            fullpath = "{}\\{}".format(dirpath, file)
            files.append(fullpath)

        for dir in dirnames:
            for file in getFiles(dir):
                fullpath = "{}\\{}\\{}".format(dirpath, dir, file)
                files.append(fullpath)

    return files


def getWithinDateRangeForLastModified(files):

    missing_date = []

    for filepath in files:

        obj = {}
        obj['filepath'] = filepath
        obj['lm'] = MISSING_DATE

        try:
            tm = os.path.getmtime(filepath)

            if (tm > START_DATE and tm < STOP_DATE):
                obj['lm'] = datetime.fromtimestamp(tm)
                missing_date.append(obj)

        except:
            print('Error when processing {}'.format(filepath))
            missing_date.append(obj)

    return missing_date


def getWithinDateRangeForJson(files):

    storage = []

    for filepath in files:

        found_match = False

        if filepath.endswith('.json'):
            print(filepath)
            try:
                with codecs.open(filepath, encoding='utf-8') as f:
                    content = f.readlines()
                    for c in content:
                        if "timestamp" in c:
                            
                            ts = int(c.strip().strip(',').split(':')[1])

                            try:
                                if (ts > 10000000000):
                                    ts = ts / 1000
                                
                                #tm = datetime.fromtimestamp(int(ts))

                                if (ts > 1 and ts > START_DATE and ts < STOP_DATE):
                                    found_match = True
                                #     print('Found timestamp within range')
                                #     print(tm)
                                # else:
                                #     print('timestamp outside range')
                                #     print(tm)
                                

                            except ValueError as e:
                                print(e)

                if found_match is True:
                    storage.append(filepath)

            except Exception as e: 
                print("[Error]: {} ({})".format(e, filepath))
                storage.append({})

    return storage


def to_data(data):
    if isinstance(data, dict):
        for key, value in data.items():
            return to_data(value)
    elif isinstance(value, list) or isinstance(value, tuple):
        for v in value:
            return to_data(v)
    else:
        return data

files = np.array(getFiles(path))
files_error = getWithinDateRangeForJson(files)

print(' ')
print(' ')
print('=== Files within range ===')
for f in files_error:
    print(f)












