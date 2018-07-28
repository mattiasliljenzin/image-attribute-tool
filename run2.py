from os import listdir
from os import walk
from os import stat
from datetime import datetime, timezone
from os.path import isfile, join
from PIL import Image
import piexif
import os
import exifread
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("year")
args = parser.parse_args()

YEAR = ''

if len(args.year) != 4:
    print('Invalid arg: {}. Exiting program'.format(args.year))
    sys.exit(0)
else:
    print('Valid arg: {}'.format(args.year))
    YEAR = args.year

path = 'F:\\BILDER NY\\By year\\' + YEAR
DEFAULT_DATE = datetime.strptime('{}:01:01 12:00:00'.format(YEAR), '%Y:%m:%d %H:%M:%S')
DEFAULT_DATE_STR = DEFAULT_DATE.strftime('%Y:%m:%d %H:%M:%S')
DTO_KEY = piexif.ExifIFD.DateTimeOriginal
MISSING_DATE_PATTERN = '0000:00:00 00:00:00'

print(DEFAULT_DATE)

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

def adjustDates(files):

    missing_date = []

    for filepath in files:
        
        try:
            print(' ')
            print(filepath)
            
            im = Image.open(filepath)
            exif_dict = piexif.load(im.info["exif"])
            date_taken = DEFAULT_DATE_STR

            if DTO_KEY in exif_dict["Exif"]:
                dto = exif_dict["Exif"][DTO_KEY].decode()
                if dto != MISSING_DATE_PATTERN: 
                    date_taken = dto
            
            exif_dict["Exif"].update({DTO_KEY: date_taken.encode()})
            exif_bytes = piexif.dump(exif_dict)
            im.save(filepath, exif=exif_bytes)
            
            st = os.stat(filepath)
            mtime = st[8]
            ctime = st[9]
            new_timestamp = datetime.strptime(date_taken, '%Y:%m:%d %H:%M:%S').timestamp()
            os.utime(filepath, (mtime, new_timestamp))
        except:
            print('Error when processing {}'.format(filepath))
            missing_date.append(filepath)

    return missing_date

files = np.array(getFiles(path))
files_error = adjustDates(files)

print(' ')
print(' ')
print('=== Files with error ===')
for f in files_error:
    print(f)











