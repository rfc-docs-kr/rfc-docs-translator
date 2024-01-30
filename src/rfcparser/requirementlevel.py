import re

progMust = re.compile(r'(MUST|REQUIRED|SHALL)')
progMustNot = re.compile(r'(MUST NOT|SHALL NOT)')
progShould = re.compile(r'(RECOMMENDED|SHOULD)')
progShouldNot = re.compile(r'(SHOULD NOT|NOT RECOMMENDED)')
progMay = re.compile(r'(MAY|OPTIONAL)')

def isRequired(text) :
    if progMustNot.search(text) != None :
        return 'MUST NOT'
    elif progMust.search(text) != None :
        return 'MUST'
    elif progShouldNot.search(text) != None :
        return 'SHOULD NOT'
    elif progShould.search(text) != None :
        return 'SHOULD'
    elif progMay.search(text) != None :
        return 'MAY'
    return None


def searchRequirements(text) :
    requiredLevels = []
    items = text.split(". ")
    for item in items :
        result = isRequired(item)
        if result == None :
            continue
        requiredLevels.append(result)

    return requiredLevels

