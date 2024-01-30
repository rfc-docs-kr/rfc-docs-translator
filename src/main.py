from converter.converterv2 import Converter
import os
import requests
import sys


converter = Converter(doTranslate=True, languages=["ko"])

def getRFC(id) :
    response = requests.get(f'https://www.ietf.org/rfc/rfc{id}.txt')
    if response.ok :
        rfcFile = open(f'./rfcs/rfc{id}.txt','wb')
        rfcFile.write(response.content)
        rfcFile.close()
        converter.convert(id)
        return True
    else :
        return False


if __name__ == "__main__" :
    getRFC(sys.argv[1])
