import yaml
import hashlib
import os

def loadCache(file) :
    result = None
    try :
        if os.path.isfile(file) :
            with open(file, 'r') as cache :
                result = yaml.load(cache.read(), Loader=yaml.SafeLoader)
    except :
        result = None
    
    return result

def dumpCache(file, data) :
    try :
        with open(file, 'w') as cache :
            dump = yaml.dump(data,
                default_style='|',allow_unicode=True,sort_keys=False,)
            cache.write(dump)
    except Exception as e:
        print(e)



class Element:
    def __init__(self, text):
        self.hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
        self.data = {
            'hash' : self.hash,
            'type' : None,
            'comment' : None,
            'original' : text,
            'fixed' : None,
            'ko' : None,
        }
        self.isCached = False

        self.cachePath = f'./elements/{self.hash}.yaml'

        cachedData = loadCache(self.cachePath)

        if cachedData != None :
            self.data = cachedData
            self.isCached = True
            
    def save(self) :
        dumpCache(self.cachePath, self.data)
        self.isCached = True
