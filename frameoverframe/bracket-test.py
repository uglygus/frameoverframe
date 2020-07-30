#!/usr/bin/env python3
"""

test bracket.py

"""


import os
import shutil
from pathlib import Path

import bracket


numimages = 15
rootdir = '/Users/tbatters/BIG-STUFF/fbracket-test'


shutil.rmtree(rootdir, ignore_errors=True)

images = rootdir + '/images'

os.makedirs(images)


for i in range(numimages):

    numbered_file = images+'/IMG_'+'{:05d}'.format(i) + '.txt'

    it = Path(numbered_file)
    with it.open('w') as it_fp:
        it_fp.write('original file number: {:05d}'.format(i))
        it_fp.close()

input('environment setup complete...')

bracket.split(5, images)

input('split done. merge...')

thisdirlist = [rootdir + '/' + d for d in os.listdir(rootdir)]

newdirlist = []

print('THISDIRLIST=', thisdirlist)

for f in thisdirlist:
    if '.DS_Store' in f:
        continue
    else:
        newdirlist.append(f)

bracket.merge(newdirlist)
