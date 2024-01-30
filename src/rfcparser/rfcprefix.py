import re

progBlock = re.compile(r'(((?<=\n\n).|.)((.|\n.)*))')
progHeadWhiteSpace = re.compile(r'^ +')
progWhiteSpace = re.compile(r'\n +')
progAllWhiteSpace = re.compile(r'\n *')
progWhiteSpaceSix = re.compile(r'\n {6}')

progContentSubdesc = re.compile(r'^ {3}( ?[^ \n])+\n {6}.') # "   item\n      this is a ..."
progContentSub = re.compile(r'^ {6}.') # "   item\n      this is a ..."
progList = re.compile(r'^(( {3}| {6})(-|o) )')
progListInContent = re.compile(r'(\n( {3}| {6})(-|o) )')
progNumberdList = re.compile(r'^(( {3}| {6})(\d+|[a-z])\. )')

def prefix(data) :
    if progList.search(data) != None :
        data = progList.sub("- ", data)
        data = progListInContent.sub("\n- ", data)
        data = progWhiteSpace.sub(" ", data)
    elif progNumberdList.search(data) != None :
        data = progNumberdList.sub("1. ", data)
        data = progAllWhiteSpace.sub(" ", data)
    elif progContentSubdesc.search(data) != None :
        data = progHeadWhiteSpace.sub("", data)
        data = data.replace("\n      ", "  -  ", 1)
        data = progWhiteSpace.sub(" ", data)
    elif progContentSub.search(data) != None :
        data = progWhiteSpace.sub(" ", data)
        data = progHeadWhiteSpace.sub("", data)
        data = "- " + data
    else :
        data = progHeadWhiteSpace.sub("", data)
        data = progAllWhiteSpace.sub(" ", data)

    return data