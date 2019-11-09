import re
import sys
import os

def walk_directory(folders,include_dir=False):
    if not isinstance(folders,list):folders=[folders]
    for folder in folders:
        for dirname, dirnames, filenames in os.walk(folder):
            if include_dir:
                yield dirname
            for filename in filenames:
                path=os.path.join(dirname,filename)
                if os.path.isfile(path):
                    path=re.sub(r'\\','/',path)
                    yield path,filename
        
        
        
        
        