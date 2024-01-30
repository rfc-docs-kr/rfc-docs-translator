import re
import os

# compile patterns

progBlock = re.compile(r'(((?<=\n\n).|.)((.|\n.)*))')
progPageHeader = re.compile(r'\[Page \d*\]')
progToC = re.compile(r'(((?<=\n)|^ )  +.+?\n?.+? \.\.+\d+)')
progHeader = re.compile(r'^(\w|\d).*$')
progTableContent = re.compile(r'(-+  )+-+(?=\n)')
progNonContent01 = re.compile(r'^ +[^ ]+\n +([^ ]|\n +)+$') # space less content
progNonContent02 = re.compile(r'\w   +[\W\w](.|\n)*[^\.]$') # have large empty space with no comma end, it can be diagram
progNonContent03 = re.compile(r'^(\d\w?| )+$') # number only diagram
progContent = re.compile(r'^   +(\n|.)*?((\]|\}|\)|\d|\w|\")\.|:|\.\)|\w|\.\,|\w,|\?|>|\])$')


rfc = open('./rfc5246.txt', 'r');


rfcContent = rfc.read()
rfc.close();

reResult = progBlock.findall(rfcContent);

for content in reResult :
    contentString = content[0]
    # recognize content type
    if progPageHeader.search(contentString) != None :
        print("Content Type is PAGE HEADER")
        # continue
    elif progToC.search(contentString) != None :
        print("Content Type is Table of Contents")
        # continue
    elif progHeader.search(contentString) != None :
        print("Content Type is Header")
        # continue
    elif progTableContent.search(contentString) != None :
        print("content Type is Table Content")
        # continue
    elif progNonContent01.search(contentString) != None :
        print("content Type is None Coneten")
        # continue
    elif progNonContent02.search(contentString) != None :
        print("content Type is None Coneten2")
        # continue
    elif progNonContent03.search(contentString) != None :
        print("content Type is None Coneten3")
        # continue
    elif progContent.search(contentString) != None : # should translate
        print("Content Type is Content")
        # continue
    else :
        print("Content Type is Unknown")
        # continue
    
    # elif 

    print(contentString)
    print("")

# OK rfc is block